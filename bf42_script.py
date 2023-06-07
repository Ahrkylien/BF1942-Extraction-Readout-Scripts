import os
import re
import math
import pickle
import json
import sys

# method to store objects as strings:
def dumps(objectToDump):
    return(json.dumps(objectToDump))
    # return(pickle.dumps(objectToDump).hex())
def loads(stringToLoad):
    return(json.loads(stringToLoad))
    # return(pickle.loads(bytes.fromhex(stringToLoad)))

class BF42_vec3:
    x = 0
    y = 0
    z = 0
    def __init__(self, vertex):
        if type(vertex) is str:
            v_str = vertex.split('/')
            v = []
            for vert_str in v_str:
                try:
                    v.append(float(vert_str))
                except ValueError:
                    pass
            if len(v) == 1 and len(v_str) == 1:
                self.x = v[0]
                self.y = v[0]
                self.z = v[0]
            elif len(v) == 2 and len(v_str) == 2:
                self.x = v[0]
                self.y = v[1]
            elif len(v) == 3 and len(v_str) == 3:
                self.x = v[0]
                self.y = v[1]
                self.z = v[2]
        else:
            self.x = vertex[0]
            self.y = vertex[1]
            self.z = vertex[2]
    def __eq__(self, other):
        if not isinstance(other, BF42_vec3):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    def str(self, numberOfSignif=6):
        strings = []
        for v in self.lst():
            if v == 0:
                v = 0 # prevent negative 0 (cosmetic)
            nrOfDigitsBeforeDot = int(math.log10(abs(v)))+1 if v != 0 else 0
            significance = max(6,4+nrOfDigitsBeforeDot)
            strings.append("%.*g" % (significance, v))
        return(strings[0]+"/"+strings[1]+"/"+strings[2])
    def str_floor(self, numberOfSignif=6): #for lightmap
        strings = []
        for v in self.lst():
            if v == 0:
                v = 0 # prevent negative 0 (cosmetic)
            nrOfDigitsBeforeDot = int(math.log10(abs(v)))+1 if v != 0 else 0
            significance = max(6,4+nrOfDigitsBeforeDot)
            string = "%.*g" % (significance, v)
            if "e" in string:
                strings.append("0")
            else:
                strings.append(string.split(".")[0])
        return(strings[0]+"-"+strings[1]+"-"+strings[2])
    def lst(self): # return new vector
        return([self.x, self.y, self.z])
    def toBlend(self,sceneScale = 1):
        return([self.x*sceneScale, self.z*sceneScale, self.y*sceneScale])
    def rotate(self, vec): # rotate vector yaw/pitch/roll
        ref = self.copy()
        self.x = ref.x*math.cos(math.radians(vec.x)) + ref.z*math.sin(math.radians(vec.x))
        self.z = -ref.x*math.sin(math.radians(vec.x)) + ref.z*math.cos(math.radians(vec.x))
        ref = self.copy()
        self.y = ref.y*math.cos(math.radians(vec.y)) - ref.z*math.sin(math.radians(vec.y))
        self.z = ref.y*math.sin(math.radians(vec.y)) + ref.z*math.cos(math.radians(vec.y))
        ref = self.copy()
        self.x = ref.x*math.cos(math.radians(vec.z)) - ref.y*math.sin(math.radians(vec.z))
        self.y = ref.x*math.sin(math.radians(vec.z)) + ref.y*math.cos(math.radians(vec.z))
        return(self)
    def add(self, vec): # return new vector
        self.x += vec.x
        self.y += vec.y
        self.z += vec.z
        return(self)
    def copy(self): # return new vector
        return(BF42_vec3((self.x,self.y,self.z)))

def bf42_vec3_Add(v1,v2):
    v = BF42_vec3((v1.x,v1.y,v1.z))
    return(v.add(v2))

