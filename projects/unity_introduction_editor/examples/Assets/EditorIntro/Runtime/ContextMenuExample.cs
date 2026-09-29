using UnityEngine;

namespace EditorIntro
{
    /// <summary>
    /// 第 3 章のサンプルです。
    /// ContextMenu 属性と ContextMenuItem 属性の使い方を示します。
    /// </summary>
    public class ContextMenuExample : MonoBehaviour
    {
        // フィールド名を右クリックすると「Randomize Name」が表示されます。
        // 第 2 引数には、実行するメソッドの名前を指定します。
        [ContextMenuItem("Randomize Name", nameof(RandomizeName))]
        [SerializeField] private string displayName = "Player";

        [SerializeField] private int score = 100;

        public string DisplayName => displayName;
        public int Score => score;

        // コンポーネント右上の「⋮」ボタン（またはヘッダーの右クリック）で表示されるメニューに
        // 「Reset Score」を追加します。
        [ContextMenu("Reset Score")]
        private void ResetScore()
        {
            score = 0;
        }

        private void RandomizeName()
        {
            displayName = $"Player{Random.Range(0, 1000):D3}";
        }
    }
}
