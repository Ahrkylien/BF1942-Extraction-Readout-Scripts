import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from BF1942_Extraction_Readout_Scripts.meme_file import MemeFile, MemeFileElement, meme_types, primitive_formats
from BF1942_Extraction_Readout_Scripts.meme_xml_tags import category

TEST_DATA_DIR = Path(__file__).parent / "meme_file_data"
CATEGORIES = ("Node", "Action", "Data", "Effect", "Style", "Event", "Function", "Pointer")
# The elements that hold a value as their text: a primitive, or a variable
VALUE_TAGS = set(primitive_formats) | {"Variable"}


def get_test_files():
    return [
        f for f in TEST_DATA_DIR.rglob("*")
        if f.is_file() and f.suffix == ""
    ]


def assert_xml_roundtrip(binary_path, tmp_path, compact=True):
    """
    Test:
    binary -> XML -> binary should produce an identical file
    """
    meme = MemeFile(binary_path)
    meme.read()

    xml_path = tmp_path / (binary_path.name + ".xml")
    meme.save_to_xml(xml_path, compact=compact)

    meme_from_xml = MemeFile(binary_path)
    meme_from_xml.load_from_xml(xml_path)
    rebuilt_path = tmp_path / (binary_path.name + ".rebuilt")
    meme_from_xml.write(rebuilt_path)

    assert binary_path.read_bytes() == rebuilt_path.read_bytes(), f"Mismatch in {binary_path.name}"
    return ET.parse(xml_path).getroot()


def assert_xml_shape(xml_root, compact, file_name):
    """Text is only the value of a primitive or a variable, and <Variables> comes first."""
    for element in xml_root.iter():
        if element.tag not in VALUE_TAGS:
            assert not (element.text or "").strip(), f"<{element.tag}> has text in {file_name}"
    variables = xml_root.find("Variables")
    assert variables is None or list(xml_root).index(variables) == 0, f"<Variables> is not first in {file_name}"
    if not compact:
        assert variables is None, f"<Variables> in the element form of {file_name}"
        for element in xml_root.iter():
            assert not element.attrib.keys() - {"name", "description", "type", "uses_crlf"}, f"<{element.tag}> has attributes in {file_name}"


def test_variable_with_different_values_uses_the_first_and_warns(tmp_path, capsys):
    """A variable has one value: the first use's. A later use with another value is written with it, and a warning names the variable."""
    def float_set(value):
        return MemeFileElement.build("SetVariableAction", [MemeFileElement.placeholder("Data", None),
                                                           MemeFileElement.build("FloatData", [MemeFileElement("Float", None, None, value)], "Some/Zero")])
    first = MemeFileElement.build("ActionNode", [None, float_set(0.0)])
    second = MemeFileElement.build("ActionNode", [first, float_set(-0.0)])
    meme = MemeFile(tmp_path / "zero")
    meme.root_element = second
    meme.save_to_xml(tmp_path / "zero.xml")

    assert "Warning: variable 'Some/Zero': a later FloatData differs from the first use" in capsys.readouterr().err
    variables = ET.parse(tmp_path / "zero.xml").getroot().find("Variables")
    assert [(v.get("name"), v.text) for v in variables] == [("Some/Zero", "0")]


def test_variable_with_equal_values_gives_no_warning(tmp_path, capsys):
    def float_set(value):
        return MemeFileElement.build("SetVariableAction", [MemeFileElement.placeholder("Data", None),
                                                           MemeFileElement.build("FloatData", [MemeFileElement("Float", None, None, value)], "Some/Zero")])
    first = MemeFileElement.build("ActionNode", [None, float_set(0.5)])
    second = MemeFileElement.build("ActionNode", [first, float_set(0.5)])
    meme = MemeFile(tmp_path / "same")
    meme.root_element = second
    meme.save_to_xml(tmp_path / "same.xml")
    assert capsys.readouterr().err == ""


@pytest.mark.parametrize("compact", [True, False], ids=["compact", "element form"])
@pytest.mark.parametrize("file_path", get_test_files())
def test_binary_xml_roundtrip(file_path, tmp_path, compact):
    """
    Test:
    binary -> XML -> binary should produce an identical file, in the compact form and in the element form
    """
    assert_xml_shape(assert_xml_roundtrip(file_path, tmp_path, compact), compact, file_path.name)


