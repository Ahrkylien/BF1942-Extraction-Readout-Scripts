# Parameter Types

## Primitive Types

| Type Name      | Description |
|----|----|
| Byte           | 1-byte value  |
| Float          | 32-bit float |
| Boolean        | Boolean value |
| Int            | 32-bit integer |
| String         | CP-1252 encoded string (preceded by 32 bit length indicator) |
| WideString     | UTF-16 LE encoded string (preceded by 32 bit length indicator) |
| PictureString  | Picture reference - CP-1252 encoded string (preceded by 8 bit length indicator) |
| FontString     | Font reference - CP-1252 encoded string (preceded by 8 bit length indicator) |
| SoundString    | Sound reference - CP-1252 encoded string (preceded by 8 bit length indicator) |
| List           | Node/Data/Action list |
| FunctionIndex  | Function/type reference |

## Complex / Reference Types

| Type Name |
|----------|
| Event |
| Action |
| Data |
| Effect |
| Function |
| PathNameNode |
| Style |
| Tree |
| NodeRef |
| NextNode |



# Nodes

## Node
- NextNode: Next node

## NameNode
- NextNode: Next node

## TransformNode
- NextNode: Next node
- Float: X
- Float: Y
- Float: Width
- Float: Height
- NodeRef: Transformed node

## BfTransformNode
- NextNode: Next node
- Data: X
- Data: Y
- Float: Width
- Float: Height
- NodeRef: Transformed node

## BfTransformNodeSize
- NextNode: Next node
- Float: X
- Float: Y
- Data: Width
- Data: Height
- NodeRef: Transformed node

## TranslateNode
- NextNode: Next node
- Data: X
- Data: Y

## ScaleNode
- NextNode: Next node
- Data: Width scale
- Data: Height scale

## ClipNode
- NextNode: Next node

## ZoomNode
- NextNode: Next node
- Data: Z

## BfListBoxNode
- NextNode: Next node

## BfNewListBoxNode
- NextNode: Next node
- Data: Listbox data
- FontString: Font
- Action: Select action
- Action: Focus action
- SoundString: Step sound
- SoundString: Select sound
- SoundString: Failed select sound
- Float: Row height
- Boolean: IsSelectable
- Boolean: Border or not
- Float: Background color red
- Float: Background color green
- Float: Background color blue
- Float: Background color alpha
- Float: Scrollbar width
- Float: Frame color red
- Float: Frame color green
- Float: Frame color blue
- Float: Frame color alpha
- Float: Select color red
- Float: Select color green
- Float: Select color blue
- Float: Select color alpha
- Boolean: Show tooltip
- Float: Scrollbar offset from border

## TextNode
- NextNode: Next node
- Data: String
- Style: Style

## BfTextNode
- NextNode: Next node
- Data: String
- Style: Style
- Data: Type

## BfSliderNode
- NextNode: Next node
- NodeRef: Cursor node
- Data: Data
- Float: Minimum value
- Float: Maximum value
- Float: Number visible

## BfFixedSliderNode
- NextNode: Next node
- NodeRef: Cursor node
- Data: Data
- Float: Minimum value
- Float: Maximum value
- Float: Number visible
- Float: Interval

## BfCreditsNode
- NextNode: Next node
- Data: Value
- Float: End value
- Float: Reset value
- Float: Time
- Data: Go

## BfVerticalScrollNode
- NextNode: Next node
- Data: Text
- FontString: Font
- Float: Scroll speed
- Data: Scroll speed multiplier
- Data: Restart toggle

## BfVerticalScrollExNode
- NextNode: Next node
- Int: Version <do not edit>
- Data: Text
- Style: Style
- Float: Scroll speed
- Data: Scroll speed multiplier
- Data: Restart toggle

## BfButtonNode
- NextNode: Next node
- PictureString: Picture
- PictureString: Mouse over picture
- Action: Action
- Float: Width
- Float: Height

