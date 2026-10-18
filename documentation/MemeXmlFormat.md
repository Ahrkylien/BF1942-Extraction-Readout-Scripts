# MemeFile XML format

A meme file in XML is a `<MemeFile>` element. Its children are the nodes of the file, in order. The first child can be `<Variables>`.

Every object is written in one of two forms:

- **Clean form**: a tag from the [tag reference](#tag-reference) for the type, with its fields as attributes, and its content as child elements. The exporter uses this form whenever the object fits it.
- **Raw form**: the type name as the tag, with one child element for each field, in the order of the fields. It needs no tags, so it works for every type in `meme_types.json`. The exporter uses it for objects that have no clean form. See [Raw form](#raw-form).

Both forms can be mixed in one file, and both are read.

## Nodes

Nodes are sibling elements: each node is followed by the nodes after it in its chain.

A node that has content holds it as child elements. `<Transform>` holds the nodes it transforms, `<Effect>` holds its effect, `<If>` holds the nodes inside it, and `<Group>` holds the nodes of the group.

A field that cannot be an attribute is a named child element instead. The child carries a `field` attribute with the name of its field, and the reader finds the field by that name. A child with no value is left out. The children of each tag are listed under the tag in the [tag reference](#tag-reference). `name`, `description` and `field` are reserved attribute names.

```xml
<ListBox font="standard6.dif" row-height="14" ...>
  <BfListBoxData name="Campaign/CampaignLevelsList" field="listbox-data">...</BfListBoxData>
  <ActionList field="select-action">...</ActionList>
</ListBox>
```

```xml
<Transform x="10" y="20" width="100" height="50">
  <Effect>
    <Color color="#8c8c8c" />
  </Effect>
  <Text string="Briefing/EscapeToCancel" style="CenterAligned('standard6.dif')" />
</Transform>
<If condition="TransitionEffect is 1 or not ShowDebriefing">
  <Text string="Load/LevelName" style="Style/LoadHeading8" />
</If>
<Text string="Load/LoadingLeftTitle" style="Style/LoadHeading8" />
```

An `<If>` with nodes after it is a CullNode inside a SplitNode. The reader builds that structure; you only write the `<If>` and the nodes after it.

## Variables

`<Variables>` defines the named objects of the file once. A name that is used in several places is written as its name, and its value is listed here. It is the first child of `<MemeFile>`.

```xml
<Variables>
  <Variable name="TransitionEffect" type="Int">0</Variable>
  <Variable name="DisconnectMessage/DisconnectMessage" type="WideString">WARNING! DISCONNECT</Variable>
  <Variable name="Locale/Locale">Locale(Locale/Valid)</Variable>
  <Variable name="Style/LoadHeading8">Style('Trebuchet MS8.dif')</Variable>
</Variables>
```

- A variable that holds a value has `type`, which is `Int`, `Float`, `Boolean`, `String` or `WideString`, and the value as its text.
- Any other variable has the [attribute text](#attribute-text) of its object, and no `type`.
- A variable is defined once, so it has one value: the value of its first use in the file. A later use with a different value is written as the variable too, so it gets the first value. The exporter prints a warning for each such use.

## Values

- Booleans: `true` or `false`.
- Numbers: plain decimals, such as `1.5`, `2` or `-0.25`. A float is written with the fewest digits that read back as the same 32-bit float. `inf`, `-inf` and `nan` are written as they are.
- Text: an attribute holds its text as it is. Inside an expression or a call, text is in single quotes, and a quote inside it is written twice: `'it''s'`. Wide text is `w'…'`.
- A number that the game names is written as its name, when the name is one word: `Button(0, ButtonPress, Select)`. The names are in `meme_engine_enums.json`. In the raw form the full name is written, such as `Scroll up`.

## Attribute text

An attribute that holds an object holds it as text. A Data object is an expression. A Style, Event or Function object is a call, or for a function its name.

### Expressions

- A literal: `1` (IntData), `1.5` or `1.0` (FloatData), `true` or `false` (BoolData), `'text'` (StringData), `w'text'` (WstringData).
- There is no difference between integers and floats in an expression. An integer literal is converted to a float when the file is loaded, so `1` and `1.0` behave the same. Constants that are not expressions, such as an `int` attribute, keep their type.
- `null` is an empty field.
- A name is a variable. A name that is a keyword is written with one more `$` in front: `and` is `$and`, and the name `$and` is `$$and`.
- `[a, b]` is a list, and `list[index]` picks an item of a list.
- Parentheses group parts of an expression.
- Comparisons do not chain. Write `(a is 1) is b`, not `a is 1 is b`.
- `a is_not b` means "not equal". `a is not b` means `a` compared with `not b`.

The operators are in the [operators](#operators) of the tag reference.

### Calls

An object that is not a literal, an operator or a list is a call: its name, then its arguments in order. The names and arguments are in the [text calls](#text-calls) of the tag reference.

```
PointerX()
LocaleString(Locale/Locale, Locale/Valid, 'MULTIPLAYER_MAPNAME')
CenterAligned('standard6.dif')
Button(0, ButtonPress, Select)
```

A named object with no fields is written with its name in front: `editbox-data="Chat/SayAllData: Edit()"`. A named object with fields is a variable, and is written by its name. A named object with fields that is not in `<Variables>` is an error.

A function is written by its name: `function="Sound/PlayMenuOk"`.

### Colors

A color is one value. It is written in one of these forms:

| Form | Meaning |
|---|---|
| `#RRGGBB` | red, green and blue as two hex digits each. Alpha is 1. |
| `#RRGGBBAA` | the same, with alpha as two hex digits. |
| `#RRGGBB, a` | red, green and blue as hex, with alpha as a number or an expression. |
| `r, g, b` | the channels as numbers or expressions. Alpha is 1. |
| `r, g, b, a` | the channels as numbers or expressions, with alpha. |

- A color with a Float field takes numbers only. An expression is an error.
- A color with a Data field takes expressions. A hex value is a number.
- The hex form needs red, green and blue to be numbers that are exact in hex. Otherwise the channels are written as a list.
- Inside a call, a color is `#RRGGBB` or `#RRGGBBAA`, or the four channels. It is never `#RRGGBB, a`.

## Shared tags

Some tags write more than one type. The type is the one whose attributes fit the tag:

- An attribute that is missing must be optional for that type.
- An attribute that holds an expression needs a Data field. A Float field takes numbers only.
- Of the types that fit, the one with the fewest expression fields is chosen, then the one with the fewest attributes.
- When two types fit equally, the tag is an error.

```xml
<Transform x="1" y="2" width="3" height="4">…</Transform>                      <!-- TransformNode -->
<Transform x="10" y="somevar plus 1" width="3" height="4">…</Transform>         <!-- BfTransformNode -->
<MultiplyColor alpha="0.5" />                                                   <!-- BfMultiplyColorEffect2 -->
<MultiplyColor color="somevar, 0.5, 0.5, 0.5" />                                <!-- BfMultiplyColorEffect -->
```

## Errors

A tag, attribute or text that does not fit raises an `XmlError` with the element and the reason. For a shared tag, the reason is given for each type that was tried, for example:

- `<Transform> with attributes ['x', 'y', 'width', 'height'] fits no type: TransformNode cannot take 'x' = 'somevar' …`
- `variable 'somevar' is defined twice, but a variable has one value`
- `unknown variable 'missing' (add it to <Variables>)`

## Tag reference

<!-- BEGIN GENERATED REFERENCE -->

## Tag reference

Generated from `meme_xml_tags.py`. Each tag lists the types it writes, its attributes and its content.

### Node tags

#### `<Action>`

XML tag for `ActionNode`. Content: one action. No attributes.

#### `<AddSubEffect>`

XML tag for `BfAddSubEffectNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `value` | numerical expression | yes |
| `end-value` | numerical expression | yes |
| `start-time` | numerical expression | yes |
| `start-percentage` | numerical expression | yes |
| `end-time` | numerical expression | yes |
| `delay` | numerical expression | yes |
| `up` | bool expression | yes |
| `trigger` | bool expression | yes |

#### `<AddSubNextEffect>`

XML tag for `BfAddSubNextEffectNode`. Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `value` | numerical expression | yes |
| `end-value` | numerical expression | yes |
| `start-time` | numerical expression | yes |
| `start-percentage` | numerical expression | yes |
| `end-time` | numerical expression | yes |
| `delay` | numerical expression | yes |
| `up` | bool expression | yes |
| `trigger` | bool expression | yes |

#### `<Animation>`

XML tag for `BfAnimationNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `picture-name` | expression | yes |
| `frames` | int | yes |
| `start` | bool | yes |
| `looping` | bool | yes |

#### `<BfSlider>`

XML tag for `BfFixedSliderNode`, `BfSliderNode`. Content: nodes.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `data` | numerical expression | yes |
| `minimum-value` | float | yes |
| `maximum-value` | float | yes |
| `number-visible` | float | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `interval` | float | yes |

#### `<Bink>`

XML tag for `BfBinkNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `bink-filename` | string expression | yes |
| `background-picture` | string expression | yes |
| `fade-time` | float | yes |
| `play` | bool expression | yes |

#### `<Button>`

XML tag for `BfButtonNode`, `BfLocalePictureButtonNode`, `BfNavigationButtonNode`, `BfSelectButtonNode`. Content: one action.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `picture` | string | yes |
| `mouse-over-picture` | string | yes |
| `width` | float | yes |
| `height` | float | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `clicked-picture` | string | yes |
| `index` | int | yes |
| `current-clicked-index` | expression | yes |
| `mouse-over-button` | bool | yes |
| `current-mouseover-index` | numerical expression | yes |
| `mouse-over-active` | bool expression | yes |

Group 2, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `start-x` | float | yes |
| `total-movement` | float | yes |
| `is-selected` | bool expression | yes |
| `current-x` | numerical expression | yes |
| `picture-name` | string expression | yes |
| `picture-path` | string expression | yes |

A tag uses the attributes of one group only.

#### `<Clip>`

XML tag for `ClipNode`. Content: none. No attributes.

#### `<ColorFill>`

XML tag for `BfColorFillNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `picture` | string | yes |
| `data` | expression | yes |
| `maximum-value` | expression | yes |
| `horizontal-align` | bool | yes |
| `fill-order` | bool | yes |
| `color` | expression | yes |
| `fill-color` | expression | yes |

#### `<ControlPointGauge>`

XML tag for `BfControlPointGauge`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `quarter-circle` | string | yes |
| `gauge-position` | numerical expression | yes |
| `owning-team` | numerical expression | yes |
| `taking-team` | numerical expression | yes |

#### `<Credits>`

XML tag for `BfCreditsNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `value` | numerical expression | yes |
| `end-value` | float | yes |
| `reset-value` | float | yes |
| `time` | float | yes |
| `trigger` | bool expression | yes |

#### `<Crosshair>`

XML tag for `BfCrosshairNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `radius` | numerical expression | yes |
| `thickness` | numerical expression | yes |
| `outline-thickness` | numerical expression | yes |
| `deviation` | numerical expression | yes |
| `color` | expression | yes |
| `outline-color` | expression | yes |

#### `<CullAction>`

XML tag for `CullActionNode`. Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `event-type` | int | yes |
| `event-data` | int | yes |

#### `<CullEventAction>`

XML tag for `CullEventActionNode`, `CullEventTimeoutActionNode`. Content: one action.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `event` | event text | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `timeout-time` | float | yes |

#### `<CullVariable>`

XML tag for `CullVariableNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `data` | expression | yes |

#### `<CullVariableAction>`

XML tag for `CullVariableActionNode`. Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |

#### `<CullVariableAndEventAction>`

XML tag for `CullVariableAndEventActionNode`. Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `event` | event text | yes |

#### `<Disable>`

XML tag for `DisableNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `disable-data` | bool expression | yes |

#### `<DragWindow>`

XML tag for `DragWindowNode`. Content: nodes.

| Attribute | Holds | Required |
|---|---|---|
| `x` | float | yes |
| `y` | float | yes |
| `width` | float | yes |
| `height` | float | yes |

#### `<Edit>`

XML tag for `BfEditNode`, `BfEditNodeNew`, `EditNode`. Content: one action or none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `font` | string | yes |
| `string` | expression | yes |
| `max-characters` | int | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `editbox-data` | expression | yes |
| `focus` | bool | yes |

Group 2, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `index` | int | yes |
| `max-index` | int | yes |
| `current-index` | expression | yes |

A tag uses the attributes of one group only.

#### `<EditInt>`

XML tag for `BfEditNodeInt`. Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `font` | string | yes |
| `number` | expression | yes |
| `string` | expression | yes |
| `min-value` | int | yes |
| `max-value` | int | yes |
| `editbox-data` | expression | yes |
| `focus` | bool | yes |

#### `<Effect>`

XML tag for `EffectNode`. Content: one effect. No attributes.

#### `<ExtendedFocusToPressedEffect>`

XML tag for `ExtendedFocusToPressedEffectNode`. Content: one effect.

| Attribute | Holds | Required |
|---|---|---|
| `min-value` | float | yes |
| `max-value` | float | yes |

#### `<ExtendedNormalToFocusEffect>`

XML tag for `ExtendedNormalToFocusEffectNode`. Content: one effect.

| Attribute | Holds | Required |
|---|---|---|
| `min-value` | float | yes |
| `max-value` | float | yes |

#### `<Focus>`

XML tag for `FocusNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `focus-x` | expression | yes |
| `focus-y` | expression | yes |

#### `<FocusEffect>`

XML tag for `FocusEffectNode`. Content: one effect. No attributes.

#### `<FocusToPressedEffect>`

XML tag for `FocusToPressedEffectNode`. Content: one effect. No attributes.

#### `<Gauge>`

XML tag for `BfGaugeNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `color` | expression | yes |
| `background-color` | expression | yes |
| `data` | expression | yes |
| `maximum-value` | expression | yes |
| `horizontal-align` | bool | yes |

#### `<Group>`

XML tag for `SplitNode`. Content: nodes. No attributes.

#### `<If>`

XML tag for `CullNode`. Content: nodes.

When nodes follow it in the same list, it is wrapped in a `<Group>`.

| Attribute | Holds | Required | Default |
|---|---|---|---|
| `condition` | expression | yes | — |
| `in-time` | float | no | `0` |
| `out-time` | float | no | `0` |

#### `<ListBox>`

XML tag for `BfNewListBoxNode`. Content: none.

| Attribute | Holds | Required | Default |
|---|---|---|---|
| `font` | string | yes | — |
| `step-sound` | string | no | `""` |
| `select-sound` | string | no | `""` |
| `failed-select-sound` | string | no | `""` |
| `row-height` | float | yes | — |
| `is-selectable` | bool | no | `true` |
| `border` | bool | no | `false` |
| `background-color` | color of numbers | yes | — |
| `scrollbar-width` | float | yes | — |
| `frame-color` | color of numbers | yes | — |
| `select-color` | color of numbers | yes | — |
| `show-tooltip` | bool | no | `false` |
| `scrollbar-offset` | float | yes | — |

Child elements, each with a `field` attribute:

| Field | Holds |
|---|---|
| `listbox-data` | data |
| `select-action` | action |
| `focus-action` | action |

#### `<Locale>`

XML tag for `BfLocaleNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `locale` | expression | yes |

#### `<Name>`

XML tag for `NameNode`. Content: none. No attributes.

#### `<NavigateView>`

XML tag for `NavigateViewNode`. Content: one element.

| Attribute | Holds | Required |
|---|---|---|
| `font` | string | yes |

#### `<NewCreditsList>`

XML tag for `BfNewCreditsListNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `style` | style text | yes |
| `heading-style` | style text | yes |
| `trigger` | bool expression | yes |
| `current-position` | numerical expression | yes |
| `step` | numerical expression | yes |
| `start-value` | numerical expression | yes |
| `end-value` | numerical expression | yes |

#### `<NodeList>`

XML tag for `NodeListNode`. Content: items.

| Attribute | Holds | Required |
|---|---|---|
| `index` | expression | yes |
| `item-height` | float | yes |
| `select-sound` | string | yes |
| `up-down-sound` | string | yes |

#### `<NormalToFocusEffect>`

XML tag for `NormalToFocusEffectNode`. Content: one effect. No attributes.

#### `<NotFocusEffect>`

XML tag for `NotFocusEffectNode`. Content: one effect. No attributes.

#### `<OccupiedVehicle>`

XML tag for `BfOccupiedVehicleNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `position` | int | yes |
| `draw-debug-pic` | bool | yes |
| `occupied-vehicle` | expression | yes |

#### `<Path>`

XML tag for `PathNode`. Content: none. No attributes.

#### `<Picture>`

XML tag for `BfPictureFillNode`, `BfVariablePictureFillNode`, `PictureNode`, `BfVariablePictureFillNode2`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `picture` | string expression | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `fill-picture` | string expression | yes |
| `data` | expression | yes |
| `maximum-value` | expression | yes |
| `horizontal-align` | bool | yes |
| `fill-order` | bool | yes |
| `size` | numerical expression | yes |

#### `<Rectangle>`

XML tag for `BfRectangle`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `thickness` | float | yes |

#### `<Scale>`

XML tag for `ScaleNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `width-scale` | expression | yes |
| `height-scale` | expression | yes |

#### `<ScrollPicture>`

XML tag for `BfScrollPictureNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `scroll-picture` | string | yes |
| `data` | numerical expression | yes |
| `maximum-value` | numerical expression | yes |
| `y-offset` | int | yes |
| `size` | int | yes |
| `var-size` | numerical expression | yes |
| `maintain-value` | numerical expression | yes |
| `from-bottom` | bool | yes |

#### `<ShowEffect>`

XML tag for `ShowEffectNode`. Content: one effect. No attributes.

#### `<Slider>`

XML tag for `SliderNode`. Content: nodes.

| Attribute | Holds | Required |
|---|---|---|
| `data` | expression | yes |
| `minimum-value` | float | yes |
| `maximum-value` | float | yes |
| `number-visible` | float | yes |

#### `<StackPath>`

XML tag for `StackPathNode`. Content: none. No attributes.

#### `<Sticky>`

XML tag for `StickyNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `data` | expression | yes |

#### `<Text>`

XML tag for `BfTextNode`, `TextNode`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `string` | expression | yes |
| `style` | style text | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `type` | numerical expression | yes |

#### `<TimeoutAction>`

XML tag for `TimeoutActionNode`. Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `timeout-time` | float | yes |

#### `<Transform>`

XML tag for `BfTransformNode`, `BfTransformNodeSize`, `TransformNode`. Content: nodes.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `x` | numerical expression | yes |
| `y` | numerical expression | yes |
| `width` | numerical expression | yes |
| `height` | numerical expression | yes |
Expressions are allowed for `x`, `y` or `width`, `height`, not for both at once.

#### `<TransitionalEffect>`

XML tag for `TransitionalEffectNode`. Content: one effect. No attributes.

#### `<TransitionalHideEffect>`

XML tag for `TransitionalHideEffectNode`. Content: one effect. No attributes.

#### `<TransitionalShowEffect>`

XML tag for `TransitionalShowEffectNode`. Content: one effect. No attributes.

#### `<Translate>`

XML tag for `TranslateNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `x` | numerical expression | yes |
| `y` | numerical expression | yes |

#### `<TriangleButtons>`

XML tag for `BfTriangleButtonsNode`. Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `top-triangle-selected` | string | yes |
| `bottom-triangle-selected` | string | yes |
| `width` | float | yes |
| `height` | float | yes |
| `selected-team` | numerical expression | yes |

#### `<VariableEffect>`

XML tag for `VariableEffectNode`. Content: one effect.

| Attribute | Holds | Required |
|---|---|---|
| `effect-level` | numerical expression | yes |

#### `<VariablePicture>`

XML tag for `BfVariablePictureNode`, `VariablePictureNode`. Content: none.

Group 1:

| Attribute | Holds | Required |
|---|---|---|
| `picture` | string expression | yes |
| `redraw` | bool expression | yes |

Group 2:

| Attribute | Holds | Required | Default |
|---|---|---|---|
| `first-part` | string expression | yes | — |
| `middle-part` | expression | no | `null` |
| `last-part` | expression | no | `null` |

A tag uses the attributes of one group only.

#### `<VariableTimeoutAction>`

XML tag for `BfVariableTimeoutActionNode`, `BfVariableTimeoutActionNode2`. Content: one action.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `timeout-time` | numerical expression | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `current-time` | numerical expression | yes |

#### `<VerticalScroll>`

XML tag for `BfVerticalScrollNode`, `BfVerticalScrollExNode`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `text` | expression | yes |
| `scroll-speed` | float | yes |
| `scroll-speed-multiplier` | expression | yes |
| `restart-toggle` | expression | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `font` | string | yes |

Group 2, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `version` | int | yes |
| `style` | style text | yes |

A tag uses the attributes of one group only.

#### `<Window>`

XML tag for `WindowNode`. Content: nodes.

| Attribute | Holds | Required |
|---|---|---|
| `x` | float | yes |
| `y` | float | yes |
| `width` | float | yes |
| `height` | float | yes |

#### `<Zoom>`

XML tag for `ZoomNode`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `z` | expression | yes |

### Action tags

#### `<ActionList>`

XML tag for `ActionListAction`. Content: items. No attributes.

#### `<CallFunction>`

XML tag for `CallFunctionAction`, `CallFunctionVariableAction`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `function` | function text | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `result-data` | expression | yes |

#### `<LastInputIndex>`

XML tag for `LastInputIndexAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `last-input-index` | expression | yes |

#### `<LockPointer>`

XML tag for `LockPointerAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `input-index-data` | expression | yes |

#### `<ModifyVariable>`

XML tag for `ModifyVariableAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `modify-value` | float | yes |
| `limit-value` | float | yes |

#### `<Navigate>`

XML tag for `NavigateAction`. Content: one element. No attributes.

#### `<NavigateChild>`

XML tag for `NavigateChildAction`. Content: one element. No attributes.

#### `<NavigateChildAndRun>`

XML tag for `NavigateChildAndRunAction`. Content: one element. No attributes.

#### `<NavigateFirstSibling>`

XML tag for `NavigateFirstSiblingAction`. Content: one element. No attributes.

#### `<NavigateLastSibling>`

XML tag for `NavigateLastSiblingAction`. Content: one element. No attributes.

#### `<NavigateNextSibling>`

XML tag for `NavigateNextSiblingAction`. Content: one element. No attributes.

#### `<NavigateParent>`

XML tag for `NavigateParentAction`. Content: one element. No attributes.

#### `<NavigateParentAndRun>`

XML tag for `NavigateParentAndRunAction`. Content: one element. No attributes.

#### `<NavigatePreviousSibling>`

XML tag for `NavigatePreviousSiblingAction`. Content: one element. No attributes.

#### `<NavigateRun>`

XML tag for `NavigateRunAction`. Content: one element. No attributes.

#### `<NavigateRunAndChild>`

XML tag for `NavigateRunAndChildAction`. Content: one element. No attributes.

#### `<NavigateSiblingIndex>`

XML tag for `NavigateSiblingIndexAction`. Content: one element.

| Attribute | Holds | Required |
|---|---|---|
| `index` | int | yes |

#### `<PopPath>`

XML tag for `PopPathAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `stack-path-node` | empty text | yes |
| `in-time` | float | yes |
| `out-time` | float | yes |
| `in-wait-time` | float | yes |
| `out-wait-time` | float | yes |
| `paint-outnode-over-innode` | bool | yes |

#### `<PushPath>`

XML tag for `PushPathAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `stack-path-node` | empty text | yes |
| `destination-node` | empty text | yes |
| `in-time` | float | yes |
| `out-time` | float | yes |
| `in-wait-time` | float | yes |
| `out-wait-time` | float | yes |
| `paint-outnode-over-innode` | bool | yes |

#### `<RemoveEvent>`

XML tag for `RemoveEventAction`. Content: none. No attributes.

#### `<SetFocus>`

XML tag for `SetFocusAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `x` | expression | yes |
| `y` | expression | yes |

#### `<SetPath>`

XML tag for `SetPathAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `path-node` | empty text | yes |
| `destination-node` | empty text | yes |
| `in-time` | float | yes |
| `out-time` | float | yes |
| `in-wait-time` | float | yes |
| `out-wait-time` | float | yes |
| `paint-outnode-over-innode` | bool | yes |

#### `<SetString>`

XML tag for `SetStringAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | string expression | yes |
| `value` | string expression | yes |

#### `<SetVariable>`

XML tag for `SetVariableAction`, `SetVariableArrayAction`, `SetVariableSoftAction`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `value` | expression | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `index` | expression | yes |

Group 2, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `speed` | float | yes |

A tag uses the attributes of one group only.

#### `<SetVariableSine>`

XML tag for `SetVariableSineAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | numerical expression | yes |
| `value` | numerical expression | yes |
| `speed` | float | yes |
| `braking-distance` | float | yes |

#### `<SetVariableSinus>`

XML tag for `SetVariableSinusAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `value` | expression | yes |
| `speed` | float | yes |
| `braking-distance` | float | yes |

#### `<Sound>`

XML tag for `SoundAction`, `VolumedSoundAction`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `sound` | string | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `volume` | float | yes |

#### `<ToggleVariable>`

XML tag for `ToggleVariableAction`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | bool expression | yes |

#### `<UnlockPointer>`

XML tag for `UnlockPointerAction`. Content: none. No attributes.

### Effect tags

#### `<AlphaFade>`

XML tag for `AlphaFadeEffect`. Content: none. No attributes.

#### `<BlendFunc>`

XML tag for `BlendFuncEffect`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `source-blend-function` | int | yes |
| `destination-blend-function` | int | yes |

#### `<Clip>`

XML tag for `ClipEffect`, `MoveClipEffect`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `x` | float | yes |
| `y` | float | yes |
| `width` | float | yes |
| `height` | float | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `move-length` | float | yes |
| `move-direction` | float | yes |

#### `<Color>`

XML tag for `ColorEffect`, `VariableColorEffect`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `color` | color of numerical expressions | yes |

#### `<HideDisable>`

XML tag for `HideDisableEffect`. Content: none. No attributes.

#### `<Move>`

XML tag for `MoveEffect`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `move-length` | expression | yes |
| `move-direction` | expression | yes |

#### `<MultiplyColor>`

XML tag for `BfMultiplyColorEffect`, `BfMultiplyColorEffect2`, `MultiplyColorEffect`. Content: none.

Group 1:

| Attribute | Holds | Required |
|---|---|---|
| `color` | color of numerical expressions | yes |

Group 2:

| Attribute | Holds | Required |
|---|---|---|
| `alpha` | numerical expression | yes |

A tag uses the attributes of one group only.

#### `<MultiplyVertexColor>`

XML tag for `MultiplyVertexColorEffect`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `top-left-color` | color of numbers | yes |
| `top-right-color` | color of numbers | yes |
| `bottom-right-color` | color of numbers | yes |
| `bottom-left-color` | color of numbers | yes |

#### `<Rotate>`

XML tag for `RotateAroundCoordinateEffect`, `RotateEffect`. Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `start-angle` | numerical expression | yes |
| `angle-multiplier` | numerical expression | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `x` | numerical expression | yes |
| `y` | numerical expression | yes |

#### `<SinMove>`

XML tag for `SinMoveEffect`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `move-length` | expression | yes |
| `move-direction` | expression | yes |

#### `<VertexColor>`

XML tag for `VertexColorEffect`. Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `top-left-color` | color of numbers | yes |
| `top-right-color` | color of numbers | yes |
| `bottom-right-color` | color of numbers | yes |
| `bottom-left-color` | color of numbers | yes |

### Pointer tags

#### `<DynamicIndex>`

XML tag for `DynamicIndexPointer`. Content: none. No attributes.

### Text calls

Calls are written inside an attribute, and their arguments are in the order listed.

### Data calls

#### `Color(...)`

Text call for `BfColorData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Red | color of numbers |

#### `ConcatenateList(...)`

Text call for `ConcatenateListData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Data list | List |

#### `Data(...)`

Text call for `Data`. No arguments.

#### `Edit(...)`

Text call for `BfEditData`. No arguments.

#### `FloatRef(...)`

Text call for `FloatRefData`. No arguments.

#### `FocusLocked(...)`

Text call for `FocusLockedData`. No arguments.

#### `IndexCount(...)`

Text call for `IndexCountData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Data | expression |

#### `ListBox(...)`

Text call for `ListBoxData`. No arguments.

#### `Locale(...)`

Text call for `BfLocaleData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Valid | bool expression |

#### `LocaleString(...)`

Text call for `BfLocaleStringData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Locale | expression |
| 2 | Valid | bool expression |
| 3 | String Id | string expression |

#### `LocaleStringInt(...)`

Text call for `LocaleStringData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Int | int |

#### `Logical(...)`

Text call for `LogicalData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Data 1 | expression |
| 2 | Data 2 | expression |

#### `OccupiedVehicle(...)`

Text call for `BfOccupiedVehicleData`. No arguments.

#### `Operator(...)`

Text call for `OperatorData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Data 1 | expression |
| 2 | Data 2 | expression |

#### `PlayerInputIndex(...)`

Text call for `PlayerInputIndexData`. No arguments.

#### `PointerX(...)`

Text call for `PointerXData`. No arguments.

#### `PointerY(...)`

Text call for `PointerYData`. No arguments.

#### `StringRef(...)`

Text call for `StringRefData`. No arguments.

#### `Toggle(...)`

Text call for `ToggleData`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Toggle data | bool expression |
| 2 | Data 1 | numerical expression |
| 3 | Data 2 | numerical expression |

### Style calls

#### `BfStyle(...)`

Text call for `BfStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `Center(...)`

Text call for `BfCenterStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `CenterAligned(...)`

Text call for `CenterAlignedStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `LeftOutline(...)`

Text call for `BfLeftOutlineStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `Outline(...)`

Text call for `BfOutlineStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `RightAligned(...)`

Text call for `RightAlignedStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `RowDistance(...)`

Text call for `RowDistanceStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |
| 2 | Row distance | float |

#### `SingleLine(...)`

Text call for `SingleLineStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `SingleLineSize(...)`

Text call for `SingleLineSizeStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |
| 2 | Size constant | float |

#### `Size(...)`

Text call for `SizeStyle`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |
| 2 | Size constant | float |

#### `Style(...)`

Text call for `Style`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `Style2(...)`

Text call for `BfStyle2`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

### Event calls

#### `AnyKey(...)`

Text call for `AnyKeyEvent`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Input index | int, named by PlayerInput |
| 2 | Event type | int, named by EventType |

#### `Button(...)`

Text call for one of these types, picked by how many arguments it has:

`ButtonEvent`, 3 arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Input index | int, named by PlayerInput |
| 2 | Event type | int, named by EventType |
| 3 | Button type | int, named by ButtonType |

`ExtendedButtonEvent`, 4 arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Input index | int, named by PlayerInput |
| 2 | Event type | int, named by EventType |
| 3 | Button type | int, named by ButtonType |
| 4 | Repeat count | int |

#### `Event(...)`

Text call for `Event`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Input index | int, named by PlayerInput |

#### `Type(...)`

Text call for `TypeEvent`. Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Input index | int, named by PlayerInput |
| 2 | Event type | int, named by EventType |

### Operators

From loosest to tightest binding. Operators with the same precedence bind equally.

| Written as | Data object | Precedence |
|---|---|---|
| `or` | OrData | 1 |
| `xor` | ExclusiveOrData | 2 |
| `and` | AndData | 3 |
| `is` | EqualData | 4 |
| `is_not` | NotEqualData | 4 |
| `less_than` | LessData | 4 |
| `less_than_or_equal` | LessEqualData | 4 |
| `plus` | AddData | 5 |
| `minus` | SubData | 5 |
| `times` | MulData | 6 |
| `divided_by` | DivData | 6 |
| `not` | NotData | 7 |

### Engine names

#### Event types

The event type of TypeEvent, ButtonEvent, ExtendedButtonEvent and AnyKeyEvent.

| Value | Name |
|---|---|
| 0 | No event |
| 1 | ButtonPress |
| 2 | ButtonRelease |
| 3 | ButtonReleaseOutside |
| 4 | UnicodePress |
| 5 | UnicodeRelease |
| 6 | UnicodeReleaseOutside |
| 7 | GainFocus |
| 8 | LostFocus |
| 9 | PointerIn |
| 10 | PointerOut |
| 11 | PointerMove |
| 12 | PointerMoveOut |
| 13 | PreShow |
| 14 | PostShow |
| 15 | PreHide |
| 16 | PostHide |
| 17 | PreWaitShow |
| 18 | PreWaitHide |
| 19 | Quit |
| 20 | Disable |
| 21 | Enable |
| 22 | Update |

#### Button types

The button type of ButtonEvent and ExtendedButtonEvent.

| Value | Name |
|---|---|
| 0 | No button |
| 1 | Select |
| 2 | Cancel |
| 3 | Back |
| 4 | Edit |
| 5 | Leftwards |
| 6 | Upwards |
| 7 | Rightwards |
| 8 | Downwards |
| 9 | Home |
| 10 | End |
| 11 | PageUp |
| 12 | PageDown |
| 13 | Insert |
| 14 | Delete |
| 15 | Backspace |
| 16 | Tab |
| 17 | Start |
| 18 | Enter |
| 19 | Scroll up |
| 20 | Scroll down |

#### Player inputs

The input index of every event: the player input that the event comes from. Index 0 means all inputs, so it has no name. Indexes without a name are written as numbers.

| Value | Name |
|---|---|
| 1 | Pitch |
| 2 | Roll |
| 3 | Throttle |
| 4 | MouseLookX |
| 5 | MouseLookY |
| 6 | CameraX |
| 7 | CameraY |
| 8 | Fire |
| 9 | Action |
| 10 | Use |
| 11 | MouseLook |
| 12 | Walk |
| 13 | Run |
| 14 | MenuSelect1 |
| 15 | MenuSelect2 |
| 16 | MenuSelect3 |
| 17 | MenuSelect4 |
| 18 | MenuSelect5 |
| 19 | MenuSelect6 |
| 20 | MenuSelect7 |
| 21 | MenuSelect8 |
| 22 | MenuSelect9 |
| 23 | AltFire |
| 24 | Reload |
| 25 | Drop |
| 26 | ToggleCameraMode |
| 27 | ToggleCamera |
| 28 | Lie |
| 29 | Crouch |
| 30 | CameraMode1 |
| 31 | CameraMode2 |
| 32 | CameraMode3 |
| 33 | CameraMode4 |
| 34 | Radio1 |
| 35 | Radio2 |
| 36 | Radio3 |
| 37 | Radio4 |
| 38 | Radio5 |
| 39 | Radio6 |
| 40 | Radio7 |
| 41 | Radio8 |
| 42 | ScreenShot |
| 43 | ToolTip |
| 44 | SayAll |
| 45 | SayTeam |
| 46 | NextItem |
| 47 | PrevItem |
| 48 | Communication |
| 49 | ShowScoreBoard |
| 50 | Map |
| 51 | ZoomMap |
| 52 | ShowMapVote |
| 53 | VoteYes |
| 54 | VoteNo |
| 55 | None |

<!-- END GENERATED REFERENCE -->

## Raw form

The raw form has no tags. The tag is the type name in `meme_types.json`, and every field is one child element, in the order of the fields. The reader matches children to fields by position and does not read `description`; the writer adds it so the file is easier to read.

```xml
<SetVariableAction>
  <BoolData description="Variable" name="FocusEffect/Init/GoFadeIn2" />
  <BoolData description="Data">
    <Boolean description="Value">true</Boolean>
  </BoolData>
</SetVariableAction>
```

- **Values** are elements with the primitive type as their tag, such as `<Float description="X">0</Float>`. Their text is the value. An enum value is written with its full name, such as `<TypeIndex description="Event type">PointerIn</TypeIndex>`.
- **Objects** are elements. An empty object field is a `<Placeholder description="Data" />`. A named placeholder has a name: `<Placeholder description="Node" name="MenuLayer" />`.
- **Node fields** hold a chain of nodes. One node is a child element. Several nodes are wrapped in `<g>`.
- **List fields** are a `<List>` element whose children are the items. An item that has nodes after it is wrapped in `<g>`. The end marker of a list is not written.
- **The body of a CullNode** is its first child, so the nodes inside the `<CullNode>` are its children.
- **A variable by its name:** an element with a `name` and nothing else refers to a variable of `<Variables>`.
- **`<Object type="…">`** is the raw element of a type whose name is also the tag of a clean form in that position. For example the base type `Action` among nodes is written `<Object type="Action">`, because `<Action>` there is the clean form of `ActionNode`.
- **Text with line breaks** is written as it is, and a `uses_crlf="true"` attribute marks Windows line breaks.

An object is written in the raw form when its type has no clean tag, or when one of its fields cannot be written as text. For example `<SplitAction>` has two action fields in a row with no name for either, so it has no clean form.
