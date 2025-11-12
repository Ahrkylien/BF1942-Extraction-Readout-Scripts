#pragma description BF1942 Meme Type

#include "std/mem.pat"
#include "std/sys.pat"
#include "std/string.pat"

#pragma endian little
#pragma eval_depth -1

struct string_8bit_length {
    u8 string_length;
    char string_value[string_length];
};

struct String8 {
    u8 string_length;
    char string_value[string_length];
};

struct FontString : String8 {

};

struct SoundString {
    std::warning("SoundString");
    return;
};

struct Wstring {
    std::warning("Wstring");
    return;
};


struct Header {
    string_8bit_length strings[while(std::mem::read_unsigned($, 1) != 0x00)];
    u8 header_termination;
};

Header header @ 0x00;

using Reference;

struct Node {
    Reference next_node;
};





struct CallFunctionAction {
    Reference field_0;
}[[name("CallFunctionAction")]];

struct ModifyVariableAction {
    Reference Variable;
    float Modify_value;
    float Limit_value;
}[[name("ModifyVariableAction")]];

struct SetPathAction {
    Reference Path_node;
    Reference Destination_node;
    float In_time;
    float Out_time;
    float In_wait_time;
    float Out_wait_time;
    bool Paint_outnode_over_innode;
}[[name("SetPathAction")]];

struct SetStringAction {
    Reference Variable;
    Reference Data;
}[[name("SetStringAction")]];

struct SetVariableAction {
    Reference Variable;
    Reference Data;
}[[name("SetVariableAction")]];

struct SplitAction {
    Reference Action_1;
    Reference Action_2;
}[[name("SplitAction")]];

struct ToggleVariableAction {
    Reference Variable;
}[[name("ToggleVariableAction")]];

struct BfColorData {
    float Red;
    float Green;
    float Blue;
    float Alpha;
}[[name("BfColorData")]];

struct BfLocaleData {
    Reference Valid;
}[[name("BfLocaleData")]];

struct BfLocaleStringData {
    Reference Locale;
    Reference Valid;
    Reference String_Id;
}[[name("BfLocaleStringData")]];

struct BoolData {
    bool Value;
}[[name("BoolData")]];

struct FloatData {
    float Value;
}[[name("FloatData")]];

struct IndexDataData {
    Reference Data;
    Reference Index;
}[[name("IndexDataData")]];

struct IntData {
    s32 Value;
}[[name("IntData")]];

struct BfListBoxData {
    Reference Create_new_action;
    Reference Create_new_string;
    Reference Profile_name;
}[[name("BfListBoxData")]];

struct LogicalData {
    Reference Data_1;
    Reference Data_2;
}[[name("LogicalData")]];

struct AndData {
    Reference Data_1;
    Reference Data_2;
}[[name("AndData")]];

struct EqualData {
    Reference Data_1;
    Reference Data_2;
}[[name("EqualData")]];

struct ExclusiveOrData {
    Reference Data_1;
    Reference Data_2;
}[[name("ExclusiveOrData")]];

struct LessData {
    Reference Data_1;
    Reference Data_2;
}[[name("LessData")]];

struct LessEqualData {
    Reference Data_1;
    Reference Data_2;
}[[name("LessEqualData")]];

struct NotData {
    Reference Data;
}[[name("NotData")]];

struct NotEqualData {
    Reference Data_1;
    Reference Data_2;
}[[name("NotEqualData")]];

struct OrData {
    Reference Data_1;
    Reference Data_2;
}[[name("OrData")]];

struct OperatorData {
    Reference Data_1;
    Reference Data_2;
}[[name("OperatorData")]];

struct AddData {
    Reference Data_1;
    Reference Data_2;
}[[name("AddData")]];

struct DivData {
    Reference Data_1;
    Reference Data_2;
}[[name("DivData")]];

struct MulData {
    Reference Data_1;
    Reference Data_2;
}[[name("MulData")]];