## BfNavigationButtonNode
- NextNode: Next node
- PictureString: Picture
- PictureString: Mouse over picture
- PictureString: Clicked picture
- Action: Action
- Boolean: MouseOver button
- Int: Index
- Data: Current mouseover index
- Data: Current clicked index
- Data: MouseOver active
- Float: Width
- Float: Height

## BfSelectButtonNode
- NextNode: Next node
- PictureString: Picture
- PictureString: Mouse over picture
- PictureString: Clicked picture
- Action: Action
- Int: Index
- Data: Current clicked index
- Float: Width
- Float: Height

## BfAnimationNode
- NextNode: Next node
- Data: Picture name
- Int: Frames
- Boolean: Start
- Boolean: Looping

## BfBinkNode
- NextNode: Next node
- Data: Bink filename
- Data: Background picture
- Float: Fade time
- Data: Play

## BfCrosshairNode
- NextNode: Next node
- Data: Radius
- Data: Thickness
- Data: Outline thickness
- Data: Deviation
- Data: Color
- Data: Outline

## PictureNode
- NextNode: Next node
- PictureString: Picture

## VariablePictureNode
- NextNode: Next node
- Data: First part
- Data: Middle part
- Data: Last part

## BfVariablePictureNode
- NextNode: Next node
- Data: Picture str
- Data: Redraw

## BfPictureFillNode
- NextNode: Next node
- PictureString: Picture
- PictureString: Fill picture
- Data: Data
- Data: Maximum value
- Boolean: Horizontal align
- Boolean: Fill order

## BfVariablePictureFillNode
- NextNode: Next node
- PictureString: Picture
- PictureString: Fill picture
- Data: Data
- Data: Maximum value
- Int: Size
- Boolean: Horizontal align
- Boolean: Fill order

## BfVariablePictureFillNode2
- NextNode: Next node
- Data: Picture
- Data: Fill picture
- Data: Data
- Data: Maximum value
- Data: Size
- Boolean: Horizontal align
- Boolean: Fill order

## BfScrollPictureNode
- NextNode: Next node
- PictureString: Scroll picture
- Data: Data
- Data: Maximum value
- Int: Y offset
- Int: Size
- Data: Var size
- Data: Maintain value
- Boolean: From bottom

## BfOccupiedVehicleNode
- NextNode: Next node
- Int: Position
- Boolean: Draw debug pic
- Data: BfOccupiedVehicleData

## BfColorFillNode
- NextNode: Next node
- PictureString: Picture
- Data: Data
- Data: Maximum value
- Boolean: Horizontal align
- Boolean: Fill order
- Data: Color
- Data: Fill color

## EditNode
- NextNode: Next node
- FontString: Font
- Data: String
- Int: Max characters (-1 = no limit)

## BfEditNode
- NextNode: Next node
- FontString: Font
- Data: String
- Int: Max characters (-1 = no limit)
- Action: Select action
- Data: Editbox data
- Boolean: Focus

## BfEditNodeInt
- NextNode: Next node
- FontString: Font
- Data: Int
- Data: String
- Int: Min value (-1 = no limit)
- Int: Max value (-1 = no limit)
- Action: Select action
- Data: Editbox data
- Boolean: Focus

## BfEditNodeNew
- NextNode: Next node
- FontString: Font
- Data: String
- Int: Max characters (-1 = no limit)
- Int: Index
- Int: Max index
- Data: Current index

## SliderNode
- NextNode: Next node
- NodeRef: Cursor node
- Data: Data
- Float: Minimum value
- Float: Maximum value
- Float: Number visible

## BfRectangle
- NextNode: Next node
- Float: Thickness

## BfLocaleNode
- NextNode: Next node
- Data: Locale

## ActionNode
- NextNode: Next node
- Action: Action

## BfVariableTimeoutActionNode
- NextNode: Next node
- Action: Action
- Data: Timeout time

## BfVariableTimeoutActionNode2
- NextNode: Next node
- Action: Action
- Data: Current time
- Data: Timeout time

