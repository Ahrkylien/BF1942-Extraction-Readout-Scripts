# BF1942-Extraction-Readout-Scripts
Several scripts for extracting and reading the Battlefield 1942 structure

#Some examples:

With one RFA:
```py
# lets get the contents of 'bf1942/levels/Berlin/init.con':
rfa = RefractorFlatArchive("path/to/file.rfa")
path = rfa.getCorrectFilePath("bf1942/levels/BeRliN/iNit.con") # this makes sure that the case of the characters is correct
init_con = rfa.extractFile(path, asString = True)

# print the file list:
fileList = rfa.getFileList()
for filePath in fileList:
  print(filePath)
```

With multiple RFA's:
```py
# set up the rfa_group object:
rfaPaths = ["path/to/file_002.rfa", "path/to/file_001.rfa", "path/to/file.rfa"] # most important rfa first!
rfa_group = RefractorFlatArchiveGroup(rfaPaths)

# check if conquest.con exists:
gpm_cq = rfa_group.fileExists("bf1942/levels/Berlin/gametypes/conquest.con")

# read the level data to get the active combat area :
level = BF42_script(rfaGroup = rfa_group)
level.read("bf1942/levels/Berlin/menu/init.con")
level.read("bf1942/levels/Berlin/init.con")
data = level.data
data.creatLinks()
activeCombatArea = data.game.activeCombatArea

# extract the ingamemap to a specific location:
ingamemapPath = rfa_group.getCorrectFilePath("bf1942/levels/Berlin/textures/ingamemap.dds")
rfa_group.extractFile(ingamemapPath, "path/to/directory")
```