class BF42_command:
    def __init__(self, cmd_str):
        self.className = None; self.method = None; self.arguments = []; self.targetVariable = None
        # regex = "^([\t\f ]*)([^\t^\f^ ^\.^\n]*)(?:(\.)([^\t^\f^ ^\n]*)){0,1}([\t\f ]*)([^\n]*)" # this is the regex to parse a whole file
        regex = "^[\t\f ]*([^\t^\f^ ^\.]*)(?:\.([^\t^\f^ ^\n]*)){0,1}[\t\f ]*(.*)"
        regexResult = re.findall(regex, cmd_str, flags = re.ASCII|re.IGNORECASE|re.MULTILINE)
        if len(regexResult) == 1:
            splitted = regexResult[0]
            if splitted[0] != "": self.className = splitted[0]
            if splitted[1] != "": self.method = splitted[1]
            if splitted[2] != "": 
                arguments_str = splitted[2]
                regex = r'(?:"(?:(?:.*?")|(?:.*)))|(?:[^\t^\f^ ]+)'
                self.arguments = [argument.replace('"', '') for argument in re.findall(regex, arguments_str, flags = re.ASCII)]
                if len(self.arguments) > 1 and self.arguments[-2] == "->" and self.arguments[-1].lower().startswith("v_"):
                    self.targetVariable = self.arguments[-1]
                    self.arguments = self.arguments[:-2]
    
    def __eq__(self, commandString): #commandString has className.method as format where either part can be empty
        parts = commandString.split('.', 1)
        className = True if parts[0] in ['', '*'] else parts[0]
        method = True if len(parts) == 1 or parts[1] in ['', '*'] else parts[1]
        if className != True:
            className = self.className.lower() == className.lower()
        if method != True:
            method = isMethod(self.method, method)
        return className == True and method == True

def isMethod(method, methodReference):
    return(method.lower() == methodReference.lower() or method.lower() == "set"+methodReference.lower())

def bf42_is_linked(template):
    return(type(template) != str or type(template) == int)

