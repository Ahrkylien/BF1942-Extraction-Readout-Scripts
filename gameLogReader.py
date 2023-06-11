import os
import re
import threading
import time
from datetime import datetime
from html import unescape as html_unescape #might only be needed for: &amp; &gt; &lt;

def unescape(string):
    def repl(match): return(int(match.groups()[1]).to_bytes().decode(encoding = 'cp1252', errors = 'ignore'))
    string = re.sub(r'(<bf:nonprint>)(\d{1,3})(</bf:nonprint>)', repl, string)
    return(html_unescape(string))

class GameLogReader:
    def __init__(self, serverGamePath, serverGamePort = None):
        self.serverGamePath = serverGamePath
        self.serverGamePort = serverGamePort
        self.registeredEventHandlers = []
        self.thread = None
        self.stopThread = False
        self.initialized = False
        
        self.currentFilePath = None
        self.currentLine = -1
        self.currentLogSize = 0
        self.lastScoreEvent = {'score_type':''}
        
        self.currentLogBlockType = ""
        self.currentEventName = ""
        self.currentParams = {}
        self.currentPlayerStatParams = {}
    
    def getLogs(self):
        logs = []
        for modName in os.listdir(os.path.join(self.serverGamePath,"mods")):
            logsPath = os.path.join(self.serverGamePath,"mods",modName,"logs")
            if os.path.isdir(logsPath):
                for dirItem in os.listdir(logsPath):
                    fileNameParts = re.split(r"[_\-.]", dirItem)
                    filePath = os.path.join(logsPath, dirItem)
                    if dirItem.endswith(".xml") and os.path.isfile(filePath) and fileNameParts[0] == 'ev' and (self.serverGamePort == None or str(self.serverGamePort) == fileNameParts[1]):
                        try:
                            creationDateTime = datetime.strptime(fileNameParts[2]+' '+fileNameParts[3], '%Y%m%d %H%M')
                            logs.append((creationDateTime, filePath))
                        except: pass # fileName format doesn't comply with the expected format
        logs.sort(key=lambda x: x[0])
        return([filePath for creationDateTime, filePath in logs])
    
    def initialize(self):
        if self.currentFilePath == None: self.currentFilePath = self.getLogs().pop()
        self.readNewEvents()
        self.initialized = True
    
    def registerEventHandler(self, eventName, function):
        self.registeredEventHandlers.append((eventName, function))
    
    def eventHandler(self, eventName):
        def decorator_addEvent(func):
            self.registerEventHandler(eventName, func)
        return decorator_addEvent
    
    def startTread(self, threadDelay = None):
        if not self.initialized: self.initialize()
        self.thread = threading.Thread(target = self.processLoop, daemon = True)
        self.stopThread = False
        self.thread.start()
        return(self.thread)
    
    def stopTread(self):
        self.stopThread = True
        
    def processLoop(self):
        while not self.stopThread:
            self.readNewEvents()
            time.sleep(.2)
    
    def readNewEvents(self):
        foundCurrentFile = False
        for filePath in self.getLogs():
            if filePath == self.currentFilePath: foundCurrentFile = True
            if foundCurrentFile == True: # Only process the current log and newer logs
                logSize = os.path.getsize(filePath)
                fileOffset = self.currentLine if filePath == self.currentFilePath else -1
                if filePath != self.currentFilePath or logSize != self.currentLogSize:
                    self.currentLine = self.processLog(filePath, fileOffset)
                    self.currentFilePath = filePath
                    self.currentLogSize =  logSize
    
    def triggerEventHandlers(self, eventName, parameters):
        for eventHandler in self.registeredEventHandlers:
            if eventHandler[0] == eventName:
                eventHandler[1](**parameters)
    
    def processLog(self, logPath, startLine):
        # ToDo:
        # <bf:server>  <bf:setting
        
        # exit vehicle is not always in log
        # suicide is not in log (it only shows as death) tk should be added to log
        # gametype (coop etc) is always "GPM_CQ"  (This is fixed in the Linux BFV server)
        # setteam is not logged when swiched due to autoballance
        # player IP is not logged
        # bot creation is not logged
        # In BF1942, radio messages sometimes (but not always) are shown as coming from wrong player_id. Haven't verified yet if this also happens in BFV.
        # In Objective Mode games, scoreEvents for achieving an objective, or TKing an objective, are not generated, but are counted in score (5 score points).
        #   This applies to both the BF1942 engine (which at least has "placeholders" for counts of these objectives in the roundstats structure (although they aren't populated),
        #   and the BFV engine, which doesn't even list them in roundstats.
        # Victory type is always logged as "4" in BF1942, despite the real victory type (it is fixed in the Linux BFV server).
        
        ###### Server Settings: ######
        # def server_settings(settings):
        
        ###### Round Stats: ######
        # def round_stats(stats):
        
        ###### Events: ######
        # def chat(player_id, player_location, team, text):
        # def playerKeyHash(player_id, keyhash):
        # def disconnectPlayer(player_id, player_location):
        # def beginMedPack(player_id, player_location, medpack_status, healed_player):
        # def endMedPack(player_id, player_location, medpack_status):
        # def beginRepair(player_id, player_location, int: repair_status, vehicle_type, vehicle_player = None):
        # def endRepair(player_id, player_location, repair_status):
        # def createPlayer(player_id, name, player_location, is_ai, team):
        # def destroyPlayer(player_id, player_location):
        # def destroyVehicle(vehicle, vehicle_pos, player_id = None, player_location = None):
        # def enterVehicle(player_id, player_location, vehicle, pco_id, is_default, is_fake):
        # def exitVehicle(player_id, player_location, vehicle, is_fake):
        # def pickupKit(player_id, player_location, kit):
        # def radioMessage(player_id, player_location, message, broadcast):
        # def restartMap(tickets_team1, tickets_team2):
        # def roundInit(tickets_team1, tickets_team2):
        # def scoreEvent(player_id, player_location, score_type, weapon, victim_id = None):
        # def setTeam(player_id, player_location, team):
        # def spawnEvent(player_id, player_location, team):  
        # def reSpawnEvent(player_id, player_location, team):
        # def changePlayerName(player_id, player_location, name):
        # def connectPlayer(player_id, player_location):
        # def pickupFlag(player_id, player_location):
        # def content_CRC32(player_id, player_location, content_CRC32):
        
        # elementName attributes(name, value) value/childElements
            
        
        lines = []
        endLine = startLine
        with open(logPath, 'r', encoding='utf-8') as file:
            for endLine, line in enumerate(file):
                if endLine > startLine:
                    if line[-2:] != ">\n": # the line should be terminated correctly. Otherwise the game is probably not done writing the log file
                        endLine = endLine - 1
                        break
                    lines.append(line.strip('\n'))
        
        for lineRaw in lines:
            line = lineRaw.strip()
            # print(line)
            if len(line) > 1:
                lastOpening = line.rfind('<')
                firstClosing = line.find('>')
                value = None if lastOpening == 0 else line[firstClosing+1:lastOpening]
                nameAndAtributesList = re.findall("(?:\".*?\"|\S)+", line[1:firstClosing])
                name = nameAndAtributesList.pop(0)
                closing = name.startswith('/')
                if name.startswith('/'): name = name[1:]
                atributes = {}
                for atribute in nameAndAtributesList:
                    splited = atribute.split('=', 2)
                    atributes[splited[0]] = splited[1][1:-1]
                    
                if not closing:
                    if name == "?xml":
                        self.triggerEventHandlers('mapStart', {})
                        self.currentParams = {}
                    elif name == "bf:setting":
                        pass
                    elif name == "bf:event":
                        self.currentEventName = atributes['name']
                    elif name == "bf:param":
                        if atributes['type'] == 'int':
                            value = int(value)
                            if atributes['name'].startswith('is_') or atributes['name'] == 'broadcast':
                                value = value == 1
                        elif atributes['type'] == 'vec3':
                            value = None if value == "(unknown)" else [float(i) for i in value.split('/')]
                        elif atributes['type'] == 'string':
                            value = unescape(value)
                        self.currentParams[atributes['name']] = value
                    elif name == "bf:roundstats":
                        pass
                    elif name == "bf:statparam":
                        pass
                else: #closing
                    if name == "bf:log":
                        self.triggerEventHandlers('mapEnd', {})
                    elif name == "bf:server":
                        self.triggerEventHandlers('roundStart', {'settings': self.currentParams})
                    elif name == "bf:event":
                        self.triggerEventHandlers(self.currentEventName, self.currentParams)
                    elif name == "bf:playerstat":
                        pass
                    elif name == "bf:statparam":
                        pass
                    elif name == "bf:roundstats":
                        self.triggerEventHandlers('roundEnd', {'settings': self.currentParams})
                    if not name == "bf:statparam": self.currentParams = {}
        return(endLine)