## IfElseEventActionNode
- NextNode: Next node
- Action: Action
- Data: Variable
- Action: Else action
- Event: Event

## TimeoutActionNode
- NextNode: Next node
- Action: Action
- Float: Timeout time

## CullActionNode
- NextNode: Next node
- Action: Action
- Byte: Event type (OBS; DO NOT USE!, OLD CLASS)
- Int: Event data (OBS; DO NOT USE!, OLD CLASS)

## CullEventActionNode
- NextNode: Next node
- Action: Action
- Event: Event

## CullVariableActionNode
- NextNode: Next node
- Action: Action
- Data: Variable

## CullVariableAndEventActionNode
- NextNode: Next node
- Action: Action
- Data: Variable
- Event: Event

## NodeListNode
- NextNode: Next node
- List: Node list
- Data: Index
- Float: Item height
- SoundString: Select sound
- SoundString: Up down sound

## PathNode
- NextNode: Next node

## StackPathNode
- NextNode: Next node

## EffectNode
- NextNode: Next node
- Effect: Effect

## VariableEffectNode
- NextNode: Next node
- Effect: Effect
- Data: Effect level

## ShowEffectNode
- NextNode: Next node
- Effect: Effect

## TransitionalEffectNode
- NextNode: Next node
- Effect: Effect

## TransitionalShowEffectNode
- NextNode: Next node
- Effect: Effect

## TransitionalHideEffectNode
- NextNode: Next node
- Effect: Effect

## NormalToFocusEffectNode
- NextNode: Next node
- Effect: Effect

## FocusEffectNode
- NextNode: Next node
- Effect: Effect

## NotFocusEffectNode
- NextNode: Next node
- Effect: Effect

## ExtendedNormalToFocusEffectNode
- NextNode: Next node
- Effect: Effect
- Float: Min value
- Float: Max value

## FocusToPressedEffectNode
- NextNode: Next node
- Effect: Effect

## ExtendedFocusToPressedEffectNode
- NextNode: Next node
- Effect: Effect
- Float: Min value
- Float: Max value

## BfAddSubEffectNode
- NextNode: Next node
- Data: Value
- Data: End value
- Data: Start time
- Data: Start percentage
- Data: End time
- Data: Delay
- Data: Up
- Data: Go

## BfAddSubNextEffectNode
- NextNode: Next node
- Data: Value
- Data: End value
- Data: Start time
- Data: Start percentage
- Data: End time
- Data: Delay
- Data: Up
- Action: Next action
- Data: Go

## CullNode
- NextNode: Next node
- Data: Data
- Float: In time
- Float: Out time

## SplitNode
- NextNode: Next node
- NodeRef: Split node

## FocusNode
- NextNode: Next node
- Data: Focus X
- Data: Focus Y

## DisableNode
- NextNode: Next node
- Data: Disable data

## CullVariableNode
- NextNode: Next node
- Data: Variable
- Data: Data

## StickyNode
- NextNode: Next node
- Data: Variable
- Data: Data

## WindowNode
- NextNode: Next node
- Float: X
- Float: Y
- Float: Width
- Float: Height
- NodeRef: Transformed node

## DragWindowNode
- NextNode: Next node
- Float: X
- Float: Y
- Float: Width
- Float: Height
- NodeRef: Transformed node



# Actions

## Action
_No parameters_

## SoundAction
- SoundString: Sound

## VolumedSoundAction
- SoundString: Sound
- Float: Volume (0-1)

## SetVariableAction
- Data: Variable
- Data: Data

## SetStringAction
- Data: Variable
- Data: Data

## ToggleVariableAction
- Data: Variable

## ModifyVariableAction
- Data: Variable
- Float: Modify value
- Float: Limit value

## SetVariableSoftAction
- Data: Variable
- Data: Data
- Float: Speed

## SetVariableSineAction
- Data: Variable
- Data: Data
- Float: Speed
- Float: Braking distance

## SetVariableSinusAction
- Data: Variable
- Data: Data
- Float: Speed
- Float: Braking distance