class BF42_data:
    def __init__(self):
        self.objectTemplates = []
        self.networkableInfos = []
        self.geometryTemplates = []
        self.objects = []
        self.staticObjects = [] # subCatergory of objects
        self.active_ObjectTemplate = None
        self.active_NetworkableInfo = None
        self.active_GeometryTemplate = None
        self.active_Object = None
        self.textureManager_alternativePaths = []
        self.console_worldSize = None
        self.game = BF42_Game()
        self.variables = {}
        self.constants = {}
        self.lastObjectTemplateID = -1
        self.lastObjectID = -1
        
        with open('constants.txt') as file:
            for line in file:
                parts = line.strip().split()
                self.constants[parts[0]] = parts[1]
    
    def getNextObjectTemplateID(self):
        self.lastObjectTemplateID += 1
        return(self.lastObjectTemplateID)
    
    def getNextObjectID(self):
        self.lastObjectID += 1
        return(self.lastObjectID)
    
    def getObject(self, name):
        for object in self.objects:
            if object.name.lower() == name.lower():
                return(objectTemplate)
        return(None)
    
    def getObjectTemplate(self, name):
        for objectTemplate in self.objectTemplates:
            if objectTemplate.name.lower() == name.lower():
                return(objectTemplate)
        # print("could not find objectTemplate: "+name)
        return(None)
    
    def getNetworkableInfo(self, name):
        for networkableInfo in self.networkableInfos:
            if networkableInfo.name.lower() == name.lower():
                return(networkableInfo)
        return(None)
    
    def getGeometryTemplate(self, name):
        for geometryTemplate in self.geometryTemplates:
            if geometryTemplate.name.lower() == name.lower():
                return(geometryTemplate)
        return(None)
        
    def creatLinks(self):
        for object in self.objects:
            if not bf42_is_linked(object.template):
                template = self.getObjectTemplate(object.template)
                if template != None:
                    object.template = template
        for objectTemplate in self.objectTemplates:
            for child in objectTemplate.childeren:
                if not bf42_is_linked(child.template):
                    template = self.getObjectTemplate(child.template)
                    if template != None:
                        child.template = template
                        template.parents.append(objectTemplate)
            if objectTemplate.NetworkableInfo:
                objectTemplate.NetworkableInfo = self.getNetworkableInfo(objectTemplate.NetworkableInfo)
            geometry = self.getGeometryTemplate(objectTemplate.geometry)
            if geometry != None:
                objectTemplate.geometry = geometry
        
    def dumps(self):
        list_dump = [[],[],[],[]]
        for objectTemplate in self.objectTemplates:
            geometry = self.geometryTemplates.index(objectTemplate.geometry) if bf42_is_linked(objectTemplate.geometry) else objectTemplate.geometry
            childeren = []
            for child in objectTemplate.childeren:
                template = self.objectTemplates.index(child.template) if bf42_is_linked(child.template) else child.template
                childeren.append([template, child.setPosition.lst(), child.setRotation.lst()])
            linePoints = [linePoint.lst() for linePoint in objectTemplate.linePoints]
            list_dump[0].append([objectTemplate.type, objectTemplate.name, geometry, objectTemplate.triggerRadius, linePoints, childeren])
        for geometryTemplate in self.geometryTemplates:
            list_dump[1].append([geometryTemplate.type, geometryTemplate.name, geometryTemplate.scale.lst(), geometryTemplate.file, geometryTemplate.materialSize, geometryTemplate.worldSize, geometryTemplate.yScale, geometryTemplate.waterLevel])
        for object in self.objects:
            template = self.objectTemplates.index(object.template) if bf42_is_linked(object.template) else object.template
            list_dump[2].append([template, object.absolutePosition.lst(), object.rotation.lst(), object.geometry_scale.lst()])
        for staticObject in self.staticObjects:
            list_dump[3].append(self.objects.index(staticObject))
        return(dumps(list_dump))
        
    def loads(self, dataDump):
        list_dump = loads(dataDump)
        # load objectTemplates
        for (type, name, geometry, triggerRadius, linePoints, childeren) in list_dump[0]:
            objectTemplate = BF42_ObjectTemplate(type, name)
            objectTemplate.geometry = geometry
            objectTemplate.triggerRadius = triggerRadius
            objectTemplate.linePoints = [BF42_vec3(linePoint) for linePoint in linePoints]
            for (template, setPosition, setRotation) in childeren:
                objectTemplateChild = BF42_ObjectTemplateChild(template)
                objectTemplateChild.setPosition = BF42_vec3(setPosition)
                objectTemplateChild.setRotation = BF42_vec3(setRotation)
                objectTemplate.childeren.append(objectTemplateChild)
            self.objectTemplates.append(objectTemplate)
        # load geometryTemplates
        for (type, name, scale, file, materialSize, worldSize, yScale, waterLevel) in list_dump[1]:
            geometryTemplate = BF42_GeometryTemplate(type, name)
            geometryTemplate.scale = BF42_vec3(scale)
            geometryTemplate.file = file
            geometryTemplate.materialSize = materialSize
            geometryTemplate.worldSize = worldSize
            geometryTemplate.yScale = yScale
            geometryTemplate.waterLevel = waterLevel
            self.geometryTemplates.append(geometryTemplate)
        # link objectTemplates
        for objectTemplate in self.objectTemplates:
            for child in objectTemplate.childeren:
                if bf42_is_linked(child.template):
                    child.template = self.objectTemplates[child.template]
            if bf42_is_linked(objectTemplate.geometry):
                objectTemplate.geometry = self.geometryTemplates[objectTemplate.geometry]
        # load and link objects
        for (template, absolutePosition, rotation, geometry_scale) in list_dump[2]:
            object = BF42_Object("")
            object.template = self.objectTemplates[template] if bf42_is_linked(template) else template
            object.absolutePosition = BF42_vec3(absolutePosition)
            object.rotation = BF42_vec3(rotation)
            object.geometry_scale = BF42_vec3(geometry_scale)
            self.objects.append(object)
        # load and link staticObjects
        for i in list_dump[3]:
            self.staticObjects.append(self.objects[i])
        return(self)

