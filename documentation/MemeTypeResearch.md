# Meme type file structure research

## DMeme.exe and CMeme.exe
Dice (I assume) made two command-line tools for Meme type files. One for decompiling and one for compiling.
I know this because I found a file called [LoadMenu.mms](LoadMenu.mms), which is the decompiled Meme file.
Alongside that file I found this bat script:
```bat
CMeme.exe "D:\modding\LoadMenu.mms"
CMeme.exe "D:\modding\InGame.mms"
CMeme.exe "D:\modding\CreditsMenu.mms"

move LoadMenu menu\
move CreditsMenu menu\
move InGame menu\

rfaPack.exe menu menu menu.rfa
```
Sadly the two tools seem lost to time.

## Thoughts
- Object might be the base class
- Data, Node, Action seem Abstract classes
- Event seems like an Abstract class but it has fields

## Interesting strings
```
Meme: DEPRECATED: CullActionNode
Meme: Error: Adding named object to nodetree (%s %s)
Meme: Error: Cannot register null pointers
Meme: Error: Cannot register objects without name
Meme: Error: Loading class ',27h,'%s',27h,' need to be inherited from object
Meme: Info: Trying old format "%s"
Meme: Warning: DEPRECATED, SetVariableSinusAction should be replaced with SetVariableSineAction
Meme: Warning: ShowEffectNode is deprecated and will be removed, use TransitionalEffectNode instead!
MemeFile 2.0
```

## Parse Methods
```
00947288 (but this seems only one of them...)

04 ClassIStream?
08 base type??


1C Byte
20
24
28
2c
30
34 Float
38 Boolean
3C Int32
40 some string type (seems to be StringData or String32)
44 Wstring (in: Tree)
48
4C
50 FontString
54 SoundString
58 ?Node list?
5C Blend function?

68 Action
6C Data
70 Effect

7C Style

80 some form of file/image

88 Next Node
```


