using System.IO;
using UnityEngine;

namespace UnityIntroduction.Chapter15
{
    /// <summary>
    /// SaveData を JSON ファイルとして保存し、読み込みます。
    /// </summary>
    public static class SaveSystem
    {
        private const string FileName = "save.json";

        /// <summary>
        /// 保存先のファイルパスです。
        /// </summary>
        /// <remarks>
        /// Application.persistentDataPath は、アプリケーションが自由に書き込めるフォルダーを指します。
        /// 実際の場所は OS によって異なります。
        /// </remarks>
        public static string FilePath => Path.Combine(Application.persistentDataPath, FileName);

        /// <summary>
        /// データをファイルに保存します。
        /// </summary>
        public static void Save(SaveData data)
        {
            // 第 2 引数に true を渡すと、人間が読みやすいように改行とインデントが入ります。
            string json = JsonUtility.ToJson(data, true);
            File.WriteAllText(FilePath, json);
        }

        /// <summary>
        /// ファイルからデータを読み込みます。ファイルが無い場合は新しいデータを返します。
        /// </summary>
        public static SaveData Load()
        {
            if (!File.Exists(FilePath))
            {
                return new SaveData();
            }

            string json = File.ReadAllText(FilePath);
            return JsonUtility.FromJson<SaveData>(json);
        }
    }
}
