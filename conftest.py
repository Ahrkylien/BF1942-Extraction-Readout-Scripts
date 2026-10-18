"""
Load this folder as the package BF1942_Extraction_Readout_Scripts, the way it is used as a submodule. Its files then
import each other relatively, and the tests import them through the package.
"""
import importlib.util
import sys
from pathlib import Path

PACKAGE_NAME = "BF1942_Extraction_Readout_Scripts"
folder = Path(__file__).parent
spec = importlib.util.spec_from_file_location(PACKAGE_NAME, folder / "__init__.py", submodule_search_locations=[str(folder)])
package = importlib.util.module_from_spec(spec)
sys.modules[PACKAGE_NAME] = package
spec.loader.exec_module(package)