struct SubData {
    Reference Data_1;
    Reference Data_2;
}[[name("SubData")]];

struct StringData {
    u32 Length;
    char Value[Length];
}[[name("StringData")]];

struct LocaleStringData {
    s32 Int;
}[[name("LocaleStringData")]];

struct WstringData {
    Wstring Wstring;
}[[name("WstringData")]];

struct ColorEffect {
    float Red;
    float Green;
    float Blue;
    float Alpha;
}[[name("ColorEffect")]];

struct BfMultiplyColorEffect {
    Reference Red;
    Reference Green;
    Reference Blue;
    Reference Alpha;
}[[name("BfMultiplyColorEffect")]];

struct BfMultiplyColorEffect2 {
    Reference Alpha;
}[[name("BfMultiplyColorEffect2")]];

struct RotateEffect {
    Reference Start_angle;
    Reference Angle_multiplyer;
}[[name("RotateEffect")]];

struct RotateAroundCoordinateEffect {
    Reference Start_angle;
    Reference Angle_multiplyer;
    Reference X;
    Reference Y;
}[[name("RotateAroundCoordinateEffect")]];

struct VariableColorEffect {
    Reference Red;
    Reference Green;
    Reference Blue;
    Reference Alpha;
}[[name("VariableColorEffect")]];

struct Event {
    u8 Input_index;
}[[name("Event")]];

struct AnyKeyEvent {
    u8 Input_index;
    u32 Event_type;
}[[name("AnyKeyEvent")]];

struct TypeEvent {
    u8 Input_index;
    u32 Event_type;
}[[name("TypeEvent")]];

struct ButtonEvent {
    u8 Input_index;
    u32 Event_type;
    u32 Button_type;
}[[name("ButtonEvent")]];

struct ExtendedButtonEvent {
    u8 Input_index;
    u32 Event_type;
    u32 Button_type;
    u32 Repeat_count;
}[[name("ExtendedButtonEvent")]];

struct ActionFunction {
    Reference Action;
}[[name("ActionFunction")]];

struct ActionNode : Node {
    Reference Action;
}[[name("ActionNode")]];

struct BfVariableTimeoutActionNode : Node {
    Reference Action;
    Reference Timeout_time;
}[[name("BfVariableTimeoutActionNode")]];

struct BfVariableTimeoutActionNode2 : Node {
    Reference Action;
    Reference Current_time;
    Reference Timeout_time;
}[[name("BfVariableTimeoutActionNode2")]];

struct CullActionNode : Node {
    Reference Action;
    u8 Event_type;
    u32 Event_data;
}[[name("CullActionNode")]];

struct CullEventActionNode : Node {
    Reference field_1;
    Reference field_2;
}[[name("CullEventActionNode")]];

struct CullVariableActionNode : Node {
    Reference Action;
    Reference Variable;
}[[name("CullVariableActionNode")]];

struct CullVariableAndEventActionNode : Node {
    Reference Action;
    Reference Variable;
    Reference Event;
}[[name("CullVariableAndEventActionNode")]];

struct IfElseEventActionNode : Node {
    Reference Action;
    Reference Variable;
    Reference Else_Action;
    Reference Event;
}[[name("IfElseEventActionNode")]];

struct TimeoutActionNode : Node {
    Reference Action;
    float Timeout_time;
}[[name("TimeoutActionNode")]];

struct BfBinkNode : Node {
    Reference Bink_filename;
    Reference Background_picture;
    float Fade_time;
    Reference Play;
}[[name("BfBinkNode")]];

struct BfButtonNode : Node {
    String8 Picture;
    String8 Mouse_over_picture;
    Reference Action;
    float Width;
    float Height;
}[[name("BfButtonNode")]];

struct BfNavigationButtonNode : Node {
    String8 Picture;
    String8 Mouse_over_picture;
    String8 Clicked_picture;
    Reference Action;
    bool MouseOver_button;
    u32 Index;
    Reference Current_mouseover_index;
    Reference Current_clicked_index;
    Reference MouseOver_active;
    float Width;
    float Height;
}[[name("BfNavigationButtonNode")]];