class BF42_Game:
    def __init__(self):
        self.mapId = None
        self.activeCombatArea = None
        self.customGameName = None
        self.customGameVersion = None
        self.multiplayerBriefingObjectives = None
        self.objectiveBriefing = None
        self.modPaths = []
    
    def execMethod(self, methodName, arguments):
        def setMapId(value): self.mapId = value
        def setActiveCombatArea(a,b,c,d): self.activeCombatArea = (int(a), int(b), int(c), int(d))
        def customGameName(value = None):
            if value != None: self.customGameName = value
            return(self.customGameName)
        def customGameVersion(value = None):
            if value != None: self.customGameVersion = value
            return(self.customGameVersion)
        def addModPath(value): self.modPaths.append(value)
        def setMultiplayerBriefingObjectives(value): self.multiplayerBriefingObjectives = value
        def setObjectiveBriefing(value): self.objectiveBriefing = value
        
        methods = locals()
        methods = {name: methods[name] for name in methods if not name in ['methodName', 'arguments']}
        for method in methods:
            if isMethod(methodName, method):
                try: return(methods[method](*arguments))
                except: pass
                break
        return(False)

class BF42_ObjectTemplate:
    def __init__(self, type, name, ID):
        self.ID = ID
        self.type = type
        self.name = name
        self.geometry = "" # string will be replaced by a reference after linking
        self.maxHitPoints = 10
        self.minRotation = BF42_vec3((0,0,0))
        self.maxRotation = BF42_vec3((0,0,0))
        self.maxSpeed = BF42_vec3((1,1,1))
        self.acceleration = BF42_vec3((0.1,0.1,0.1))
        self.inputToYaw = 55
        self.inputToPitch = 55
        self.inputToRoll = 55
        self.automaticReset = False
        self.magSize = 30
        self.numOfMag = 3
        self.numberOfGears = None
        self.gearUp = 0.7
        self.gearDown = 0.3
        self.triggerRadius = 0
        self.linePoints = []
        self.controlPointName = ""
        self.team = None
        self.unableToChangeTeam = None
        
        self.MinSpawnDelay = None
        self.MaxSpawnDelay = None
        self.SpawnDelayAtStart = None
        self.TimeToLive = None
        self.Distance = None
        self.DamageWhenLost = None
        self.maxNrOfObjectSpawned = None
        self.teamOnVehicle = None
        self.objectTemplates = {} # for objectSpawners
        
        self.childeren = []
        self.active_child = None
        self.parents = []
        
        self.NetworkableInfo = None
    
    def execMethod(self, methodName, arguments):
        def geometry(value): self.geometry = value
        def maxHitPoints(value = None):
            if value != None: self.maxHitPoints = float(value)
            return(self.maxHitPoints)
        def minRotation(value = None):
            if value != None: self.minRotation = BF42_vec3(value)
            return(self.minRotation)
        def maxRotation(value = None):
            if value != None: self.maxRotation = BF42_vec3(value)
            return(self.maxRotation)
        def maxSpeed(value = None):
            if value != None: self.maxSpeed = BF42_vec3(value)
            return(self.maxSpeed)
        def acceleration(value = None):
            if value != None: self.acceleration = BF42_vec3(value)
            return(self.acceleration)
        def inputToPitch(value = None):
            if value != None: self.inputToPitch = int(value)
            return(self.inputToPitch)
        def inputToYaw(value = None):
            if value != None: self.inputToYaw = int(value)
            return(self.inputToYaw)
        def inputToRoll(value = None):
            if value != None: self.inputToRoll = int(value)
            return(self.inputToRoll)
        def automaticReset(value = None):
            if value != None: self.automaticReset = bool(int(value))
            return(self.automaticReset)
        def magSize(value = None):
            if value != None: self.magSize = int(value)
            return(self.magSize)
        def numOfMag(value = None):
            if value != None: self.numOfMag = int(value)
            return(self.numOfMag)
        def numberOfGears(value = None):
            if value != None: self.numberOfGears  = int(value)
            return(self.numberOfGears)
        def gearUp(value = None):
            if value != None: self.gearUp  = float(value)
            return(self.gearUp )
        def gearDown(value = None):
            if value != None: self.gearDown  = float(value)
            return(self.gearDown)
        def triggerRadius(value): self.triggerRadius = int(value)
        def addLinePoint(value): self.linePoints.append(BF42_vec3(value))
        def controlPointName(value): self.controlPointName = value
        def team(value): self.team = value
        def unableToChangeTeam(value): self.unableToChangeTeam = value
        
        def MinSpawnDelay(value): self.MinSpawnDelay = value
        def MaxSpawnDelay(value): self.MaxSpawnDelay = value
        def SpawnDelayAtStart(value): self.SpawnDelayAtStart = value
        def TimeToLive(value): self.TimeToLive = value
        def Distance(value): self.Distance = value
        def DamageWhenLost(value): self.DamageWhenLost = value
        def maxNrOfObjectSpawned(value): self.maxNrOfObjectSpawned = value
        def teamOnVehicle(value): self.teamOnVehicle = value
        def setObjectTemplate(key, value): self.objectTemplates[int(key)] = value
        
        def addTemplate(value):
            self.active_child = BF42_ObjectTemplateChild(value)
            self.childeren.append(self.active_child)
        def setActiveTemplate(value):
            if len(self.childeren) > int(value):
                self.active_child = self.childeren[int(value)]
        def removeTemplate(value):
            if len(self.childeren) > int(value):
                self.childeren.pop(int(value))
        def setPosition(value):
            if self.active_child != None:
                self.active_child.setPosition = BF42_vec3(value)
        def setRotation(value):
            if self.active_child != None:
                self.active_child.setRotation = BF42_vec3(value)
        def networkableInfo(value): self.NetworkableInfo = value
        
        methods = locals()
        methods = {name: methods[name] for name in methods if not name in ['methodName', 'arguments']}
        for method in methods:
            if isMethod(methodName, method):
                try: return(methods[method](*arguments))
                except: pass
                break
        return(False)

