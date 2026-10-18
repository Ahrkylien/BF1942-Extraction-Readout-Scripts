"""
The text inside an XML attribute: primitive values, names, colors, expressions and calls.

Writing and reading are kept apart: TextWriter turns an object into text, and TextReader turns text into an object.
Both use the tags in meme_xml_tags.py for the names of calls and for the fields of each call.
"""
import copy
import json
import math
import re
import struct
from pathlib import Path

from .meme_file import MemeFileElement, meme_types, primitive_formats
from . import meme_xml_tags as tags


class XmlError(ValueError):
    """The XML does not fit the format: a tag, an attribute or a text that no type can take."""


class Unwritable(Exception):
    """An object has no text form, so the element that holds it is written with child elements."""


ENGINE_NAMES = json.loads((Path(__file__).parent / "meme_engine_enums.json").read_text(encoding="utf-8"))

IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
NUMBER = r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?"
PLAIN_NUMBER = re.compile(NUMBER)
NAME = r"\$*[A-Za-z_][A-Za-z0-9_/]*"
TOKEN = re.compile(rf"""\s*(?:
    (?P<punctuation>[()\[\],:])
  | (?P<hex>\#[0-9A-Fa-f]+)
  | (?P<number>{NUMBER})
  | (?P<wide>w'(?:[^']|'')*')
  | (?P<text>'(?:[^']|'')*'|"[^"]*")
  | (?P<word>{NAME})
)""", re.VERBOSE)

# Binary operators: Data type -> (word, precedence). A higher precedence binds tighter.
BINARY_OPERATORS = {
    "OrData": ("or", 1),
    "ExclusiveOrData": ("xor", 2),
    "AndData": ("and", 3),
    "EqualData": ("is", 4),
    "NotEqualData": ("is_not", 4),
    "LessData": ("less_than", 4),
    "LessEqualData": ("less_than_or_equal", 4),
    "AddData": ("plus", 5),
    "SubData": ("minus", 5),
    "MulData": ("times", 6),
    "DivData": ("divided_by", 6),
}
OPERATOR_BY_WORD = {word: kind for kind, (word, _) in BINARY_OPERATORS.items()}
COMPARISON = 4
NOT = 7
ATOM = 8
KEYWORDS = set(OPERATOR_BY_WORD) | {"not", "true", "false", "null"}

# The Data type of a literal, by the primitive type of its value
LITERAL_KIND = {"Int": "IntData", "Float": "FloatData", "Boolean": "BoolData", "String": "StringData", "WideString": "WstringData"}
LITERAL_PRIMITIVE = {kind: primitive for primitive, kind in LITERAL_KIND.items()}
TEXT_CATEGORIES = tags.TEXT_CATEGORIES
DATA = "Data"


# --- Numbers, names and values -----------------------------------------------------------------------------------------

def float32(value):
    """The value a 32-bit float stores: the binary holds every float this way."""
    return struct.unpack("<f", struct.pack("<f", value))[0]


def float_to_text(value):
    """The shortest plain decimal that reads back as the same 32-bit float."""
    if not math.isfinite(value):
        return repr(value)
    value = float32(value)
    stored = struct.pack("<f", value)
    # Nine significant digits are always enough for a 32-bit float
    for digits in range(1, 10):
        scientific = f"{value:.{digits - 1}e}"
        if struct.pack("<f", float(scientific)) == stored:
            break
    exponent = int(scientific.split("e")[1])
    return f"{float(scientific):.{max(0, digits - 1 - exponent)}f}"


def float_literal(value):
    """A float in an expression keeps its decimal point, so it does not read back as an integer."""
    text = float_to_text(value)
    return text if "." in text else text + ".0"


def value_text(primitive_type, value, enum=None, in_attribute=False):
    """
    The text of a primitive value. A number the game names is written as its name, if the name is an identifier
    when it is in an attribute (names such as "Scroll up" are only written in element text).
    """
    if primitive_type == "Boolean":
        return "true" if value else "false"
    if primitive_type == "Float":
        return float_to_text(value)
    if primitive_formats[primitive_type][1] is not None:
        return value
    if enum is not None:
        name = ENGINE_NAMES[enum].get(str(value))
        if name is not None and (not in_attribute or IDENTIFIER.fullmatch(name)):
            return name
    return str(value)


