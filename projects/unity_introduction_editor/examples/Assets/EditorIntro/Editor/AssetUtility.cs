using UnityEditor;
using UnityEngine;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 10 章のサンプルです。
    /// AssetDatabase を使って、アセットの作成・検索・変更を行います。
    /// </summary>
    public static class AssetUtility
    {
        // アセットを作成するフォルダーです。「Assets」から始まるパスで指定します。
        private const string OutputFolder = "Assets";

        [MenuItem("Tools/Editor Intro/Assets/Create Item Data")]
        private static void CreateItemData()
        {
            // ScriptableObject は new ではなく CreateInstance で作成します。
            var item = ScriptableObject.CreateInstance<ItemData>();

            // 同じ名前のファイルがあれば「NewItemData 1.asset」のような重複しないパスを返します。
            var path = AssetDatabase.GenerateUniqueAssetPath($"{OutputFolder}/NewItemData.asset");
            AssetDatabase.CreateAsset(item, path);
            AssetDatabase.SaveAssets();

            // 作成したアセットを選択し、Project ウィンドウで強調表示します。
            Selection.activeObject = item;
            EditorGUIUtility.PingObject(item);
        }

        [MenuItem("Tools/Editor Intro/Assets/List Item Data")]
        private static void ListItemData()
        {
            // 「t:型名」で、指定した型のアセットを検索します。結果は GUID の配列です。
            var guids = AssetDatabase.FindAssets("t:ItemData");
            Debug.Log($"ItemData アセットが {guids.Length} 個見つかりました。");

            foreach (var guid in guids)
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var item = AssetDatabase.LoadAssetAtPath<ItemData>(path);
                Debug.Log($"{path}：{item.ItemName}（{item.Price} G）");
            }
        }

        [MenuItem("Tools/Editor Intro/Assets/Double Price Of Selected Item Data", true)]
        private static bool ValidateDoublePrice()
        {
            return Selection.GetFiltered<ItemData>(SelectionMode.Assets).Length > 0;
        }

        [MenuItem("Tools/Editor Intro/Assets/Double Price Of Selected Item Data")]
        private static void DoublePrice()
        {
            foreach (var item in Selection.GetFiltered<ItemData>(SelectionMode.Assets))
            {
                // SerializedObject 経由で変更すると、Undo への記録と変更済みの印付けが自動で行われます。
                var itemObject = new SerializedObject(item);
                var priceProperty = itemObject.FindProperty("price");
                priceProperty.intValue *= 2;
                itemObject.ApplyModifiedProperties();

                // 変更をすぐにファイルへ書き込みます。
                // 呼ばない場合は、プロジェクトの保存時（File > Save Project など）に書き込まれます。
                AssetDatabase.SaveAssetIfDirty(item);
            }
        }
    }
}
