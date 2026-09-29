using UnityEngine;

namespace EditorIntro
{
    /// <summary>
    /// フィールドの上に補足説明を表示する属性です。
    /// 表示の処理は第 7 章の NoteDrawer に記述します。
    /// </summary>
    public class NoteAttribute : PropertyAttribute
    {
        public NoteAttribute(string text)
        {
            Text = text;
        }

        public string Text { get; }
    }
}