def value_from_text(primitive_type, text, enum=None):
    """Read the text of a primitive value. A named number is read by its name or by its number."""
    if primitive_formats[primitive_type][1] is not None:
        return text
    stripped = text.strip()
    if primitive_type == "Boolean":
        if stripped in ("true", "false"):
            return stripped == "true"
        raise XmlError(f"'{text}' is not true or false")
    if enum is not None:
        for number, name in ENGINE_NAMES[enum].items():
            if stripped == name:
                return int(number)
    if primitive_type == "Float":
        if PLAIN_NUMBER.fullmatch(stripped) or stripped in ("inf", "-inf", "nan"):
            return float32(float(stripped))
        raise XmlError(f"'{text}' is not a number")
    if re.fullmatch(r"[-+]?\d+", stripped):
        return int(stripped)
    raise XmlError(f"'{text}' is not a whole number")


def escape_name(name):
    """A name that is a keyword gets one more $, so that it can be told apart from the keyword."""
    return "$" + name if name.lstrip("$") in KEYWORDS else name


def unescape_name(word):
    """Undo escape_name."""
    return word[1:] if word.startswith("$") and word.lstrip("$") in KEYWORDS else word


def name_text(name):
    text = escape_name(name)
    if not re.fullmatch(NAME, text):
        raise Unwritable(f"the name '{name}' has no text form")
    return text


def quote(text):
    return "'" + text.replace("'", "''") + "'"


def split_list(text):
    """Split text at the commas that are not inside brackets or quotes."""
    parts, depth, quoting, start = [], 0, None, 0
    for index, character in enumerate(text):
        if quoting:
            quoting = None if character == quoting else quoting
        elif character in "'\"":
            quoting = character
        elif character in "([":
            depth += 1
        elif character in ")]":
            depth -= 1
        elif character == "," and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def eight_bit(value):
    """The 0-255 number k when a color channel is exactly k/255 in a 32-bit float, otherwise None."""
    if value is None or not math.isfinite(value):
        return None
    k = round(value * 255)
    return k if 0 <= k <= 255 and float32(k / 255) == float32(value) else None


# --- Writing ---------------------------------------------------------------------------------------------------------

def _has_fields(type_name):
    return any(slot != "NextNode" for slot, _ in meme_types[type_name])


def _constant(element):
    """The number of a constant channel: a Float field, or an unnamed Data literal. None for anything else."""
    if element.type_name == "Float":
        return element.child_elements
    if element.type_name in LITERAL_PRIMITIVE and element.object_name is None:
        return element.child_elements[0].child_elements
    return None