@pytest.mark.parametrize("compact", [True, False], ids=["compact", "element form"])
@pytest.mark.parametrize("file_path", get_test_files())
def test_flattened_binary_xml_roundtrip(file_path, tmp_path, compact):
    """
    Test:
    binary -> flatten -> binary, and that binary -> XML -> binary should produce an identical file
    """
    meme = MemeFile(file_path)
    meme.read()
    meme.flatten()
    flattened_path = tmp_path / (file_path.name + ".flattened")
    meme.write(flattened_path)

    assert_xml_shape(assert_xml_roundtrip(flattened_path, tmp_path, compact), compact, file_path.name)


# ---------------------------------------------------------------------------------------------------------------------
# A file with every type, and objects the game files do not have
# ---------------------------------------------------------------------------------------------------------------------

PRIMITIVE_OF_KIND = {"IntData": "Int", "FloatData": "Float", "BoolData": "Boolean", "StringData": "String", "WstringData": "WideString"}
DEFAULT_PRIMITIVES = {"Boolean": True, "Byte": 1, "Int": 2, "TypeIndex": 3, "Float": 0.5,
                      "String": "text", "WideString": "wide", "PictureString": "a.tga", "FontString": "f.dif", "SoundString": "s.wav"}


def new_object(type_name, name=None, **fields):
    """An object of type_name, with a default in each primitive field and an empty reference in each object field."""
    values = []
    for slot_type, label in meme_types[type_name]:
        if label in fields:
            values.append(fields[label])
        elif slot_type in primitive_formats:
            values.append(MemeFileElement(slot_type, None, None, DEFAULT_PRIMITIVES[slot_type]))
        else:
            values.append([] if slot_type == "List" else None)
    return MemeFileElement.build(type_name, values, name)


def value_element(type_name, value, name=None):
    """A Data element holding value, which is a literal, or a variable when it has a name."""
    return MemeFileElement.build(type_name, [MemeFileElement(PRIMITIVE_OF_KIND[type_name], None, None, value)], name)


def chain(*nodes):
    for node, following in zip(nodes, nodes[1:]):
        following.description = "Next node"
        node.child_elements[0] = following
    return nodes[0]


def in_node_position(content):
    """A TransformNode whose transformed node field holds content."""
    return new_object("TransformNode", **{"Transformed node": content})


