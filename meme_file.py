import struct
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def read_byte(f):
    """Read a byte from file."""
    data = f.read(1)
    if len(data) < 1:
        raise EOFError("Unexpected EOF while reading uint16")
    return data[0]


def read_u16(f):
    """Read an unsigned 16-bit integer (little-endian) from file."""
    data = f.read(2)
    if len(data) < 2:
        raise EOFError("Unexpected EOF while reading uint16")
    return struct.unpack('<H', data)[0]


def read_u32(f):
    """Read an unsigned 32-bit integer (little-endian) from file."""
    data = f.read(4)
    if len(data) < 4:
        raise EOFError("Unexpected EOF while reading uint32")
    return struct.unpack('<I', data)[0]


def read_int32(f):
    """Read a 32-bit integer (little-endian) from file."""
    data = f.read(4)
    if len(data) < 4:
        raise EOFError("Unexpected EOF while reading uint32")
    return struct.unpack('<i', data)[0]


def read_float32(f):
    """Read a 32-bit float (little-endian) from file."""
    data = f.read(4)
    if len(data) < 4:
        raise EOFError("Unexpected EOF while reading float32")
    return struct.unpack('<f', data)[0]


def bytes_remaining(f):
    """Return the number of bytes left in the file after the current pointer."""
    current = f.tell()
    f.seek(0, 2)  # seek to end
    end = f.tell()
    f.seek(current)
    return end - current


def read_8bit_string(f, n):
    """Read an 8bit string of length n from file."""
    data = f.read(n)
    if len(data) < n:
        raise EOFError(f"Unexpected EOF while reading {n}-byte string")
    return data.decode('cp1252')


def read_16bit_string(f, n):
    """Read an ASCII string of length n from file."""
    n = n * 2
    data = f.read(n)
    if len(data) < n:
        raise EOFError(f"Unexpected EOF while reading {n}-byte string")
    return data.decode('UTF-16 LE')


with open(Path(__file__).parent / 'meme_types.json') as f:
    meme_types = json.load(f)


type_string_prefix = "dice::meme::"


version_string = "MemeFile 2.0"


class MemeFileElement:
    def __init__(self, type_name, object_name, description, child_elements):
        self.type_name = type_name
        self.object_name = object_name
        self.description = description
        self.child_elements = child_elements
        
    @property
    def is_placeholder(self):
        return self.type_name.endswith("Placeholder")
    
    @property
    def is_primitive(self):
        return not isinstance(self.child_elements, list) and not self.is_placeholder
    
    @property
    def is_complex_type(self):
        return not self.is_primitive and not self.is_placeholder
    
    @property
    def has_next_node(self):
        return self.is_complex_type and len(self.child_elements) > 0 and self.child_elements[0].description == "Next node"
    
    @property
    def has_occupied_next_node(self):
        return self.has_next_node and self.child_elements[0].is_complex_type


class MemeFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.root_element = None
    
    def read(self):
        def parse_element(type_name, description, f):
            if type_name in ["Node", "Action", "Data", "Event", "Effect", "Function", "Style"]:
                return read_node_reference(description, f, type_name)
            
            child_elements = parse_type(type_name, f)
            
            return MemeFileElement(type_name, None, description, child_elements)
        
        def parse_type(type_name, f):
            if type_name in meme_types:
                child_elements = []
                for child_type_name, description in meme_types[type_name]:
                    if child_type_name.endswith("[]"):
                        while True:
                            node = parse_element(child_type_name[:-2], None, f)
                            child_elements.append(node)
                            if node.child_elements == None:
                                break
                    else:
                        node = parse_element(child_type_name, description, f)
                        child_elements.append(node)
                return child_elements
            elif type_name == "Boolean":
                return read_byte(f) == 1
            elif type_name == "Byte":
                return read_byte(f)
            elif type_name == "Int32":
                return read_int32(f)
            elif type_name == "Float":
                return read_float32(f)
            elif type_name in ["String8", "FontString", "SoundString"]:
                string_size = read_byte(f)
                return read_8bit_string(f, string_size)
            elif type_name == "String32":
                string_size = read_u32(f)
                return read_8bit_string(f, string_size)
            elif type_name == "Wstring":
                string_size = read_u32(f)
                return read_16bit_string(f, string_size)
            else:
                raise Exception(f"Unknown type: {type_name}")
        
        def get_string(index):
            type_string = get_raw_string(index)
            
            if not type_string.startswith(type_string_prefix):
                raise Exception(f"Type without prefix: {type_string}")
            
            type_string_without_prefix = type_string[len(type_string_prefix):]
            
            if type_string_without_prefix not in meme_types and type_string_without_prefix not in ["ActionListAction", "DataListData"]:
                raise Exception(f"Unknown type: {type_string_without_prefix}")
            
            return type_string_without_prefix

        def read_node_reference(description, f, generic_type_name, skip_header=False):
            if not skip_header:
                current_block_size = read_u32(f)
                object_name_index = read_u16(f)
                object_name = None if object_name_index == 0 else get_raw_string(object_name_index)
            else:
                object_name = None
            
            string_index = read_u16(f)
            
            # 0 means no reference (NULL)
            if string_index == 0:
                return MemeFileElement(f"{generic_type_name}Placeholder", object_name, description, None)
            
            type_name = get_string(string_index)
            
            parameters = parse_type(type_name, f)
            
            return MemeFileElement(type_name, object_name, description, parameters)
        
        strings = []
        def get_raw_string(index):
            return strings[index]

        with open(self.file_path, "rb") as f:
            while True:
                value = read_8bit_string(f)

                if len(value) == 0:
                    break
                
                strings.append(value)
            
            self.root_element = read_node_reference(None, f, "", skip_header=True)
            
            bytes_left_in_tail = bytes_remaining(f)
            if bytes_left_in_tail > 0:
                raise Exception(f"Data left at tail: {bytes_left_in_tail}")

    def write(self, output_path=None):
        """Write the MemeFileElement structure to a binary meme file."""
        output_path = output_path or Path(self.file_path).with_suffix("")
        
        root_element = self.root_element

        with open(output_path, "wb") as f:
            strings = [version_string]
            def add_string(value):
                if value not in strings:
                    strings.append(value)

            def collect_strings(element):
                if element.object_name:
                    add_string(element.object_name)
                
                # Apparently placeholders can contain names, so do this check after adding the name
                if not isinstance(element.child_elements, list) or element.type_name.endswith("Placeholder"):
                    return
                    
                add_string(type_string_prefix + element.type_name)
                for c in element.child_elements:
                    collect_strings(c)

            # Recursive element writing
            def write_element(element, is_root=False):
                if element.is_primitive:
                    val = element.child_elements
                    if element.type_name == "Boolean":
                        f.write(struct.pack("B", 1 if val else 0))
                    elif element.type_name == "Byte":
                        f.write(struct.pack("B", val))
                    elif element.type_name == "Int32":
                        f.write(struct.pack("<i", val))
                    elif element.type_name == "Float":
                        f.write(struct.pack("<f", val))
                    elif element.type_name in ["String8", "FontString", "SoundString"]:
                        encoded = val.encode("cp1252")
                        f.write(struct.pack("B", len(encoded)))
                        f.write(encoded)
                    elif element.type_name == "String32":
                        encoded = val.encode("cp1252")
                        f.write(struct.pack("<I", len(encoded)))
                        f.write(encoded)
                    elif element.type_name == "Wstring":
                        encoded = val.encode("UTF-16 LE")
                        f.write(struct.pack("<I", len(val)))
                        f.write(encoded)
                    else:
                        raise Exception(f"Unknown primitive type: {element.type_name}")
                    return

                # Complex node types (and placeholders)
                if not is_root:
                    block_start = f.tell()
                    f.write(struct.pack("<I", 0))  # Placeholder for block size

                    name_index = strings.index(element.object_name) if element.object_name else 0

                    f.write(struct.pack("<H", name_index))

                type_index = 0 if element.is_placeholder else strings.index(type_string_prefix + element.type_name)
                f.write(struct.pack("<H", type_index))
                
                if not element.is_placeholder:
                    for child in element.child_elements:
                        write_element(child)
                
                if not is_root:
                    # Backfill block size
                    block_end = f.tell()
                    block_size = block_end - block_start
                    f.seek(block_start)
                    f.write(struct.pack("<I", block_size))
                    f.seek(block_end)
            
            # First, gather all strings used
            collect_strings(root_element)

            # Write string table (each string prefixed by length byte)
            for s in strings:
                b = s.encode("ascii")
                if len(b) > 255:
                    raise ValueError(f"String too long ({len(b)}): {s}")
                f.write(struct.pack("B", len(b)))
                f.write(b)
            f.write(b"\x00")  # Terminator byte
            
            write_element(root_element, is_root=True)

    def load_from_xml(self, xml_path=None):
        """Load a MemeFileElement tree from an XML file."""
        xml_path = xml_path or Path(self.file_path).with_suffix('.meme.xml')
        tree = ET.parse(xml_path)
        root_xml = tree.getroot()
        
        def parse_primitive_element_text(type_name, text_value):
            if type_name in ["Boolean"]:
                return text_value.lower() == "true"
            elif type_name in ["Byte", "Int32"]:
                return int(text_value)
            elif type_name in ["Float"]:
                return float(text_value)
            elif type_name in ["String8", "FontString", "SoundString", "String32", "Wstring"]:
                return text_value if text_value is not None else ""
            else:
                raise Exception(f"Unknown primitive type {type_name} with value '{text_value}'")

        def parse_xml_element(xml_element):
            type_name = xml_element.tag
            object_name = xml_element.get("name")
            description = xml_element.get("description")
            
            is_group = type_name in ["g", "MemeFile"]
            if is_group:
                chained_elements = [parse_xml_element(child) for child in xml_element]
                for i in range(len(chained_elements) - 1):
                    chained_elements[i].child_elements[0] = chained_elements[i + 1]
                    chained_elements[i + 1].description = "Next node"
                chained_elements[0].description = description
                chained_elements[0].object_name = object_name
                return chained_elements[0]
            
            matching_meme_type = meme_types[type_name] if type_name in meme_types else None
            has_next_node = matching_meme_type and len(matching_meme_type) > 0 and matching_meme_type[0][1] == "Next node"
            number_of_childeren_besides_next_node = (len(matching_meme_type) - (1 if has_next_node else 0)) if matching_meme_type else 0
            
            text_value = xml_element.text if len(xml_element) == 0 else None
            
            # Has value, thus primitive type
            if text_value:
                if matching_meme_type:
                    primitive_child_index = 1 if has_next_node else 0
                    primitive_child_meme_type = matching_meme_type[primitive_child_index]
                    value = parse_primitive_element_text(primitive_child_meme_type[0], text_value)
                    child_node = MemeFileElement(primitive_child_meme_type[0], None, primitive_child_meme_type[1], value)
                    children = [child_node]
                    meme_file_element = MemeFileElement(type_name, object_name, description, [child_node])
                else:
                    value = parse_primitive_element_text(type_name, text_value)
                    meme_file_element = MemeFileElement(type_name, object_name, description, value)
            else:
                # Complex type — recursively parse children
                children = [parse_xml_element(child) for child in xml_element]
                meme_file_element = MemeFileElement(type_name, object_name, description, children)
            
            if has_next_node:
                meme_file_element.child_elements.insert(0, MemeFileElement(matching_meme_type[0][0] + "Placeholder", None, matching_meme_type[0][1], None))
            
            return meme_file_element
            
        # Parse XML and rebuild internal structure
        self.root_element = parse_xml_element(root_xml)

    def save_to_xml(self, xml_path=None):
        def build_xml(element, parent_xml):
            description = None if element.description == "Next node" else element.description
            
            add_group_element = element.has_occupied_next_node and not parent_xml.tag in ["g", "MemeFile"]
            
            if add_group_element:
                parent_xml = ET.SubElement(parent_xml, "g")
                if description is not None:
                    parent_xml.set("description", description)
            
            xml_node = ET.SubElement(parent_xml, element.type_name)
            
            if not add_group_element and description is not None:
                xml_node.set("description", description)
            
            if element.object_name is not None:
                xml_node.set("name", element.object_name)

            if element.is_primitive:
                # No list — just a value
                value = element.child_elements
                if value is not None:
                    xml_node.text = str(value)
            elif element.is_complex_type and len(element.child_elements) > 0:
                next_node = None
                children = element.child_elements
                first_child = children[0]
                if element.has_next_node:
                    next_node = first_child
                    children = children[1:]

                # Recurse for remaining children
                # If there is only one child which is a value type directly put that in the xml_node
                if len(children) == 1 and first_child.is_primitive:
                    xml_node.text = str(first_child.child_elements)
                else:
                    for child in children:
                        build_xml(child, xml_node)

                # After processing, move "Next Node" to parent level
                if element.has_occupied_next_node:
                    build_xml(next_node, parent_xml)

            return xml_node
            
        xml_path = xml_path or Path(self.file_path).with_suffix('.meme.xml')
        
        # Build XML tree
        root_xml = ET.Element("MemeFile")
        build_xml(self.root_element, root_xml)
        tree = ET.ElementTree(root_xml)
        ET.indent(tree, space="  ", level=0)
        
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