## Types
```
VariableColorEffect
	6C Red
	6C Green
	6C Blue
	6C Alpha
VariablePictureNode
	~Next node~
	6C First part
	6C Middle part
	6C Last part
CullVariableNode
	~Next node~
	6C Variable
	6C Data
LocaleStringData
	40 String <do not edit>
NodeListNode
	~Next node~
	58 Node list
	6C Index
	34 Item height
	54 Select sound
	54 Up down sound
ScaleNode
	~Next node~
	6C Width scale
	6C Height scale
HideDisableEffect
	(No parameters)
BfListBoxNode
	~Next node~
BfNewListBoxNode
	~Next node~
	(dice::meme::BfLocaleData got initialized here)
	6C Listbox data
	50 Font
	68 Select action
	68 Focus action
	54 Step sound
	54 Select sound
	54 Failed select sound
	34 Row height
	38 IsSelectable
	38 Border or not
	34 Background color red
	34 Background color green
	34 Background color blue
	34 Background color alpha
	34 Scrollbar width
	34 Frame color red
	34 Frame color green
	34 Frame color blue
	34 Frame color alpha
	34 Select color red
	34 Select color green
	34 Select color blue
	34 Select color alpha
	38 Show tooltip
	34 Scrollbar offset from border
	80 Outlands_2.dif
	80 Outlands_2_inv.dif
BfListBoxData
	68 Create new action
	6C Create new string
	6C Profile name
ListBoxData
	(No parameters)
BfTextNode
	~Next node~
	6C String
	7C Style
	6C Type
BfAddSubEffectNode
	~Next node~
	6C Value
	6C End value
	6C Start time
	6C Start percentage
	6C End time
	6C Delay
	6C Up
	6C Go
BfMultiplyColorEffect
	6C Red
	6C Green
	6C Blue
	6C Alpha
BfMultiplyColorEffect2
	6C Alpha
BfAddSubNextEffectNode
	~Next node~
	6C Value
	6C End value
	6C Start time
	6C Start percentage
	6C End time
	6C Delay
	6C Up
	68 Next action
	6C Go
BfStyle
	50 Font handle
BfCenterStyle
	50 Font handle
BfStyle2
	50 Font handle
BfOutlineStyle
	50 Font handle
BfLeftOutlineStyle
	50 Font handle
BfSliderNode
	~Next node~
	84 Cursor node
	6C Data
	34 Minimum value
	34 Maximum value
	34 Number visible
BfFixedSliderNode
	~Next node~
	84 Cursor node
	6C Data
	34 Minimum value
	34 Maximum value
	34 Number visible
	34 Interval
BfCreditsNode
	~Next node~
	6C Value
	34 End value
	34 Reset value
	34 Time
	6C Go
BfVerticalScrollNode
	~Next node~
	6C Text
	50 Font
	34 Scroll speed
	6C Scroll speed multiplier
	6C Restart toggle
BfVerticalScrollExNode
	~Next node~
	3C Version <do not edit>
	6C Text
	7C Style
	34 Scroll speed
	6C Scroll speed multiplier
	6C Restart toggle
BfLocaleNode
	~Next node~
	(dice::meme::BfLocaleData got initialized here)
	6C Locale
BfLocaleData
	6C Valid
BfLocaleStringData
	(dice::meme::BfLocaleData got initialized here)
	6C Locale
	6C Valid
	6C String Id
BfButtonNode
	~Next node~
	4C Picture
	4C Mouse over picture
	68 Action
	34 Width
	34 Height
BfNavigationButtonNode
	~Next node~
	4C Picture
	4C Mouse over picture
	4C Clicked picture
	68 Action
	38 MouseOver button
	3C Index
	6C Current mouseover index
	6C Current clicked index
	6C MouseOver active
	34 Width
	34 Height
BfSelectButtonNode
	~Next node~
	4C Picture
	4C Mouse over picture
	4C Clicked picture
	68 Action
	3C Index
	6C Current clicked index
	34 Width
	34 Height
BfVariablePictureNode
	~Next node~
	6C picture str
	6C redraw
BfTransformNode
	~Next node~
	6C X
	6C Y
	34 Width
	34 Height
	84 Transformed node
BfTransformNodeSize
	~Next node~
	34 X
	34 Y
	6C Width
	6C Height
	84 Transformed node
BfAnimationNode
	~Next node~
	6C Picture name (without extension)
	3C Frames
	38 Start
	38 Looping
BfBinkNode
	~Next node~
	6C Bink filename (without extension)
	6C Background picture
	34 Fade time
	6C Play
BfCrosshairNode
	~Next node~
	6C Radius
	6C Thickness
	6C outline thickness
	6C Deviation
	(dice::meme::BfColorData got initialized here)
	6C color
	(dice::meme::BfColorData got initialized here)
	6C outline
BfPictureFillNode
	~Next node~
	4C Picture
	4C Fill picture
	6C Data
	6C Maximum value
	38 Horizontal align
	38 Fill order
BfVariablePictureFillNode
	~Next node~
	4C Picture
	4C Fill picture
	6C Data
	6C Maximum value
	3C Size
	38 Horizontal align
	38 Fill order
BfVariablePictureFillNode2
	~Next node~
	6C Picture
	6C Fill picture
	6C Data
	6C Maximum value
	6C Size
	38 Horizontal align
	38 Fill order
BfScrollPictureNode
	~Next node~
	4C Scroll picture
	6C Data
	6C Maximum value
	3C Y offset
	3C Size
	6C Var size
	6C Maintain value
	38 From bottom
BfVariableTimeoutActionNode
BfVariableTimeoutActionNode2
BfOccupiedVehicleNode
BfOccupiedVehicleData
BfColorFillNode
BfColorData
BfGaugeNode
BfEditNode
	~Next node~
	50 Font
	6C String
	3C Max characters(-1 = no limit)
	68 Select action
	(dice::meme::BfEditData got initialized here)
	6C Editbox data
	38 Focus
BfEditNodeInt
BfEditData
BfEditNodeNew
ClipNode
PointerXData
	(No parameters)
PointerYData
	(No parameters)
OperatorData
AddData
SubData
MulData
DivData
ButtonEvent
ExtendedButtonEvent
AnyKeyEvent
TypeEvent
ActionFunction
ZoomNode
DisableNode
RotateEffect
RotateAroundCoordinateEffect
EditNode
BfRectangle
BoolData
ActionNode
IfElseEventActionNode
TimeoutActionNode
CullActionNode
CullEventActionNode
CullVariableActionNode
CullVariableAndEventActionNode
CullEventTimeoutActionNode
CallFunctionAction
CallFunctionVariableAction
FloatData
FloatRefData
SizeStyle
SingleLineSizeStyle
RowDistanceStyle
ColorEffect
MultiplyColorEffect
AlphaFadeEffect
VertexColorEffect
MultiplyVertexColorEffect
PathNode
StackPathNode
SetPathAction
PushPathAction
PopPathAction
EffectNode
VariableEffectNode
ShowEffectNode
TransitionalEffectNode
TransitionalShowEffectNode
TransitionalHideEffectNode
NormalToFocusEffectNode
	~Next node~
	70 Effect
FocusEffectNode
NotFocusEffectNode
ExtendedNormalToFocusEffectNode
FocusToPressedEffectNode
ExtendedFocusToPressedEffectNode
SetVariableAction
SetStringAction
ToggleVariableAction
ModifyVariableAction
SetVariableSoftAction
SetVariableSineAction
SetVariableSinusAction
SetVariableArrayAction
TransformNode
TranslateNode
IntData
StringData
	40 String <do not edit>
StringRefData
WstringData
	44 Wstring <do not edit>
TextNode
SliderNode
SplitNode
PictureNode
Data
System
Node
	~Next node~
NameNode
	~Next node~ (but not inherited from Node)
Pointer
	(No parameters)
Object
	(No parameters)
Effect
	(No parameters)
ClipEffect
	34 X
	34 Y
	34 Width
	34 Height
MoveClipEffect
	34 X
	34 Y
	34 Width
	34 Height
	34 Move length
	34 Move direction
BlendFuncEffect
	5C Source blend func
	5C Destination blend func
LastInputIndexAction
RightAlignedStyle
LogicalData
EqualData
NotEqualData
LessEqualData
LessData
OrData
AndData
ExclusiveOrData
NotData
DataListData
IndexDataData
IndexCountData
ConcatenateListData
SoundAction
	54 Sound
VolumedSoundAction
CullNode
	~Next node~
	6C Data
	34 In time
	34 Out time
SplitEffect
	70 Effect 1
	70 Effect 2
NavigateViewNode
ActionListAction
NavigateAction
NavigateNextSiblingAction
NavigatePreviousSiblingAction
NavigateParentAction
NavigateChildAction
NavigateRunAction
NavigateRunAndChildAction
NavigateChildAndRunAction
NavigateParentAndRunAction
NavigateFirstSiblingAction
NavigateLastSiblingAction
NavigateSiblingIndexAction
SplitAction
SetFocusAction
WindowNode
DragWindowNode
Style
SingleLineStyle
StickyNode
MoveEffect
SinMoveEffect
Function
	(No parameters)
Action
	(No parameters)
FocusNode
	~Next node~
	6C Focus X
	6C Focus Y
RemoveEventAction
	(No parameters)
CenterAlignedStyle
	50 Font handle
FocusLockedData
OStream
DynamicIndexPointer
LockPointerAction
UnlockPointerAction
PlayerInputIndexData
IStream
Event
	1C Input index (0 == all indexes)
ClassIStream
NavigateTree
Tree
	(Info below is from 0x34, not 0x30)
	38 Bool
	44
	34
	.. some fancy recursive stuff
```