class BF42_ObjectTemplateChild:
    def __init__(self, template):
        self.template = template
        self.setPosition = BF42_vec3((0,0,0))
        self.setRotation = BF42_vec3((0,0,0))

class BF42_NetworkableInfo:
    predictionModeEnum = ['PMNone', 'PMLinear', 'PMCubic', 'PMUsePhysics']
    def __init__(self, name):
        self.name = name
        self.isUnique = False
        self.basePriority = 1.0
        self.predictionMode = 0 # PMNone
        self.forceNetworkableId = False
    def execMethod(self, methodName, arguments):
        def setBasePriority(value): self.basePriority = float(value)
        def setIsUnique(value): self.isUnique = bool(int(value))
        def setPredictionMode(value): self.predictionMode = self.predictionModeEnum.index(value)
        
        methods = locals()
        methods = {name: methods[name] for name in methods if not name in ['methodName', 'arguments']}
        for method in methods:
            if isMethod(methodName, method):
                # try:
                return(methods[method](*arguments))
                # except: pass
                break
        return(False)

class BF42_GeometryTemplate:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.scale = BF42_vec3((1,1,1))
        self.file = None
        self.materialSize = 256
        self.worldSize = 1024
        self.yScale = 1
        self.waterLevel = 0
    
    def execMethod(self, methodName, arguments):
        def scale(value): self.scale = BF42_vec3(value)
        def file(value): self.file = value.replace("\\","/")
        def materialsize(value): self.materialsize = int(value)
        def worldsize(value): self.worldsize = int(value)
        def yscale(value): self.yscale = float(value)
        def waterlevel(value): self.waterlevel = float(value)
        methods = locals()
        methods = {name: methods[name] for name in methods if not name in ['methodName', 'arguments']}
        for method in methods:
            if isMethod(methodName, method):
                try: methods[method](*arguments)
                except: pass
                break
        
class BF42_Object:
    def __init__(self, template, ID):
        self.ID = ID
        self.template = template
        self.name = "" # toDo: find out the object ID/name logic/generation
        self.absolutePosition = BF42_vec3((0,0,0))
        self.rotation = BF42_vec3((0,0,0))
        self.geometry_scale = BF42_vec3((1,1,1))
        self.OSId = None
        self.team = None
    
    def setProperty(self, name, arguments):
        if len(arguments) == 1: # all used commands thus far require 1 argument
            value = arguments[0]
            if isMethod(name, "absoluteposition"): self.absolutePosition = BF42_vec3(value)
            elif isMethod(name, "rotation"): self.rotation = BF42_vec3(value)
            elif isMethod(name, "geometry.scale"): self.geometry_scale = BF42_vec3(value)
            elif isMethod(name, "osid"): self.OSId = value
            elif isMethod(name, "team"): self.team = value
            elif isMethod(name, "name"): self.name = value

