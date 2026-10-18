from pathlib import Path

import pytest

from BF1942_Extraction_Readout_Scripts.meme_file import MemeFile, MemeFileElement
from BF1942_Extraction_Readout_Scripts.meme_xml_text import TextReader, TextWriter, Variables, XmlError, float_to_text, value_from_text, value_text

TEST_DATA_DIR = Path(__file__).parent / "meme_file_data"
RAW_XML_DIR = Path(__file__).parent / "raw_meme_types_xml"
CONDITION_VARIABLES = {
    "somevar": ("Int", 0),
    "flag": ("Boolean", False),
    "Navigation/NavigationY": ("Float", 33.0),
}


def variables_of(values):
    variables = Variables()
    variables.values.update(values)
    return variables


def read_expression(text, values=CONDITION_VARIABLES):
    return TextReader(variables_of(values)).object(text, "Data")


def write_expression(element):
    return TextWriter(lambda named: named.object_name is not None).object(element, "Data")


def value(type_name, number, name=None):
    primitive = {"IntData": "Int", "FloatData": "Float", "BoolData": "Boolean"}[type_name]
    return MemeFileElement.build(type_name, [MemeFileElement(primitive, None, None, number)], name)


def operator(type_name, *operands):
    return MemeFileElement.build(type_name, list(operands))


@pytest.mark.parametrize(("condition", "expected"), [
    ("somevar is 1", "somevar is 1"),
    ("not flag", "not flag"),
    ("(somevar is 1) or (somevar is 2)", "somevar is 1 or somevar is 2"),
    ("somevar is 1 and (flag or not flag)", "somevar is 1 and (flag or not flag)"),
    ("not (somevar is 1)", "not (somevar is 1)"),
    ("somevar is (not flag)", "somevar is not flag"),
    ("somevar minus (1 minus 2)", "somevar minus (1 minus 2)"),
    ("somevar plus 1 times 2", "somevar plus 1 times 2"),
    ("Navigation/NavigationY divided_by 2.0 less_than 1.5", "Navigation/NavigationY divided_by 2.0 less_than 1.5"),
    ("[flag, not flag][somevar]", "[flag, not flag][somevar]"),
    ("not null", "not null"),
])
def test_expression_text_is_canonical(condition, expected):
    assert write_expression(read_expression(condition)) == expected


@pytest.mark.parametrize(("build", "expected"), [
    (lambda: operator("EqualData", value("IntData", 0, "somevar"), operator("NotData", value("BoolData", False, "flag"))),
     "somevar is not flag"),
    (lambda: operator("NotData", operator("EqualData", value("IntData", 0, "somevar"), value("IntData", 1))),
     "not (somevar is 1)"),
    (lambda: operator("EqualData", operator("EqualData", value("IntData", 0, "somevar"), value("IntData", 1)), value("BoolData", False, "flag")),
     "(somevar is 1) is flag"),
    (lambda: operator("SubData", value("IntData", 0, "somevar"), operator("SubData", value("IntData", 0, "somevar"), value("IntData", 1))),
     "somevar minus (somevar minus 1)"),
])
def test_written_expression_reads_back_as_the_same_tree(build, expected):
    tree = build()
    assert write_expression(tree) == expected
    assert_same_tree(read_expression(expected, dict(CONDITION_VARIABLES, somevar=("Int", 0))), tree)


def assert_same_tree(a, b):
    assert (a.type_name, a.object_name) == (b.type_name, b.object_name)
    if isinstance(a.child_elements, list):
        assert len(a.child_elements) == len(b.child_elements)
        for x, y in zip(a.child_elements, b.child_elements):
            assert_same_tree(x, y)
    else:
        assert a.child_elements == b.child_elements


@pytest.mark.parametrize(("name", "text"), [("and", "$and"), ("$and", "$$and"), ("$flag", "$flag")])
def test_keyword_names_are_escaped_and_read_back(name, text):
    element = value("BoolData", False, name)
    assert write_expression(element) == text
    assert read_expression(text, {name: ("Boolean", False)}).object_name == name


@pytest.mark.parametrize(("value_", "expected"), [
    (0.8999999761581421, "0.9"),
    (1.0, "1"),
    (800.0, "800"),
    (1e20, "100000000000000000000"),
    (-0.0, "-0"),
])
def test_float_text_is_the_shortest_that_reads_back(value_, expected):
    assert float_to_text(value_) == expected