struct BfSelectButtonNode : Node {
    String8 Picture;
    String8 Mouse_over_picture;
    String8 Clicked_picture;
    Reference Action;
    u32 Index;
    Reference Current_clicked_index;
    float Width;
    float Height;
}[[name("BfSelectButtonNode")]];

struct BfCreditsNode : Node {
    Reference Value;
    float End_value;
    float Reset_value;
    float Time;
    Reference Go;
}[[name("BfCreditsNode")]];

struct BfCrosshairNode : Node {
    Reference Radius;
    Reference Thickness;
    Reference outline_thickness;
    Reference Deviation;
    Reference color;
    Reference outline;
}[[name("BfCrosshairNode")]];

struct BfEditNode : Node {
    Reference Next_node;
    FontString Font;
    Reference String;
    u32 Max_characters;
    Reference Select_action;
    Reference Editbox_data;
    bool Focus;
}[[name("BfEditNode")]];

struct BfEditNodeInt : Node {
    FontString Font;
    Reference Int;
    Reference String;
    u32 Min_value;
    u32 Max_value;
    Reference Select_action;
    Reference Editbox_data;
    bool Focus;
}[[name("BfEditNodeInt")]];

struct BfListBoxNode : Node {
}[[name("BfListBoxNode")]];

struct BfNewListBoxNode : Node {
    Reference Listbox_data;
    FontString Font;
    Reference Select_action;
    Reference Focus_action;
    SoundString Step_sound;
    SoundString Select_sound;
    SoundString Failed_select_sound;
    float Row_height;
    bool IsSelectable;
    bool Border_or_not;
    float Background_color_red;
    float Background_color_green;
    float Background_color_blue;
    float Background_color_alpha;
    float Scrollbar_width;
    float Frame_color_red;
    float Frame_color_green;
    float Frame_color_blue;
    float Frame_color_alpha;
    float Select_color_red;
    float Select_color_green;
    float Select_color_blue;
    float Select_color_alpha;
    bool Show_tooltip;
    float Scrollbar_offset_from_border;
}[[name("BfNewListBoxNode")]];

struct BfLocaleNode : Node {
    Reference Locale;
}[[name("BfLocaleNode")]];

struct BfOccupiedVehicleNode : Node {
    u32 Gui_Index;
    bool Draw_debug_pic;
    Reference BfOccupiedVehicleData;
}[[name("BfOccupiedVehicleNode")]];

struct BfRectangle : Node {
    float Thickness;
}[[name("BfRectangle")]];

struct BfTextNode : Node {
    Reference String;
    Reference Style;
    Reference Type;
}[[name("BfTextNode")]];

struct BfVariablePictureNode : Node {
    Reference picture_str;
    Reference redraw;
}[[name("BfVariablePictureNode")]];

struct ClipNode : Node {

}[[name("ClipNode")]];

struct CullNode : Node {
    Reference Do_Show;
    float In_time;
    float Out_time;
}[[name("CullNode")]];

struct CullVariableNode : Node {
    Reference Variable;
    Reference Data;
}[[name("CullVariableNode")]];

struct DisableNode : Node {
    Reference Disable_data;
}[[name("DisableNode")]];

struct EditNode : Node {
    FontString Font;
    Reference String;
    u32 Max_characters;
}[[name("EditNode")]];

struct EffectNode : Node {
    Reference Effect;
}[[name("EffectNode")]];

struct BfAddSubEffectNode : Node {
    Reference Value;
    Reference End_value;
    Reference Start_time;
    Reference Start_percentage;
    Reference End_time;
    Reference Delay;
    Reference Up;
    Reference Go;
}[[name("BfAddSubEffectNode")]];

