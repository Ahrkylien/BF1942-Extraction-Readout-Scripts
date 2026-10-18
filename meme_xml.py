"""
The XML form of meme files, as described in documentation/MemeXmlFormat.md.

A file is a <MemeFile> element. Its first child is <Variables>, and the other children are its nodes.

An object is written in one of two forms, and both can be read, mixed freely:
- the compact form: a tag from meme_xml_tags.py, with the fields written as attributes, and the content as child elements;
- the raw form: the type name as the tag, with one child element for each field, in the order of the fields.
"""
import collections
import sys
import xml.etree.ElementTree as ET

from .meme_file import MemeFileElement, meme_types, primitive_formats
from . import meme_xml_tags as tags
from .meme_xml_text import (
    LITERAL_PRIMITIVE, TEXT_CATEGORIES, TextReader, TextWriter, Unwritable, Variables, XmlError, value_from_text, value_text,
)

DATA = "Data"
PLACEHOLDER_SLOTS = {slot for schema in meme_types.values() for slot, _ in schema} | {"Object"}
# The enum that names the numbers of each field, by type and field index (from the compact tags)
ENUM_OF_FIELD = {(c.type_name, index): attribute.enum
                 for c in tags.COMPACT for attribute in c.attributes for index in attribute.fields if attribute.enum}


class _AnyName:
    """Takes the place of the variables while checking which tags fit an attribute: every name counts as defined."""

    def element(self, name, category):
        # A name can be a list, which is what an index applies to
        return MemeFileElement.build("DataListData", [[]], name) if category in (None, DATA) else MemeFileElement.placeholder(category, None, name)


_ANY = _AnyName()


def _slot_category(slot, owner):
    """The category of the objects a field of slot holds. The items of a list are of the category of their owner."""
    if slot == "List":
        return tags.category(owner)
    return slot if slot in ("Node", "Action", "Effect", "Data", "Style", "Event", "Function", "Empty") else None


def _element_text(xml_element):
    text = xml_element.text or ""
    return text.replace("\n", "\r\n") if xml_element.get("uses_crlf", "").lower() == "true" else text


def _set_text(xml_node, text):
    if "\r\n" in text:
        if text.count("\r\n") != text.count("\n"):
            raise XmlError(f"a text has mixed line endings: {text!r}")
        xml_node.set("uses_crlf", "true")
        text = text.replace("\r\n", "\n")
    xml_node.text = text


def _same_object(a, b):
    """
    Whether two elements hold the same object. Descriptions are labels, so they do not count. Values are compared by
    their repr, so 0.0 and -0.0 differ.
    """
    if (a.type_name, a.object_name) != (b.type_name, b.object_name):
        return False
    if not isinstance(a.child_elements, list) or not isinstance(b.child_elements, list):
        return type(a.child_elements) is type(b.child_elements) and repr(a.child_elements) == repr(b.child_elements)
    return len(a.child_elements) == len(b.child_elements) and all(map(_same_object, a.child_elements, b.child_elements))


def _is_data(entry, attribute):
    return meme_types[entry.type_name][attribute.fields[0]][0] == DATA


def _accepts(entry, attribute, text):
    """Whether the text of an attribute can be read into the field it writes. Names are allowed, and not checked here."""
    slot = meme_types[entry.type_name][attribute.fields[0]][0]
    try:
        if len(attribute.fields) == 4:
            TextReader(_ANY).color(text, slot)
        elif slot in primitive_formats:
            value_from_text(slot, text, attribute.enum)
        else:
            TextReader(_ANY).object(text, slot)
    except XmlError:
        return False
    return True


