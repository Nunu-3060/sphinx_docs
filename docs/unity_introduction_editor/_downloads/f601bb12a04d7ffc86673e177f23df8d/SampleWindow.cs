using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 8 章のサンプルです。
    /// UXML と USS で画面を構成し、選択中のオブジェクトを表示するウィンドウです。
    /// </summary>
    public class SampleWindow : EditorWindow
    {
        // UXML ファイルの場所です。サンプルコードを別のフォルダーに置いた場合は変更してください。
        private const string UxmlPath = "Assets/EditorIntro/Editor/UI/SampleWindow.uxml";

        private Label countLabel;
        private Label namesLabel;

        [MenuItem("Tools/Editor Intro/Sample Window")]
        public static void Open()
        {
            // 同じ種類のウィンドウが既に開いていればそのウィンドウを、開いていなければ新しく作成して返します。
            var window = GetWindow<SampleWindow>();
            window.titleContent = new GUIContent("Sample Window");
        }

        // ウィンドウの UI を作成するタイミングで呼ばれます。
        private void CreateGUI()
        {
            var visualTree = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>(UxmlPath);
            if (visualTree == null)
            {
                rootVisualElement.Add(new HelpBox($"{UxmlPath} が見つかりません。", HelpBoxMessageType.Error));
                return;
            }

            // UXML の内容を rootVisualElement の子として複製します。
            visualTree.CloneTree(rootVisualElement);

            // Q メソッドで、UXML の name 属性を指定して要素を取得します。
            countLabel = rootVisualElement.Q<Label>("count-label");
            namesLabel = rootVisualElement.Q<Label>("names-label");
            rootVisualElement.Q<Button>("ping-button").clicked += PingActiveObject;
            rootVisualElement.Q<Button>("clear-button").clicked += ClearSelection;

            Refresh();
        }

        // 選択が変わると呼ばれます。
        private void OnSelectionChange()
        {
            Refresh();
        }

        private void Refresh()
        {
            // CreateGUI より前に呼ばれた場合や、UXML が見つからなかった場合は何もしません。
            if (countLabel == null)
            {
                return;
            }

            var objects = Selection.objects;
            countLabel.text = $"選択数：{objects.Length}";
            namesLabel.text = objects.Length == 0
                ? "（なし）"
                : string.Join("\n", objects.Select(o => o.name));
        }

        private static void PingActiveObject()
        {
            // Hierarchy ウィンドウや Project ウィンドウで、対象を一時的に強調表示します。
            if (Selection.activeObject != null)
            {
                EditorGUIUtility.PingObject(Selection.activeObject);
            }
        }

        private static void ClearSelection()
        {
            Selection.objects = new Object[0];
        }
    }
}