def every_type_tree():
    types_of = {c: [t for t in meme_types if category(t) == c] for c in CATEGORIES}
    nodes = [new_object("NameNode")]
    for type_name in types_of["Node"]:
        node = new_object(type_name)
        nodes.append(node if node.has_next_node else in_node_position(node))
    for type_name in types_of["Pointer"] + [t for t in meme_types if category(t) is None]:
        nodes.append(in_node_position(new_object(type_name)))
    nodes.append(new_object("ActionNode", Action=new_object("ActionListAction", **{"Action list": [new_object(t) for t in types_of["Action"]]})))
    for type_name in types_of["Data"]:
        nodes.append(new_object("ActionNode", Action=new_object("SetVariableAction", Data=new_object(type_name))))
    for type_name in types_of["Effect"]:
        nodes.append(new_object("EffectNode", Effect=new_object(type_name)))
    for type_name in types_of["Style"]:
        nodes.append(new_object("TextNode", Style=new_object(type_name)))
    for type_name in types_of["Event"]:
        nodes.append(new_object("CullEventActionNode", Event=new_object(type_name)))
    for type_name in types_of["Function"]:
        nodes.append(new_object("ActionNode", Action=new_object("CallFunctionAction", Function=new_object(type_name, "Some/Function"))))

    def set_data(data):
        return new_object("ActionNode", Action=new_object("SetVariableAction", Variable=value_element("IntData", 1, "Some/Int"), Data=data))

    def color(type_name, *channels):
        return new_object("EffectNode", Effect=new_object(type_name, **dict(zip(("Red", "Green", "Blue", "Alpha"), channels))))

    def floats(*values):
        return [MemeFileElement("Float", None, None, value) for value in values]

    unusual = [
        # Objects in a field of another category
        set_data(new_object("TextNode")),
        in_node_position(new_object("Action")),
        in_node_position(new_object("Effect")),
        in_node_position(new_object("IntData")),
        new_object("EffectNode", Effect=new_object("SetVariableAction")),
        # Names: a named event, a name that is no identifier, a name that is a keyword, variables made of variables
        new_object("CullEventActionNode", Event=new_object("ButtonEvent", "Named/Event")),
        new_object("CullEventActionNode", Event=new_object("ButtonEvent", "Named/Event")),
        set_data(value_element("IntData", 5, "bad name!")),
        set_data(value_element("BoolData", True, "and")),
        set_data(new_object("BfLocaleData", "Some/Locale", Valid=value_element("BoolData", True, "Some/Valid"))),
        set_data(new_object("BfLocaleData", "Some/Locale", Valid=value_element("BoolData", True, "Some/Valid"))),
        set_data(MemeFileElement.placeholder("Data", None, "Named/Empty")),
        new_object("TextNode", Style=new_object("CenterAlignedStyle", "Some/Style")),
        new_object("ActionNode", Action=new_object("CallFunctionAction", Function=new_object("Function"))),
        set_data(new_object("BfEditData", "Named/Edit")),
        # A named end marker, a named empty node field, and nodes in a list
        set_data(MemeFileElement.build("DataListData", [[value_element("IntData", 1), MemeFileElement.placeholder("Object", None, "Named/End")]])),
        in_node_position(MemeFileElement.placeholder("Node", None, "Named/Node")),
        new_object("NodeListNode", **{"Node list": [chain(new_object("NameNode"), new_object("NameNode")), new_object("NameNode")]}),
        # Values that need care: quotes, line breaks, floats that are not finite, exact and inexact colors
        set_data(value_element("StringData", "it's \"quoted\"\r\nline two")),
        set_data(value_element("WstringData", "w'ide")),
        set_data(value_element("FloatData", float("inf"))),
        new_object("TimeoutActionNode", **{"Timeout time": MemeFileElement("Float", None, None, float("nan"))}),
        color("ColorEffect", *floats(17 / 255, 34 / 255, 51 / 255, 1.0)),
        color("ColorEffect", *floats(17 / 255, 34 / 255, 51 / 255, 68 / 255)),
        color("ColorEffect", *floats(0.8437, 0.73, 0.65, 0.5)),
        color("VariableColorEffect", *[value_element("FloatData", v) for v in (17 / 255, 34 / 255, 51 / 255, 1.0)]),
        color("VariableColorEffect", value_element("FloatData", 0.0, "Some/Red"), *[value_element("FloatData", 0.5) for _ in range(3)]),
        color("BfMultiplyColorEffect", *[value_element("IntData", 1) for _ in range(4)]),
        new_object("BfTransformNode", X=value_element("IntData", 1), Y=value_element("IntData", 2)),
        # A CullNode whose condition has no text form, and a split node around one
        new_object("SplitNode", **{"Split node": new_object("CullNode", Data=new_object("BfListBoxData"))}),
        new_object("CullNode", **{"In time": MemeFileElement("Float", None, None, float("inf"))}),
        new_object("CullNode", Data=new_object("BfListBoxData")),
        new_object("NameNode"),
    ]
    return chain(*nodes, *unusual)


@pytest.mark.parametrize("compact", [True, False], ids=["compact", "element form"])
def test_every_type_roundtrip(tmp_path, compact):
    """A binary with every type, and objects the game files do not have, reads back from XML identically."""
    meme = MemeFile(tmp_path / "every_type")
    meme.root_element = every_type_tree()
    # The tree must hold every type in meme_types.json, so that the test covers all of them
    used = {element.type_name for element in meme.root_element.walk()}
    assert set(meme_types) - used == set(), "types missing from the every-type tree"
    meme.write()
    assert_xml_roundtrip(tmp_path / "every_type", tmp_path, compact)


def test_every_type_compact_xml_is_stable(tmp_path):
    """Writing the XML of a file that was read from that XML gives the same XML."""
    meme = MemeFile(tmp_path / "every_type")
    meme.root_element = every_type_tree()
    meme.save_to_xml(tmp_path / "first.xml")
    meme.load_from_xml(tmp_path / "first.xml")
    meme.save_to_xml(tmp_path / "second.xml")
    assert (tmp_path / "first.xml").read_text(encoding="utf-8") == (tmp_path / "second.xml").read_text(encoding="utf-8")
