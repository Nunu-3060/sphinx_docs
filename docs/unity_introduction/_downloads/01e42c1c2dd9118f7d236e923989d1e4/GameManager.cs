using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace UnityIntroduction.RollABall
{
    /// <summary>
    /// スコアの管理、ゲームクリアとゲームオーバーの判定、リトライを行います。
    /// </summary>
    public class GameManager : MonoBehaviour
    {
        [SerializeField]
        private PlayerController _player;

        [SerializeField]
        private TextMeshProUGUI _scoreText;

        [SerializeField]
        private TextMeshProUGUI _messageText;

        [SerializeField]
        private GameObject _retryButton;

        [SerializeField, Tooltip("プレイヤーがこの高さより下に落ちたらゲームオーバー")]
        private float _fallThreshold = -10f;

        private int _score;
        private int _totalPickups;
        private bool _isFinished;

        private void OnEnable()
        {
            Pickup.Collected += OnPickupCollected;
        }

        private void OnDisable()
        {
            // static なイベントの購読を解除し忘れると、シーンを読み直した後も
            // 破棄済みの GameManager が呼ばれてしまいます。
            Pickup.Collected -= OnPickupCollected;
        }

        private void Start()
        {
            // シーンに置かれている Pickup の数を数えます。
            _totalPickups = FindObjectsByType<Pickup>(FindObjectsSortMode.None).Length;

            UpdateScoreText();
            _messageText.gameObject.SetActive(false);
            _retryButton.SetActive(false);
        }

        private void Update()
        {
            if (!_isFinished && _player.transform.position.y < _fallThreshold)
            {
                Finish("Game Over");
            }
        }

        /// <summary>
        /// 現在のシーンを読み込み直して、ゲームを最初からやり直します。
        /// </summary>
        /// <remarks>
        /// Retry ボタンの On Click () から呼び出します。
        /// </remarks>
        public void Retry()
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        }

        private void OnPickupCollected(Pickup pickup)
        {
            if (_isFinished)
            {
                return;
            }

            _score++;
            UpdateScoreText();

            if (_score >= _totalPickups)
            {
                Finish("Clear!");
            }
        }

        private void UpdateScoreText()
        {
            _scoreText.text = $"Score: {_score} / {_totalPickups}";
        }

        private void Finish(string message)
        {
            _isFinished = true;
            _player.StopMoving();

            _messageText.text = message;
            _messageText.gameObject.SetActive(true);
            _retryButton.SetActive(true);
        }
    }
}