class TextWriter:
    """
    Writes objects as text. is_variable(element) tells whether a named object is written by its name, because it is
    defined in <Variables>. Raises Unwritable when an object has no text form.
    """

    def __init__(self, is_variable):
        self.is_variable = is_variable

    def object(self, element, category):
        """The text of an object in a field of a text category (Data, Style, Event, Function or Empty)."""
        return self._object(element, category)[0]

    def unnamed(self, element):
        """The text of an object without its name, as it is defined in <Variables>."""
        return self._unnamed(element)[0]

    def _object(self, element, category):
        """(text, precedence) of an object in a field of category."""
        name = element.object_name
        if element.is_placeholder:
            if element.type_name != f"{category}Placeholder" and category != "Empty":
                raise Unwritable(f"{element.type_name} in a {category} field")
            if category == "Empty":
                return (name_text(name) if name is not None else "null"), ATOM
            return (f"{name_text(name)}: null" if name is not None else "null"), ATOM
        if element.is_primitive or tags.category(element.type_name) != category:
            raise Unwritable(f"{element.type_name} in a {category} field")
        if category == "Function":
            # A function without fields is written as its name; one with fields (such as an ActionFunction) has no text form
            if name is None or _has_fields(element.type_name):
                raise Unwritable("a function that is not a plain name")
            return name_text(name), ATOM
        if name is not None and _has_fields(element.type_name):
            if not self.is_variable(element):
                raise Unwritable(f"'{name}' holds a value, so it is a variable, but it is not in <Variables>")
            return name_text(name), ATOM
        text, precedence = self._unnamed(element)
        if name is None:
            return text, precedence
        return f"{name_text(name)}: {text}", ATOM

    def _unnamed(self, element):
        """(text, precedence) of an object written without its name."""
        kind = element.type_name
        values = element.field_values()
        if kind in LITERAL_PRIMITIVE:
            return self._literal(kind, values[0].child_elements), ATOM
        if kind == "NotData":
            text, precedence = self._object(values[0], DATA)
            return (f"not {text}" if precedence >= NOT else f"not ({text})"), NOT
        if kind in BINARY_OPERATORS:
            word, precedence = BINARY_OPERATORS[kind]
            left = self._operand(values[0], precedence, is_right=False)
            right = self._operand(values[1], precedence, is_right=True)
            return f"{left} {word} {right}", precedence
        if kind == "DataListData":
            return self._list(values[0]), ATOM
        if kind == "IndexDataData" and values[0].type_name == "DataListData":
            return f"{self.object(values[0], DATA)}[{self.object(values[1], DATA)}]", ATOM
        return self._call(element, values), ATOM

    def _operand(self, element, parent, is_right):
        text, precedence = self._object(element, DATA)
        # Operators group from the left, and comparisons do not chain
        if precedence < parent or (precedence == parent and (is_right or parent == COMPARISON)):
            return f"({text})"
        return text

    def _list(self, items):
        if items[-1].type_name != "ObjectPlaceholder" or items[-1].object_name is not None:
            raise Unwritable("a list with a named end marker")
        return "[" + ", ".join(self.object(item, DATA) for item in items[:-1]) + "]"

    def _literal(self, kind, value):
        if kind == "BoolData":
            return "true" if value else "false"
        if kind == "IntData":
            return str(value)
        if kind == "FloatData":
            if not math.isfinite(value):
                raise Unwritable("a float that is not finite")
            return float_literal(value)
        if kind == "WstringData":
            return "w" + quote(value)
        return quote(value)

    def _call(self, element, values):
        entry = tags.BY_TYPE.get(element.type_name)
        if entry is None or entry.content is not None or tags.category(element.type_name) not in TEXT_CATEGORIES:
            raise Unwritable(f"{element.type_name} has no text form")
        arguments = []
        for attribute in entry.attributes:
            slot = meme_types[element.type_name][attribute.fields[0]][0]
            field = [values[index] for index in attribute.fields]
            if len(attribute.fields) == 4:
                arguments.append(self.color(field, slot, in_call=True))
            elif slot in primitive_formats:
                arguments.append(self._primitive(field[0], attribute.enum))
            elif slot == "List":
                arguments.append(self._list(field[0]))
            else:
                arguments.append(self._object(field[0], slot)[0])
        return f"{entry.tag}({', '.join(arguments)})"

    @staticmethod
    def _primitive(element, enum):
        primitive_type = element.type_name
        if primitive_formats[primitive_type][1] is not None:
            return quote(element.child_elements)
        return value_text(primitive_type, element.child_elements, enum, in_attribute=True)

    def color(self, channels, slot, marked=False, in_call=False):
        """
        The text of a color: #RRGGBB, #RRGGBBAA, '#RRGGBB, alpha', 'red, green, blue' or 'red, green, blue, alpha'.
        Alpha is left out when it is 1. With marked, alpha is written in parentheses (it is an expression).
        In a call, a color is #RRGGBB or #RRGGBBAA, or the four channels: the call reads nothing after a hex value.
        """
        if slot == "Float":
            numbers = [channel.child_elements for channel in channels]
            if not all(math.isfinite(number) for number in numbers):
                raise Unwritable("a color with a float that is not finite")
            constants = numbers
        else:
            constants = [_constant(channel) for channel in channels]
        red, green, blue, alpha = constants
        if not marked and None not in (red, green, blue) and all(eight_bit(v) is not None for v in (red, green, blue)):
            digits = "".join(f"{eight_bit(v):02x}" for v in (red, green, blue))
            if alpha == 1.0:
                return "#" + digits
            if alpha is not None and eight_bit(alpha) not in (None, 255):
                return f"#{digits}{eight_bit(alpha):02x}"
            if in_call:
                return ", ".join(self._channel(channel, slot) for channel in channels)
            return f"#{digits}, {self._channel(channels[3], slot)}"
        texts = [self._channel(channel, slot) for channel in channels[:3]]
        if alpha == 1.0 and not marked:
            return ", ".join(texts)
        alpha_text = self._channel(channels[3], slot)
        return ", ".join(texts + [f"({alpha_text})" if marked else alpha_text])

    def _channel(self, channel, slot):
        if slot == "Float":
            return float_to_text(channel.child_elements)
        return self.object(channel, DATA)