def test_unknown_variable_is_an_error():
    with pytest.raises(XmlError, match="unknown variable 'missing'"):
        read_expression("missing is 1")


def test_chained_comparison_is_an_error():
    with pytest.raises(XmlError, match="cannot be chained"):
        read_expression("somevar is 1 is 2")


# --- Colors --------------------------------------------------------------------------------------------------------

def read_color(text, slot, values=None):
    return TextReader(variables_of(values or {})).color(text, slot)


@pytest.mark.parametrize(("text", "expected"), [
    ("#112233", [0x11 / 255, 0x22 / 255, 0x33 / 255, 1.0]),
    ("#11223344", [0x11 / 255, 0x22 / 255, 0x33 / 255, 0x44 / 255]),
    ("#112233, 0.5", [0x11 / 255, 0x22 / 255, 0x33 / 255, 0.5]),
    ("0.8, 0.7, 0.6", [0.8, 0.7, 0.6, 1.0]),
    ("0.8, 0.7, 0.6, 0.5", [0.8, 0.7, 0.6, 0.5]),
])
def test_float_color_forms_are_read(text, expected):
    channels = read_color(text, "Float")
    assert [channel.child_elements for channel in channels] == pytest.approx(expected, rel=1e-6)


def test_float_color_takes_no_expression():
    with pytest.raises(XmlError, match="takes only numbers"):
        read_color("0.5, somevar, 0.5, 1.0", "Float", {"somevar": ("Float", 1.0)})


def test_data_color_takes_expressions_per_channel():
    channels = read_color("0.5, somevar, 0.5, 1.0 minus somevar", "Data", {"somevar": ("Int", 0)})
    assert [channel.type_name for channel in channels] == ["FloatData", "IntData", "FloatData", "SubData"]


@pytest.mark.parametrize(("values", "expected"), [
    ((17 / 255, 34 / 255, 51 / 255, 1.0), "#112233"),
    ((17 / 255, 34 / 255, 51 / 255, 68 / 255), "#11223344"),
    ((17 / 255, 34 / 255, 51 / 255, 0.5), "#112233, 0.5"),
    ((0.8, 0.7, 0.6, 1.0), "0.8, 0.7, 0.6"),
    ((0.8, 0.7, 0.6, 0.5), "0.8, 0.7, 0.6, 0.5"),
])
def test_color_is_written_in_the_shortest_form(values, expected):
    channels = [MemeFileElement("Float", None, None, value_) for value_ in values]
    assert TextWriter(lambda element: False).color(channels, "Float") == expected


def test_color_with_expression_alpha_is_written_after_the_hex():
    channels = [value("FloatData", 17 / 255), value("FloatData", 34 / 255), value("FloatData", 51 / 255), value("FloatData", 1.0)]
    channels[3] = operator("SubData", value("FloatData", 1.0), value("IntData", 0, "somevar"))
    assert TextWriter(lambda element: element.object_name is not None).color(channels, "Data") == "#112233, 1.0 minus somevar"


# --- Tags and their picking ----------------------------------------------------------------------------------------

def load(tmp_path, body, variables=""):
    xml_path = tmp_path / "statement.xml"
    xml_path.write_text(f"""<?xml version='1.0' encoding='utf-8'?>
<MemeFile>
  <Variables>
    <Variable name="somevar" type="Int">0</Variable>
    {variables}
  </Variables>
  <NameNode />
  {body}
</MemeFile>
""", encoding="utf-8")
    meme = MemeFile(tmp_path / "statement")
    meme.load_from_xml(xml_path)
    return meme.root_element.child_elements[0]


@pytest.mark.parametrize(("attributes", "expected_type"), [
    ('x="1" y="2" width="3" height="4"', "TransformNode"),
    ('x="10" y="somevar plus 1" width="3" height="4"', "BfTransformNode"),
    ('x="1" y="2" width="somevar" height="4.0"', "BfTransformNodeSize"),
])
def test_shared_tag_is_read_as_the_type_that_fits(tmp_path, attributes, expected_type):
    assert load(tmp_path, f"<Transform {attributes}><NameNode /></Transform>").type_name == expected_type


