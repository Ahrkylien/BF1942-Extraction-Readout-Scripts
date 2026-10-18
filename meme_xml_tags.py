"""
The XML tags of the meme format: which type each tag writes, and which field each attribute and the content writes.

The tags are listed by hand in this file, so renaming a field in meme_types.json does not rename a tag. Every field of a
type is either an attribute, the content, or the next node. This is checked when the module loads.

Tags of one category name one type each, unless several types share a tag (see SHARED). A shared tag is read as the type
whose attributes fit: the one that needs the fewest expressions, then the one with the fewest attributes.
"""
import dataclasses
import re

from .meme_file import meme_types

# The default of an attribute that has none: the attribute must be written
REQUIRED = object()
# The content of a CullNode: the nodes inside its if
BODY = "body"
# The default of an object field that holds nothing (a placeholder); the attribute is left out when it is empty
NULL = object()


@dataclasses.dataclass(frozen=True)
class Attribute:
    """An attribute of a tag. fields are the schema positions it writes: one, or four for a color (red, green, blue, alpha)."""
    name: str
    fields: tuple
    enum: str = None       # the table in meme_engine_enums.json that names the numbers of this field
    default: object = REQUIRED


@dataclasses.dataclass(frozen=True)
class Child:
    """
    A child element that writes one field of a tag. The child carries field="name", and the reader finds the field by
    that name. A field with no value is left out.
    """
    name: str
    field: int


@dataclasses.dataclass(frozen=True)
class Compact:
    """
    A tag and the type it writes. content is the schema position of the field the child elements fill, or None.
    children are the named child elements, one for each field that is not in the content.
    For a type of the Data, Style, Event or Function category, the tag is the name of a call and the attributes are its
    arguments, in order.
    """
    tag: str
    type_name: str
    attributes: tuple
    content: int = None
    children: tuple = ()


def attr(name, *fields, enum=None, default=REQUIRED):
    return Attribute(name, fields, enum, default)


