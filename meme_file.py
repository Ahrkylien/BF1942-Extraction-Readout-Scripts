import json
import struct
from pathlib import Path


with open(Path(__file__).parent / "meme_types.json", encoding="utf-8") as f:
    meme_types = json.load(f)

# Primitive type -> (struct format of the value, or of the length before the text; text encoding, or None for a number)
primitive_formats = {
    "Boolean": ("B", None),
    "Byte": ("B", None),
    "Int": ("<i", None),
    "TypeIndex": ("<i", None),
    "Float": ("<f", None),
    "PictureString": ("B", "cp1252"),
    "FontString": ("B", "cp1252"),
    "SoundString": ("B", "cp1252"),
    "String": ("<I", "cp1252"),
    "WideString": ("<I", "UTF-16 LE"),
}

_type_string_prefix = "dice::meme::"
_version_string = "MemeFile 2.0"
_reference_type_names = ["Object", "Event", "Action", "Data", "Effect", "Function", "Empty", "Style", "Tree", "Node", "NextNode"]


def _read_struct(f, struct_format):
    size = struct.calcsize(struct_format)
    data = f.read(size)
    if len(data) < size:
        raise EOFError(f"Unexpected EOF while reading '{struct_format}'")
    return struct.unpack(struct_format, data)[0]


def _read_primitive(f, type_name):
    value_format, encoding = primitive_formats[type_name]
    value = _read_struct(f, value_format)
    if encoding is None:
        return value == 1 if type_name == "Boolean" else value
    # The length of a WideString counts characters of two bytes
    size = value * 2 if encoding == "UTF-16 LE" else value
    data = f.read(size)
    if len(data) < size:
        raise EOFError(f"Unexpected EOF while reading a {size}-byte string")
    return data.decode(encoding)


def _write_primitive(f, type_name, value):
    value_format, encoding = primitive_formats[type_name]
    if encoding is None:
        f.write(struct.pack(value_format, int(value) if type_name == "Boolean" else value))
        return
    encoded = value.encode(encoding)
    f.write(struct.pack(value_format, len(value) if encoding == "UTF-16 LE" else len(encoded)))
    f.write(encoded)


class MemeFileElement:
    """
    An object of the file: a complex type with its child elements, or a primitive value (child_elements is the value).
    A placeholder is an empty reference: its type is <slot type>Placeholder, and it has no child elements.
    """

    def __init__(self, type_name, object_name, description, child_elements):
        self.type_name = type_name
        self.object_name = object_name
        self.description = description
        self.child_elements = child_elements

    @classmethod
    def placeholder(cls, slot_type, description, object_name=None):
        """An empty reference: the field of type slot_type holds nothing."""
        return cls(f"{slot_type}Placeholder", object_name, description, None)

    @classmethod
    def build(cls, type_name, values, object_name=None, description=None):
        """
        A new complex element from one value per schema field. A list field takes its items; the end marker is added.
        A field that is None becomes an empty reference, and a primitive field that is None is an error.
        """
        children = []
        for (slot_type, label), value in zip(meme_types[type_name], values):
            if slot_type == "List":
                items = list(value or [])
                if not items or not items[-1].is_placeholder:
                    items.append(cls.placeholder("Object", None))
                children.extend(items)
                continue
            if value is None:
                if slot_type in primitive_formats:
                    raise ValueError(f"<{type_name}> needs its '{label}' field")
                value = cls.placeholder(slot_type, None)
            value.description = label
            children.append(value)
        return cls(type_name, object_name, description, children)

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
    def is_occupied(self):
        """A complex type, or a placeholder with a name."""
        return self.is_complex_type or self.object_name is not None

    @property
    def has_next_node(self):
        return self.is_complex_type and len(self.child_elements) > 0 and self.child_elements[0].description == "Next node"

    @property
    def has_occupied_next_node(self):
        return self.has_next_node and self.child_elements[0].is_occupied

    def field_values(self):
        """The value of each schema field: a primitive or an element, or for a list the list of its items with the end marker."""
        values = []
        position = 0
        for slot_type, _ in meme_types[self.type_name]:
            if slot_type == "List":
                end = position
                while not self.child_elements[end].is_placeholder:
                    end += 1
                values.append(self.child_elements[position:end + 1])
                position = end + 1
            else:
                values.append(self.child_elements[position])
                position += 1
        return values

    def walk(self):
        """This element and everything below it, depth first."""
        yield self
        if self.is_complex_type:
            for child in self.child_elements:
                yield from child.walk()