@pytest.mark.parametrize(("body", "expected_type"), [
    ('<Effect><MultiplyColor alpha="0.5" /></Effect>', "BfMultiplyColorEffect2"),
    ('<Effect><MultiplyColor color="0.5, 0.5, 0.5, 0.5" /></Effect>', "MultiplyColorEffect"),
    ('<Effect><MultiplyColor color="somevar, 0.5, 0.5, 0.5" /></Effect>', "BfMultiplyColorEffect"),
])
def test_multiply_color_is_read_by_its_attributes(tmp_path, body, expected_type):
    assert load(tmp_path, body).child_elements[1].type_name == expected_type


STYLE = "style=\"CenterAligned('standard6.dif')\""
VERTICAL_SCROLL = "text=\"'Hello'\" scroll-speed=\"1\" scroll-speed-multiplier=\"1\" restart-toggle=\"0\""


@pytest.mark.parametrize(("attributes", "expected_type"), [
    (f'font="Font1" {VERTICAL_SCROLL}', "BfVerticalScrollNode"),
    (f'version="1" {STYLE} {VERTICAL_SCROLL}', "BfVerticalScrollExNode"),
    (f'{VERTICAL_SCROLL} font="Font1"', "BfVerticalScrollNode"),
    (f'{VERTICAL_SCROLL} {STYLE} version="1"', "BfVerticalScrollExNode"),
])
def test_vertical_scroll_is_read_by_its_attributes_in_any_order(tmp_path, attributes, expected_type):
    assert load(tmp_path, f"<VerticalScroll {attributes} />").type_name == expected_type


@pytest.mark.parametrize("attributes", [
    f'font="Font1" {STYLE} {VERTICAL_SCROLL}',
    f'version="1" font="Font1" {VERTICAL_SCROLL}',
    f'version="1" {VERTICAL_SCROLL}',
    f'{STYLE} {VERTICAL_SCROLL}',
    VERTICAL_SCROLL,
])
def test_vertical_scroll_with_attributes_of_no_type_is_an_error(tmp_path, attributes):
    with pytest.raises(XmlError, match="fits no type"):
        load(tmp_path, f"<VerticalScroll {attributes} />")


PICTURE_FILL = 'fill-picture="fill.dds" data="somevar" maximum-value="1" horizontal-align="true" fill-order="true"'


@pytest.mark.parametrize(("attributes", "expected_type"), [
    (f'picture="base.dds" {PICTURE_FILL}', "BfPictureFillNode"),
    (f'picture="base.dds" size="2" {PICTURE_FILL}', "BfVariablePictureFillNode"),
    ("picture=\"'base.dds'\" fill-picture=\"'fill.dds'\" size=\"somevar\" data=\"somevar\" maximum-value=\"1\" "
     "horizontal-align=\"true\" fill-order=\"true\"", "BfVariablePictureFillNode2"),
])
def test_picture_is_read_by_its_attributes(tmp_path, attributes, expected_type):
    assert load(tmp_path, f"<Picture {attributes} />").type_name == expected_type


def test_picture_with_size_and_no_fill_order_is_an_error(tmp_path):
    with pytest.raises(XmlError, match="fits no type"):
        load(tmp_path, '<Picture picture="base.dds" size="2" fill-picture="fill.dds" data="somevar" '
                       'maximum-value="1" horizontal-align="true" />')


LIST_BOX_DATA = '<BfListBoxData field="listbox-data"><Placeholder /><Placeholder /><Placeholder /></BfListBoxData>'
NEW_LIST_BOX = ('font="standard6 - Latin.dif" step-sound="Sounds/Step" '
                'select-sound="Sounds/Select" failed-select-sound="Sounds/Failed" row-height="18" is-selectable="true" '
                'border="false" background-color="0, 0, 0, 0" scrollbar-width="6" frame-color="107, 380, 36, 0" '
                'select-color="0, 0.1875, 0.539, 0" show-tooltip="false" scrollbar-offset="0"')


def test_new_list_box_reads_each_action_by_its_field_attribute(tmp_path):
    node = load(tmp_path, f'<ListBox {NEW_LIST_BOX}>{LIST_BOX_DATA}'
                          '<CallFunction field="focus-action" function="Some/Func" /></ListBox>')
    assert node.type_name == "BfNewListBoxNode"
    assert node.field_values()[1].type_name == "BfListBoxData"
    assert node.field_values()[3].is_placeholder
    assert node.field_values()[4].type_name == "CallFunctionAction"