COMPACT = [
    # Node tags
    Compact('Action', 'ActionNode', (), content=1),
    Compact('AddSubEffect', 'BfAddSubEffectNode', (
            attr('value', 1),
            attr('end-value', 2),
            attr('start-time', 3),
            attr('start-percentage', 4),
            attr('end-time', 5),
            attr('delay', 6),
            attr('up', 7),
            attr('trigger', 8),
        )),
    Compact('AddSubNextEffect', 'BfAddSubNextEffectNode', (
            attr('value', 1),
            attr('end-value', 2),
            attr('start-time', 3),
            attr('start-percentage', 4),
            attr('end-time', 5),
            attr('delay', 6),
            attr('up', 7),
            attr('trigger', 9),
        ), content=8),
    Compact('Animation', 'BfAnimationNode', (attr('picture-name', 1), attr('frames', 2), attr('start', 3), attr('looping', 4),)),
    Compact('Bink', 'BfBinkNode', (
            attr('bink-filename', 1),
            attr('background-picture', 2),
            attr('fade-time', 3),
            attr('play', 4),
        )),
    Compact('Button', 'BfButtonNode', (attr('picture', 1), attr('mouse-over-picture', 2), attr('width', 4), attr('height', 5),), content=3),
    Compact('Button', 'BfLocalePictureButtonNode', (
            attr('picture', 1),
            attr('mouse-over-picture', 2),
            attr('start-x', 4),
            attr('total-movement', 5),
            attr('width', 6),
            attr('height', 7),
            attr('is-selected', 8),
            attr('current-x', 9),
            attr('picture-name', 10),
            attr('picture-path', 11),
        ), content=3),
    Compact('Button', 'BfNavigationButtonNode', (
            attr('picture', 1),
            attr('mouse-over-picture', 2),
            attr('clicked-picture', 3),
            attr('mouse-over-button', 5),
            attr('index', 6),
            attr('current-mouseover-index', 7),
            attr('current-clicked-index', 8),
            attr('mouse-over-active', 9),
            attr('width', 10),
            attr('height', 11),
        ), content=4),
    Compact('Button', 'BfSelectButtonNode', (
            attr('picture', 1),
            attr('mouse-over-picture', 2),
            attr('clicked-picture', 3),
            attr('index', 5),
            attr('current-clicked-index', 6),
            attr('width', 7),
            attr('height', 8),
        ), content=4),
    Compact('Clip', 'ClipNode', ()),
    Compact('ColorFill', 'BfColorFillNode', (
            attr('picture', 1),
            attr('data', 2),
            attr('maximum-value', 3),
            attr('horizontal-align', 4),
            attr('fill-order', 5),
            attr('color', 6),
            attr('fill-color', 7),
        )),
    Compact('ControlPointGauge', 'BfControlPointGauge', (
            attr('quarter-circle', 1),
            attr('gauge-position', 2),
            attr('owning-team', 3),
            attr('taking-team', 4),
        )),
    Compact('Credits', 'BfCreditsNode', (
            attr('value', 1),
            attr('end-value', 2),
            attr('reset-value', 3),
            attr('time', 4),
            attr('trigger', 5),
        )),
    Compact('Crosshair', 'BfCrosshairNode', (
            attr('radius', 1),
            attr('thickness', 2),
            attr('outline-thickness', 3),
            attr('deviation', 4),
            attr('color', 5),
            attr('outline-color', 6),
        )),
    Compact('CullAction', 'CullActionNode', (attr('event-type', 2), attr('event-data', 3),), content=1),
    Compact('CullEventAction', 'CullEventActionNode', (attr('event', 2),), content=1),
    Compact('CullEventAction', 'CullEventTimeoutActionNode', (attr('event', 2), attr('timeout-time', 3),), content=1),
    Compact('CullVariable', 'CullVariableNode', (attr('variable', 1), attr('data', 2),)),
    Compact('CullVariableAction', 'CullVariableActionNode', (attr('variable', 2),), content=1),
    Compact('CullVariableAndEventAction', 'CullVariableAndEventActionNode', (attr('variable', 2), attr('event', 3),), content=1),
    Compact('Disable', 'DisableNode', (attr('disable-data', 1),)),
    Compact('DragWindow', 'DragWindowNode', (attr('x', 1), attr('y', 2), attr('width', 3), attr('height', 4),), content=5),
    Compact('Edit', 'BfEditNode', (
            attr('font', 1),
            attr('string', 2),
            attr('max-characters', 3),
            attr('editbox-data', 5),
            attr('focus', 6),
        ), content=4),
    Compact('Edit', 'BfEditNodeNew', (
            attr('font', 1),
            attr('string', 2),
            attr('max-characters', 3),
            attr('index', 4),
            attr('max-index', 5),
            attr('current-index', 6),
        )),
    Compact('Edit', 'EditNode', (attr('font', 1), attr('string', 2), attr('max-characters', 3),)),
    Compact('EditInt', 'BfEditNodeInt', (
            attr('font', 1),
            attr('number', 2),
            attr('string', 3),
            attr('min-value', 4),
            attr('max-value', 5),
            attr('editbox-data', 7),
            attr('focus', 8),
        ), content=6),
    Compact('Effect', 'EffectNode', (), content=1),
    Compact('ExtendedFocusToPressedEffect', 'ExtendedFocusToPressedEffectNode', (attr('min-value', 2), attr('max-value', 3),), content=1),
    Compact('ExtendedNormalToFocusEffect', 'ExtendedNormalToFocusEffectNode', (attr('min-value', 2), attr('max-value', 3),), content=1),
    Compact('Focus', 'FocusNode', (attr('focus-x', 1), attr('focus-y', 2),)),
    Compact('FocusEffect', 'FocusEffectNode', (), content=1),
    Compact('FocusToPressedEffect', 'FocusToPressedEffectNode', (), content=1),
    Compact('Gauge', 'BfGaugeNode', (
            attr('color', 0),
            attr('background-color', 1),
            attr('data', 2),
            attr('maximum-value', 3),
            attr('horizontal-align', 4),
        )),
    Compact('Group', 'SplitNode', (), content=1),
    Compact('If', 'CullNode', (attr('condition', 1), attr('in-time', 2, default=0.0), attr('out-time', 3, default=0.0),), content=BODY),
    Compact('ListBox', 'BfNewListBoxNode', (
            attr('font', 2),
            attr('step-sound', 5, default=''),
            attr('select-sound', 6, default=''),
            attr('failed-select-sound', 7, default=''),
            attr('row-height', 8),
            attr('is-selectable', 9, default=True),
            attr('border', 10, default=False),
            attr('background-color', 11, 12, 13, 14),
            attr('scrollbar-width', 15),
            attr('frame-color', 16, 17, 18, 19),
            attr('select-color', 20, 21, 22, 23),
            attr('show-tooltip', 24, default=False),
            attr('scrollbar-offset', 25),
        ), children=(Child('listbox-data', 1), Child('select-action', 3), Child('focus-action', 4))),
    Compact('Locale', 'BfLocaleNode', (attr('locale', 1),)),
    Compact('Name', 'NameNode', ()),
    Compact('NavigateView', 'NavigateViewNode', (attr('font', 1),), content=0),
    Compact('NewCreditsList', 'BfNewCreditsListNode', (
            attr('style', 1),
            attr('heading-style', 2),
            attr('trigger', 3),
            attr('current-position', 4),
            attr('step', 5),
            attr('start-value', 6),
            attr('end-value', 7),
        )),
    Compact('NodeList', 'NodeListNode', (
            attr('index', 2),
            attr('item-height', 3),
            attr('select-sound', 4),
            attr('up-down-sound', 5),
        ), content=1),
    Compact('NormalToFocusEffect', 'NormalToFocusEffectNode', (), content=1),
    Compact('NotFocusEffect', 'NotFocusEffectNode', (), content=1),
    Compact('OccupiedVehicle', 'BfOccupiedVehicleNode', (attr('position', 1), attr('draw-debug-pic', 2), attr('occupied-vehicle', 3),)),
    Compact('Path', 'PathNode', ()),
    Compact('Picture', 'BfPictureFillNode', (
            attr('picture', 1),
            attr('fill-picture', 2),
            attr('data', 3),
            attr('maximum-value', 4),
            attr('horizontal-align', 5),
            attr('fill-order', 6),
        )),
    Compact('Picture', 'BfVariablePictureFillNode', (
            attr('picture', 1),
            attr('fill-picture', 2),
            attr('data', 3),
            attr('maximum-value', 4),
            attr('size', 5),
            attr('horizontal-align', 6),
            attr('fill-order', 7),
        )),
    Compact('Picture', 'PictureNode', (attr('picture', 1),)),
    Compact('Rectangle', 'BfRectangle', (attr('thickness', 1),)),
    Compact('Scale', 'ScaleNode', (attr('width-scale', 1), attr('height-scale', 2),)),
    Compact('ScrollPicture', 'BfScrollPictureNode', (
            attr('scroll-picture', 1),
            attr('data', 2),
            attr('maximum-value', 3),
            attr('y-offset', 4),
            attr('size', 5),
            attr('var-size', 6),
            attr('maintain-value', 7),
            attr('from-bottom', 8),
        )),
    Compact('ShowEffect', 'ShowEffectNode', (), content=1),
    Compact('BfSlider', 'BfFixedSliderNode', (
            attr('data', 2),
            attr('minimum-value', 3),
            attr('maximum-value', 4),
            attr('number-visible', 5),
            attr('interval', 6),
        ), content=1),
    Compact('BfSlider', 'BfSliderNode', (
            attr('data', 2),
            attr('minimum-value', 3),
            attr('maximum-value', 4),
            attr('number-visible', 5),
        ), content=1),
    Compact('Slider', 'SliderNode', (
            attr('data', 2),
            attr('minimum-value', 3),
            attr('maximum-value', 4),
            attr('number-visible', 5),
        ), content=1),
    Compact('StackPath', 'StackPathNode', ()),
    Compact('Sticky', 'StickyNode', (attr('variable', 1), attr('data', 2),)),
    Compact('Text', 'BfTextNode', (attr('string', 1), attr('style', 2), attr('type', 3),)),
    Compact('Text', 'TextNode', (attr('string', 1), attr('style', 2),)),
    Compact('TimeoutAction', 'TimeoutActionNode', (attr('timeout-time', 2),), content=1),
    Compact('Transform', 'BfTransformNode', (attr('x', 1), attr('y', 2), attr('width', 3), attr('height', 4),), content=5),
    Compact('Transform', 'BfTransformNodeSize', (attr('x', 1), attr('y', 2), attr('width', 3), attr('height', 4),), content=5),
    Compact('Transform', 'TransformNode', (attr('x', 1), attr('y', 2), attr('width', 3), attr('height', 4),), content=5),
    Compact('TransitionalEffect', 'TransitionalEffectNode', (), content=1),
    Compact('TransitionalHideEffect', 'TransitionalHideEffectNode', (), content=1),
    Compact('TransitionalShowEffect', 'TransitionalShowEffectNode', (), content=1),
    Compact('Translate', 'TranslateNode', (attr('x', 1), attr('y', 2),)),
    Compact('TriangleButtons', 'BfTriangleButtonsNode', (
            attr('top-triangle-selected', 1),
            attr('bottom-triangle-selected', 2),
            attr('width', 4),
            attr('height', 5),
            attr('selected-team', 6),
        ), content=3),
    Compact('VariableEffect', 'VariableEffectNode', (attr('effect-level', 2),), content=1),
    Compact('VariablePicture', 'BfVariablePictureNode', (attr('picture', 1), attr('redraw', 2),)),
    Compact('VariablePicture', 'VariablePictureNode', (
            attr('first-part', 1),
            attr('middle-part', 2, default=NULL),
            attr('last-part', 3, default=NULL),
        )),
    Compact('Picture', 'BfVariablePictureFillNode2', (
            attr('picture', 1),
            attr('fill-picture', 2),
            attr('data', 3),
            attr('maximum-value', 4),
            attr('size', 5),
            attr('horizontal-align', 6),
            attr('fill-order', 7),
        )),
    Compact('VariableTimeoutAction', 'BfVariableTimeoutActionNode', (attr('timeout-time', 2),), content=1),
    Compact('VariableTimeoutAction', 'BfVariableTimeoutActionNode2', (attr('current-time', 2), attr('timeout-time', 3),), content=1),
    Compact('VerticalScroll', 'BfVerticalScrollNode', (
            attr('text', 1),
            attr('font', 2),
            attr('scroll-speed', 3),
            attr('scroll-speed-multiplier', 4),
            attr('restart-toggle', 5),
        )),
    Compact('VerticalScroll', 'BfVerticalScrollExNode', (
            attr('version', 1),
            attr('text', 2),
            attr('style', 3),
            attr('scroll-speed', 4),
            attr('scroll-speed-multiplier', 5),
            attr('restart-toggle', 6),
        )),
    Compact('Window', 'WindowNode', (attr('x', 1), attr('y', 2), attr('width', 3), attr('height', 4),), content=5),
    Compact('Zoom', 'ZoomNode', (attr('z', 1),)),
    # Action tags
    Compact('ActionList', 'ActionListAction', (), content=0),
    Compact('CallFunction', 'CallFunctionAction', (attr('function', 0),)),
    Compact('CallFunction', 'CallFunctionVariableAction', (attr('function', 0), attr('result-data', 1),)),
    Compact('LastInputIndex', 'LastInputIndexAction', (attr('last-input-index', 0),)),
    Compact('LockPointer', 'LockPointerAction', (attr('input-index-data', 0),)),
    Compact('ModifyVariable', 'ModifyVariableAction', (attr('variable', 0), attr('modify-value', 1), attr('limit-value', 2),)),
    Compact('Navigate', 'NavigateAction', (), content=0),
    Compact('NavigateChild', 'NavigateChildAction', (), content=0),
    Compact('NavigateChildAndRun', 'NavigateChildAndRunAction', (), content=0),
    Compact('NavigateFirstSibling', 'NavigateFirstSiblingAction', (), content=0),
    Compact('NavigateLastSibling', 'NavigateLastSiblingAction', (), content=0),
    Compact('NavigateNextSibling', 'NavigateNextSiblingAction', (), content=0),
    Compact('NavigateParent', 'NavigateParentAction', (), content=0),
    Compact('NavigateParentAndRun', 'NavigateParentAndRunAction', (), content=0),
    Compact('NavigatePreviousSibling', 'NavigatePreviousSiblingAction', (), content=0),
    Compact('NavigateRun', 'NavigateRunAction', (), content=0),
    Compact('NavigateRunAndChild', 'NavigateRunAndChildAction', (), content=0),
    Compact('NavigateSiblingIndex', 'NavigateSiblingIndexAction', (attr('index', 1),), content=0),
    Compact('PopPath', 'PopPathAction', (
            attr('stack-path-node', 0),
            attr('in-time', 1),
            attr('out-time', 2),
            attr('in-wait-time', 3),
            attr('out-wait-time', 4),
            attr('paint-outnode-over-innode', 5),
        )),
    Compact('PushPath', 'PushPathAction', (
            attr('stack-path-node', 0),
            attr('destination-node', 1),
            attr('in-time', 2),
            attr('out-time', 3),
            attr('in-wait-time', 4),
            attr('out-wait-time', 5),
            attr('paint-outnode-over-innode', 6),
        )),
    Compact('RemoveEvent', 'RemoveEventAction', ()),
    Compact('SetFocus', 'SetFocusAction', (attr('x', 0), attr('y', 1),)),
    Compact('SetPath', 'SetPathAction', (
            attr('path-node', 0),
            attr('destination-node', 1),
            attr('in-time', 2),
            attr('out-time', 3),
            attr('in-wait-time', 4),
            attr('out-wait-time', 5),
            attr('paint-outnode-over-innode', 6),
        )),
    Compact('SetString', 'SetStringAction', (attr('variable', 0), attr('value', 1),)),
    Compact('SetVariable', 'SetVariableAction', (attr('variable', 0), attr('value', 1),)),
    Compact('SetVariable', 'SetVariableArrayAction', (attr('variable', 0), attr('value', 1), attr('index', 2),)),
    Compact('SetVariable', 'SetVariableSoftAction', (attr('variable', 0), attr('value', 1), attr('speed', 2),)),
    Compact('SetVariableSine', 'SetVariableSineAction', (attr('variable', 0), attr('value', 1), attr('speed', 2), attr('braking-distance', 3),)),
    Compact('SetVariableSinus', 'SetVariableSinusAction', (attr('variable', 0), attr('value', 1), attr('speed', 2), attr('braking-distance', 3),)),
    Compact('Sound', 'SoundAction', (attr('sound', 0),)),
    Compact('Sound', 'VolumedSoundAction', (attr('sound', 0), attr('volume', 1),)),
    Compact('ToggleVariable', 'ToggleVariableAction', (attr('variable', 0),)),
    Compact('UnlockPointer', 'UnlockPointerAction', ()),
    # Effect tags
    Compact('AlphaFade', 'AlphaFadeEffect', ()),
    Compact('BlendFunc', 'BlendFuncEffect', (attr('source-blend-function', 0), attr('destination-blend-function', 1),)),
    Compact('Clip', 'ClipEffect', (attr('x', 0), attr('y', 1), attr('width', 2), attr('height', 3),)),
    Compact('Clip', 'MoveClipEffect', (
            attr('x', 0),
            attr('y', 1),
            attr('width', 2),
            attr('height', 3),
            attr('move-length', 4),
            attr('move-direction', 5),
        )),
    Compact('Color', 'ColorEffect', (attr('color', 0, 1, 2, 3),)),
    Compact('Color', 'VariableColorEffect', (attr('color', 0, 1, 2, 3),)),
    Compact('HideDisable', 'HideDisableEffect', ()),
    Compact('Move', 'MoveEffect', (attr('move-length', 0), attr('move-direction', 1),)),
    Compact('MultiplyColor', 'BfMultiplyColorEffect', (attr('color', 0, 1, 2, 3),)),
    Compact('MultiplyColor', 'BfMultiplyColorEffect2', (attr('alpha', 0),)),
    Compact('MultiplyColor', 'MultiplyColorEffect', (attr('color', 0, 1, 2, 3),)),
    Compact('MultiplyVertexColor', 'MultiplyVertexColorEffect', (
            attr('top-left-color', 0, 1, 2, 3),
            attr('top-right-color', 4, 5, 6, 7),
            attr('bottom-right-color', 8, 9, 10, 11),
            attr('bottom-left-color', 12, 13, 14, 15),
        )),
    Compact('Rotate', 'RotateAroundCoordinateEffect', (attr('start-angle', 0), attr('angle-multiplier', 1), attr('x', 2), attr('y', 3),)),
    Compact('Rotate', 'RotateEffect', (attr('start-angle', 0), attr('angle-multiplier', 1),)),
    Compact('SinMove', 'SinMoveEffect', (attr('move-length', 0), attr('move-direction', 1),)),
    Compact('VertexColor', 'VertexColorEffect', (
            attr('top-left-color', 0, 1, 2, 3),
            attr('top-right-color', 4, 5, 6, 7),
            attr('bottom-right-color', 8, 9, 10, 11),
            attr('bottom-left-color', 12, 13, 14, 15),
        )),
    # Pointer tags
    Compact('DynamicIndex', 'DynamicIndexPointer', ()),
    # Data calls
    Compact('Color', 'BfColorData', (attr('color', 0, 1, 2, 3),)),
    Compact('ConcatenateList', 'ConcatenateListData', (attr('data-list', 0),)),
    Compact('Data', 'Data', ()),
    Compact('Edit', 'BfEditData', ()),
    Compact('FloatRef', 'FloatRefData', ()),
    Compact('FocusLocked', 'FocusLockedData', ()),
    Compact('IndexCount', 'IndexCountData', (attr('data', 0),)),
    Compact('ListBox', 'ListBoxData', ()),
    Compact('Locale', 'BfLocaleData', (attr('valid', 0),)),
    Compact('LocaleString', 'BfLocaleStringData', (attr('locale', 0), attr('valid', 1), attr('string-id', 2),)),
    Compact('LocaleStringInt', 'LocaleStringData', (attr('id', 0),)),
    Compact('Logical', 'LogicalData', (attr('data-1', 0), attr('data-2', 1),)),
    Compact('OccupiedVehicle', 'BfOccupiedVehicleData', ()),
    Compact('Operator', 'OperatorData', (attr('data-1', 0), attr('data-2', 1),)),
    Compact('PlayerInputIndex', 'PlayerInputIndexData', ()),
    Compact('PointerX', 'PointerXData', ()),
    Compact('PointerY', 'PointerYData', ()),
    Compact('StringRef', 'StringRefData', ()),
    Compact('Toggle', 'ToggleData', (attr('toggle-data', 0), attr('data-1', 1), attr('data-2', 2),)),
    # Style calls
    Compact('BfStyle', 'BfStyle', (attr('font-handle', 0),)),
    Compact('Center', 'BfCenterStyle', (attr('font-handle', 0),)),
    Compact('CenterAligned', 'CenterAlignedStyle', (attr('font-handle', 0),)),
    Compact('LeftOutline', 'BfLeftOutlineStyle', (attr('font-handle', 0),)),
    Compact('Outline', 'BfOutlineStyle', (attr('font-handle', 0),)),
    Compact('RightAligned', 'RightAlignedStyle', (attr('font-handle', 0),)),
    Compact('RowDistance', 'RowDistanceStyle', (attr('font-handle', 0), attr('row-distance', 1),)),
    Compact('SingleLine', 'SingleLineStyle', (attr('font-handle', 0),)),
    Compact('SingleLineSize', 'SingleLineSizeStyle', (attr('font-handle', 0), attr('size-constant', 1),)),
    Compact('Size', 'SizeStyle', (attr('font-handle', 0), attr('size-constant', 1),)),
    Compact('Style', 'Style', (attr('font-handle', 0),)),
    Compact('Style2', 'BfStyle2', (attr('font-handle', 0),)),
    # Event calls
    Compact('AnyKey', 'AnyKeyEvent', (attr('input-index', 0, enum='PlayerInput'), attr('event-type', 1, enum='EventType'),)),
    Compact('Button', 'ButtonEvent', (
            attr('input-index', 0, enum='PlayerInput'),
            attr('event-type', 1, enum='EventType'),
            attr('button-type', 2, enum='ButtonType'),
        )),
    Compact('Event', 'Event', (attr('input-index', 0, enum='PlayerInput'),)),
    Compact('Button', 'ExtendedButtonEvent', (
            attr('input-index', 0, enum='PlayerInput'),
            attr('event-type', 1, enum='EventType'),
            attr('button-type', 2, enum='ButtonType'),
            attr('repeat-count', 3),
        )),
    Compact('Type', 'TypeEvent', (attr('input-index', 0, enum='PlayerInput'), attr('event-type', 1, enum='EventType'),)),
]


