using System;
using System.Collections.Generic;

namespace UnityIntroduction.Chapter15
{
    /// <summary>
    /// ファイルに保存するデータです。
    /// </summary>
    /// <remarks>
    /// JsonUtility で変換できるのは、public フィールドと [SerializeField] を付けたフィールドです。
    /// プロパティや Dictionary は変換されません。
    /// </remarks>
    [Serializable]
    public class SaveData
    {
        public string PlayerName = "Player";

        public int HighScore;

        public List<string> ClearedStages = new List<string>();
    }
}