def _problem(entry, attributes, has_children, field_names=()):
    """Why an entry does not fit the attributes and named children, or None when it fits."""
    by_name = {attribute.name: attribute for attribute in entry.attributes}
    for name in attributes:
        if name not in by_name:
            return f"has no attribute '{name}'"
    for attribute in entry.attributes:
        if attribute.name not in attributes and attribute.default is tags.REQUIRED:
            return f"needs '{attribute.name}'"
    if has_children and entry.content is None:
        return "takes no child elements"
    child_names = {child.name for child in entry.children}
    for name in field_names:
        if name not in child_names:
            return f"has no child named '{name}'"
    for name, text in attributes.items():
        if not _accepts(entry, by_name[name], text):
            return f"cannot take '{name}' = '{text}'"
    return None


def _score(entry):
    """The fewer expression fields and attributes an entry has, the more it is preferred."""
    return (sum(_is_data(entry, attribute) for attribute in entry.attributes), len(entry.attributes))


def _pick(tag, entries, attributes, has_children, field_names=()):
    """The entry that a tag with these attributes and children stands for. A tie between entries is an error."""
    fitting, reasons = [], []
    for entry in entries:
        problem = _problem(entry, attributes, has_children, field_names)
        if problem is None:
            fitting.append(entry)
        else:
            reasons.append(f"{entry.type_name} {problem}")
    if not fitting:
        raise XmlError(f"<{tag}> with attributes {sorted(attributes)} fits no type: {'; '.join(reasons)}")
    ranked = sorted(fitting, key=_score)
    if len(ranked) > 1 and _score(ranked[0]) == _score(ranked[1]):
        raise XmlError(f"<{tag}> with attributes {sorted(attributes)} fits {ranked[0].type_name} and {ranked[1].type_name} equally")
    return ranked[0]


# --- Reading ---------------------------------------------------------------------------------------------------------

