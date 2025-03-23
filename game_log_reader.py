import os
import re
import threading
import time
from datetime import datetime
from html import unescape as html_unescape  # might only be needed for: &amp; &gt; &lt;


def unescape(string):
    def repl(match):
        return int(match.groups()[1]).to_bytes(1, "big")

    bytes = string.encode(encoding='UTF-8', errors='ignore')
    string = re.sub(b"(<bf:nonprint>)(\d{1,3})(</bf:nonprint>)", repl, bytes).decode(encoding='UTF-8', errors='ignore')
    return (html_unescape(string))


class GameLogReader:
    def __init__(self, serverGamePath, serverGamePort=None):
        self.serverGamePath = serverGamePath
        self.serverGamePort = serverGamePort
        self.registeredEventHandlers = []
        self.thread = None
        self.stopThread = False
        self.initialized = False

        self.currentFilePath = None
        self.currentLine = -1
        self.currentLogSize = 0
        self.lastScoreEvent = {'score_type': ''}

        self.currentEventName = ""
        self.currentParams = {}
        self.currentPlayerStatID = None

        ExtraEvents(self)

    def getLogs(self):
        logs = []
        for modName in os.listdir(os.path.join(self.serverGamePath, "mods")):
            logsPath = os.path.join(self.serverGamePath, "mods", modName, "logs")
            if os.path.isdir(logsPath):
                for dirItem in os.listdir(logsPath):
                    fileNameParts = re.split(r"[_\-.]", dirItem)
                    filePath = os.path.join(logsPath, dirItem)
                    if dirItem.endswith(".xml") and os.path.isfile(filePath) and fileNameParts[0] == 'ev' and (
                            self.serverGamePort is None or str(self.serverGamePort) == fileNameParts[1]):
                        try:
                            creationDateTime = datetime.strptime(fileNameParts[2] + ' ' + fileNameParts[3],
                                                                 '%Y%m%d %H%M')
                            logs.append((creationDateTime, filePath))
                        except:
                            pass  # fileName format doesn't comply with the expected format
        logs.sort(key=lambda x: x[0])
        return [filePath for creationDateTime, filePath in logs]

    def initialize(self):
        if self.currentFilePath is None:
            self.currentFilePath = self.getLogs().pop()
        self.readNewEvents()
        self.initialized = True

    def registerEventHandler(self, eventName, function):
        self.registeredEventHandlers.append((eventName, function))

    def eventHandler(self, eventName):
        def decorator_addEvent(func):
            self.registerEventHandler(eventName, func)
            return func

        return decorator_addEvent

    def startTread(self, threadDelay=None):
        if not self.initialized: self.initialize()
        self.thread = threading.Thread(target=self.processLoop, daemon=True)
        self.stopThread = False
        self.thread.start()
        return self.thread

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
            if foundCurrentFile:  # Only process the current log and newer logs
                logSize = os.path.getsize(filePath)
                fileOffset = self.currentLine if filePath == self.currentFilePath else -1
                if filePath != self.currentFilePath or logSize != self.currentLogSize:
                    self.currentLine = self.processLog(filePath, fileOffset)
                    self.currentFilePath = filePath
                    self.currentLogSize = logSize

    def triggerEventHandlers(self, eventName, parameters):
        for eventHandler in self.registeredEventHandlers:
            if eventHandler[0] == eventName:
                eventHandler[1](**parameters)

    def processLog(self, logPath, startLine):
        """
        ### Known problems with the xml logs: ###
        - exit vehicle is not always in log
        - suicide is not in log (it only shows as death) tk should be added to log
        - gametype (coop etc) is always "GPM_CQ"  (This is fixed in the Linux BFV server)
        - setteam is not logged when swiched due to autoballance
        - player IP is not logged
        - bot creation is not logged
        - In BF1942, radio messages sometimes (but not always) are shown as coming from wrong player_id. Haven't verified yet if this also happens in BFV.
        - In Objective Mode games, scoreEvents for achieving an objective, or TKing an objective, are not generated, but are counted in score (5 score points).
          - This applies to both the BF1942 engine (which at least has "placeholders" for counts of these objectives in the roundstats structure (although they aren't populated),
            and the BFV engine, which doesn't even list them in roundstats.
        - Victory type is always logged as "4" in BF1942, despite the real victory type (it is fixed in the Linux BFV server).

        ### event Names and their parameters: ###
        - mapStart()
        - mapEnd()
        - roundStart(dict: settings)
        - roundEnd(dict: roundstats)

        - chat(int: player_id, list: player_location, int: int: team, string: text)
        - playerKeyHash(int: player_id, string: keyhash)
        - disconnectPlayer(int: player_id, list: player_location)
        - beginMedPack(int: player_id, list: player_location, int: medpack_status, int: healed_player)
        - endMedPack(int: player_id, list: player_location, int: medpack_status)
        - beginRepair(int: player_id, list: player_location, int: repair_status, string: vehicle_type, int: vehicle_player = None)
        - endRepair(int: player_id, list: player_location, int: repair_status)
        - createPlayer(int: player_id, string: name, list: player_location, bool: is_ai, int: team)
        - destroyPlayer(int: player_id, list: player_location)
        - destroyVehicle(string: vehicle, list: vehicle_pos, int: player_id = None, list: player_location = None)
        - enterVehicle(int: player_id, list: player_location, string: vehicle, int: pco_id, bool: is_default, bool: is_fake)
        - exitVehicle(int: player_id, list: player_location, string: vehicle, bool: is_fake)
        - pickupKit(int: player_id, list: player_location, string: kit)
        - radioMessage(int: player_id, list: player_location, int: message, bool: broadcast)
        - restartMap(int: tickets_team1, int: tickets_team2)
        - roundInit(int: tickets_team1, int: tickets_team2)
        - scoreEvent(int: player_id, list: player_location, string: score_type, string: weapon, int: victim_id = None)
        - setTeam(int: player_id, list: player_location, int: team)
        - spawnEvent(int: player_id, list: player_location, int: team)
        - reSpawnEvent(int: player_id, list: player_location, int: team)
        - changePlayerName(int: player_id, list: player_location, string: name)
        - connectPlayer(int: player_id, list: player_location)
        - pickupFlag(int: player_id, list: player_location)

        ### Extra info on the different score_types in scoreEvent: ###
        - FlagCapture: Captured CTF flag
        - Attack: Captured ControlPoint
        - Kill -> DeathNoMsg: Kill (weapon or killed)
        - TK -> Death: TK and is no more
        - Death: is no more (fall, suicide, teamswitch)
        ## used params:
        - "FlagCapture", [player_id, player_name, player_location]
        - "ControlPointCapture", [player_id, player_name, player_location, controlPoint.controlPointName]
        - "Kill", [player_id, player_name, player_location, victim_player_id, victim_player_name, victim_player_location, weapon, isTK]
        - "Death", [player_id, player_name, player_location]

        ### Extra Custom Events (derived from one or more scoreEvents): ###
        - scoreEventKill(player_id, player_location, weapon, victim_id, victim_location)
        - scoreEventTK(player_id, player_location, weapon, victim_id, victim_location)
        - scoreEventFlagCapture(player_id, player_location):
        - scoreEventAttack(player_id, player_location):
        - scoreEventDeath(player_id, player_location):
        """

        lines = []
        endLine = startLine
        with open(logPath, 'r', encoding='utf-8') as file:
            for endLine, line in enumerate(file):
                if endLine > startLine:
                    # the line should be terminated correctly.
                    # Otherwise the game is probably not done writing the log file
                    if line[-2:] != ">\n":
                        endLine = endLine - 1
                        break
                    lines.append(line.strip('\n'))

        for lineRaw in lines:
            line = lineRaw.strip()
            if len(line) > 1:
                lastOpening = line.rfind('<')
                firstClosing = line.find('>')
                value = None if lastOpening == 0 else line[firstClosing + 1:lastOpening]
                nameAndAttributesList = re.findall("(?:\".*?\"|\S)+", line[1:firstClosing])
                name = nameAndAttributesList.pop(0)
                closing = name.startswith('/')
                if closing: name = name[1:]
                attributes = {}
                for attribute in nameAndAttributesList:
                    splitted = attribute.split('=', 2)
                    attributes[splitted[0]] = splitted[1][1:-1]

                if not closing:
                    if name == "?xml":
                        self.triggerEventHandlers('mapStart', {})
                        self.currentParams = {}
                    elif name == "bf:setting":
                        if attributes['name'] in ['server name', 'modid', 'mapid', 'map', 'game mode']:
                            value = unescape(value)
                        elif attributes['name'] in ['internet', 'allownosecam', 'freecamera', 'externalviews',
                                                   'autobalance', 'hitindication', 'tkpunish', 'crosshairpoint',
                                                   'sv_punkbuster']:
                            value = value == '1'
                        elif attributes['name'] in ['kickbacksplash']:
                            value = float(value)
                        else:
                            value = int(value)
                        self.currentParams[attributes['name']] = value
                    elif name == "bf:event":
                        self.currentEventName = attributes['name']
                    elif name == "bf:param":
                        if attributes['type'] == 'int':
                            value = int(value)
                            if attributes['name'].startswith('is_') or attributes['name'] == 'broadcast':
                                value = value == 1
                        elif attributes['type'] == 'vec3':
                            value = None if value == "(unknown)" else [float(i) for i in value.split('/')]
                        elif attributes['type'] == 'string':
                            value = unescape(value)
                            if self.currentEventName == 'scoreEvent' and attributes['name'] == 'weapon' and value == "(none)":
                                value = None
                        self.currentParams[attributes['name']] = value
                    elif name == "bf:roundstats":
                        self.currentParams['teamtickets'] = {}
                        self.currentParams['playerstats'] = {}
                    elif name in ["bf:winningteam", "bf:victorytype"]:
                        self.currentParams[name] = value
                    elif name == "bf:teamtickets":
                        self.currentParams['teamtickets'][attributes['team']] = value
                    elif name == "bf:playerstat":
                        self.currentPlayerStatID = attributes['playerid']
                        self.currentParams['playerstats'][self.currentPlayerStatID] = {}
                    elif name == "bf:statparam":
                        if attributes['name'] == 'player_name':
                            value = unescape(value)
                        elif attributes['name'] == 'is_ai':
                            value = value == '1'
                        else:
                            value = int(value)
                        self.currentParams['playerstats'][self.currentPlayerStatID][attributes['name']] = value
                else:  # closing
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
                        self.triggerEventHandlers('roundEnd', {'roundstats': self.currentParams})
                    if not name == "bf:playerstat":
                        self.currentParams = {}
        return endLine


class ExtraEvents:
    def __init__(self, gameLogReader):
        self.previous = {'score_type': None}

        @gameLogReader.eventHandler("scoreEvent")
        def scoreEvent(player_id, player_location, score_type, weapon, victim_id=None):
            parameters = locals()
            if (self.previous['score_type'] == "Kill" and score_type == "DeathNoMsg") or (self.previous['score_type'] == "TK" and score_type == "Death"):
                gameLogReader.triggerEventHandlers("scoreEvent" + self.previous['score_type'],
                                                   {'player_id': self.previous['player_id'],
                                                    'player_location': self.previous['player_location'],
                                                    'weapon': self.previous['weapon'], 'victim_id': player_id,
                                                    'victim_location': player_location})
            if score_type in ["FlagCapture", "Attack", "Death"]:
                gameLogReader.triggerEventHandlers("scoreEvent" + score_type, {'player_id': player_id, 'player_location': player_location})
            self.previous = parameters
