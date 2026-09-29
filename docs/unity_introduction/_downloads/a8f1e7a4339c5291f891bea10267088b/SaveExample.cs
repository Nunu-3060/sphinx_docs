using UnityEngine;

namespace UnityIntroduction.Chapter15
{
    /// <summary>
    /// SaveSystem と PlayerPrefs の使用例です。
    /// </summary>
    /// <remarks>
    /// Inspector のコンポーネント名の右にあるメニュー（⋮）から各処理を実行できます。
    /// </remarks>
    public class SaveExample : MonoBehaviour
    {
        private const string VolumeKey = "Volume";

        [ContextMenu("JSON ファイルに保存する")]
        private void SaveToFile()
        {
            var data = new SaveData
            {
                PlayerName = "Unity",
                HighScore = 1200,
            };
            data.ClearedStages.Add("Stage1");

            SaveSystem.Save(data);
            Debug.Log($"保存しました: {SaveSystem.FilePath}");
        }

        [ContextMenu("JSON ファイルから読み込む")]
        private void LoadFromFile()
        {
            SaveData data = SaveSystem.Load();
            Debug.Log($"{data.PlayerName} のハイスコア: {data.HighScore}");
        }

        [ContextMenu("PlayerPrefs に音量を保存する")]
        private void SaveVolume()
        {
            PlayerPrefs.SetFloat(VolumeKey, 0.8f);

            // Save を呼ぶと、その時点でディスクに書き込まれます。
            PlayerPrefs.Save();
        }

        [ContextMenu("PlayerPrefs から音量を読み込む")]
        private void LoadVolume()
        {
            // キーが存在しない場合は、第 2 引数の値が返ります。
            float volume = PlayerPrefs.GetFloat(VolumeKey, 1f);
            Debug.Log($"音量: {volume}");
        }
    }
}