def test_list_box_attributes_with_a_default_can_be_left_out(tmp_path):
    required = ('font="standard6 - Latin.dif" row-height="18" background-color="0, 0, 0, 0" scrollbar-width="6" '
                'frame-color="107, 380, 36, 0" select-color="0, 0.1875, 0.539, 0"')
    node = load(tmp_path, f'<ListBox {required} scrollbar-offset="4">{LIST_BOX_DATA}</ListBox>')
    values = node.field_values()
    assert node.type_name == "BfNewListBoxNode"
    assert (values[5].child_elements, values[6].child_elements, values[7].child_elements) == ("", "", "")
    assert (values[9].child_elements, values[10].child_elements) == (True, False)
    assert values[24].child_elements is False


def test_new_list_box_child_with_an_unknown_field_name_is_an_error(tmp_path):
    with pytest.raises(XmlError, match="no child named 'middle-action'"):
        load(tmp_path, f'<ListBox {NEW_LIST_BOX}>{LIST_BOX_DATA}<CallFunction field="middle-action" function="Some/Func" /></ListBox>')


def test_new_list_box_two_children_for_one_field_is_an_error(tmp_path):
    with pytest.raises(XmlError, match="two children named 'focus-action'"):
        load(tmp_path, f'<ListBox {NEW_LIST_BOX}>{LIST_BOX_DATA}'
                       '<CallFunction field="focus-action" function="Some/Func" />'
                       '<CallFunction field="focus-action" function="Other/Func" /></ListBox>')


@pytest.mark.parametrize(("children", "message"), [
    ((("field", 3),), "reserved"),
    ((("select-action", 5),), "must write a field of an element type"),
    ((("select-action", 3), ("select-action", 4)), "used twice"),
])
def test_child_definitions_are_checked(children, message):
    from BF1942_Extraction_Readout_Scripts.meme_xml_tags import Child, Compact, _check
    compact = Compact("ListBox", "BfNewListBoxNode", (), children=tuple(Child(name, field) for name, field in children))
    with pytest.raises(ValueError, match=message):
        _check(compact)


def test_tag_that_fits_no_type_names_each_candidate(tmp_path):
    with pytest.raises(XmlError, match="fits no type"):
        load(tmp_path, '<Transform x="somevar" y="somevar" width="somevar" height="4" />')


def test_float_only_attribute_takes_no_expression(tmp_path):
    with pytest.raises(XmlError, match="top-left-color"):
        load(tmp_path, '<Effect><VertexColor top-left-color="somevar, 1, 1, 1" top-right-color="#ffffff" '
                       'bottom-right-color="#ffffff" bottom-left-color="#ffffff" /></Effect>')


@pytest.mark.parametrize(("body", "expected_type"), [
    ("<Clip />", "ClipNode"),
    ('<Effect><Clip x="0" y="0" width="1" height="1" /></Effect>', "ClipEffect"),
])
def test_a_tag_is_read_in_the_category_of_its_field(tmp_path, body, expected_type):
    node = load(tmp_path, body)
    found = node.child_elements[1] if node.type_name == "EffectNode" else node
    assert found.type_name == expected_type


def test_unknown_tag_is_an_error(tmp_path):
    with pytest.raises(XmlError, match="nor a type name"):
        load(tmp_path, "<NotAType />")


def test_unknown_attribute_is_an_error(tmp_path):
    with pytest.raises(XmlError, match="has no attribute 'colour'"):
        load(tmp_path, '<Effect><Color colour="#000000" /></Effect>')


def test_object_escape_reads_a_type_by_its_full_name(tmp_path):
    assert load(tmp_path, '<Object type="Action" />').type_name == "Action"


# --- Ifs, groups and chains ----------------------------------------------------------------------------------------

@pytest.mark.parametrize(("statement", "expected_type"), [
    ('<If condition="somevar is 1"><NameNode /></If>', "CullNode"),
    ('<Group><If condition="somevar is 1"><NameNode /></If></Group>', "SplitNode"),
])
def test_last_if_is_a_cull_node_or_a_group(tmp_path, statement, expected_type):
    last = load(tmp_path, statement)
    assert last.type_name == expected_type