## SetVariableArrayAction
- Data: Variable
- Data: Data
- Data: Index

## LastInputIndexAction
- Data: Last input index

## LockPointerAction
- Data: Input index data

## ActionListAction
- List: Action list

## NavigateAction
- Tree: Action tree

## NavigateNextSiblingAction
- Tree: Action tree

## NavigatePreviousSiblingAction
- Tree: Action tree

## NavigateParentAction
- Tree: Action tree

## NavigateChildAction
- Tree: Action tree

## NavigateRunAction
- Tree: Action tree

## NavigateRunAndChildAction
- Tree: Action tree

## NavigateChildAndRunAction
- Tree: Action tree

## NavigateParentAndRunAction
- Tree: Action tree

## NavigateFirstSiblingAction
- Tree: Action tree

## NavigateLastSiblingAction
- Tree: Action tree

## NavigateSiblingIndexAction
- Tree: Action tree
- Int: Index

## SetPathAction
- PathNameNode: Path node
- PathNameNode: Destination node
- Float: In time
- Float: Out time
- Float: In wait time
- Float: Out wait time
- Boolean: Paint outnode over innode

## PushPathAction
- PathNameNode: Stack path node
- PathNameNode: Destination node
- Float: In time
- Float: Out time
- Float: In wait time
- Float: Out wait time
- Boolean: Paint outnode over innode

## PopPathAction
- PathNode: Stack path node
- Float: In time
- Float: Out time
- Float: In wait time
- Float: Out wait time
- Boolean: Paint outnode over innode

## SplitAction
- Action: Action 1
- Action: Action 2

## SetFocusAction
- Data: X
- Data: Y

## CullEventTimeoutActionNode
- NextNode: Next node
- Action: Action
- Event: Event
- Float: Timeout time

## CallFunctionAction
- Function: Function

## CallFunctionVariableAction
- Function: Function
- Data: Result data

## UnlockPointerAction
_No parameters_

## RemoveEventAction
_No parameters_



# Data Objects

## Data
_No parameters_

## BoolData
- Boolean: Value <do not edit>

## IntData
- Int: Value <do not edit>

## FloatData
- Float: Value <do not edit>

## StringData
- String: String <do not edit>

## WstringData
- WideString: Wstring <do not edit>

## FloatRefData
_No parameters_

## StringRefData
_No parameters_

## BfLocaleData
- Data: Valid

## LocaleStringData
- Int: Int

## BfLocaleStringData
- Data: Locale
- Data: Valid
- Data: String Id

## DataListData
- List: Data list

## IndexDataData
- Data: Data
- Data: Index

## IndexCountData
- Data: Data

## ConcatenateListData
- List: Data list

## BfColorData
- Float: Red
- Float: Green
- Float: Blue
- Float: Alpha

## ListBoxData
_No parameters_

## BfListBoxData
- Action: Create new action
- Data: Create new string
- Data: Profile name

## BfOccupiedVehicleData
_No parameters_

## BfEditData
_No parameters_

## PointerXData
_No parameters_

## PointerYData
_No parameters_

## PlayerInputIndexData
_No parameters_

## FocusLockedData
_No parameters_

## LogicalData
- Data: Data 1
- Data: Data 2

## EqualData
- Data: Data 1
- Data: Data 2

## NotEqualData
- Data: Data 1
- Data: Data 2

## LessEqualData
- Data: Data 1
- Data: Data 2

## LessData
- Data: Data 1
- Data: Data 2

## OrData
- Data: Data 1
- Data: Data 2

## AndData
- Data: Data 1
- Data: Data 2

## ExclusiveOrData
- Data: Data 1
- Data: Data 2

## NotData
- Data: Data

## OperatorData
- Data: Data 1
- Data: Data 2

## AddData
- Data: Data 1
- Data: Data 2

## SubData
- Data: Data 1
- Data: Data 2

## MulData
- Data: Data 1
- Data: Data 2

## DivData
- Data: Data 1
- Data: Data 2



# Effects

