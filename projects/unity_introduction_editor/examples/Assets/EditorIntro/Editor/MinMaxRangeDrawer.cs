using UnityEditor;
using UnityEditor.UIElements;
using UnityEngine.UIElements;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 7 章のサンプルです。
    /// MinMaxRange 型のフィールドを「ラベル・最小値・最大値」の 1 行で表示します。
    /// </summary>
    [CustomPropertyDrawer(typeof(MinMaxRange))]
    public class MinMaxRangeDrawer : PropertyDrawer
    {
        public override VisualElement CreatePropertyGUI(SerializedProperty property)
        {
            // MinMaxRange 構造体の中にある private フィールドを取得します。
            var minProperty = property.FindPropertyRelative("min");
            var maxProperty = property.FindPropertyRelative("max");

            var root = new VisualElement();

            var row = new VisualElement();
            row.style.flexDirection = FlexDirection.Row;
            root.Add(row);

            var label = new Label(property.displayName);
            label.style.width = 120;
            label.style.unityTextAlign = UnityEngine.TextAnchor.MiddleLeft;
            row.Add(label);

            row.Add(CreateFloatField("最小", minProperty));
            row.Add(CreateFloatField("最大", maxProperty));

            // 最小値が最大値を超えているときだけ警告を表示します。
            var warning = new HelpBox("最小値が最大値を超えています。", HelpBoxMessageType.Warning);
            root.Add(warning);

            void UpdateWarning()
            {
                var isInvalid = minProperty.floatValue > maxProperty.floatValue;
                warning.style.display = isInvalid ? DisplayStyle.Flex : DisplayStyle.None;
            }

            UpdateWarning();
            root.TrackPropertyValue(minProperty, _ => UpdateWarning());
            root.TrackPropertyValue(maxProperty, _ => UpdateWarning());

            return root;
        }

        private static FloatField CreateFloatField(string label, SerializedProperty property)
        {
            var field = new FloatField(label);

            // BindProperty で、入力欄と SerializedProperty を結び付けます。
            field.BindProperty(property);

            // 残りの幅を 2 つの入力欄で等分し、短いラベルが入力欄を圧迫しないようにします。
            field.style.flexGrow = 1;
            field.style.flexBasis = 0;
            field.labelElement.style.minWidth = 0;
            return field;
        }
    }
}