def test_if_with_nodes_after_is_a_split_node_around_the_cull_node(tmp_path):
    xml_path = tmp_path / "if.xml"
    xml_path.write_text("""<?xml version='1.0' encoding='utf-8'?>
<MemeFile>
  <Variables><Variable name="somevar" type="Int">0</Variable></Variables>
  <If condition="somevar is 1"><NameNode /></If>
  <NameNode />
</MemeFile>
""", encoding="utf-8")
    meme = MemeFile(tmp_path / "if")
    meme.load_from_xml(xml_path)
    split = meme.root_element
    assert split.type_name == "SplitNode"
    assert split.child_elements[1].type_name == "CullNode"
    assert split.child_elements[0].type_name == "NameNode"


def test_if_defaults_its_fade_times_to_zero(tmp_path):
    cull = load(tmp_path, '<If condition="null" />')
    assert cull.type_name == "CullNode"
    assert [cull.child_elements[2].child_elements, cull.child_elements[3].child_elements] == [0.0, 0.0]


# --- Variables -----------------------------------------------------------------------------------------------------

def test_variable_can_hold_an_object(tmp_path):
    node = load(tmp_path, '<Text string="Some/Locale" style="CenterAligned(\'standard6.dif\')" />', """
    <Variable name="Some/Locale">LocaleString(Locale(Some/Valid), Some/Valid, 'ID')</Variable>
    <Variable name="Some/Valid" type="Boolean">true</Variable>""")
    string = node.child_elements[1]
    assert (string.type_name, string.object_name) == ("BfLocaleStringData", "Some/Locale")
    assert string.child_elements[0].child_elements[0].object_name == "Some/Valid"


def test_variable_defined_twice_is_an_error(tmp_path):
    with pytest.raises(XmlError, match="defined twice"):
        load(tmp_path, "<NameNode />", '<Variable name="somevar" type="Int">1</Variable>')


def test_named_object_with_fields_outside_variables_is_an_error():
    with pytest.raises(XmlError, match="belongs in <Variables>"):
        read_expression("Some/Sum: (somevar plus 1)")


# --- Engine names --------------------------------------------------------------------------------------------------

@pytest.mark.parametrize(("text", "expected"), [
    ("Button(0, ButtonPress, Select)", "Button(0, ButtonPress, Select)"),
    ("Button(0, 1, 1)", "Button(0, ButtonPress, Select)"),
    ("Button(0, ButtonPress, 19)", "Button(0, ButtonPress, 19)"),
    ("Type(0, 23)", "Type(0, 23)"),
    ("Button(8, 1, 1)", "Button(Fire, ButtonPress, Select)"),
])
def test_engine_names_in_attribute_text(text, expected):
    from BF1942_Extraction_Readout_Scripts.meme_xml_text import TextReader as Reader
    element = Reader(variables_of({})).object(text, "Event")
    assert TextWriter(lambda named: False).object(element, "Event") == expected


@pytest.mark.parametrize(("text", "expected_type"), [
    ("Button(0, ButtonPress, Select)", "ButtonEvent"),
    ("Button(0, ButtonPress, Select, 2)", "ExtendedButtonEvent"),
])
def test_call_with_a_shared_name_is_read_by_its_argument_count(text, expected_type):
    from BF1942_Extraction_Readout_Scripts.meme_xml_text import TextReader as Reader
    element = Reader(variables_of({})).object(text, "Event")
    assert element.type_name == expected_type
    assert TextWriter(lambda named: False).object(element, "Event") == text


def test_call_with_no_matching_argument_count_is_an_error():
    from BF1942_Extraction_Readout_Scripts.meme_xml_text import TextReader as Reader
    with pytest.raises(XmlError, match="takes 3 or 4 arguments, not 2"):
        Reader(variables_of({})).object("Button(0, ButtonPress)", "Event")


@pytest.mark.parametrize(("number", "name"), [(8, "Fire"), (24, "Reload"), (30, "CameraMode1"), (55, "None"), (0, None)])
def test_player_input_names(number, name):
    assert value_text("Byte", number, "PlayerInput", in_attribute=True) == (name if name is not None else str(number))
    assert value_from_text("Byte", str(number), "PlayerInput") == number


# --- Raw form ------------------------------------------------------------------------------------------------------

def test_raw_form_loads_with_full_type_names_and_no_compact_tags(tmp_path):
    binary_path = TEST_DATA_DIR / "BF1942" / "ProfileMenu"
    meme = MemeFile(binary_path)
    meme.load_from_xml(RAW_XML_DIR / "ProfileMenu.xml")
    meme.write(tmp_path / "rebuilt")
    assert (tmp_path / "rebuilt").read_bytes() == binary_path.read_bytes()