# --- Reading ---------------------------------------------------------------------------------------------------------

class Variables:
    """
    The variables of a file, from <Variables>. A variable with a value has a primitive type and the value; any other
    variable has the text of its object. Each use of a variable is a copy of its object.
    """

    def __init__(self):
        self.values = {}   # name -> (primitive type, value)
        self.texts = {}    # name -> text of the object
        self._parsed = {}  # name -> element, read once
        self._resolving = set()

    def has(self, name):
        return name in self.values or name in self.texts

    def element(self, name, category):
        """A new element for the variable name in a field of category (None: any category, for a variable's own text)."""
        if name in self.values:
            primitive_type, value = self.values[name]
            kind = LITERAL_KIND[primitive_type]
            if category not in (DATA, None):
                raise XmlError(f"variable '{name}' is a {primitive_type}, which cannot be used in a {category} field")
            return MemeFileElement.build(kind, [MemeFileElement(primitive_type, None, None, value)], name)
        if name not in self.texts:
            raise XmlError(f"unknown variable '{name}' (add it to <Variables>)")
        if name not in self._parsed:
            if name in self._resolving:
                raise XmlError(f"variable '{name}' is defined in terms of itself")
            self._resolving.add(name)
            self._parsed[name] = TextReader(self).object(self.texts[name], None)
            self._resolving.discard(name)
        element = self._parsed[name]
        if category is not None and tags.category(element.type_name) != category:
            raise XmlError(f"variable '{name}' is a {element.type_name}, which cannot be used in a {category} field")
        element = copy.deepcopy(element)
        element.object_name = name
        return element


class TextReader:
    """Reads the text of an attribute, or of a variable, into an element."""

    def __init__(self, variables):
        self.variables = variables

    def object(self, text, category):
        """The object written by text in a field of category (None: a variable's text, of any text category)."""
        parser = _Parser(text, self.variables)
        element = parser.parse(category)
        return element

    def color(self, text, slot):
        """The four channels of a color text, in a field of slot (Float or Data)."""
        text = text.strip()
        if text.startswith("#"):
            match = re.fullmatch(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})(?:\s*,\s*(.+))?", text)
            if match is None:
                raise XmlError(f"'{text}' is not #RRGGBB, #RRGGBBAA, '#RRGGBB, alpha' or a list of channels")
            digits, rest = match.groups()
            if len(digits) == 8 and rest is not None:
                raise XmlError(f"'{text}' has alpha in its hex value and after it")
            channels = [self._constant(float32(int(digits[i:i + 2], 16) / 255), slot) for i in range(0, 6, 2)]
            if len(digits) == 8:
                channels.append(self._constant(float32(int(digits[6:8], 16) / 255), slot))
            elif rest is not None:
                channels.append(self._channel(rest, slot))
            else:
                channels.append(self._constant(1.0, slot))
            return channels
        parts = split_list(text)
        if len(parts) not in (3, 4):
            raise XmlError(f"'{text}' is not #RRGGBB, #RRGGBBAA, '#RRGGBB, alpha' or a list of channels")
        channels = [self._channel(part, slot) for part in parts]
        if len(parts) == 3:
            channels.append(self._constant(1.0, slot))
        return channels

    @staticmethod
    def _constant(value, slot):
        if slot == "Float":
            return MemeFileElement("Float", None, None, value)
        return MemeFileElement.build("FloatData", [MemeFileElement("Float", None, None, value)])

    def _channel(self, text, slot):
        if slot == "Float":
            if not PLAIN_NUMBER.fullmatch(text.strip()):
                raise XmlError(f"the color channel '{text}' is an expression, but a Float color takes only numbers")
            return MemeFileElement("Float", None, None, float32(float(text)))
        return self.object(text, DATA)


