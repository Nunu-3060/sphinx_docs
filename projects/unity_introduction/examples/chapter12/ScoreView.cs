using TMPro;
using UnityEngine;

namespace UnityIntroduction.Chapter12
{
    /// <summary>
    /// スコアを TextMeshPro のテキストに表示します。
    /// </summary>
    public class ScoreView : MonoBehaviour
    {
        [SerializeField]
        private TextMeshProUGUI _scoreText;

        /// <summary>
        /// 表示するスコアを更新します。
        /// </summary>
        public void SetScore(int score)
        {
            _scoreText.text = $"Score: {score}";
        }
    }
}