# Node types that do not affect the nodes after them in their chain, so a group of them can be removed (see MemeFile.flatten).
# Nodes such as EffectNode and TranslateNode apply to the nodes after them; any type not listed here is treated that way.
_SELF_CONTAINED_NODE_TYPES = {
    "TransformNode", "BfTransformNode", "BfTransformNodeSize", "PictureNode", "BfNavigationButtonNode",
    "BfLocalePictureButtonNode", "BfCreditsNode", "BfAddSubEffectNode", "BfAddSubNextEffectNode",
    "CullEventActionNode", "CullVariableActionNode", "CullVariableAndEventActionNode",
    # The body of an if and the content of a group stay apart from the nodes after them
    "CullNode", "SplitNode",
}


def _link_chain(elements):
    """Link elements into one chain in this order, and return them. The first element may have changed."""
    for i in range(len(elements) - 1):
        # A CullNode's next node holds its body, so a CullNode with nodes after it needs a SplitNode around it
        if elements[i].type_name == "CullNode":
            cull = elements[i]
            elements[i] = MemeFileElement("SplitNode", cull.object_name, cull.description,
                                          [MemeFileElement.placeholder("NextNode", "Next node"), cull])
            cull.object_name = None
            cull.description = "Split node"
    for element in elements[1:]:
        element.description = "Next node"
    for i in range(len(elements) - 1):
        elements[i].child_elements[0] = elements[i + 1]
    return elements


def _chain_nodes(head):
    """The nodes of a chain in order. A CullNode ends its chain, because its next node holds its body."""
    nodes = []
    node = head
    while node.is_complex_type:
        nodes.append(node)
        if node.type_name == "CullNode" or not node.has_next_node:
            break
        node = node.child_elements[0]
    return nodes


class MemeFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.root_element = None

    def read(self):
        """Read the binary meme file."""
        with open(self.file_path, "rb") as f:
            strings = []
            while True:
                string_length = _read_struct(f, "B")
                if string_length == 0:
                    break
                strings.append(f.read(string_length).decode("cp1252"))

            def type_name_at(index):
                type_string = strings[index]
                if not type_string.startswith(_type_string_prefix):
                    raise ValueError(f"Type without prefix: {type_string}")
                type_name = type_string[len(_type_string_prefix):]
                if type_name not in meme_types:
                    raise ValueError(f"Unknown type: {type_name}")
                return type_name

            def read_children(type_name):
                children = []
                for child_type, description in meme_types[type_name]:
                    if child_type == "List":
                        # A list is a run of objects, ended by an empty reference
                        while True:
                            child = read_reference("Object", None)
                            children.append(child)
                            if child.is_placeholder:
                                break
                    elif child_type in _reference_type_names:
                        children.append(read_reference(child_type, description))
                    elif child_type in primitive_formats:
                        children.append(MemeFileElement(child_type, None, description, _read_primitive(f, child_type)))
                    else:
                        children.append(MemeFileElement(child_type, None, description, read_children(child_type)))
                return children

            def read_reference(slot_type, description, is_root=False):
                object_name = None
                if not is_root:
                    _read_struct(f, "<I")  # Block size, which write works out again
                    name_index = _read_struct(f, "<H")
                    if name_index != 0:
                        object_name = strings[name_index]
                type_index = _read_struct(f, "<H")
                if type_index == 0:
                    return MemeFileElement.placeholder(slot_type, description, object_name)
                type_name = type_name_at(type_index)
                return MemeFileElement(type_name, object_name, description, read_children(type_name))

            self.root_element = read_reference("", None, is_root=True)

            bytes_left = len(f.read())
            if bytes_left > 0:
                raise ValueError(f"Data left at tail: {bytes_left}")

    def write(self, output_path=None):
        """Write the binary meme file."""
        output_path = output_path or self.file_path

        strings = [_version_string]
        for element in self.root_element.walk():
            # Placeholders can have names too
            for string in (element.object_name, _type_string_prefix + element.type_name if element.is_complex_type else None):
                if string and string not in strings:
                    strings.append(string)

        with open(output_path, "wb") as f:
            def write_element(element, is_root=False):
                if element.is_primitive:
                    _write_primitive(f, element.type_name, element.child_elements)
                    return
                if not is_root:
                    block_start = f.tell()
                    # The block size is filled in once the block is written
                    f.write(struct.pack("<IH", 0, strings.index(element.object_name) if element.object_name else 0))
                f.write(struct.pack("<H", 0 if element.is_placeholder else strings.index(_type_string_prefix + element.type_name)))
                if element.is_complex_type:
                    for child in element.child_elements:
                        write_element(child)
                if not is_root:
                    block_end = f.tell()
                    f.seek(block_start)
                    f.write(struct.pack("<I", block_end - block_start))
                    f.seek(block_end)

            for string in strings:
                encoded = string.encode("cp1252")
                if len(encoded) > 255:
                    raise ValueError(f"String too long ({len(encoded)}): {string}")
                f.write(struct.pack("B", len(encoded)))
                f.write(encoded)
            f.write(b"\x00")

            write_element(self.root_element, is_root=True)

    def flatten(self):
        """
        Remove the groups that are not needed. A group is a SplitNode that is not part of an if. It is not needed when
        nothing follows it, or when none of the nodes directly in it affects the nodes after it.
        """
        def is_removable_group(element):
            if element.type_name != "SplitNode" or element.object_name is not None:
                return False
            next_node, content = element.child_elements
            if content.type_name == "CullNode" and next_node.is_occupied:
                return False  # The SplitNode of an if with nodes after it
            if content.is_placeholder:
                return content.object_name is None
            nodes = _chain_nodes(content)
            last = nodes[-1]
            if last.type_name != "CullNode" and (not last.has_next_node or last.child_elements[0].is_occupied):
                return False  # The content ends in a named placeholder, so nothing can be attached after it
            return not next_node.is_occupied or all(node.type_name in _SELF_CONTAINED_NODE_TYPES for node in nodes)

        def remove_group(group):
            """Put the group's nodes in its place, followed by the nodes after the group."""
            next_node, content = group.child_elements
            nodes = [] if content.is_placeholder else _chain_nodes(content)
            head = _link_chain(nodes + [next_node] if next_node.is_occupied or not nodes else nodes)[0]
            head.description = group.description
            return head

        def flatten_element(element):
            if not element.is_complex_type:
                return element
            element.child_elements = [flatten_element(child) for child in element.child_elements]
            return remove_group(element) if is_removable_group(element) else element

        self.root_element = flatten_element(self.root_element)

    def load_from_xml(self, xml_path=None):
        """Read an XML file, in either form of documentation/MemeXmlFormat.md."""
        from .meme_xml import load_xml
        self.root_element = load_xml(xml_path or Path(self.file_path).with_suffix(".meme.xml"))

    def save_to_xml(self, xml_path=None, compact=True):
        """Write the XML file: the compact form, or with compact=False every field as a child element."""
        from .meme_xml import save_xml
        save_xml(self.root_element, xml_path or Path(self.file_path).with_suffix(".meme.xml"), compact)
