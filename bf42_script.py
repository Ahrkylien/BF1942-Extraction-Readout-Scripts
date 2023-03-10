from shlex import split as bf42_split_arguments
import os
import math
import pickle
import json

#method to store objects as strings:
def dumps(objectToDump):
    return(json.dumps(objectToDump))
    # return(pickle.dumps(objectToDump).hex())
def loads(stringToLoad):
    return(json.loads(stringToLoad))
    # return(pickle.loads(bytes.fromhex(stringToLoad)))

def isMethod(method, methodReference):
    return(method.lower() == methodReference.lower() or method.lower() == "set"+methodReference.lower())

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
    def lst(self): #return new vector
        return([self.x, self.y, self.z])
    def toBlend(self,sceneScale = 1):
        return([self.x*sceneScale, self.z*sceneScale, self.y*sceneScale])
    def rotate(self, vec): #rotate vector yaw/pitch/roll
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
    def add(self, vec): #return new vector
        self.x += vec.x
        self.y += vec.y
        self.z += vec.z
        return(self)
    def copy(self): #return new vector
        return(BF42_vec3((self.x,self.y,self.z)))

def bf42_vec3_Add(v1,v2):
    v = BF42_vec3((v1.x,v1.y,v1.z))
    return(v.add(v2))

class BF42_command:
    def __init__(self, cmd_str):
        self.className = ""; self.method = ""; self.arguments = []
        cmd_split1 = cmd_str.split(' ',1)
        cmd_split2 = cmd_split1[0].split('.',1)
        self.className = cmd_split2[0].lower() #ToDo, try to avoid lower this early in the chain
        if len(cmd_split2) == 2:
            self.method = cmd_split2[1].lower() #ToDo, try to avoid lower this early in the chain
        if len(cmd_split1) == 2:
            arguments_str = cmd_split1[1].replace("\\", "/").replace("'", "'\\'")
            try:
                self.arguments = bf42_split_arguments(arguments_str)
            except: # avoid not closing quote error:
                self.arguments = bf42_split_arguments(arguments_str+'"')
    
def bf42_is_linked(template):
    return(type(template) != str or type(template) == int)

class BF42_data:
    def __init__(self):
        self.objectTemplates = []
        self.geometryTemplates = []
        self.objects = []
        self.staticObjects = [] #subCatergory of objects
        self.active_ObjectTemplate = None
        self.active_GeometryTemplate = None
        self.active_Object = None
        self.textureManager_alternativePaths = []
        self.console_worldSize = None
        self.game = BF42_Game()
        self.variables = []
        self.constants = []
    
    def getObjectTemplate(self, name):
        for objectTemplate in self.objectTemplates:
            if objectTemplate.name == name:
                return(objectTemplate)
#        print("could not find objectTemplate: "+name)
        return(None)
    
    def getGeometryTemplate(self, name):
        for geometryTemplate in self.geometryTemplates:
            if geometryTemplate.name == name:
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
        #load objectTemplates
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
        #load geometryTemplates
        for (type, name, scale, file, materialSize, worldSize, yScale, waterLevel) in list_dump[1]:
            geometryTemplate = BF42_GeometryTemplate(type, name)
            geometryTemplate.scale = BF42_vec3(scale)
            geometryTemplate.file = file
            geometryTemplate.materialSize = materialSize
            geometryTemplate.worldSize = worldSize
            geometryTemplate.yScale = yScale
            geometryTemplate.waterLevel = waterLevel
            self.geometryTemplates.append(geometryTemplate)
        #link objectTemplates
        for objectTemplate in self.objectTemplates:
            for child in objectTemplate.childeren:
                if bf42_is_linked(child.template):
                    child.template = self.objectTemplates[child.template]
            if bf42_is_linked(objectTemplate.geometry):
                objectTemplate.geometry = self.geometryTemplates[objectTemplate.geometry]
        #load and link objects
        for (template, absolutePosition, rotation, geometry_scale) in list_dump[2]:
            object = BF42_Object("")
            object.template = self.objectTemplates[template] if bf42_is_linked(template) else template
            object.absolutePosition = BF42_vec3(absolutePosition)
            object.rotation = BF42_vec3(rotation)
            object.geometry_scale = BF42_vec3(geometry_scale)
            self.objects.append(object)
        #load and link staticObjects
        for i in list_dump[3]:
            self.staticObjects.append(self.objects[i])
        return(self)