struct BfAddSubNextEffectNode : Node {
    Reference Value;
    Reference End_value;
    Reference Start_time;
    Reference Start_percentage;
    Reference End_time;
    Reference Delay;
    Reference Up;
    Reference Next_action;
    Reference Go;
}[[name("BfAddSubNextEffectNode")]];

struct BfScrollPictureNode : Node {
    String8 Scroll_picture;
    Reference Data;
    Reference Maximum_value;
    u32 Y_offset;
    u32 Size;
    Reference Var_size;
    Reference Maintain_value;
    bool From_bottom;
}[[name("BfScrollPictureNode")]];

struct BfScrollPictureNode2 : Node {
    String8 Scroll_picture;
    Reference Data;
    Reference Maximum_value;
    u32 Y_offset;
    u32 Size;
    Reference Var_size;
    Reference Maintain_value;
    bool From_top;
}[[name("BfScrollPictureNode2")]];

struct BfVariablePictureFillNode : Node {
    String8 Picture;
    String8 Fill_picture;
    Reference Data;
    Reference Maximum_value;
    u32 Size;
    bool Horizontal_align;
    bool Fill_order;
}[[name("BfVariablePictureFillNode")]];

struct BfVariablePictureFillNode2 {
    Reference Picture;
    Reference Fill_picture;
    Reference Data;
    Reference Maximum_value;
    Reference Size;
    bool Horizontal_align;
    bool Fill_order;
}[[name("BfVariablePictureFillNode2")]];

struct FocusEffectNode : Node {
    Reference Effect;
}[[name("FocusEffectNode")]];

struct ShowEffectNode : Node {
    Reference Effect;
}[[name("ShowEffectNode")]];

struct NameNode : Node {

}[[name("NameNode")]];

struct PathNode : Node {

}[[name("PathNode")]];

struct PictureNode : Node {
    String8 Picture;
}[[name("PictureNode")]];

struct SliderNode : Node {
    Reference Cursor_node;
    Reference Data;
    float Minimum_value;
    float Maximum_value;
    float Number_visible;
}[[name("SliderNode")]];

struct BfFixedSliderNode : Node {
    Reference Cursor_node;
    Reference Data;
    float Minimum_value;
    float Maximum_value;
    float Number_visible;
    float Interval;
}[[name("BfFixedSliderNode")]];

struct BfSliderNode : Node {
    Reference Cursor_node;
    Reference Data;
    float Minimum_value;
    float Maximum_value;
    float Number_visible;
}[[name("BfSliderNode")]];

struct SplitNode : Node {
    Reference Split_node;
}[[name("SplitNode")]];

struct TextNode : Node {
    Reference String;
    Reference Style;
}[[name("TextNode")]];

struct TransformNode : Node {
    float X;
    float Y;
    float Width;
    float Height;
    Reference Transformed_node;
}[[name("TransformNode")]];

struct BfTransformNode : Node {
    Reference X;
    Reference Y;
    float Width;
    float Height;
    Reference Transformed_node;
}[[name("BfTransformNode")]];

struct BfTransformNodeSize : Node {
    float X;
    float Y;
    Reference Width;
    Reference Height;
    Reference Transformed_node;
}[[name("BfTransformNodeSize")]];

struct TranslateNode : Node {
    Reference X;
    Reference Y;
}[[name("TranslateNode")]];

struct VariablePictureNode : Node {
    Reference First_part;
    Reference Middle_part;
    Reference Last_part;
}[[name("VariablePictureNode")]];

struct Style {
    FontString Font_handle;
}[[name("Style")]];

struct BfCenterStyle {
    FontString Font_handle;
}[[name("BfCenterStyle")]];

struct BfLeftOutlineStyle {
    FontString Font_handle;
}[[name("BfLeftOutlineStyle")]];

struct BfOutlineStyle {
    FontString Font_handle;
}[[name("BfOutlineStyle")]];

struct BfStyle {
    FontString Font_handle;
}[[name("BfStyle")]];

