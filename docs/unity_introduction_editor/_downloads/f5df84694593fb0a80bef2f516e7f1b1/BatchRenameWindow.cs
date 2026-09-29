using System.Collections.Generic;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 12 章のサンプルです。
    /// Hierarchy ウィンドウで選択したゲームオブジェクトの名前を、連番付きで一括変更します。
    /// </summary>
    public class BatchRenameWindow : EditorWindow
    {
        private TextField prefixField;
        private IntegerField startNumberField;
        private SliderInt digitsField;
        private ScrollView previewList;
        private Button renameButton;

        [MenuItem("Tools/Editor Intro/Batch Rename")]
        public static void Open()
        {
            var window = GetWindow<BatchRenameWindow>();
            window.titleContent = new GUIContent("Batch Rename");
            window.minSize = new Vector2(320, 240);
        }

        private void CreateGUI()
        {
            // 入力欄の初期値は、Project Settings ウィンドウで設定した値（第 11 章）を使います。
            var settings = BatchRenameSettings.instance;

            var root = rootVisualElement;
            root.style.paddingLeft = 6;
            root.style.paddingRight = 6;
            root.style.paddingTop = 6;
            root.style.paddingBottom = 6;

            prefixField = new TextField("接頭辞") { value = settings.Prefix };
            startNumberField = new IntegerField("開始番号") { value = settings.StartNumber };
            digitsField = new SliderInt("桁数", BatchRenameSettings.MinDigits, BatchRenameSettings.MaxDigits)
            {
                value = settings.Digits,
                showInputField = true,
            };

            // 入力が変わるたびにプレビューを更新します。
            prefixField.RegisterValueChangedCallback(_ => RefreshPreview());
            startNumberField.RegisterValueChangedCallback(evt =>
            {
                // 開始番号に負の値を入力できないようにします。
                if (evt.newValue < 0)
                {
                    startNumberField.SetValueWithoutNotify(0);
                }

                RefreshPreview();
            });
            digitsField.RegisterValueChangedCallback(_ => RefreshPreview());

            root.Add(prefixField);
            root.Add(startNumberField);
            root.Add(digitsField);

            var previewLabel = new Label("プレビュー");
            previewLabel.style.unityFontStyleAndWeight = FontStyle.Bold;
            previewLabel.style.marginTop = 8;
            root.Add(previewLabel);

            // プレビューは残りの高さいっぱいに広げ、はみ出した分はスクロールで表示します。
            previewList = new ScrollView();
            previewList.style.flexGrow = 1;
            root.Add(previewList);

            renameButton = new Button(Rename) { text = "名前を変更" };
            renameButton.style.height = 24;
            root.Add(renameButton);

            RefreshPreview();
        }

        // 選択が変わったときと、Hierarchy ウィンドウの内容が変わったとき（名前や並び順の変更など）にプレビューを更新します。
        private void OnSelectionChange()
        {
            RefreshPreview();
        }

        private void OnHierarchyChange()
        {
            RefreshPreview();
        }

        private void RefreshPreview()
        {
            // CreateGUI より前に呼ばれた場合は何もしません。
            if (previewList == null)
            {
                return;
            }

            previewList.Clear();

            var targets = GetTargets();
            if (targets.Count == 0)
            {
                previewList.Add(new HelpBox(
                    "Hierarchy ウィンドウで、名前を変更するゲームオブジェクトを選択してください。",
                    HelpBoxMessageType.Info));
                renameButton.SetEnabled(false);
                return;
            }

            for (var i = 0; i < targets.Count; i++)
            {
                previewList.Add(new Label($"{targets[i].name} → {CreateName(i)}"));
            }

            renameButton.SetEnabled(true);
        }

        private void Rename()
        {
            var targets = GetTargets();

            // 複数のオブジェクトの変更を、1 回の Undo 操作で元に戻せるようにまとめて記録します。
            Undo.RecordObjects(targets.ToArray(), "Batch Rename");

            for (var i = 0; i < targets.Count; i++)
            {
                targets[i].name = CreateName(i);

                if (PrefabUtility.IsPartOfPrefabInstance(targets[i]))
                {
                    PrefabUtility.RecordPrefabInstancePropertyModifications(targets[i]);
                }
            }

            RefreshPreview();
        }

        /// <summary>
        /// 選択中のゲームオブジェクトのうち、シーン上にあるものを Hierarchy ウィンドウの表示順で返します。
        /// </summary>
        private static List<GameObject> GetTargets()
        {
            // IsPersistent はアセット（Project ウィンドウで選択したプレハブなど）のとき true になります。
            var targets = Selection.gameObjects
                .Where(go => !EditorUtility.IsPersistent(go))
                .ToList();

            // Selection.gameObjects の順序は決まっていないため、表示順に並べ替えます。
            targets.Sort(CompareHierarchyOrder);
            return targets;
        }

        private string CreateName(int index)
        {
            // 例：接頭辞「Item_」、開始番号 1、桁数 2 のとき → Item_01、Item_02、…
            var number = startNumberField.value + index;
            return prefixField.value + number.ToString($"D{digitsField.value}");
        }

        /// <summary>
        /// 2 つのゲームオブジェクトを、Hierarchy ウィンドウの表示順で比較します。
        /// 複数のシーンを開いている場合、シーンをまたいだ順序は考慮しません。
        /// </summary>
        private static int CompareHierarchyOrder(GameObject a, GameObject b)
        {
            var pathA = GetSiblingIndexPath(a.transform);
            var pathB = GetSiblingIndexPath(b.transform);

            var length = Mathf.Min(pathA.Count, pathB.Count);
            for (var i = 0; i < length; i++)
            {
                if (pathA[i] != pathB[i])
                {
                    return pathA[i].CompareTo(pathB[i]);
                }
            }

            // 一方が他方の親の場合は、親を先にします。
            return pathA.Count.CompareTo(pathB.Count);
        }

        /// <summary>
        /// ルートから対象までの、各階層での並び順（兄弟の中での番号）のリストを返します。
        /// </summary>
        private static List<int> GetSiblingIndexPath(Transform transform)
        {
            var path = new List<int>();
            for (var current = transform; current != null; current = current.parent)
            {
                path.Insert(0, current.GetSiblingIndex());
            }

            return path;
        }
    }
}