def bf42_evaluate(value1, operator, value2):
    if operator == "==":
        return(value1.lower() == value2.lower())
    return(False)

class BF42_script:
    def __init__(self, data = None, rfaGroup = None):
        if data == None: data = BF42_data()
        self.REM = False
        self.IFs = [] # 0 = False, 1 = True, 2 = has already been True
        self.rfaGroup = rfaGroup
        self.data = data
        
    def read(self, path, staticObjects = False, forceExternalPath = False, v_args = None):
        data = self.data
        if v_args != None:
            for i, v_arg in enumerate(v_args):
                data.variables["v_arg"+str(i+1)] = v_arg
        directory = os.path.dirname(path)
        lineno = 0
        try:
            if self.rfaGroup == None or forceExternalPath:
                fp = open(path, 'r', errors='replace')
                lines = fp.readlines()
            else:
                fileString = self.rfaGroup.extractFile(path, asString = True)
                if fileString != False:
                    lines = iter(fileString.splitlines())
                else:
                    lines = []
                    print("Could not find file: "+path, file=sys.stderr)
            for line_raw in lines:
                lineno += 1
                line = line_raw.strip()
                command = BF42_command(line)
                if command.className != None:
                    numArgs = len(command.arguments)
                    if command not in ["var", "const"]:
                        for i in range(numArgs):
                            if command.arguments[i].lower().startswith('v_'):
                                command.arguments[i] = data.variables[command.arguments[i]] if command.arguments[i] in data.variables else command.arguments[i]
                            elif command.arguments[i].lower().startswith('c_'):
                                command.arguments[i] = data.constants[command.arguments[i]] if command.arguments[i] in data.constants else command.arguments[i]
                    if command == "beginrem":
                        self.REM = True
                    elif command == "endrem":
                        self.REM = False
                    elif not command == "rem" and not self.REM:
                        if command == "if" and numArgs == 3:
                            if bf42_evaluate(*command.arguments):
                                self.IFs.append(1)
                            else:
                                self.IFs.append(0)
                        elif command == "elseif" and numArgs == 3:
                            if len(self.IFs) > 0:
                                if self.IFs[-1] == 0:
                                    if bf42_evaluate(*command.arguments):
                                        self.IFs[-1] = 1
                                elif self.IFs[-1] == 1:
                                    self.IFs[-1] = 2
                            else:
                                pass # elseif without if
                        elif command == "else" and numArgs == 0:
                            if len(self.IFs) > 0:
                                if self.IFs[-1] == 0:
                                    self.IFs[-1] = 1
                                elif self.IFs[-1] == 1:
                                    self.IFs[-1] = 2
                            else:
                                pass # else without if
                        elif command == "endif" and numArgs == 0:
                            if len(self.IFs) > 0:
                                self.IFs.pop()
                            else:
                                pass # endif without if
                        elif not any(x in self.IFs for x in [0, 2]):
                            if command.method != None:
                                if command == "objecttemplate":
                                    if command == ".create":
                                        if numArgs == 2:
                                            if data.getObjectTemplate(command.arguments[1]) == None:
                                                data.active_ObjectTemplate = BF42_ObjectTemplate(command.arguments[0], command.arguments[1], data.getNextObjectTemplateID())
                                                data.objectTemplates.append(data.active_ObjectTemplate)
                                    elif command == ".active":
                                        if numArgs == 1:
                                            refered_ObjectTemplate = data.getObjectTemplate(command.arguments[0])
                                            if refered_ObjectTemplate != None:
                                                data.active_ObjectTemplate = refered_ObjectTemplate
                                    else:
                                        if data.active_ObjectTemplate != None:
                                            data.active_ObjectTemplate.execMethod(command.method, command.arguments)
                                if command == "networkableinfo":
                                    if command == ".createNewInfo":
                                        if numArgs == 1:
                                            if data.getNetworkableInfo(command.arguments[0]) == None:
                                                data.active_NetworkableInfo = BF42_NetworkableInfo(command.arguments[0])
                                                data.networkableInfos.append(data.active_NetworkableInfo)
                                    else:
                                        if data.active_NetworkableInfo != None:
                                            data.active_NetworkableInfo.execMethod(command.method, command.arguments)
                                if command == "geometrytemplate":
                                    if command == ".create":
                                        if numArgs == 2:
                                            if data.getGeometryTemplate(command.arguments[1]) == None:
                                                data.active_GeometryTemplate = BF42_GeometryTemplate(command.arguments[0], command.arguments[1])
                                                data.geometryTemplates.append(data.active_GeometryTemplate)
                                    elif command == ".active":
                                        if numArgs == 1:
                                            refered_GeometryTemplate = data.getGeometryTemplate(command.arguments[0])
                                            if refered_GeometryTemplate != None:
                                                data.active_GeometryTemplate = refered_GeometryTemplate
                                    else:
                                        if data.active_GeometryTemplate != None:
                                            data.active_GeometryTemplate.execMethod(command.method, command.arguments)
                                
                                elif command == "object":
                                    if command == ".create":
                                        if numArgs == 1:
                                            data.active_Object = BF42_Object(command.arguments[0], data.getNextObjectID())
                                            data.objects.append(data.active_Object)
                                            if staticObjects:
                                                data.staticObjects.append(data.active_Object)
                                    elif command == ".active":
                                        if numArgs == 1:
                                            refered_Object = data.getObject(command.arguments[0])
                                            if refered_Object != None:
                                                data.active_Object = refered_Object
                                    else:
                                        if data.active_Object != None:
                                            data.active_Object.setProperty(command.method, command.arguments)
                                
                                elif command == "texturemanager":
                                    if command == ".alternativepath":
                                        if numArgs == 1:
                                            data.textureManager_alternativePaths.append(command.arguments[0])
                                
                                elif command == "game":
                                    returnValue = data.game.execMethod(command.method, command.arguments)
                                    if command.targetVariable != None and returnValue != False and command.targetVariable in data.variables:
                                        data.variables[command.targetVariable] = returnValue
                                
                                elif command == "console":
                                    if command == ".worldsize":
                                        if numArgs == 1:
                                            data.console_worldSize = int(command.arguments[0])
                            else:
                                if command == "include":
                                    if numArgs == 1:
                                        path_include = os.path.join(directory,command.arguments[0])
                                        self.read(path_include, data)
                                elif command == "run":
                                    if numArgs >= 1:
                                        extension = os.path.splitext(command.arguments[0])[1]
                                        if extension == "":
                                            path_run = os.path.join(directory,command.arguments[0]+".con")
                                        else:
                                            path_run = os.path.join(directory,command.arguments[0])
                                        v_args_run = command.arguments[1:] if len(command.arguments) > 1 else []
                                        BF42_script(data = data, rfaGroup = self.rfaGroup).read(path_run, v_args = v_args_run)
                                elif command == "var":
                                    if numArgs == 3:
                                        data.variables[command.arguments[0]] = command.arguments[2]
                                    elif numArgs == 1:
                                        if command.arguments[0] not in data.variables:
                                            data.variables[command.arguments[0]] = "" # or should it be set to None?
                                elif command == "const":
                                    if numArgs == 3:
                                        data.constants[command.arguments[0]] = command.arguments[2]
                                    elif numArgs == 1:
                                        if command.arguments[0] not in data.constants:
                                            data.constants[command.arguments[0]] = "" # or should it be set to None?
                                elif command.className.lower().startswith('v_'):
                                    if numArgs == 2:
                                        if command.className in data.variables:
                                            data.variables[command.className] = command.arguments[1]
                                elif command.className.lower().startswith('c_'):
                                    if numArgs == 2:
                                        if command.className in data.constants:
                                            data.constants[command.className] = command.arguments[1]
        except EnvironmentError:
            print("Could not find file: "+path, file=sys.stderr)
        except:
            print('exception in BF42_script.read ', path, lineno, file=sys.stderr)
            raise
        return(self.data)