struct BfStyle2 {
    FontString Font_handle;
}[[name("BfStyle2")]];

struct CenterAlignedStyle {
    FontString Font_handle;
}[[name("CenterAlignedStyle")]];

struct RightAlignedStyle {
    FontString Font_handle;
}[[name("RightAlignedStyle")]];

struct BfOccupiedVehicleData {
    // (no fields)
}[[name("BfOccupiedVehicleData")]];

struct BfEditData {
    // (no fields)
}[[name("BfEditData")]];

struct Function {
    // (no fields)
}[[name("Function")]];

struct BfTriangleButtonsNode : Node {
    String8 Picture_A;
    String8 Picture_B;
    Reference Action;
    float Width;
    float Height;
    Reference Clicked_Index_;
}[[name("BfTriangleButtonsNode")]];

struct SizeStyle {
    FontString Font_handle;
    float Size;
}[[name("SizeStyle")]];

struct BfControlPointGauge : Node {
    String8 Picture;
    Reference unkData_A;
    Reference unkData_B;
    Reference unkData_C;
}[[name("BfControlPointGauge")]];

struct AlphaFadeEffect {
    // (no fields)
}[[name("AlphaFadeEffect")]];

struct VariableEffectNode {
    Reference Button;
    Reference Fade_Effect;
    Reference Variable;
}[[name("VariableEffectNode")]];

struct BfLocalePictureButtonNode : Node {
    u8 Unk1;
    u8 Unk2;
    Reference Action;
    float _9_0;
    float _32_0;
    float _100_0;
    float _36_0;
    Reference BoolData_0;
    Reference Float_Data_9_0;
    Reference options_tga;
    Reference Main_Buttons_;
}[[name("BfLocalePictureButtonNode")]];

struct BfNewCreditsListNode : Node {
    Reference BfStyle;
    Reference RightAlignedStyle;
    Reference BoolData_1;
    Reference FloatData1;
    Reference FloatData2;
    Reference FloatData3;
    Reference FloatData4;
}[[name("BfNewCreditsListNode")]];

struct PointerXData {
    Reference Data;
}[[name("PointerXData")]];

struct PointerYData {
    Reference Data;
}[[name("PointerYData")]];

struct RemoveEventAction {
    // (no fields)
}[[name("RemoveEventAction")]];

struct FloatRefData {
    // (no fields)
}[[name("FloatRefData")]];

struct ActionListAction {
    Reference items[while(std::mem::read_unsigned($, 8) != 0x08)];
    Reference terminating_reference;
}[[name("ActionListAction")]];



