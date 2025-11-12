# Meme type file structure research

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
HideDisableEffect
BfListBoxNode
BfNewListBoxNode
BfListBoxData
ListBoxData
BfTextNode
BfAddSubEffectNode
BfMultiplyColorEffect
BfMultiplyColorEffect2
BfAddSubNextEffectNode
BfStyle
BfCenterStyle
BfStyle2
BfOutlineStyle
BfLeftOutlineStyle
BfSliderNode
BfFixedSliderNode
BfCreditsNode
BfVerticalScrollNode
BfVerticalScrollExNode
BfLocaleNode
BfLocaleData
BfLocaleStringData
	(dice::meme::BfLocaleData got initialized here)
	6C Locale
	6C Valid
	6C String Id
BfButtonNode
BfNavigationButtonNode
BfSelectButtonNode
BfVariablePictureNode
BfTransformNode
BfTransformNodeSize
BfAnimationNode
BfBinkNode
BfCrosshairNode
BfPictureFillNode
BfVariablePictureFillNode
BfVariablePictureFillNode2
BfScrollPictureNode
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