CATEGORIES = ("Node", "Action", "Data", "Effect", "Style", "Event", "Function", "Pointer")
ELEMENT_CATEGORIES = ("Node", "Action", "Effect", "Pointer")
TEXT_CATEGORIES = ("Data", "Style", "Event", "Function")
# The fields that can be a child element: the object has no text form, or it is an element
CHILD_ELEMENT_SLOTS = ("Action", "Effect", "Pointer", "Data")
RESERVED_ATTRIBUTES = ("name", "description", "field")
PRIMITIVE_SLOTS = ("Boolean", "Byte", "Int", "TypeIndex", "Float", "PictureString", "FontString", "SoundString", "String", "WideString")
CHILD_SLOTS = ("Node", "Action", "Effect", "Tree", "List", "PathNode")
ENUM_SLOTS = ("TypeIndex", "Byte")


def category(type_name):
    """The category of a type: Node for a type with a next node, otherwise the category its name ends with."""
    schema = meme_types[type_name]
    if schema and schema[0][0] == "NextNode":
        return "Node"
    match = re.fullmatch(r"(.*)(Node|Action|Data|Effect|Style|Event|Function|Pointer)(\d+|[A-Z][a-z]+)?", type_name)
    return match.group(2) if match else None


def _check(compact):
    """Raise if the tag does not describe its type exactly: every field written once, with a value it can hold."""
    where = f"<{compact.tag}> ({compact.type_name})"
    if compact.type_name not in meme_types:
        raise ValueError(f"{where}: unknown type")
    schema = meme_types[compact.type_name]
    written = set()
    for attribute in compact.attributes:
        if attribute.name in RESERVED_ATTRIBUTES:
            raise ValueError(f"{where}: attribute name '{attribute.name}' is reserved")
        slots = [schema[i][0] for i in attribute.fields]
        if len(attribute.fields) == 4 and (len(set(slots)) != 1 or slots[0] not in ("Float", "Data")):
            raise ValueError(f"{where}: color '{attribute.name}' needs four Float or four Data fields")
        if len(attribute.fields) not in (1, 4):
            raise ValueError(f"{where}: attribute '{attribute.name}' writes {len(attribute.fields)} fields")
        for index, slot in zip(attribute.fields, slots):
            if index in written or index >= len(schema) or schema[index][0] == "NextNode":
                raise ValueError(f"{where}: field {index} is written twice, does not exist, or is the next node")
            text_list = slot == "List" and category(compact.type_name) in TEXT_CATEGORIES
            if slot in CHILD_SLOTS and not text_list:
                raise ValueError(f"{where}: attribute '{attribute.name}' writes a {slot} field")
            if attribute.enum and slot not in ENUM_SLOTS:
                raise ValueError(f"{where}: attribute '{attribute.name}' has an enum, but {slot} has no names")
            written.add(index)
        if attribute.default is not REQUIRED and attribute.default is not NULL and not isinstance(attribute.default, (int, float, bool, str)):
            raise ValueError(f"{where}: default of '{attribute.name}' must be a number, a text, a bool or NULL")
    child_names = set()
    for child in compact.children:
        if child.name in child_names or child.name in RESERVED_ATTRIBUTES:
            raise ValueError(f"{where}: child name '{child.name}' is used twice or is reserved")
        child_names.add(child.name)
        if child.field >= len(schema) or child.field in written or schema[child.field][0] not in CHILD_ELEMENT_SLOTS:
            raise ValueError(f"{where}: child '{child.name}' must write a field of an element type that is not written yet")
        if compact.content is not None and compact.content == child.field:
            raise ValueError(f"{where}: child '{child.name}' is also the content")
        written.add(child.field)
    if compact.content is not None:
        if compact.content != BODY and compact.content in written:
            raise ValueError(f"{where}: the content is also an attribute")
        if compact.content == BODY:
            if compact.type_name != "CullNode":
                raise ValueError(f"{where}: only a CullNode has a body")
        else:
            if schema[compact.content][0] not in CHILD_SLOTS:
                raise ValueError(f"{where}: the content must be a child field")
            written.add(compact.content)
    for index, (slot, label) in enumerate(schema):
        if slot != "NextNode" and index not in written:
            raise ValueError(f"{where}: field '{label}' is not written")


def _signature(compact):
    """What a reader can tell two tags of one name apart by: the attribute names, and whether each holds an expression."""
    return frozenset((a.name, meme_types[compact.type_name][a.fields[0]][0] == "Data") for a in compact.attributes)


def _check_table(compacts):
    for compact in compacts:
        _check(compact)
    by_key = {}
    for compact in compacts:
        key = (category(compact.type_name), compact.tag)
        by_key.setdefault(key, []).append(compact)
    for key, members in by_key.items():
        for i, a in enumerate(members):
            for b in members[i + 1:]:
                if _signature(a) == _signature(b):
                    raise ValueError(f"{a.type_name} and {b.type_name} both write <{key[1]}> with the same attributes")
    call_categories = {}
    for c in compacts:
        if category(c.type_name) in TEXT_CATEGORIES:
            call_categories.setdefault(c.tag, set()).add(category(c.type_name))
    duplicates = {tag for tag, found in call_categories.items() if len(found) > 1}
    if duplicates:
        raise ValueError(f"call names used in more than one text category: {sorted(duplicates)}")
    return by_key


BY_KEY = _check_table(COMPACT)
BY_TYPE = {c.type_name: c for c in COMPACT}
