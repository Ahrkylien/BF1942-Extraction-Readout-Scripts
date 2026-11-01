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

### Placeholders

An empty reference is written as `<Placeholder />`, in both forms. A name on it is kept, as `name="..."`, because the binary stores a name on empty references too (for example the end of the `Global` chain in `Battlefield 2/Ingame`):

```xml
<Group>
  <If condition="somevar is 1"><NameNode /></If>
  <Placeholder name="Global" />
</Group>
```

The field a placeholder fills comes from its position:

- After a node in a chain, it is the next node of that node.
- At the start of a chain, or as the content of a tag such as `<Group>` or `<Effect>`, it is the node or effect in that field.
- As a named child with a `field` attribute, it is that field.

The raw form uses `<Placeholder description="..." />` for every empty field, so the compact form uses the same tag.

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

### Calls

An object that is not a literal, an operator or a list is a call: its name, then its arguments in order. The names and arguments are listed in the tag reference, from [Data calls](#data-calls) on.

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

Each tag lists the types it writes, its attributes and its content.

Calls are written inside an attribute, and their arguments are in the order listed.

### Node tags

#### `<Action>`&nbsp;&nbsp;&nbsp;🔗 [ActionNode](MemeType.md#actionnode)

Content: one action. No attributes.

#### `<AddSubEffect>`&nbsp;&nbsp;&nbsp;🔗 [BfAddSubEffectNode](MemeType.md#bfaddsubeffectnode)

Content: none.

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

#### `<AddSubNextEffect>`&nbsp;&nbsp;&nbsp;🔗 [BfAddSubNextEffectNode](MemeType.md#bfaddsubnexteffectnode)

Content: one action.

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

#### `<Animation>`&nbsp;&nbsp;&nbsp;🔗 [BfAnimationNode](MemeType.md#bfanimationnode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `picture-name` | expression | yes |
| `frames` | int | yes |
| `start` | bool | yes |
| `looping` | bool | yes |

#### `<BfSlider>`&nbsp;&nbsp;&nbsp;🔗 [BfSliderNode](MemeType.md#bfslidernode), [BfFixedSliderNode](MemeType.md#bffixedslidernode)

Content: nodes.

| Attribute | Holds | Required |
|---|---|---|
| `data` | numerical expression | yes |
| `minimum-value` | float | yes |
| `maximum-value` | float | yes |
| `number-visible` | float | yes |
| `interval` | float | no |

#### `<Bink>`&nbsp;&nbsp;&nbsp;🔗 [BfBinkNode](MemeType.md#bfbinknode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `bink-filename` | string expression | yes |
| `background-picture` | string expression | yes |
| `fade-time` | float | yes |
| `play` | bool expression | yes |

#### `<Button>`&nbsp;&nbsp;&nbsp;🔗 [BfButtonNode](MemeType.md#bfbuttonnode), [BfLocalePictureButtonNode](MemeType.md#bflocalepicturebuttonnode), [BfNavigationButtonNode](MemeType.md#bfnavigationbuttonnode), [BfSelectButtonNode](MemeType.md#bfselectbuttonnode)

Content: one action.

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

#### `<Clip>`&nbsp;&nbsp;&nbsp;🔗 [ClipNode](MemeType.md#clipnode)

Content: none. No attributes.

#### `<ColorFill>`&nbsp;&nbsp;&nbsp;🔗 [BfColorFillNode](MemeType.md#bfcolorfillnode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `picture` | string | yes |
| `data` | expression | yes |
| `maximum-value` | expression | yes |
| `horizontal-align` | bool | yes |
| `fill-order` | bool | yes |
| `color` | expression | yes |
| `fill-color` | expression | yes |

#### `<ControlPointGauge>`&nbsp;&nbsp;&nbsp;🔗 [BfControlPointGauge](MemeType.md#bfcontrolpointgauge)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `quarter-circle` | string | yes |
| `gauge-position` | numerical expression | yes |
| `owning-team` | numerical expression | yes |
| `taking-team` | numerical expression | yes |

#### `<Credits>`&nbsp;&nbsp;&nbsp;🔗 [BfCreditsNode](MemeType.md#bfcreditsnode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `value` | numerical expression | yes |
| `end-value` | float | yes |
| `reset-value` | float | yes |
| `time` | float | yes |
| `trigger` | bool expression | yes |

#### `<Crosshair>`&nbsp;&nbsp;&nbsp;🔗 [BfCrosshairNode](MemeType.md#bfcrosshairnode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `radius` | numerical expression | yes |
| `thickness` | numerical expression | yes |
| `outline-thickness` | numerical expression | yes |
| `deviation` | numerical expression | yes |
| `color` | expression | yes |
| `outline-color` | expression | yes |

#### `<CullAction>`&nbsp;&nbsp;&nbsp;🔗 [CullActionNode](MemeType.md#cullactionnode)

Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `event-type` | int | yes |
| `event-data` | int | yes |

#### `<CullEventAction>`&nbsp;&nbsp;&nbsp;🔗 [CullEventActionNode](MemeType.md#culleventactionnode), [CullEventTimeoutActionNode](MemeType.md#culleventtimeoutactionnode)

Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `event` | event text | yes |
| `timeout-time` | float | no |

#### `<CullVariable>`&nbsp;&nbsp;&nbsp;🔗 [CullVariableNode](MemeType.md#cullvariablenode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `data` | expression | yes |

#### `<CullVariableAction>`&nbsp;&nbsp;&nbsp;🔗 [CullVariableActionNode](MemeType.md#cullvariableactionnode)

Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |

#### `<CullVariableAndEventAction>`&nbsp;&nbsp;&nbsp;🔗 [CullVariableAndEventActionNode](MemeType.md#cullvariableandeventactionnode)

Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `event` | event text | yes |

#### `<Disable>`&nbsp;&nbsp;&nbsp;🔗 [DisableNode](MemeType.md#disablenode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `disable-data` | bool expression | yes |

#### `<DragWindow>`&nbsp;&nbsp;&nbsp;🔗 [DragWindowNode](MemeType.md#dragwindownode)

Content: nodes.

| Attribute | Holds | Required |
|---|---|---|
| `x` | float | yes |
| `y` | float | yes |
| `width` | float | yes |
| `height` | float | yes |

#### `<Edit>`&nbsp;&nbsp;&nbsp;🔗 [BfEditNode](MemeType.md#bfeditnode), [BfEditNodeNew](MemeType.md#bfeditnodenew), [EditNode](MemeType.md#editnode)

Content: one action or none.

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

#### `<EditInt>`&nbsp;&nbsp;&nbsp;🔗 [BfEditNodeInt](MemeType.md#bfeditnodeint)

Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `font` | string | yes |
| `number` | expression | yes |
| `string` | expression | yes |
| `min-value` | int | yes |
| `max-value` | int | yes |
| `editbox-data` | expression | yes |
| `focus` | bool | yes |

#### `<Effect>`&nbsp;&nbsp;&nbsp;🔗 [EffectNode](MemeType.md#effectnode)

Content: one effect. No attributes.

#### `<ExtendedFocusToPressedEffect>`&nbsp;&nbsp;&nbsp;🔗 [ExtendedFocusToPressedEffectNode](MemeType.md#extendedfocustopressedeffectnode)

Content: one effect.

| Attribute | Holds | Required |
|---|---|---|
| `min-value` | float | yes |
| `max-value` | float | yes |

#### `<ExtendedNormalToFocusEffect>`&nbsp;&nbsp;&nbsp;🔗 [ExtendedNormalToFocusEffectNode](MemeType.md#extendednormaltofocuseffectnode)

Content: one effect.

| Attribute | Holds | Required |
|---|---|---|
| `min-value` | float | yes |
| `max-value` | float | yes |

#### `<Focus>`&nbsp;&nbsp;&nbsp;🔗 [FocusNode](MemeType.md#focusnode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `focus-x` | expression | yes |
| `focus-y` | expression | yes |

#### `<FocusEffect>`&nbsp;&nbsp;&nbsp;🔗 [FocusEffectNode](MemeType.md#focuseffectnode)

Content: one effect. No attributes.

#### `<FocusToPressedEffect>`&nbsp;&nbsp;&nbsp;🔗 [FocusToPressedEffectNode](MemeType.md#focustopressedeffectnode)

Content: one effect. No attributes.

#### `<Gauge>`&nbsp;&nbsp;&nbsp;🔗 [BfGaugeNode](MemeType.md#bfgaugenode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `color` | expression | yes |
| `background-color` | expression | yes |
| `data` | expression | yes |
| `maximum-value` | expression | yes |
| `horizontal-align` | bool | yes |

#### `<Group>`&nbsp;&nbsp;&nbsp;🔗 [SplitNode](MemeType.md#splitnode)

Content: nodes. No attributes.

#### `<If>`&nbsp;&nbsp;&nbsp;🔗 [CullNode](MemeType.md#cullnode)

Content: nodes.

When nodes follow it in the same list, it is wrapped in a `<Group>`.

| Attribute | Holds | Required | Default |
|---|---|---|---|
| `condition` | expression | yes | — |
| `in-time` | float | no | `0` |
| `out-time` | float | no | `0` |

#### `<ListBox>`&nbsp;&nbsp;&nbsp;🔗 [BfNewListBoxNode](MemeType.md#bfnewlistboxnode)

Content: none.

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

#### `<Locale>`&nbsp;&nbsp;&nbsp;🔗 [BfLocaleNode](MemeType.md#bflocalenode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `locale` | expression | yes |

#### `<Name>`&nbsp;&nbsp;&nbsp;🔗 [NameNode](MemeType.md#namenode)

Content: none. No attributes.

#### `<NavigateView>`&nbsp;&nbsp;&nbsp;🔗 [NavigateViewNode](MemeType.md#navigateviewnode)

Content: one element.

| Attribute | Holds | Required |
|---|---|---|
| `font` | string | yes |

#### `<NewCreditsList>`&nbsp;&nbsp;&nbsp;🔗 [BfNewCreditsListNode](MemeType.md#bfnewcreditslistnode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `style` | style text | yes |
| `heading-style` | style text | yes |
| `trigger` | bool expression | yes |
| `current-position` | numerical expression | yes |
| `step` | numerical expression | yes |
| `start-value` | numerical expression | yes |
| `end-value` | numerical expression | yes |

#### `<NodeList>`&nbsp;&nbsp;&nbsp;🔗 [NodeListNode](MemeType.md#nodelistnode)

Content: items.

| Attribute | Holds | Required |
|---|---|---|
| `index` | expression | yes |
| `item-height` | float | yes |
| `select-sound` | string | yes |
| `up-down-sound` | string | yes |

#### `<NormalToFocusEffect>`&nbsp;&nbsp;&nbsp;🔗 [NormalToFocusEffectNode](MemeType.md#normaltofocuseffectnode)

Content: one effect. No attributes.

#### `<NotFocusEffect>`&nbsp;&nbsp;&nbsp;🔗 [NotFocusEffectNode](MemeType.md#notfocuseffectnode)

Content: one effect. No attributes.

#### `<OccupiedVehicle>`&nbsp;&nbsp;&nbsp;🔗 [BfOccupiedVehicleNode](MemeType.md#bfoccupiedvehiclenode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `position` | int | yes |
| `draw-debug-pic` | bool | yes |
| `occupied-vehicle` | expression | yes |

#### `<Path>`&nbsp;&nbsp;&nbsp;🔗 [PathNode](MemeType.md#pathnode)

Content: none. No attributes.

#### `<Picture>`&nbsp;&nbsp;&nbsp;🔗 [BfPictureFillNode](MemeType.md#bfpicturefillnode), [BfVariablePictureFillNode](MemeType.md#bfvariablepicturefillnode), [PictureNode](MemeType.md#picturenode), [BfVariablePictureFillNode2](MemeType.md#bfvariablepicturefillnode2)

Content: none.

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

#### `<Rectangle>`&nbsp;&nbsp;&nbsp;🔗 [BfRectangle](MemeType.md#bfrectangle)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `thickness` | float | yes |

#### `<Scale>`&nbsp;&nbsp;&nbsp;🔗 [ScaleNode](MemeType.md#scalenode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `width-scale` | expression | yes |
| `height-scale` | expression | yes |

#### `<ScrollPicture>`&nbsp;&nbsp;&nbsp;🔗 [BfScrollPictureNode](MemeType.md#bfscrollpicturenode)

Content: none.

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

#### `<ShowEffect>`&nbsp;&nbsp;&nbsp;🔗 [ShowEffectNode](MemeType.md#showeffectnode)

Content: one effect. No attributes.

#### `<Slider>`&nbsp;&nbsp;&nbsp;🔗 [SliderNode](MemeType.md#slidernode)

Content: nodes.

| Attribute | Holds | Required |
|---|---|---|
| `data` | expression | yes |
| `minimum-value` | float | yes |
| `maximum-value` | float | yes |
| `number-visible` | float | yes |

#### `<StackPath>`&nbsp;&nbsp;&nbsp;🔗 [StackPathNode](MemeType.md#stackpathnode)

Content: none. No attributes.

#### `<Sticky>`&nbsp;&nbsp;&nbsp;🔗 [StickyNode](MemeType.md#stickynode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `data` | expression | yes |

#### `<Text>`&nbsp;&nbsp;&nbsp;🔗 [BfTextNode](MemeType.md#bftextnode), [TextNode](MemeType.md#textnode)

Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `string` | expression | yes |
| `style` | style text | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `type` | numerical expression | yes |

#### `<TimeoutAction>`&nbsp;&nbsp;&nbsp;🔗 [TimeoutActionNode](MemeType.md#timeoutactionnode)

Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `timeout-time` | float | yes |

#### `<Transform>`&nbsp;&nbsp;&nbsp;🔗 [BfTransformNode](MemeType.md#bftransformnode), [BfTransformNodeSize](MemeType.md#bftransformnodesize), [TransformNode](MemeType.md#transformnode)

Content: nodes.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `x` | numerical expression | yes |
| `y` | numerical expression | yes |
| `width` | numerical expression | yes |
| `height` | numerical expression | yes |
Expressions are allowed for `x`, `y` or `width`, `height`, not for both at once.

#### `<TransitionalEffect>`&nbsp;&nbsp;&nbsp;🔗 [TransitionalEffectNode](MemeType.md#transitionaleffectnode)

Content: one effect. No attributes.

#### `<TransitionalHideEffect>`&nbsp;&nbsp;&nbsp;🔗 [TransitionalHideEffectNode](MemeType.md#transitionalhideeffectnode)

Content: one effect. No attributes.

#### `<TransitionalShowEffect>`&nbsp;&nbsp;&nbsp;🔗 [TransitionalShowEffectNode](MemeType.md#transitionalshoweffectnode)

Content: one effect. No attributes.

#### `<Translate>`&nbsp;&nbsp;&nbsp;🔗 [TranslateNode](MemeType.md#translatenode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `x` | numerical expression | yes |
| `y` | numerical expression | yes |

#### `<TriangleButtons>`&nbsp;&nbsp;&nbsp;🔗 [BfTriangleButtonsNode](MemeType.md#bftrianglebuttonsnode)

Content: one action.

| Attribute | Holds | Required |
|---|---|---|
| `top-triangle-selected` | string | yes |
| `bottom-triangle-selected` | string | yes |
| `width` | float | yes |
| `height` | float | yes |
| `selected-team` | numerical expression | yes |

#### `<VariableEffect>`&nbsp;&nbsp;&nbsp;🔗 [VariableEffectNode](MemeType.md#variableeffectnode)

Content: one effect.

| Attribute | Holds | Required |
|---|---|---|
| `effect-level` | numerical expression | yes |

#### `<VariablePicture>`&nbsp;&nbsp;&nbsp;🔗 [BfVariablePictureNode](MemeType.md#bfvariablepicturenode), [VariablePictureNode](MemeType.md#variablepicturenode)

Content: none.

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

#### `<VariableTimeoutAction>`&nbsp;&nbsp;&nbsp;🔗 [BfVariableTimeoutActionNode](MemeType.md#bfvariabletimeoutactionnode), [BfVariableTimeoutActionNode2](MemeType.md#bfvariabletimeoutactionnode2)

Content: one action.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `timeout-time` | numerical expression | yes |

Group 1, optional, on top of the base attributes:

| Attribute | Holds | Required |
|---|---|---|
| `current-time` | numerical expression | yes |

#### `<VerticalScroll>`&nbsp;&nbsp;&nbsp;🔗 [BfVerticalScrollNode](MemeType.md#bfverticalscrollnode), [BfVerticalScrollExNode](MemeType.md#bfverticalscrollexnode)

Content: none.

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

#### `<Window>`&nbsp;&nbsp;&nbsp;🔗 [WindowNode](MemeType.md#windownode)

Content: nodes.

| Attribute | Holds | Required |
|---|---|---|
| `x` | float | yes |
| `y` | float | yes |
| `width` | float | yes |
| `height` | float | yes |

#### `<Zoom>`&nbsp;&nbsp;&nbsp;🔗 [ZoomNode](MemeType.md#zoomnode)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `z` | expression | yes |

### Action tags

#### `<ActionList>`&nbsp;&nbsp;&nbsp;🔗 [ActionListAction](MemeType.md#actionlistaction)

Content: items. No attributes.

#### `<CallFunction>`&nbsp;&nbsp;&nbsp;🔗 [CallFunctionAction](MemeType.md#callfunctionaction), [CallFunctionVariableAction](MemeType.md#callfunctionvariableaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `function` | function text | yes |
| `result-data` | expression | no |

#### `<LastInputIndex>`&nbsp;&nbsp;&nbsp;🔗 [LastInputIndexAction](MemeType.md#lastinputindexaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `last-input-index` | expression | yes |

#### `<LockPointer>`&nbsp;&nbsp;&nbsp;🔗 [LockPointerAction](MemeType.md#lockpointeraction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `input-index-data` | expression | yes |

#### `<ModifyVariable>`&nbsp;&nbsp;&nbsp;🔗 [ModifyVariableAction](MemeType.md#modifyvariableaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `modify-value` | float | yes |
| `limit-value` | float | yes |

#### `<Navigate>`&nbsp;&nbsp;&nbsp;🔗 [NavigateAction](MemeType.md#navigateaction)

Content: one element. No attributes.

#### `<NavigateChild>`&nbsp;&nbsp;&nbsp;🔗 [NavigateChildAction](MemeType.md#navigatechildaction)

Content: one element. No attributes.

#### `<NavigateChildAndRun>`&nbsp;&nbsp;&nbsp;🔗 [NavigateChildAndRunAction](MemeType.md#navigatechildandrunaction)

Content: one element. No attributes.

#### `<NavigateFirstSibling>`&nbsp;&nbsp;&nbsp;🔗 [NavigateFirstSiblingAction](MemeType.md#navigatefirstsiblingaction)

Content: one element. No attributes.

#### `<NavigateLastSibling>`&nbsp;&nbsp;&nbsp;🔗 [NavigateLastSiblingAction](MemeType.md#navigatelastsiblingaction)

Content: one element. No attributes.

#### `<NavigateNextSibling>`&nbsp;&nbsp;&nbsp;🔗 [NavigateNextSiblingAction](MemeType.md#navigatenextsiblingaction)

Content: one element. No attributes.

#### `<NavigateParent>`&nbsp;&nbsp;&nbsp;🔗 [NavigateParentAction](MemeType.md#navigateparentaction)

Content: one element. No attributes.

#### `<NavigateParentAndRun>`&nbsp;&nbsp;&nbsp;🔗 [NavigateParentAndRunAction](MemeType.md#navigateparentandrunaction)

Content: one element. No attributes.

#### `<NavigatePreviousSibling>`&nbsp;&nbsp;&nbsp;🔗 [NavigatePreviousSiblingAction](MemeType.md#navigateprevioussiblingaction)

Content: one element. No attributes.

#### `<NavigateRun>`&nbsp;&nbsp;&nbsp;🔗 [NavigateRunAction](MemeType.md#navigaterunaction)

Content: one element. No attributes.

#### `<NavigateRunAndChild>`&nbsp;&nbsp;&nbsp;🔗 [NavigateRunAndChildAction](MemeType.md#navigaterunandchildaction)

Content: one element. No attributes.

#### `<NavigateSiblingIndex>`&nbsp;&nbsp;&nbsp;🔗 [NavigateSiblingIndexAction](MemeType.md#navigatesiblingindexaction)

Content: one element.

| Attribute | Holds | Required |
|---|---|---|
| `index` | int | yes |

#### `<PopPath>`&nbsp;&nbsp;&nbsp;🔗 [PopPathAction](MemeType.md#poppathaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `stack-path-node` | empty text | yes |
| `in-time` | float | yes |
| `out-time` | float | yes |
| `in-wait-time` | float | yes |
| `out-wait-time` | float | yes |
| `paint-outnode-over-innode` | bool | yes |

#### `<PushPath>`&nbsp;&nbsp;&nbsp;🔗 [PushPathAction](MemeType.md#pushpathaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `stack-path-node` | empty text | yes |
| `destination-node` | empty text | yes |
| `in-time` | float | yes |
| `out-time` | float | yes |
| `in-wait-time` | float | yes |
| `out-wait-time` | float | yes |
| `paint-outnode-over-innode` | bool | yes |

#### `<RemoveEvent>`&nbsp;&nbsp;&nbsp;🔗 [RemoveEventAction](MemeType.md#removeeventaction)

Content: none. No attributes.

#### `<SetFocus>`&nbsp;&nbsp;&nbsp;🔗 [SetFocusAction](MemeType.md#setfocusaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `x` | expression | yes |
| `y` | expression | yes |

#### `<SetPath>`&nbsp;&nbsp;&nbsp;🔗 [SetPathAction](MemeType.md#setpathaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `path-node` | empty text | yes |
| `destination-node` | empty text | yes |
| `in-time` | float | yes |
| `out-time` | float | yes |
| `in-wait-time` | float | yes |
| `out-wait-time` | float | yes |
| `paint-outnode-over-innode` | bool | yes |

#### `<SetString>`&nbsp;&nbsp;&nbsp;🔗 [SetStringAction](MemeType.md#setstringaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | string expression | yes |
| `value` | string expression | yes |

#### `<SetVariable>`&nbsp;&nbsp;&nbsp;🔗 [SetVariableAction](MemeType.md#setvariableaction), [SetVariableArrayAction](MemeType.md#setvariablearrayaction), [SetVariableSoftAction](MemeType.md#setvariablesoftaction)

Content: none.

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

#### `<SetVariableSine>`&nbsp;&nbsp;&nbsp;🔗 [SetVariableSineAction](MemeType.md#setvariablesineaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | numerical expression | yes |
| `value` | numerical expression | yes |
| `speed` | float | yes |
| `braking-distance` | float | yes |

#### `<SetVariableSinus>`&nbsp;&nbsp;&nbsp;🔗 [SetVariableSinusAction](MemeType.md#setvariablesinusaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | expression | yes |
| `value` | expression | yes |
| `speed` | float | yes |
| `braking-distance` | float | yes |

#### `<Sound>`&nbsp;&nbsp;&nbsp;🔗 [SoundAction](MemeType.md#soundaction), [VolumedSoundAction](MemeType.md#volumedsoundaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `sound` | string | yes |
| `volume` | float | no |

#### `<ToggleVariable>`&nbsp;&nbsp;&nbsp;🔗 [ToggleVariableAction](MemeType.md#togglevariableaction)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `variable` | bool expression | yes |

#### `<UnlockPointer>`&nbsp;&nbsp;&nbsp;🔗 [UnlockPointerAction](MemeType.md#unlockpointeraction)

Content: none. No attributes.

### Effect tags

#### `<AlphaFade>`&nbsp;&nbsp;&nbsp;🔗 [AlphaFadeEffect](MemeType.md#alphafadeeffect)

Content: none. No attributes.

#### `<BlendFunc>`&nbsp;&nbsp;&nbsp;🔗 [BlendFuncEffect](MemeType.md#blendfunceffect)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `source-blend-function` | int | yes |
| `destination-blend-function` | int | yes |

#### `<Clip>`&nbsp;&nbsp;&nbsp;🔗 [ClipEffect](MemeType.md#clipeffect), [MoveClipEffect](MemeType.md#moveclipeffect)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `x` | float | yes |
| `y` | float | yes |
| `width` | float | yes |
| `height` | float | yes |
| `move-length` | float | no |
| `move-direction` | float | no |

#### `<Color>`&nbsp;&nbsp;&nbsp;🔗 [ColorEffect](MemeType.md#coloreffect), [VariableColorEffect](MemeType.md#variablecoloreffect)

Content: none.

Base attributes, every type has these:

| Attribute | Holds | Required |
|---|---|---|
| `color` | color of numerical expressions | yes |

#### `<HideDisable>`&nbsp;&nbsp;&nbsp;🔗 [HideDisableEffect](MemeType.md#hidedisableeffect)

Content: none. No attributes.

#### `<Move>`&nbsp;&nbsp;&nbsp;🔗 [MoveEffect](MemeType.md#moveeffect)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `move-length` | expression | yes |
| `move-direction` | expression | yes |

#### `<MultiplyColor>`&nbsp;&nbsp;&nbsp;🔗 [BfMultiplyColorEffect](MemeType.md#bfmultiplycoloreffect), [BfMultiplyColorEffect2](MemeType.md#bfmultiplycoloreffect2), [MultiplyColorEffect](MemeType.md#multiplycoloreffect)

Content: none.

Group 1:

| Attribute | Holds | Required |
|---|---|---|
| `color` | color of numerical expressions | yes |

Group 2:

| Attribute | Holds | Required |
|---|---|---|
| `alpha` | numerical expression | yes |

A tag uses the attributes of one group only.

#### `<MultiplyVertexColor>`&nbsp;&nbsp;&nbsp;🔗 [MultiplyVertexColorEffect](MemeType.md#multiplyvertexcoloreffect)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `top-left-color` | color of numbers | yes |
| `top-right-color` | color of numbers | yes |
| `bottom-right-color` | color of numbers | yes |
| `bottom-left-color` | color of numbers | yes |

#### `<Rotate>`&nbsp;&nbsp;&nbsp;🔗 [RotateEffect](MemeType.md#rotateeffect), [RotateAroundCoordinateEffect](MemeType.md#rotatearoundcoordinateeffect)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `start-angle` | numerical expression | yes |
| `angle-multiplier` | numerical expression | yes |
| `x` | numerical expression | no |
| `y` | numerical expression | no |

#### `<SinMove>`&nbsp;&nbsp;&nbsp;🔗 [SinMoveEffect](MemeType.md#sinmoveeffect)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `move-length` | expression | yes |
| `move-direction` | expression | yes |

#### `<VertexColor>`&nbsp;&nbsp;&nbsp;🔗 [VertexColorEffect](MemeType.md#vertexcoloreffect)

Content: none.

| Attribute | Holds | Required |
|---|---|---|
| `top-left-color` | color of numbers | yes |
| `top-right-color` | color of numbers | yes |
| `bottom-right-color` | color of numbers | yes |
| `bottom-left-color` | color of numbers | yes |

### Pointer tags

#### `<DynamicIndex>`&nbsp;&nbsp;&nbsp;🔗 [DynamicIndexPointer](MemeType.md#dynamicindexpointer)

Content: none. No attributes.

### Data calls

#### `Color(...)`&nbsp;&nbsp;&nbsp;🔗 [BfColorData](MemeType.md#bfcolordata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Color | color of numbers |

#### `ConcatenateList(...)`&nbsp;&nbsp;&nbsp;🔗 [ConcatenateListData](MemeType.md#concatenatelistdata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Data list | List |

#### `Data()`&nbsp;&nbsp;&nbsp;🔗 [Data](MemeType.md#data)

No arguments.

#### `Edit()`&nbsp;&nbsp;&nbsp;🔗 [BfEditData](MemeType.md#bfeditdata)

No arguments.

#### `FloatRef()`&nbsp;&nbsp;&nbsp;🔗 [FloatRefData](MemeType.md#floatrefdata)

No arguments.

#### `FocusLocked()`&nbsp;&nbsp;&nbsp;🔗 [FocusLockedData](MemeType.md#focuslockeddata)

No arguments.

#### `IndexCount(...)`&nbsp;&nbsp;&nbsp;🔗 [IndexCountData](MemeType.md#indexcountdata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Data | expression |

#### `ListBox()`&nbsp;&nbsp;&nbsp;🔗 [ListBoxData](MemeType.md#listboxdata)

No arguments.

#### `Locale(...)`&nbsp;&nbsp;&nbsp;🔗 [BfLocaleData](MemeType.md#bflocaledata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Valid | bool expression |

#### `LocaleString(...)`&nbsp;&nbsp;&nbsp;🔗 [BfLocaleStringData](MemeType.md#bflocalestringdata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Locale | expression |
| 2 | Valid | bool expression |
| 3 | String Id | string expression |

#### `LocaleStringInt(...)`&nbsp;&nbsp;&nbsp;🔗 [LocaleStringData](MemeType.md#localestringdata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Int | int |

#### `Logical(...)`&nbsp;&nbsp;&nbsp;🔗 [LogicalData](MemeType.md#logicaldata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Data 1 | expression |
| 2 | Data 2 | expression |

#### `OccupiedVehicle()`&nbsp;&nbsp;&nbsp;🔗 [BfOccupiedVehicleData](MemeType.md#bfoccupiedvehicledata)

No arguments.

#### `Operator(...)`&nbsp;&nbsp;&nbsp;🔗 [OperatorData](MemeType.md#operatordata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Data 1 | expression |
| 2 | Data 2 | expression |

#### `PlayerInputIndex()`&nbsp;&nbsp;&nbsp;🔗 [PlayerInputIndexData](MemeType.md#playerinputindexdata)

No arguments.

#### `PointerX()`&nbsp;&nbsp;&nbsp;🔗 [PointerXData](MemeType.md#pointerxdata)

No arguments.

#### `PointerY()`&nbsp;&nbsp;&nbsp;🔗 [PointerYData](MemeType.md#pointerydata)

No arguments.

#### `StringRef()`&nbsp;&nbsp;&nbsp;🔗 [StringRefData](MemeType.md#stringrefdata)

No arguments.

#### `Toggle(...)`&nbsp;&nbsp;&nbsp;🔗 [ToggleData](MemeType.md#toggledata)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Toggle data | bool expression |
| 2 | Data 1 | numerical expression |
| 3 | Data 2 | numerical expression |

### Style calls

#### `BfStyle(...)`&nbsp;&nbsp;&nbsp;🔗 [BfStyle](MemeType.md#bfstyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `Center(...)`&nbsp;&nbsp;&nbsp;🔗 [BfCenterStyle](MemeType.md#bfcenterstyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `CenterAligned(...)`&nbsp;&nbsp;&nbsp;🔗 [CenterAlignedStyle](MemeType.md#centeralignedstyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `LeftOutline(...)`&nbsp;&nbsp;&nbsp;🔗 [BfLeftOutlineStyle](MemeType.md#bfleftoutlinestyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `Outline(...)`&nbsp;&nbsp;&nbsp;🔗 [BfOutlineStyle](MemeType.md#bfoutlinestyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `RightAligned(...)`&nbsp;&nbsp;&nbsp;🔗 [RightAlignedStyle](MemeType.md#rightalignedstyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `RowDistance(...)`&nbsp;&nbsp;&nbsp;🔗 [RowDistanceStyle](MemeType.md#rowdistancestyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |
| 2 | Row distance | float |

#### `SingleLine(...)`&nbsp;&nbsp;&nbsp;🔗 [SingleLineStyle](MemeType.md#singlelinestyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `SingleLineSize(...)`&nbsp;&nbsp;&nbsp;🔗 [SingleLineSizeStyle](MemeType.md#singlelinesizestyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |
| 2 | Size constant | float |

#### `Size(...)`&nbsp;&nbsp;&nbsp;🔗 [SizeStyle](MemeType.md#sizestyle)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |
| 2 | Size constant | float |

#### `Style(...)`&nbsp;&nbsp;&nbsp;🔗 [Style](MemeType.md#style)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

#### `Style2(...)`&nbsp;&nbsp;&nbsp;🔗 [BfStyle2](MemeType.md#bfstyle2)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Font handle | string |

### Event calls

#### `AnyKey(...)`&nbsp;&nbsp;&nbsp;🔗 [AnyKeyEvent](MemeType.md#anykeyevent)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Input index | int, named by PlayerInput |
| 2 | Event type | int, named by EventType |

#### `Button(...)`&nbsp;&nbsp;&nbsp;🔗 [ButtonEvent](MemeType.md#buttonevent), [ExtendedButtonEvent](MemeType.md#extendedbuttonevent)

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

#### `Event(...)`&nbsp;&nbsp;&nbsp;🔗 [Event](MemeType.md#event)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Input index | int, named by PlayerInput |

#### `Type(...)`&nbsp;&nbsp;&nbsp;🔗 [TypeEvent](MemeType.md#typeevent)

Arguments:

| Argument | Description | Holds |
|---|---|---|
| 1 | Input index | int, named by PlayerInput |
| 2 | Event type | int, named by EventType |

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