## Unused (Vietnam? old binary?)
```C
struct dice::meme::BfScrollPictureNode2
{
	dice::meme::Node	"Next node";
	String8	"Scroll picture";
	dice::meme::Data	"Data";
	dice::meme::Data	"Maximum value";
	Int32	"Y offset";
	Int32	"Size";
	dice::meme::Data	"Var size";
	dice::meme::Data	"Maintain value";
	Boolean	"From top";
};
struct dice::meme::BfTriangleButtonsNode
{	
	dice::meme::Node	"Next node";
	String8	"Picture A";
	String8	"Picture B";
	dice::meme::Action	"Action";
	Float	"Width";
	Float	"Height";
	dice::meme::Data	"Clicked Index?";
};
struct dice::meme::BfControlPointGauge
{
	dice::meme::Node	"Next node";
	String8	"Picture";
	dice::meme::Data	"unkData_A";
	dice::meme::Data	"unkData_B";	
	dice::meme::Data	"unkData_C";
};
struct dice::meme::BfLocalePictureButtonNode
{
	dice::meme::Node	"Next node";
	Byte	"Unk1";
	Byte	"Unk2";
	dice::meme::Node	"Action";
	Float "9.0";
	Float "32.0";
	Float "100.0";
	Float "36.0";

	dice::meme::Node	"BoolData 0";
	dice::meme::Node	"Float Data 9.0";
	dice::meme::Node	"options.tga";
	dice::meme::Node	"Main/Buttons/";
};
struct dice::meme::BfNewCreditsListNode
{
	dice::meme::Node	"Next node";

	dice::meme::Node	"BfStyle";
	dice::meme::Node	"RightAlignedStyle";
	dice::meme::Node	"BoolData 1";

	dice::meme::Node	"FloatData";
	dice::meme::Node	"FloatData";
	dice::meme::Node	"FloatData";
	dice::meme::Node	"FloatData";
};
```