def bf42_readAllScripts(bf42_data, base_path, level = None):
    for path, subdirs, files in os.walk(os.path.join(base_path,"Objects")):
        for name in files:
            filePath = os.path.join(path, name)
            extension = os.path.splitext(filePath)[1]
            if extension.lower() == ".con":
                BF42_script().read(filePath,bf42_data)
    if level != None:
        BF42_script().read(os.path.join(base_path,"Bf1942\\Levels\\"+level+"\\Init.con"),bf42_data)
        BF42_script().read(os.path.join(base_path,"Bf1942\\Levels\\"+level+"\\Conquest.con"),bf42_data)
        BF42_script().read(os.path.join(base_path,"Bf1942\\Levels\\"+level+"\\StaticObjects.con"),bf42_data, True)

def bf42_writeStaticCon(path, objects, data):
    data.objects = objects
    data.creatLinks()
    with open(path, 'w') as f:
        for object in objects:
            templateName = object.template.name if bf42_is_linked(object.template) else object.template
            f.write("object.create "+templateName+"\n")
            f.write("object.absolutePosition "+object.absolutePosition.str()+"\n")
            f.write("object.rotation "+object.rotation.str()+"\n")
            if bf42_is_linked(object.template):
                meshes = bf42_listAllGeometries(object.template)
                for mesh in meshes[0]:
                    if mesh[1].lower() == "treemesh":
                        f.write("object.geometry.scale 1\n")
                        break
            f.write("\n")
    return objects

