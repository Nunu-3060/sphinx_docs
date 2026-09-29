using UnityEditor;
using UnityEngine;

namespace UnityIntroduction.Chapter08.EditorTools
{
    /// <summary>
    /// 選択中の GameObject を Y = 0 の高さにそろえるメニューを追加します。
    /// </summary>
    /// <remarks>
    /// Editor という名前のフォルダーに置いたスクリプトはエディター専用となり、
    /// ビルドしたアプリケーションには含まれません。
    /// </remarks>
    public static class AlignToGroundMenu
    {
        private const string MenuPath = "Tools/Unity Introduction/Align To Ground";

        [MenuItem(MenuPath)]
        private static void AlignToGround()
        {
            Transform[] targets = Selection.transforms;

            // Undo に登録しておくと、Ctrl + Z で元に戻せます。
            Undo.RecordObjects(targets, "Align To Ground");

            foreach (Transform target in targets)
            {
                Vector3 position = target.position;
                position.y = 0f;
                target.position = position;
            }
        }

        // 同じパスで第 2 引数に true を指定したメソッドは、メニューを有効にするかどうかの判定に使われます。
        [MenuItem(MenuPath, true)]
        private static bool ValidateAlignToGround()
        {
            return Selection.transforms.Length > 0;
        }
    }
}