class BF42_Game:
    def __init__(self):
        self.mapId = None
        self.activeCombatArea = None
        self.customGameName = None
        self.customGameVersion = None
        self.modPaths = []

class BF42_ObjectTemplate:
    def __init__(self, type, name):
        self.type = type.lower() #ToDo, try to avoid lower this early in the chain
        self.name = name.lower() #ToDo, try to avoid lower this early in the chain
        self.geometry = "" #string will be replaced by a reference after linking
        self.triggerRadius = 0
        self.linePoints = []
        self.controlPointName = ""
        self.team = None
        self.unableToChangeTeam = None
        self.childeren = []
        self.active_child = None
        
    def setProperty(self, method, arguments):
        if len(arguments) == 1: #all used commands thus far require 1 argument
            value = arguments[0]
            if method == 'geometry':
                self.geometry = value.lower() #ToDo, try to avoid lower this early in the chain
            elif method == 'triggerradius':
                if value.isdigit():
                    self.triggerRadius = int(value)
            elif method == 'addlinepoint':
                self.linePoints.append(BF42_vec3(value))
            elif method == 'setcontrolpointname':
                self.controlPointName = value
            elif method == 'team':
                self.team = value
            elif method == 'unabletochangeteam':
                self.unableToChangeTeam = value
            elif method == 'addtemplate':
                self.active_child = BF42_ObjectTemplateChild(value)
                self.childeren.append(self.active_child)
            elif method == 'setactivetemplate':
                if value.isdigit():
                    if len(self.childeren) > int(value):
                        self.active_child = self.childeren[int(value)]
            elif method == 'removetemplate':
                if value.isdigit():
                    if len(self.childeren) > int(value):
                        self.childeren.pop(int(value))
            elif self.active_child != None:
                if method == 'setposition':
                    self.active_child.setPosition = BF42_vec3(value)
                elif method == 'setrotation':
                    self.active_child.setRotation = BF42_vec3(value)
                    
class BF42_ObjectTemplateChild:
    def __init__(self, template):
        self.template = template.lower() #string will be replaced by a reference after linking. ToDo, try to avoid lower this early in the chain
        self.setPosition = BF42_vec3((0,0,0))
        self.setRotation = BF42_vec3((0,0,0))
        
class BF42_GeometryTemplate:
    def __init__(self, type, name):
        self.type = type.lower() #ToDo, try to avoid lower this early in the chain
        self.name = name.lower() #ToDo, try to avoid lower this early in the chain
        self.scale = BF42_vec3((1,1,1))
        self.file = None
        self.materialSize = 256
        self.worldSize = 1024
        self.yScale = 1
        self.waterLevel = 0
        
    def setProperty(self, method, arguments):
        if len(arguments) == 1: #all used commands thus far require 1 argument
            value = arguments[0]
            if method == 'scale':
                self.scale = BF42_vec3(value)
            elif method == 'file':
                self.file = value.replace("\\","/")
            elif method == 'materialsize':
                if value.isdigit():
                    self.materialSize = int(value)
            elif method == 'worldsize':
                if value.isdigit():
                    self.worldSize = int(value)
            elif method == 'yscale':
                try:
                    self.yScale = float(value)
                except ValueError:
                    pass
            elif method == 'waterlevel':
                try:
                    self.waterLevel = float(value)
                except ValueError:
                    pass
        
