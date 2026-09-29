using UnityEditor;
using UnityEngine;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 11 章のサンプルです。
    /// EditorPrefs に値を保存し、メニュー項目のチェックマークで状態を表示します。
    /// </summary>
    public static class EditorPrefsExample
    {
        private const string MenuPath = "Tools/Editor Intro/Verbose Log";

        // EditorPrefs はすべてのプロジェクトで共有されるため、ほかのツールと重ならないキーにします。
        private const string PrefsKey = "EditorIntro.VerboseLog";

        public static bool VerboseLog
        {
            get => EditorPrefs.GetBool(PrefsKey, false);
            set => EditorPrefs.SetBool(PrefsKey, value);
        }

        [MenuItem(MenuPath)]
        private static void ToggleVerboseLog()
        {
            VerboseLog = !VerboseLog;
            var state = VerboseLog ? "有効" : "無効";
            Debug.Log($"詳細ログを{state}にしました。");
        }

        // 検証関数はメニューを開くたびに呼ばれるため、ここでチェックマークの状態を更新します。
        [MenuItem(MenuPath, true)]
        private static bool ValidateToggleVerboseLog()
        {
            Menu.SetChecked(MenuPath, VerboseLog);
            return true;
        }
    }
}
