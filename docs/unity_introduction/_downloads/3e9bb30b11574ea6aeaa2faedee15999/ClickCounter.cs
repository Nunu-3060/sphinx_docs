using UnityEngine;
using UnityEngine.UI;

namespace UnityIntroduction.Chapter12
{
    /// <summary>
    /// ボタンがクリックされた回数を数え、ScoreView に表示します。
    /// </summary>
    public class ClickCounter : MonoBehaviour
    {
        [SerializeField]
        private Button _button;

        [SerializeField]
        private ScoreView _scoreView;

        private int _count;

        private void Start()
        {
            _scoreView.SetScore(_count);
        }

        private void OnEnable()
        {
            // Inspector の On Click () に登録する代わりに、スクリプトから登録することもできます。
            _button.onClick.AddListener(OnButtonClicked);
        }

        private void OnDisable()
        {
            _button.onClick.RemoveListener(OnButtonClicked);
        }

        private void OnButtonClicked()
        {
            _count++;
            _scoreView.SetScore(_count);
        }
    }
}