## Effect
_No parameters_

## ClipEffect
- Float: X
- Float: Y
- Float: Width
- Float: Height

## MoveClipEffect
- Float: X
- Float: Y
- Float: Width
- Float: Height
- Float: Move length
- Float: Move direction

## BlendFuncEffect
- FunctionIndex: Source blend func
- FunctionIndex: Destination blend func

## MoveEffect
- Data: Move length
- Data: Move direction

## SinMoveEffect
- Data: Move length
- Data: Move direction

## SplitEffect
- Effect: Effect 1
- Effect: Effect 2

## ColorEffect
- Float: Red
- Float: Green
- Float: Blue
- Float: Alpha

## MultiplyColorEffect
- Float: Red
- Float: Green
- Float: Blue
- Float: Alpha

## AlphaFadeEffect
_No parameters_

## VertexColorEffect
- Float: Top left red
- Float: Top left green
- Float: Top left blue
- Float: Top left alpha
- Float: Top right red
- Float: Top right green
- Float: Top right blue
- Float: Top right alpha
- Float: Bottom right red
- Float: Bottom right green
- Float: Bottom right blue
- Float: Bottom right alpha
- Float: Bottom left red
- Float: Bottom left green
- Float: Bottom left blue
- Float: Bottom left alpha

## MultiplyVertexColorEffect
- Float: Top left red
- Float: Top left green
- Float: Top left blue
- Float: Top left alpha
- Float: Top right red
- Float: Top right green
- Float: Top right blue
- Float: Top right alpha
- Float: Bottom right red
- Float: Bottom right green
- Float: Bottom right blue
- Float: Bottom right alpha
- Float: Bottom left red
- Float: Bottom left green
- Float: Bottom left blue
- Float: Bottom left alpha

## RotateEffect
- Data: Start angle
- Data: Angle multiplier

## RotateAroundCoordinateEffect
- Data: Start angle
- Data: Angle multiplier
- Data: X
- Data: Y

## BfMultiplyColorEffect
- Data: Red
- Data: Green
- Data: Blue
- Data: Alpha

## BfMultiplyColorEffect2
- Data: Alpha

## VariableColorEffect
- Data: Red
- Data: Green
- Data: Blue
- Data: Alpha

## HideDisableEffect
_No parameters_



# Styles

## Style
- FontString: Font handle

## BfStyle
- FontString: Font handle

## BfStyle2
- FontString: Font handle

## CenterAlignedStyle
- FontString: Font handle

## BfCenterStyle
- FontString: Font handle

## RightAlignedStyle
- FontString: Font handle

## SingleLineStyle
- FontString: Font handle

## SizeStyle
- FontString: Font handle
- Float: Size constant

## SingleLineSizeStyle
- FontString: Font handle
- Float: Size constant

## RowDistanceStyle
- FontString: Font handle
- Float: Row distance

## BfOutlineStyle
- FontString: Font handle

## BfLeftOutlineStyle
- FontString: Font handle



# Events

## Event
- Byte: Input index (0 == all indexes)

## TypeEvent
- Byte: Input index (0 == all indexes)
- FunctionRef: Event type

## ButtonEvent
- Byte: Input index (0 == all indexes)
- FunctionRef: Event type
- FunctionRef: Button type

## ExtendedButtonEvent
- Byte: Input index (0 == all indexes)
- FunctionRef: Event type
- FunctionRef: Button type
- Int: Repeat count

## AnyKeyEvent
- Byte: Input index (0 == all indexes)
- FunctionRef: Event type



# Functions

## Function
_No parameters_

## ActionFunction
- Action: Action



# Pointers

## Pointer
_No parameters_

## DynamicIndexPointer
_No parameters_



# Core/Misc Types

## Object
_No parameters_

## System
_No parameters_

## NavigateViewNode
- Tree: Navigate tree
- FontString: Font

## BfGaugeNode
- Data: Color
- Data: Background color
- Data: Data
- Data: Maximum value
- Boolean: Horizontal align

```
