# BF1942-Extraction-Readout-Scripts
Several scripts for extracting and reading the Battlefield 1942 structure

# Dependencies
The module `refractor_flat_archive` requires Python 3.10 or higher. Other modules in this project may support earlier Python versions, but this minimum version is necessary to ensure full compatibility with refractor_flat_archive.
The module `refractor_flat_archive` also depends on the python-lzo package for LZO compression support (pypi.org/project/python-lzo).

# Some examples:

With one RFA:

```py
# lets get the contents of 'bf1942/levels/Berlin/init.con':
rfa = RefractorFlatArchive("path/to/file.rfa")
path = rfa.get_correct_file_path("bf1942/levels/BeRliN/iNit.con")  # this makes sure that the case of the characters is correct
init_con = rfa.extract_file(path, as_string=True)

# print the file list:
file_list = rfa.get_file_list()
for file_path in file_list:
    print(file_path)
```

With multiple RFA's:

```py
# set up the rfa_group object:
rfa_paths = ["path/to/file_002.rfa", "path/to/file_001.rfa", "path/to/file.rfa"]  # most important rfa first!
rfa_group = RefractorFlatArchiveGroup(rfa_paths)

# check if conquest.con exists:
gpm_cq = rfa_group.file_exists("bf1942/levels/Berlin/gametypes/conquest.con")

# read the level data to get the active combat area :
level = BF42_script(rfaGroup=rfa_group)
level.read("bf1942/levels/Berlin/menu/init.con")
level.read("bf1942/levels/Berlin/init.con")
data = level.data
data.creatLinks()
active_combat_area = data.game.activeCombatArea

# extract the ingamemap to a specific location:
ingame_map_path = rfa_group.get_correct_file_path("bf1942/levels/Berlin/textures/ingamemap.dds")
rfa_group.extract_file(ingame_map_path, "path/to/directory")
```
