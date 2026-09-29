using UnityEditor;
using UnityEngine;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 11 章のサンプルです。
    /// 第 12 章の一括リネームツールで使う初期値を、プロジェクトの設定として保存します。
    /// </summary>
    // FilePath 属性で保存先を指定します。ProjectFolder はプロジェクトのルートフォルダーを基準にします。
    [FilePath("ProjectSettings/EditorIntroBatchRenameSettings.asset", FilePathAttribute.Location.ProjectFolder)]
    public class BatchRenameSettings : ScriptableSingleton<BatchRenameSettings>
    {
        public const int MinDigits = 1;
        public const int MaxDigits = 6;

        [SerializeField] private string prefix = "Item_";
        [SerializeField] private int startNumber = 1;
        [SerializeField] private int digits = 2;

        /// <summary>名前の先頭に付ける文字列です。</summary>
        public string Prefix
        {
            get => prefix;
            set => prefix = value;
        }

        /// <summary>連番の開始番号です（0 以上）。</summary>
        public int StartNumber
        {
            get => startNumber;
            set => startNumber = Mathf.Max(0, value);
        }

        /// <summary>連番の桁数です。足りない桁は 0 で埋めます。</summary>
        public int Digits
        {
            get => digits;
            set => digits = Mathf.Clamp(value, MinDigits, MaxDigits);
        }

        /// <summary>設定をファイルに保存します。</summary>
        public void SaveSettings()
        {
            // Save は protected メソッドです。引数を true にすると、テキスト形式で保存します。
            Save(true);
        }
    }
}
