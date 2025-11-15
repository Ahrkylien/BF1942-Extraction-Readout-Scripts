import sys
import os
import glob
import shutil
from refractor_flat_archive import RefractorFlatArchive
from lexicon import LexiconFile
from meme_file import MemeFile

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


if __name__ == "__main__":
    extract_mod(sys.argv[1], sys.argv[2])
