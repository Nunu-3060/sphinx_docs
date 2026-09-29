using UnityEditor;
using UnityEngine.UIElements;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 7 章のサンプルです。
    /// Note 属性が付いたフィールドの上に、補足説明を表示します。
    /// </summary>
    [CustomPropertyDrawer(typeof(NoteAttribute))]
    public class NoteDrawer : DecoratorDrawer
    {
        // DecoratorDrawer はフィールドの値を扱わないため、引数に SerializedProperty がありません。
        public override VisualElement CreatePropertyGUI()
        {
            var note = (NoteAttribute)attribute;
            return new HelpBox(note.Text, HelpBoxMessageType.Info);
        }
    }
}