class BF42_Object:
    def __init__(self, template):
        self.template = template.lower() #string will be replaced by a reference after linking, ToDo, try to avoid lower this early in the chain
        self.absolutePosition = BF42_vec3((0,0,0))
        self.rotation = BF42_vec3((0,0,0))
        self.geometry_scale = BF42_vec3((1,1,1))
    
    def setProperty(self, name, arguments):
        if len(arguments) == 1: #all used commands thus far require 1 argument
            value = arguments[0]
            if name == 'absoluteposition':
                self.absolutePosition = BF42_vec3(value)
            elif name == 'rotation':
                self.rotation = BF42_vec3(value)
            elif name == 'geometry.scale':
                self.geometry_scale = BF42_vec3(value)

class BF42_script:
    def __init__(self, data = None, rfaGroup = None):
        if data == None: data = BF42_data()
        self.REM = False
        self.IFs = [] #0 = False, 1 = True, 2 = has already been True
        self.rfaGroup = rfaGroup
        self.data = data
        
    def read(self, path, staticObjects = False):
        data = self.data
        directory = os.path.dirname(path)
        try:
            if self.rfaGroup == None:
                fp = open(path, 'r', errors='replace')
                lines = fp.readlines()
            else:
                fileString = self.rfaGroup.extractFile(path, asString = True)
                if fileString != False:
                    lines = iter(fileString.splitlines())
                else:
                    lines = []
                    # print("Could not find file: "+path)
            for line_raw in lines:
                line = line_raw.strip()
                command = BF42_command(line)
                numArgs = len(command.arguments)
                if command.className == "beginrem":
                    self.REM = True
                elif command.className == "endrem":
                    self.REM = False
                elif not command.className == "rem" and not self.REM:
                    if command.className == "if":
                        if True:
                            self.IFs.append(1)
                        else:
                            self.IFs.append(0)
                    elif command.className == "elseif":
                        if len(self.IFs) > 0:
                            if self.IFs[-1] == 0:
                                if True:
                                    self.IFs[-1] = 1
                            elif self.IFs[-1] == 1:
                                self.IFs[-1] = 2
                        else:
                            pass #elseif without if
                    elif command.className == "else":
                        if len(self.IFs) > 0:
                            if self.IFs[-1] == 0:
                                self.IFs[-1] = 1
                            elif self.IFs[-1] == 1:
                                self.IFs[-1] = 2
                        else:
                            pass #else without if
                    elif command.className == "endif":
                        if len(self.IFs) > 0:
                            self.IFs.pop()
                        else:
                            pass #endif without if
                    elif not [0,2] in self.IFs:
                        if command.className == "objecttemplate":
                            if command.method == "create":
                                if numArgs == 2:
                                    # ToDo: create fails if BF42_ObjectTemplate name already exists...
                                    data.active_ObjectTemplate = BF42_ObjectTemplate(command.arguments[0], command.arguments[1])
                                    data.objectTemplates.append(data.active_ObjectTemplate)
                            elif command.method == "active":
                                if numArgs == 1:
                                    refered_ObjectTemplate = data.getObjectTemplate(command.arguments[0])
                                    if refered_ObjectTemplate != None:
                                        data.active_ObjectTemplate = refered_ObjectTemplate
                            else:
                                if data.active_ObjectTemplate != None:
                                    data.active_ObjectTemplate.setProperty(command.method, command.arguments)
                        
                        if command.className == "geometrytemplate":
                            if command.method == "create":
                                if numArgs == 2:
                                    # ToDo: create fails if BF42_GeometryTemplate name already exists...
                                    data.active_GeometryTemplate = BF42_GeometryTemplate(command.arguments[0], command.arguments[1])
                                    data.geometryTemplates.append(data.active_GeometryTemplate)
                            elif command.method == "active":
                                if numArgs == 1:
                                    refered_GeometryTemplate = data.getGeometryTemplate(command.arguments[0])
                                    if refered_GeometryTemplate != None:
                                        data.active_GeometryTemplate = refered_GeometryTemplate
                            else:
                                if data.active_GeometryTemplate != None:
                                    data.active_GeometryTemplate.setProperty(command.method, command.arguments)
                        
                        elif command.className == "object":
                            if command.method == "create":
                                if numArgs == 1:
                                    data.active_Object = BF42_Object(command.arguments[0])
                                    data.objects.append(data.active_Object)
                                    if staticObjects:
                                        data.staticObjects.append(data.active_Object)
                            else:
                                if data.active_Object != None:
                                    data.active_Object.setProperty(command.method, command.arguments)
                        
                        elif command.className == "texturemanager":
                            if command.method == "alternativepath":
                                if numArgs == 1:
                                    data.textureManager_alternativePaths.append(command.arguments[0])
                        
                        elif command.className == "game":
                            if isMethod(command.method, "MapId"):
                                if numArgs == 1:
                                    data.game.mapId = command.arguments[0]
                            elif isMethod(command.method, "activecombatarea"):
                                if numArgs == 4:
                                    data.game.activeCombatArea = [int(item) for item in command.arguments]
                            elif isMethod(command.method, "customgamename"):
                                if numArgs == 1:
                                    data.game.customGameName = command.arguments[0]
                            elif isMethod(command.method, "customgameversion"):
                                if numArgs == 1:
                                    data.game.customGameVersion = command.arguments[0]
                            elif isMethod(command.method, "addmodpath"):
                                if numArgs == 1:
                                    data.game.modPaths.append(command.arguments[0])
                        
                        elif command.className == "console":
                            if command.method == "worldsize":
                                if numArgs == 1:
                                    data.console_worldSize = int(command.arguments[0])
                        
                        elif command.className == "include":
                            if numArgs == 1:
                                path_include = os.path.join(directory,command.arguments[0])
                                self.read(path_include, data)
                        elif command.className == "run":
                            if numArgs >= 1:
                                extension = os.path.splitext(command.arguments[0])[1]
                                if extension == "":
                                    path_run = os.path.join(directory,command.arguments[0]+".con")
                                else:
                                    path_run = os.path.join(directory,command.arguments[0])
                                BF42_script(data = data, rfaGroup = self.rfaGroup).read(path_run) # need to add v_args
                        elif command.className == "var":
                            if numArgs == 3:
                                data.variables.append("v_test = 12")
                            elif numArgs == 1:
                                data.variables.append("v_test")
                        elif command.className == "const":
                            if numArgs == 3:
                                data.constants.append("c_test = 12")
                            elif numArgs == 1:
                                data.constants.append("c_test")
        except EnvironmentError:
            print("Could not find file: "+path)
        return(self.data)


def bf42_readAllScripts(bf42_data, base_path, level = None):
    for path, subdirs, files in os.walk(os.path.join(base_path,"Objects")):
        for name in files:
            filePath = os.path.join(path, name)
            extension = os.path.splitext(filePath)[1]
            if extension == ".con":
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
                    if mesh[1] == "treemesh":
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
        if objectTemplate.type == "lodobject":
            if not len(objectTemplate.childeren) in [2,3]:
                print("Error: "+objectTemplate.name+" has wrong number of childeren for LodObject!!")
            if i == 1:
                isFarLod = True
            if i == 2: #dont add destroyed LOD
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
        if objectTemplate.type == "lodobject":
            if not len(objectTemplate.childeren) in [2,3]:
                print("Error: "+objectTemplate.name+" has wrong number of childeren for LodObject!!")
            if i == 1:
                isFarLod = True
            if i == 2: #dont add destroyed LOD
                break
        if bf42_is_linked(child.template):
            subList = bf42_listAllGeometries_new(child.template, bf42_vec3_Add(pos, child.setPosition.copy().rotate(rot)), bf42_vec3_Add(rot, child.setRotation), isFarLod) # can I add rotation vectors?
            list[0] += subList[0]
            list[1] += subList[1]
    return(list)