def bf42_readAllConFiles(base_path,level):
    bf42_data = BF42_data()
    bf42_readAllScripts(bf42_data, base_path, level) 
    bf42_data.creatLinks()
    return(bf42_data)



# These two functions are for processing in Blender:
def bf42_listAllGeometries(objectTemplate, pos = None, rot = None, isFarLod = False):
    # ToDo:
    # child templates are first moved and then rotated (relative to the parent origin)
    if pos == None:
        pos = BF42_vec3((0,0,0))
    if rot == None:
        rot = BF42_vec3((0,0,0))
    list = [[],[]] # [[close LOD] , [far LOD]]
    if bf42_is_linked(objectTemplate.geometry):
        geometryTemplate = objectTemplate.geometry
        if geometryTemplate.file != "":
            list[1 if isFarLod else 0].append((geometryTemplate.file, geometryTemplate.type, pos, rot))
    for i, child in enumerate(objectTemplate.childeren):
        if objectTemplate.type.lower() == "lodobject":
            if not len(objectTemplate.childeren) in [2,3]:
                print("Error: "+objectTemplate.name+" has wrong number of children for LodObject!!")
            if i == 1:
                isFarLod = True
            if i == 2: # dont add destroyed LOD
                break
        if bf42_is_linked(child.template):
            subList = bf42_listAllGeometries(child.template, bf42_vec3_Add(pos, child.setPosition.copy().rotate(rot)), bf42_vec3_Add(rot, child.setRotation), isFarLod) # can I add rotation vectors?
            list[0] += subList[0]
            list[1] += subList[1]
    return(list)

def bf42_listAllGeometries_new(objectTemplate, pos = None, rot = None, isFarLod = False):
    # ToDo:
    # child templates are first moved and then rotated (relative to the parent origin)
    if pos == None:
        pos = BF42_vec3((0,0,0))
    if rot == None:
        rot = BF42_vec3((0,0,0))
    list = [[],[]] # [[close LOD] , [far LOD]]
    if bf42_is_linked(objectTemplate.geometry):
        if objectTemplate.geometry.file != "":
            list[1 if isFarLod else 0].append((objectTemplate.geometry, pos, rot))
    for i, child in enumerate(objectTemplate.childeren):
        if objectTemplate.type.lower() == "lodobject":
            if not len(objectTemplate.childeren) in [2,3]:
                print("Error: "+objectTemplate.name+" has wrong number of childeren for LodObject!!")
            if i == 1:
                isFarLod = True
            if i == 2: # dont add destroyed LOD
                break
        if bf42_is_linked(child.template):
            subList = bf42_listAllGeometries_new(child.template, bf42_vec3_Add(pos, child.setPosition.copy().rotate(rot)), bf42_vec3_Add(rot, child.setRotation), isFarLod) # can I add rotation vectors?
            list[0] += subList[0]
            list[1] += subList[1]
    return(list)
