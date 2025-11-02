import struct
import csv
import xml.etree.ElementTree as ET
from pathlib import Path


class LexiconFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.languages = []  # list of languages (from the first entry)
        self.lexicon = {}    # {word: [translations or values]}

    # ---------- Binary I/O ----------
    @staticmethod
    def _read_i_32(f):
        res = struct.unpack('I', f.read(4))
        return res[0]

    def read(self):
        """Read binary lexicon file (with LANGUAGE row)."""
        # Note: 38 unknown bytes in tail
        with open(self.file_path, 'rb') as f:
            encoding = "UTF-16 LE"
            num_entries = self._read_i_32(f)
            num_cols = self._read_i_32(f)
            lexi_strings = f.read().decode(encoding, 'ignore').split('\x00')

            # Extract LANGUAGE row
            self.languages = lexi_strings[1:num_cols]
            
            # Entries
            for i in range(1, num_entries):
                key = lexi_strings[i * num_cols]
                if self.key_exists(key):
                    print(f"Ignoring duplicate entry for {key}")
                    continue
                self.lexicon[key] = lexi_strings[1 + i * num_cols:num_cols + i * num_cols]
            
            if len(lexi_strings) > num_entries * num_cols:
                print(f"Extra data in footer: {lexi_strings[num_entries * num_cols:]}")
            
            # There are ?random? unknown bytes in the tail

    def write(self):
        """Write binary lexicon file."""
        with open(self.file_path, 'wb') as f:
            num_entries = len(self.lexicon) + 1  # +1 for the LANGUAGE row
            num_cols = len(self.languages) + 1   # +1 for the 'LANGUAGE' column

            f.write(struct.pack('I', num_entries))
            f.write(struct.pack('I', num_cols))

            # Flatten content
            flat_strings = ["LANGUAGE"] + self.languages
            for word, values in self.lexicon.items():
                flat_strings.append(word)
                flat_strings.extend(values)

            encoded = '\x00'.join(flat_strings).encode('UTF-16 LE', 'ignore')
            f.write(encoded)

    def key_exists(self, key):
        lower_key = key.lower()
        for existing_key in list(self.lexicon):
            if existing_key.lower() == lower_key:
                return True
        return False
    
    def get_entry(self, name, language=None):
        try:
            column = 0 if language == None else self.languages.index(language)
            for key, values in self.lexicon.items():
                if key.lower() == name.lower():
                    return values[column]
        except Exception:
            pass
        return name

    # ---------- Other formats ----------

    def save_to_json(self, json_path=None, indent=2):
        """Save lexicon + languages to JSON."""
        json_path = json_path or Path(self.file_path).with_suffix('.json')
        data = {
            "languages": self.languages,
            "entries": self.lexicon
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

    def load_from_json(self, json_path=None):
        """Load lexicon + languages from JSON."""
        json_path = json_path or Path(self.file_path).with_suffix('.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.languages = data.get("languages", [])
            self.lexicon = data.get("entries", {})

    def save_to_xml(self, xml_path=None):
        """Save to XML where each <entry> contains <col language="..."> elements."""
        xml_path = xml_path or Path(self.file_path).with_suffix('.xml')
        root = ET.Element("lexicon")

        # Write entries
        for word, values in self.lexicon.items():
            entry_elem = ET.SubElement(root, "entry", word=word)
            for idx, val in enumerate(values):
                lang_name = self.languages[idx] if idx < len(self.languages) else f"Lang{idx+1}"
                col_elem = ET.SubElement(entry_elem, "col", language=lang_name)
                col_elem.text = val

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)  # use tabs like your example
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)


    def load_from_xml(self, xml_path=None):
        """Load lexicon + languages from XML with <col language="..."> structure."""
        xml_path = xml_path or Path(self.file_path).with_suffix('.xml')
        tree = ET.parse(xml_path)
        root = tree.getroot()

        self.lexicon = {}
        language_set = []

        for entry in root.findall("entry"):
            word = entry.attrib["word"]
            values = []
            for col in entry.findall("col"):
                lang = col.attrib.get("language", "")
                if lang and lang not in language_set:
                    language_set.append(lang)
                values.append(col.text or "")
            self.lexicon[word] = values

        # Preserve consistent language order
        self.languages = language_set