struct ReferenceWithoutHeader {
    u16 string_index;
    if (string_index != 0) {
        str node_name = header.strings[string_index].string_value;
        match (node_name) {
            ("dice::meme::CallFunctionAction"): CallFunctionAction node;
            ("dice::meme::ModifyVariableAction"): ModifyVariableAction node;
            ("dice::meme::SetPathAction"): SetPathAction node;
            ("dice::meme::SetStringAction"): SetStringAction node;
            ("dice::meme::SetVariableAction"): SetVariableAction node;
            ("dice::meme::SplitAction"): SplitAction node;
            ("dice::meme::ToggleVariableAction"): ToggleVariableAction node;
            ("dice::meme::BfColorData"): BfColorData node;
            ("dice::meme::BfLocaleData"): BfLocaleData node;
            ("dice::meme::BfLocaleStringData"): BfLocaleStringData node;
            ("dice::meme::BoolData"): BoolData node;
            ("dice::meme::FloatData"): FloatData node;
            ("dice::meme::IndexDataData"): IndexDataData node;
            ("dice::meme::IntData"): IntData node;
            ("dice::meme::BfListBoxData"): BfListBoxData node;
            ("dice::meme::LogicalData"): LogicalData node;
            ("dice::meme::AndData"): AndData node;
            ("dice::meme::EqualData"): EqualData node;
            ("dice::meme::ExclusiveOrData"): ExclusiveOrData node;
            ("dice::meme::LessData"): LessData node;
            ("dice::meme::LessEqualData"): LessEqualData node;
            ("dice::meme::NotData"): NotData node;
            ("dice::meme::NotEqualData"): NotEqualData node;
            ("dice::meme::OrData"): OrData node;
            ("dice::meme::OperatorData"): OperatorData node;
            ("dice::meme::AddData"): AddData node;
            ("dice::meme::DivData"): DivData node;
            ("dice::meme::MulData"): MulData node;
            ("dice::meme::SubData"): SubData node;
            ("dice::meme::StringData"): StringData node;
            ("dice::meme::LocaleStringData"): LocaleStringData node;
            ("dice::meme::WstringData"): WstringData node;
            ("dice::meme::ColorEffect"): ColorEffect node;
            ("dice::meme::BfMultiplyColorEffect"): BfMultiplyColorEffect node;
            ("dice::meme::BfMultiplyColorEffect2"): BfMultiplyColorEffect2 node;
            ("dice::meme::RotateEffect"): RotateEffect node;
            ("dice::meme::RotateAroundCoordinateEffect"): RotateAroundCoordinateEffect node;
            ("dice::meme::VariableColorEffect"): VariableColorEffect node;
            ("dice::meme::Event"): Event node;
            ("dice::meme::AnyKeyEvent"): AnyKeyEvent node;
            ("dice::meme::TypeEvent"): TypeEvent node;
            ("dice::meme::ButtonEvent"): ButtonEvent node;
            ("dice::meme::ExtendedButtonEvent"): ExtendedButtonEvent node;
            ("dice::meme::ActionFunction"): ActionFunction node;
            ("dice::meme::ActionNode"): ActionNode node;
            ("dice::meme::BfVariableTimeoutActionNode"): BfVariableTimeoutActionNode node;
            ("dice::meme::BfVariableTimeoutActionNode2"): BfVariableTimeoutActionNode2 node;
            ("dice::meme::CullActionNode"): CullActionNode node;
            ("dice::meme::CullEventActionNode"): CullEventActionNode node;
            ("dice::meme::CullVariableActionNode"): CullVariableActionNode node;
            ("dice::meme::CullVariableAndEventActionNode"): CullVariableAndEventActionNode node;
            ("dice::meme::IfElseEventActionNode"): IfElseEventActionNode node;
            ("dice::meme::TimeoutActionNode"): TimeoutActionNode node;
            ("dice::meme::BfBinkNode"): BfBinkNode node;
            ("dice::meme::BfButtonNode"): BfButtonNode node;
            ("dice::meme::BfNavigationButtonNode"): BfNavigationButtonNode node;
            ("dice::meme::BfSelectButtonNode"): BfSelectButtonNode node;
            ("dice::meme::BfCreditsNode"): BfCreditsNode node;
            ("dice::meme::BfCrosshairNode"): BfCrosshairNode node;
            ("dice::meme::BfEditNode"): BfEditNode node;
            ("dice::meme::BfEditNodeInt"): BfEditNodeInt node;
            ("dice::meme::BfListBoxNode"): BfListBoxNode node;
            ("dice::meme::BfNewListBoxNode"): BfNewListBoxNode node;
            ("dice::meme::BfLocaleNode"): BfLocaleNode node;
            ("dice::meme::BfOccupiedVehicleNode"): BfOccupiedVehicleNode node;
            ("dice::meme::BfRectangle"): BfRectangle node;
            ("dice::meme::BfTextNode"): BfTextNode node;
            ("dice::meme::BfVariablePictureNode"): BfVariablePictureNode node;
            ("dice::meme::ClipNode"): ClipNode node;
            ("dice::meme::CullNode"): CullNode node;
            ("dice::meme::CullVariableNode"): CullVariableNode node;
            ("dice::meme::DisableNode"): DisableNode node;
            ("dice::meme::EditNode"): EditNode node;
            ("dice::meme::EffectNode"): EffectNode node;
            ("dice::meme::BfAddSubEffectNode"): BfAddSubEffectNode node;
            ("dice::meme::BfAddSubNextEffectNode"): BfAddSubNextEffectNode node;
            ("dice::meme::BfScrollPictureNode"): BfScrollPictureNode node;
            ("dice::meme::BfScrollPictureNode2"): BfScrollPictureNode2 node;
            ("dice::meme::BfVariablePictureFillNode"): BfVariablePictureFillNode node;
            ("dice::meme::BfVariablePictureFillNode2"): BfVariablePictureFillNode2 node;
            ("dice::meme::FocusEffectNode"): FocusEffectNode node;
            ("dice::meme::ShowEffectNode"): ShowEffectNode node;
            ("dice::meme::NameNode"): NameNode node;
            ("dice::meme::PathNode"): PathNode node;
            ("dice::meme::PictureNode"): PictureNode node;
            ("dice::meme::SliderNode"): SliderNode node;
            ("dice::meme::BfFixedSliderNode"): BfFixedSliderNode node;
            ("dice::meme::BfSliderNode"): BfSliderNode node;
            ("dice::meme::SplitNode"): SplitNode node;
            ("dice::meme::TextNode"): TextNode node;
            ("dice::meme::TransformNode"): TransformNode node;
            ("dice::meme::BfTransformNode"): BfTransformNode node;
            ("dice::meme::BfTransformNodeSize"): BfTransformNodeSize node;
            ("dice::meme::TranslateNode"): TranslateNode node;
            ("dice::meme::VariablePictureNode"): VariablePictureNode node;
            ("dice::meme::Style"): Style node;
            ("dice::meme::BfCenterStyle"): BfCenterStyle node;
            ("dice::meme::BfLeftOutlineStyle"): BfLeftOutlineStyle node;
            ("dice::meme::BfOutlineStyle"): BfOutlineStyle node;
            ("dice::meme::BfStyle"): BfStyle node;
            ("dice::meme::BfStyle2"): BfStyle2 node;
            ("dice::meme::CenterAlignedStyle"): CenterAlignedStyle node;
            ("dice::meme::RightAlignedStyle"): RightAlignedStyle node;
            ("dice::meme::BfOccupiedVehicleData"): BfOccupiedVehicleData node;
            ("dice::meme::BfEditData"): BfEditData node;
            ("dice::meme::Function"): Function node;
            ("dice::meme::BfTriangleButtonsNode"): BfTriangleButtonsNode node;
            ("dice::meme::SizeStyle"): SizeStyle node;
            ("dice::meme::BfControlPointGauge"): BfControlPointGauge node;
            ("dice::meme::AlphaFadeEffect"): AlphaFadeEffect node;
            ("dice::meme::VariableEffectNode"): VariableEffectNode node;
            ("dice::meme::BfLocalePictureButtonNode"): BfLocalePictureButtonNode node;
            ("dice::meme::BfNewCreditsListNode"): BfNewCreditsListNode node;
            ("dice::meme::PointerXData"): PointerXData node;
            ("dice::meme::PointerYData"): PointerYData node;
            ("dice::meme::RemoveEventAction"): RemoveEventAction node;
            ("dice::meme::FloatRefData"): FloatRefData node;
            ("dice::meme::ActionListAction"): ActionListAction node;
            (_): {
                std::warning(node_name);
                return;
            }
        }
    }
}[[name("ReferenceWithoutHeader")]];

struct Reference {
    u32 size;
    u16 unknown;
    str node_name = header.strings[unknown].string_value;
    if (unknown != 0)
        std::warning("Unknown is:" + std::string::to_string(unknown) + " -> " + node_name);
    ReferenceWithoutHeader node;
}[[name("Reference")]];

ReferenceWithoutHeader first_node_reference @ $;