import sys
import os
import glob
import shutil
from pathlib import Path
from .refractor_flat_archive import RefractorFlatArchive
from .lexicon import LexiconFile
from .meme_file import MemeFile

def extract_mod(mod_directory_path, destination_directory_path):
    mod_name = os.path.basename(mod_directory_path)
    destination_mod_path = os.path.join(destination_directory_path, "Mods", mod_name)

    if os.path.exists(destination_directory_path):
        shutil.rmtree(destination_directory_path)

    for file in glob.glob(f"{mod_directory_path}/**/*.rfa", recursive=True):
        print(f"Extracting {file}")
        rfa = RefractorFlatArchive(file)
        rfa.extract_all(destination_directory_path)

    print(f"Copying the mod folder, excluding 'Archives'.")

    def ignore_archives(dir, files):
        """Ignore 'Archives' directory only."""
        return ['Archives'] if 'Archives' in files else []

    # Copy the tree, skipping 'Archives'
    shutil.copytree(
        mod_directory_path,
        destination_mod_path,
        dirs_exist_ok=True,
        ignore=ignore_archives
    )

    # convert lexiconAll.dat to lexiconAll.xml
    lexicon_file_path = os.path.join(destination_mod_path, "lexiconAll.dat")
    if os.path.isfile(lexicon_file_path):
        print(f"Extracting the lexicon.")
        lex = LexiconFile(lexicon_file_path)
        lex.read()
        lex.save_to_xml()
        os.remove(lexicon_file_path)
    
    # convert MemeFiles to XML
    menu_directory_path = os.path.join(destination_directory_path, "Menu")
    files_with_no_extension = [os.path.join(menu_directory_path, f) for f in os.listdir(menu_directory_path) if '.' not in f]
    files_with_no_extension = [f for f in files_with_no_extension if os.path.isfile(f)]
    for file in files_with_no_extension:
        print(f"Extracting {file}")
        meme_file = MemeFile(file)
        meme_file.read()
        meme_file.save_to_xml()
        os.remove(file)


def pack_lexicon_and_menu_files(src_folder_path, mod_name):
    # convert meme.xml to binary form
    for file in glob.glob(f"{src_folder_path}/Menu/*.meme.xml"):
        print(f"packing {file}")
        meme_file = MemeFile(Path(file).with_suffix(''))
        meme_file.load_from_xml()
        meme_file.write()

    # convert lexiconAll.xml to lexiconAll.dat
    lexicon_file_path = os.path.join(src_folder_path, "Mods", mod_name, "lexiconAll.xml")
    if os.path.isfile(lexicon_file_path):
        print(f"packing {lexicon_file_path}")
        lex = LexiconFile(Path(lexicon_file_path).with_suffix('.dat'))
        lex.load_from_xml()
        lex.write()


def pack_mod(src_folder_path, mod_name, destination_directory_path):
    packed_mod_folder_path = os.path.join(destination_directory_path, mod_name)
    levels_folder_path = os.path.join(src_folder_path, "bf1942", "levels")
    game_folder_path = os.path.join(src_folder_path, "bf1942", "game")

    level_paths = [ f.path for f in os.scandir(levels_folder_path) if f.is_dir() ]
    mod_archive_paths = [ f.path for f in os.scandir(src_folder_path) if f.is_dir() and f.name.lower() not in ["bf1942", "mods", "cache"] ]

    if os.path.isdir(game_folder_path):
        mod_archive_paths.append(game_folder_path)

    archive_paths = mod_archive_paths + level_paths
    
    pack_lexicon_and_menu_files(src_folder_path, mod_name)

    if os.path.exists(packed_mod_folder_path):
        shutil.rmtree(packed_mod_folder_path)

    for archive_path in archive_paths:
        print(f"packing {archive_path}")
        relative_path = os.path.relpath(archive_path, src_folder_path)
        rfa_file_path = os.path.join(packed_mod_folder_path, "Archives", f"{relative_path}.rfa")
        
        rfa = RefractorFlatArchive(rfa_file_path, read=False)
        rfa.add_directory(archive_path, src_folder_path)
        
        # When packing the menu file dont pack the xml meme files
        if relative_path.lower() == "menu":
            for file_path in rfa.get_file_list():
                if file_path.endswith(".meme.xml"):
                    rfa.remove_file(file_path)
        
        folder_path = os.path.split(rfa_file_path)[0]

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        rfa.write(rfa_file_path)

    shutil.copytree(os.path.join(src_folder_path, "Mods", mod_name), packed_mod_folder_path, dirs_exist_ok=True)

    copied_logs_folder_path = os.path.join(packed_mod_folder_path, "logs")
    if os.path.exists(copied_logs_folder_path):
        shutil.rmtree(copied_logs_folder_path)
    
    # remove the xml lexiconAll
    lexicon_file_path = os.path.join(packed_mod_folder_path, "lexiconAll.xml")
    if os.path.isfile(lexicon_file_path):
        os.remove(lexicon_file_path)


if __name__ == "__main__":
    extract_mod(sys.argv[1], sys.argv[2])