class _Reader:
    def __init__(self):
        self.variables = Variables()
        self.text = TextReader(self.variables)

    def file(self, root):
        if root.tag != "MemeFile":
            raise XmlError(f"the root element is <{root.tag}>, but it must be <MemeFile>")
        children = list(root)
        if children and children[0].tag == "Variables":
            self._variables(children[0])
            children = children[1:]
        if any(child.tag == "Variables" for child in children):
            raise XmlError("<Variables> must be the first child of <MemeFile>")
        return self.chain(children, None)

    def _variables(self, xml):
        for variable in xml:
            name = variable.get("name")
            if name is None:
                raise XmlError("a variable needs a name")
            if self.variables.has(name):
                raise XmlError(f"variable '{name}' is defined twice, but a variable has one value")
            primitive_type = variable.get("type")
            if primitive_type is None:
                self.variables.texts[name] = _element_text(variable)
            elif primitive_type in primitive_formats:
                self.variables.values[name] = (primitive_type, value_from_text(primitive_type, _element_text(variable)))
            else:
                raise XmlError(f"variable '{name}' has the unknown type '{primitive_type}'")

    def chain(self, xml_children, label, empty_slot="Node"):
        """The first node of the chain that the elements form. A CullNode with nodes after it gets a SplitNode around it."""
        if not xml_children:
            return MemeFileElement.placeholder(empty_slot, label)
        nodes = [self.element(child, "Node", None) for child in xml_children]
        for index, node in enumerate(nodes[:-1]):
            if node.type_name == "CullNode":
                # A CullNode's next node holds its body, so the nodes after an if are the next node of a SplitNode
                node.description = "Split node"
                nodes[index] = MemeFileElement("SplitNode", None, None,
                                               [MemeFileElement.placeholder("NextNode", "Next node"), node])
            elif not node.has_next_node:
                raise XmlError(f"<{xml_children[index].tag}> has no next node, so nothing can follow it")
        for node, following in zip(nodes, nodes[1:]):
            following.description = "Next node"
            node.child_elements[0] = following
        nodes[0].description = label
        return nodes[0]

    def element(self, xml, category, label):
        """The object of one element, in a field of category (None: any category)."""
        tag = xml.tag
        name = xml.get("name")
        if tag == "g":
            raise XmlError("<g> is only allowed around the nodes of a field in the raw form")
        if tag.endswith("Placeholder") and tag[:-len("Placeholder")] in PLACEHOLDER_SLOTS:
            return MemeFileElement(tag, name, label, None)
        if tag in primitive_formats:
            raise XmlError(f"<{tag}> is a value, which belongs in a field of an element")
        # A variable is written by its name alone (an <Object> also carries its type)
        bare = not (set(xml.attrib) - {"name", "description", "type"} if tag == "Object" else set(xml.attrib) - {"name", "description", "field"})
        bare = bare and len(xml) == 0 and not (xml.text or "").strip()
        if name is not None and bare and self.variables.has(name):
            element = self.variables.element(name, category)
            element.description = label
            return element
        if tag == "Object":
            type_name = xml.get("type")
            if type_name not in meme_types:
                raise XmlError(f"<Object> needs a type attribute with a type name, not '{type_name}'")
            return self._raw(xml, type_name, label)
        entries = tags.BY_KEY.get((category, tag)) if category in tags.ELEMENT_CATEGORIES else None
        if entries:
            return self._compact(xml, entries, label)
        if tag in meme_types:
            return self._raw(xml, tag, label)
        raise XmlError(f"<{tag}> is neither a tag of the {category} category nor a type name")

    def _compact(self, xml, entries, label):
        attributes = {key: value for key, value in xml.attrib.items() if key not in ("name", "description", "field")}
        children = [child for child in xml if child.get("field") is None]
        named = [child for child in xml if child.get("field") is not None]
        entry = _pick(xml.tag, entries, attributes, bool(children), [child.get("field") for child in named])
        schema = meme_types[entry.type_name]
        values = [None] * len(schema)
        for attribute in entry.attributes:
            index = attribute.fields[0]
            if attribute.name in attributes:
                self._attribute(values, entry, attribute, attributes[attribute.name])
            elif attribute.default is tags.NULL:
                values[index] = MemeFileElement.placeholder(schema[index][0], None)
            elif attribute.default is not tags.REQUIRED:
                values[index] = MemeFileElement(schema[index][0], None, None, attribute.default)
        for child_xml in named:
            child = next(c for c in entry.children if c.name == child_xml.get("field"))
            if values[child.field] is not None:
                raise XmlError(f"<{xml.tag}> has two children named '{child.name}'")
            values[child.field] = self.element(child_xml, _slot_category(schema[child.field][0], entry.type_name), None)
        if entry.content == tags.BODY:
            values[0] = self.chain(children, "Next node", empty_slot="NextNode")
        elif entry.content is not None:
            values[entry.content] = self._content(xml, entry, children)
        return MemeFileElement.build(entry.type_name, values, xml.get("name"), label)

    def _attribute(self, values, entry, attribute, text):
        schema = meme_types[entry.type_name]
        slot = schema[attribute.fields[0]][0]
        try:
            if len(attribute.fields) == 4:
                for index, channel in zip(attribute.fields, self.text.color(text, slot)):
                    values[index] = channel
            elif slot in primitive_formats:
                values[attribute.fields[0]] = MemeFileElement(slot, None, None, value_from_text(slot, text, attribute.enum))
            else:
                values[attribute.fields[0]] = self.text.object(text, slot)
        except XmlError as error:
            raise XmlError(f"<{entry.tag}> attribute '{attribute.name}': {error}") from None

    def _content(self, xml, entry, children):
        slot, label = meme_types[entry.type_name][entry.content]
        if slot == "Node":
            return self.chain(children, label)
        if slot == "List":
            return [self.element(child, tags.category(entry.type_name), None) for child in children]
        if len(children) > 1:
            raise XmlError(f"<{xml.tag}> has {len(children)} child elements, but it takes one")
        return self.element(children[0], _slot_category(slot, entry.type_name), label) if children else None

    def _raw(self, xml, type_name, label):
        """
        An element in the raw form: one child for each field, in the order of the fields. Descriptions are not read.
        An empty node, action or data field is a <Placeholder />, a list is a <List> of its items.
        """
        schema = meme_types[type_name]
        # The body of a CullNode is its next node, which the raw form writes as the first field
        fields = [index for index, (slot, _) in enumerate(schema) if slot != "NextNode" or (type_name == "CullNode" and index == 0)]
        children = list(xml)
        if len(children) != len(fields):
            raise XmlError(f"<{xml.tag}> has {len(children)} children, but its type has {len(fields)} fields")
        values = [None] * len(schema)
        for index, child in zip(fields, children):
            slot, field_label = schema[index]
            if slot in primitive_formats:
                if child.tag != slot:
                    raise XmlError(f"<{xml.tag}> needs <{slot}> for field {index}, not <{child.tag}>")
                values[index] = MemeFileElement(slot, None, None,
                                                value_from_text(slot, _element_text(child), ENUM_OF_FIELD.get((type_name, index))))
            elif child.tag == "Placeholder":
                values[index] = MemeFileElement.placeholder(slot, None, child.get("name"))
            elif slot == "List":
                # An item is a chain of nodes: a <g> holds the nodes of an item that has nodes after it
                values[index] = [self.chain(list(item) if item.tag == "g" else [item], field_label) for item in child]
            elif slot == "Node" or index == 0 and type_name == "CullNode":
                nodes = list(child) if child.tag == "g" else [child]
                values[index] = self.chain(nodes, field_label, empty_slot="NextNode" if index == 0 else "Node")
            else:
                values[index] = self.element(child, _slot_category(slot, type_name), field_label)
        return MemeFileElement.build(type_name, values, xml.get("name"), label)