class _Parser:
    """
    Reads object text: literals, operators and lists for Data; calls and names for every category.

    object   := operand (binary_operator operand)*                 Data only
    operand  := "not" operand | primary ("[" object "]")*          Data only
    primary  := literal | "null" | name | call | "(" object ")" | "[" items "]"
    call     := tag "(" argument ("," argument)* ")"               the arguments of the tag, in field order
    """

    def __init__(self, text, variables):
        self.variables = variables
        self.tokens = []
        self.position = 0
        index = 0
        text = text.strip()
        while index < len(text):
            match = TOKEN.match(text, index)
            if match is None or match.end() == index:
                raise XmlError(f"unexpected text at position {index} of '{text}'")
            kind = match.lastgroup
            value = match.group(kind)
            if kind == "word":
                if value in KEYWORDS:
                    kind = "keyword"
                else:
                    value = unescape_name(value)
            self.tokens.append((kind, value))
            index = match.end()

    def _peek(self, offset=0):
        position = self.position + offset
        return self.tokens[position] if position < len(self.tokens) else (None, None)

    def _take(self, kind, value=None):
        token_kind, token_value = self._peek()
        if token_kind == kind and (value is None or token_value == value):
            self.position += 1
            return token_value
        return None

    def _expect(self, kind, value):
        if self._take(kind, value) is None:
            raise XmlError(f"expected '{value}'")

    def parse(self, category):
        if category is None:
            # A variable's text: a call of a text category, or an expression
            kind, value = self._peek()
            if kind == "word" and self._peek(1) == ("punctuation", "("):
                matches = [c for c in TEXT_CATEGORIES if (c, value) in tags.BY_KEY]
                if matches:
                    element = self._object(matches[0])
                    return self._finish(element)
            category = DATA
        return self._finish(self._value(category))

    def _finish(self, element):
        if self.position != len(self.tokens):
            raise XmlError("unexpected text after the end of the object")
        return element

    def _value(self, category):
        if category == DATA:
            return self._expression(1)
        return self._object(category)

    def _expression(self, minimum):
        left = self._operand()
        while True:
            kind = self._operator()
            if kind is None or BINARY_OPERATORS[kind][1] < minimum:
                return left
            precedence = BINARY_OPERATORS[kind][1]
            self.position += 1
            left = build_data(kind, [left, self._expression(precedence + 1)])
            following = self._operator()
            if precedence == COMPARISON and following and BINARY_OPERATORS[following][1] == COMPARISON:
                raise XmlError("comparisons cannot be chained, use parentheses")

    def _operator(self):
        kind, value = self._peek()
        return OPERATOR_BY_WORD.get(value) if kind == "keyword" else None

    def _operand(self):
        if self._take("keyword", "not"):
            return build_data("NotData", [self._operand()])
        element = self._object(DATA)
        while element.type_name == "DataListData" and self._take("punctuation", "["):
            index = self._expression(1)
            self._expect("punctuation", "]")
            element = build_data("IndexDataData", [element, index])
        return element

    def _object(self, category):
        """A primary object of category: a literal, a name, a call, a bracketed object or a list (Data)."""
        kind, value = self._peek()
        if kind is None:
            raise XmlError("the text ends too early")
        self.position += 1
        if kind == "keyword" and value == "null":
            return MemeFileElement.placeholder(category, None)
        if kind == "punctuation" and value == "(":
            element = self._value(category)
            self._expect("punctuation", ")")
            return element
        if kind == "word":
            if self._take("punctuation", ":"):
                element = self._object(category)
                if element.is_complex_type and _has_fields(element.type_name):
                    raise XmlError(f"'{value}:' names an object with fields, which belongs in <Variables>")
                element.object_name = value
                return element
            if self._take("punctuation", "("):
                return self._call(value, category)
            if category == "Function":
                return MemeFileElement("Function", value, None, [])
            if category == "Empty":
                return MemeFileElement.placeholder("Empty", None, value)
            return self.variables_element(value, category)
        if category != DATA:
            raise XmlError(f"'{value}' is not a {category}")
        if kind == "punctuation" and value == "[":
            return MemeFileElement.build("DataListData", [self._list_items()])
        if kind == "number":
            if any(c in value for c in ".eE"):
                return TextReader._constant(float32(float(value)), "Data")
            return MemeFileElement.build("IntData", [MemeFileElement("Int", None, None, int(value))])
        if kind == "text":
            return MemeFileElement.build("StringData", [MemeFileElement("String", None, None, unquote(value))])
        if kind == "wide":
            return MemeFileElement.build("WstringData", [MemeFileElement("WideString", None, None, unquote(value[1:]))])
        if kind == "keyword" and value in ("true", "false"):
            return MemeFileElement.build("BoolData", [MemeFileElement("Boolean", None, None, value == "true")])
        raise XmlError(f"unexpected '{value}'")

    def variables_element(self, name, category):
        return self.variables.element(name, category)

    def _list_items(self):
        items = []
        if not self._take("punctuation", "]"):
            while True:
                items.append(self._expression(1))
                if self._take("punctuation", "]"):
                    break
                self._expect("punctuation", ",")
        return items

    def _argument_count(self):
        """The arguments of the call whose '(' was just read: the commas outside brackets, up to its ')'."""
        if self._peek() == ("punctuation", ")"):
            return 0
        count, depth = 1, 0
        for kind, value in self.tokens[self.position:]:
            if kind != "punctuation":
                continue
            if value in ("(", "["):
                depth += 1
            elif value in (")", "]"):
                if depth == 0:
                    break
                depth -= 1
            elif value == "," and depth == 0:
                count += 1
        return count

    def _entry_with_arguments(self, entries, name):
        """The tag of a call name that takes as many arguments as the call has."""
        count = self._argument_count()
        for entry in entries:
            if len(entry.attributes) == count:
                return entry
        counts = " or ".join(str(len(entry.attributes)) for entry in entries)
        raise XmlError(f"'{name}' takes {counts} arguments, not {count}")

    def _call(self, name, category):
        """A call of the tag name: its arguments are read in the order of the tag's attributes."""
        found = [c for c in TEXT_CATEGORIES if (c, name) in tags.BY_KEY]
        if not found:
            raise XmlError(f"'{name}' is not a known call")
        # Call names are unique across the text categories (checked when the tags load)
        if category is not None and found[0] != category:
            raise XmlError(f"'{name}' is a {found[0]} call, which cannot be used in a {category} field")
        entries = tags.BY_KEY[(found[0], name)]
        entry = entries[0] if len(entries) == 1 else self._entry_with_arguments(entries, name)
        schema = meme_types[entry.type_name]
        values = [None] * len(schema)
        for number, attribute in enumerate(entry.attributes):
            if number:
                self._expect("punctuation", ",")
            slot = schema[attribute.fields[0]][0]
            label = schema[attribute.fields[0]][1]
            if len(attribute.fields) == 4:
                channels = self._color_arguments(slot)
                for index, channel in zip(attribute.fields, channels):
                    values[index] = channel
            elif slot in primitive_formats:
                values[attribute.fields[0]] = self._primitive(slot, attribute.enum, label)
            elif slot == "List":
                self._expect("punctuation", "[")
                values[attribute.fields[0]] = self._list_items()
            else:
                values[attribute.fields[0]] = self._value(slot)
        self._expect("punctuation", ")")
        return MemeFileElement.build(entry.type_name, values)

    def _primitive(self, slot, enum, label):
        kind, value = self._peek()
        self.position += 1
        if primitive_formats[slot][1] is not None:
            if kind != "text":
                raise XmlError(f"'{value}' is not a quoted {slot} for '{label}'")
            return MemeFileElement(slot, None, label, unquote(value))
        if kind not in ("number", "keyword", "word"):
            raise XmlError(f"'{value}' is not a {slot} for '{label}'")
        return MemeFileElement(slot, None, label, value_from_text(slot, value, enum))

    def _color_arguments(self, slot):
        """A color argument: #RRGGBB(AA), or four channels separated by commas."""
        hex_token = self._take("hex")
        if hex_token is not None:
            return TextReader(self.variables).color(hex_token, slot)
        channels = []
        for number in range(4):
            if number:
                self._expect("punctuation", ",")
            channels.append(self._primitive("Float", None, "color") if slot == "Float" else self._expression(1))
        return channels


def build_data(kind, children):
    """A new Data element that combines Data elements, such as AndData or NotData."""
    return MemeFileElement.build(kind, children)


def unquote(token):
    """The text of a quoted token: 'text' (with '' for a quote), or "text"."""
    if token.startswith('"'):
        return token[1:-1]
    return token[1:-1].replace("''", "'")
