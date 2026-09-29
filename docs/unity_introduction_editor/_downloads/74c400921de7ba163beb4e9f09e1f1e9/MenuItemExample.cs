using UnityEditor;
using UnityEngine;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 3 章のサンプルです。
    /// MenuItem 属性でメニューに項目を追加します。
    /// </summary>
    public static class MenuItemExample
    {
        // メニューバーの「Tools > Editor Intro > Hello」に項目を追加します。
        // MenuItem 属性を付けるメソッドは static にします。
        [MenuItem("Tools/Editor Intro/Hello")]
        private static void Hello()
        {
            Debug.Log("Hello, Editor!");
        }

        // パスの末尾に「%&h」を付けると、Ctrl + Alt + H（macOS では Cmd + Option + H）で実行できます。
        // % は Ctrl（macOS では Cmd）、& は Alt（macOS では Option）、# は Shift を表します。
        [MenuItem("Tools/Editor Intro/Hello With Shortcut %&h")]
        private static void HelloWithShortcut()
        {
            Debug.Log("ショートカットキーから実行しました。");
        }

        // 第 2 引数を true にしたメソッドは「検証関数」になります。
        // 検証関数が false を返すと、同じパスのメニュー項目はグレーアウトして選択できなくなります。
        [MenuItem("Tools/Editor Intro/Log Selected Name", true)]
        private static bool ValidateLogSelectedName()
        {
            return Selection.activeGameObject != null;
        }

        [MenuItem("Tools/Editor Intro/Log Selected Name")]
        private static void LogSelectedName()
        {
            Debug.Log($"選択中のゲームオブジェクト：{Selection.activeGameObject.name}");
        }

        // 第 3 引数は表示順（priority）です。値が小さいほど上に表示されます。
        // 直前の項目と値が大きく離れている（目安として 11 以上）と、間に区切り線が入ります。
        [MenuItem("Tools/Editor Intro/About", false, 2000)]
        private static void About()
        {
            EditorUtility.DisplayDialog("About", "Unity エディター拡張入門のサンプルです。", "OK");
        }

        // 「CONTEXT/コンポーネント名/」で始まるパスは、コンポーネントのコンテキストメニューに追加されます。
        // MenuCommand.context には、操作対象のコンポーネントが入ります。
        [MenuItem("CONTEXT/Transform/Reset Y Position")]
        private static void ResetYPosition(MenuCommand command)
        {
            var transform = (Transform)command.context;

            // 変更前に Undo.RecordObject を呼ぶと、Ctrl + Z で元に戻せます（第 5 章で説明します）。
            Undo.RecordObject(transform, "Reset Y Position");
            var position = transform.localPosition;
            position.y = 0f;
            transform.localPosition = position;
        }

        // 「GameObject/」で始まるパスで priority を 10 にすると、ほかのゲームオブジェクト作成メニューと同じグループになり、
        // Hierarchy ウィンドウの「+」ボタンのメニューと右クリックメニューにも表示されます。
        [MenuItem("GameObject/Editor Intro/Marker", false, 10)]
        private static void CreateMarker(MenuCommand command)
        {
            var marker = new GameObject("Marker");

            // 右クリックしたゲームオブジェクトがあれば、その子にします。
            GameObjectUtility.SetParentAndAlign(marker, command.context as GameObject);

            // 作成したゲームオブジェクトを Undo に登録し、選択状態にします。
            Undo.RegisterCreatedObjectUndo(marker, "Create Marker");
            Selection.activeObject = marker;
        }
    }
}
