using UnityEditor;
using UnityEditor.UIElements;
using UnityEngine.UIElements;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 6 章のサンプルです。
    /// Enemy コンポーネントの Inspector ウィンドウの表示を UI Toolkit でカスタマイズします。
    /// </summary>
    [CustomEditor(typeof(Enemy))]
    [CanEditMultipleObjects]
    public class EnemyEditor : Editor
    {
        // Enemy クラスの private フィールドの名前です。
        // フィールド名を変更したときは、ここも合わせて変更します。
        private const string EnemyNameField = "enemyName";
        private const string MaxHpField = "maxHp";
        private const string HpField = "hp";
        private const string MoveSpeedField = "moveSpeed";

        private HelpBox hpWarning;

        public override VisualElement CreateInspectorGUI()
        {
            var root = new VisualElement();

            var maxHpProperty = serializedObject.FindProperty(MaxHpField);
            var hpProperty = serializedObject.FindProperty(HpField);

            // PropertyField は、プロパティの型に合った入力欄を自動で作成します。
            // ここで返した要素は Inspector ウィンドウが自動でバインドするため、Bind を呼ぶ必要はありません。
            root.Add(new PropertyField(serializedObject.FindProperty(EnemyNameField), "名前"));
            root.Add(new PropertyField(maxHpProperty, "最大 HP"));
            root.Add(new PropertyField(hpProperty, "HP"));
            root.Add(new PropertyField(serializedObject.FindProperty(MoveSpeedField), "移動速度"));

            // HP が最大 HP を超えているときだけ警告を表示します。
            hpWarning = new HelpBox("HP が最大 HP を超えています。", HelpBoxMessageType.Warning);
            root.Add(hpWarning);
            UpdateHpWarning();

            // 値が変わるたびに警告の表示を更新します。
            root.TrackPropertyValue(maxHpProperty, _ => UpdateHpWarning());
            root.TrackPropertyValue(hpProperty, _ => UpdateHpWarning());

            var healButton = new Button(HealAll) { text = "HP を全回復" };
            healButton.style.marginTop = 6;
            root.Add(healButton);

            return root;
        }

        private void UpdateHpWarning()
        {
            // 複数選択時は、1 つでも条件を満たせば警告を表示します。
            var showWarning = false;
            foreach (var t in targets)
            {
                var enemy = (Enemy)t;
                if (enemy.Hp > enemy.MaxHp)
                {
                    showWarning = true;
                    break;
                }
            }

            hpWarning.style.display = showWarning ? DisplayStyle.Flex : DisplayStyle.None;
        }

        private void HealAll()
        {
            // 最大 HP は対象ごとに異なる可能性があるため、1 つずつ SerializedObject を作成して変更します。
            // ApplyModifiedProperties を呼ぶと、変更は Undo に記録されます。
            foreach (var t in targets)
            {
                var enemyObject = new SerializedObject(t);
                var maxHp = enemyObject.FindProperty(MaxHpField).intValue;
                enemyObject.FindProperty(HpField).intValue = maxHp;
                enemyObject.ApplyModifiedProperties();
            }
        }
    }
}
