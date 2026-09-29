using UnityEditor;
using UnityEditor.UIElements;
using UnityEngine.UIElements;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 7 章のサンプルです。
    /// TagSelector 属性が付いた string 型のフィールドを、タグのドロップダウンで表示します。
    /// </summary>
    [CustomPropertyDrawer(typeof(TagSelectorAttribute))]
    public class TagSelectorDrawer : PropertyDrawer
    {
        public override VisualElement CreatePropertyGUI(SerializedProperty property)
        {
            // string 型以外のフィールドに付けられた場合は、エラーメッセージを表示します。
            if (property.propertyType != SerializedPropertyType.String)
            {
                return new HelpBox(
                    $"{property.displayName}：TagSelector 属性は string 型のフィールドにだけ使用できます。",
                    HelpBoxMessageType.Error);
            }

            // TagField は、プロジェクトに登録されているタグを選択肢に持つドロップダウンです。
            var field = new TagField(property.displayName);
            field.BindProperty(property);

            // ほかのフィールドとラベルの幅をそろえます。
            field.AddToClassList(BaseField<string>.alignedFieldUssClassName);
            return field;
        }
    }
}