# --- Writing ---------------------------------------------------------------------------------------------------------

def _definitions(root):
    """
    The variables: every named object with fields in a text category. A variable has one value, the one of its first
    use in the file. A later use with a different value is written as the variable too, and a warning is printed for it.
    A variable whose text cannot be written (because it uses an object that is not a variable) is not defined.
    """
    uses = collections.defaultdict(list)
    for element in root.walk():
        if (element.object_name is not None and element.is_complex_type
                and tags.category(element.type_name) in TEXT_CATEGORIES and any(slot != "NextNode" for slot, _ in meme_types[element.type_name])):
            uses[element.object_name].append(element)
    defined = {name: objects[0] for name, objects in uses.items()}
    changed = True
    while changed:
        changed = False
        writer = TextWriter(lambda element: element.object_name in defined)
        for name, element in list(defined.items()):
            try:
                writer.unnamed(element)
            except Unwritable:
                del defined[name]
                changed = True
    for name, element in defined.items():
        for other in uses[name][1:]:
            if not _same_object(element, other):
                print(f"Warning: variable '{name}': a later {other.type_name} differs from the first use; "
                      f"every use is written with the first value", file=sys.stderr)
    return defined


class _Writer:
    def __init__(self, compact, defined):
        self.compact = compact
        self.defined = defined
        self.text = TextWriter(lambda element: element.object_name in self.defined)

    def file(self, root):
        xml_root = ET.Element("MemeFile")
        if self.defined:
            variables = ET.SubElement(xml_root, "Variables")
            for name in sorted(self.defined):
                self._variable(variables, name, self.defined[name])
        self.chain(root, xml_root, None)
        return xml_root

    def _variable(self, variables, name, element):
        if element.type_name in LITERAL_PRIMITIVE:
            value = element.child_elements[0]
            node = ET.SubElement(variables, "Variable", name=name, type=value.type_name)
            _set_text(node, value_text(value.type_name, value.child_elements))
        else:
            _set_text(ET.SubElement(variables, "Variable", name=name), self.text.unnamed(element))

    def chain(self, head, parent, label):
        """The nodes of a chain, one after the other in parent. Only the first is labelled."""
        node = head
        while True:
            if (node.type_name == "SplitNode" and node.object_name is None and node.child_elements[0].is_occupied
                    and node.child_elements[1].type_name == "CullNode" and node.child_elements[1].object_name is None):
                # An if with nodes after it: the if is written, and the nodes after it follow it as siblings
                self.element(node.child_elements[1], parent, "Node", label)
                node = node.child_elements[0]
                label = None
                continue
            self.element(node, parent, "Node", label)
            if not node.has_occupied_next_node or node.type_name == "CullNode":
                return
            node = node.child_elements[0]
            label = None

    def element(self, element, parent, field_category, label):
        """Write one object into parent: in the compact form when it fits, otherwise in the raw form."""
        if element.is_placeholder:
            return self._placeholder(element, parent, label)
        if self.compact:
            written = self._compact(element, parent, field_category, label)
            if written is not None:
                return written
        return self._raw(element, parent, field_category, label)

    def _placeholder(self, element, parent, label):
        node = ET.SubElement(parent, element.type_name)
        if label is not None:
            node.set("description", label)
        if element.object_name is not None:
            node.set("name", element.object_name)
        return node

    def _compact(self, element, parent, field_category, label):
        entry = tags.BY_TYPE.get(element.type_name)
        if field_category not in tags.ELEMENT_CATEGORIES or entry is None or tags.category(element.type_name) != field_category:
            return None
        entries = tags.BY_KEY[(field_category, entry.tag)]
        # The attributes are written as they are; if the tag would read as another type, the last expression is marked
        for marked in (False, True):
            try:
                self._check_content(element, entry)
                attributes = self._attributes(element, entry, marked)
                if _pick(entry.tag, entries, attributes, self._has_content(element, entry),
                         self._field_names(element, entry)).type_name == entry.type_name:
                    break
            except (Unwritable, XmlError):
                pass
        else:
            return None
        node = ET.Element(entry.tag)
        if label is not None:
            node.set("description", label)
        if element.object_name is not None:
            node.set("name", element.object_name)
        for name, text in attributes.items():
            node.set(name, text)
        self._content(element, entry, node)
        self._field_children(element, entry, node)
        parent.append(node)
        return node

    def _attributes(self, element, entry, marked):
        """The text of each attribute. An attribute that holds its default is left out."""
        values = element.field_values()
        schema = meme_types[element.type_name]
        expressions = [attribute for attribute in entry.attributes if _is_data(entry, attribute)]
        marked_attribute = expressions[-1] if (marked and expressions) else None
        if marked and marked_attribute is None:
            raise Unwritable("no expression to mark")
        attributes = {}
        for attribute in entry.attributes:
            slot = schema[attribute.fields[0]][0]
            fields = [values[index] for index in attribute.fields]
            if len(attribute.fields) == 4:
                text = self.text.color(fields, slot, marked=attribute is marked_attribute)
            elif slot in primitive_formats:
                if attribute.default not in (tags.REQUIRED, tags.NULL) and fields[0].child_elements == attribute.default:
                    continue
                text = value_text(slot, fields[0].child_elements, attribute.enum, in_attribute=True)
            else:
                value = fields[0]
                if value.is_placeholder and value.object_name is None and attribute.default is tags.NULL:
                    continue
                text = self.text.object(value, slot)
                if attribute is marked_attribute:
                    text = f"({text})"
            attributes[attribute.name] = text
        return attributes

    @staticmethod
    def _check_content(element, entry):
        """Raise Unwritable when the content has no compact form, so that the element is written in the raw form."""
        if entry.content is None or entry.content == tags.BODY:
            return
        value = element.field_values()[entry.content]
        if isinstance(value, list):
            if value[-1].object_name is not None:
                raise Unwritable("a list with a named end marker")
            if any(item.has_occupied_next_node for item in value[:-1]):
                raise Unwritable("a list whose items have nodes after them")

    @staticmethod
    def _field_names(element, entry):
        """The names of the children of a tag that have a value."""
        values = element.field_values()
        return [child.name for child in entry.children if values[child.field].is_occupied]

    def _field_children(self, element, entry, node):
        """Each child of a tag that has a value: written as its element, with its name in the field attribute."""
        values = element.field_values()
        for child in entry.children:
            value = values[child.field]
            if value.is_occupied:
                written = self.element(value, node, _slot_category(meme_types[element.type_name][child.field][0], element.type_name), None)
                written.set("field", child.name)

    @staticmethod
    def _has_content(element, entry):
        if entry.content is None:
            return False
        if entry.content == tags.BODY:
            return element.child_elements[0].is_occupied
        value = element.field_values()[entry.content]
        return any(item.is_occupied for item in value) if isinstance(value, list) else value.is_occupied

    def _content(self, element, entry, node):
        if entry.content is None:
            return
        if entry.content == tags.BODY:
            if element.child_elements[0].is_occupied:
                self.chain(element.child_elements[0], node, None)
            return
        slot = meme_types[element.type_name][entry.content][0]
        value = element.field_values()[entry.content]
        if slot == "Node":
            if value.is_occupied:
                self.chain(value, node, None)
        elif slot == "List":
            for item in value[:-1]:
                self.element(item, node, tags.category(element.type_name), None)
        elif value.is_occupied:
            self.element(value, node, _slot_category(slot, element.type_name), None)

    def _raw(self, element, parent, field_category, label):
        """An element in the raw form: one child for each field, in the order of the fields, labelled by its description."""
        tag = element.type_name
        if (field_category, tag) in tags.BY_KEY or tag == "Object":
            node = ET.SubElement(parent, "Object", type=tag)
        else:
            node = ET.SubElement(parent, tag)
        if label is not None:
            node.set("description", label)
        if element.object_name is not None:
            node.set("name", element.object_name)
        if element.object_name in self.defined:
            return node  # The value is in <Variables>
        schema = meme_types[tag]
        for index, value in enumerate(element.field_values()):
            slot, field_label = schema[index]
            if slot == "NextNode" and not (tag == "CullNode" and index == 0):
                continue
            if slot in primitive_formats:
                child = ET.SubElement(node, slot, description=field_label)
                _set_text(child, value_text(slot, value.child_elements, ENUM_OF_FIELD.get((tag, index))))
            elif slot == "List":
                wrapper = ET.SubElement(node, "List", description=field_label)
                items = value if value[-1].object_name is not None else value[:-1]
                for item in items:
                    holder = ET.Element("holder")
                    self.chain(item, holder, field_label)
                    children = list(holder)
                    if len(children) == 1:
                        wrapper.append(children[0])
                    else:
                        group = ET.SubElement(wrapper, "g")
                        group.extend(children)
            elif slot == "Node" or slot == "NextNode":
                holder = ET.Element("holder")
                if value.is_occupied:
                    self.chain(value, holder, field_label)
                children = list(holder)
                if not children:
                    self._empty(node, value, field_label)
                elif len(children) == 1:
                    node.append(children[0])
                else:
                    group = ET.SubElement(node, "g", description=field_label)
                    children[0].attrib.pop("description", None)
                    group.extend(children)
            elif value.is_occupied:
                self.element(value, node, _slot_category(slot, tag), field_label)
            else:
                self._empty(node, value, field_label)
        return node

    @staticmethod
    def _empty(node, value, field_label):
        """An empty field: a <Placeholder />, labelled by the field, with the name of the placeholder when it has one."""
        placeholder = ET.SubElement(node, "Placeholder", description=field_label)
        if value.object_name is not None:
            placeholder.set("name", value.object_name)


def load_xml(xml_path):
    """The root element of an XML file."""
    return _Reader().file(ET.parse(xml_path).getroot())


def save_xml(root_element, xml_path, compact=True):
    """Write the root element as XML, in the compact form, or in the raw form when compact is False."""
    # The raw form has no <Variables>: every object is written in full
    xml_root = _Writer(compact, _definitions(root_element) if compact else {}).file(root_element)
    tree = ET.ElementTree(xml_root)
    ET.indent(tree, space="  ", level=0)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
