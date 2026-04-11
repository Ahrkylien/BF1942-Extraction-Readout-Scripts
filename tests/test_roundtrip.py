import filecmp
import tempfile
from pathlib import Path

import pytest

from meme_file import MemeFile


TEST_DATA_DIR = Path(__file__).parent / "data"


def get_test_files():
    return [f for f in TEST_DATA_DIR.iterdir() if f.is_file()]


@pytest.mark.parametrize("file_path", get_test_files())
def test_binary_xml_roundtrip(file_path):
    """
    Test:
    binary -> XML -> binary should produce identical file
    """
    # Step 1: Read original binary
    meme = MemeFile(file_path)
    meme.read()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Step 2: Save to XML
        xml_path = tmpdir / (file_path.stem + ".xml")
        meme.save_to_xml(xml_path)

        # Step 3: Load XML back
        meme_from_xml = MemeFile(file_path)
        meme_from_xml.load_from_xml(xml_path)

        # Step 4: Write back to binary
        rebuilt_path = tmpdir / file_path.name
        meme_from_xml.write(rebuilt_path)

        # Step 5: Compare binary files
        with open(file_path, "rb") as f1, open(rebuilt_path, "rb") as f2:
            original_bytes = f1.read()
            rebuilt_bytes = f2.read()

        assert original_bytes == rebuilt_bytes, f"Mismatch in {file_path.name}"