// 第 19 章 簡単なゲームを作る
// 取得したアイテムの数の管理、UI の更新、クリア判定、やり直しを担当するスクリプトです。
// 使い方: 空の GameObject（名前は GameManager）にアタッチし、Score Text と Clear Message を設定します。
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI _scoreText;
    [SerializeField] private GameObject _clearMessage;

    private int _collectedCount;
    private int _totalCount;
    private bool _isCleared;

    // どのスクリプトからも GameManager.Instance で参照できるようにします（シングルトン）。
    public static GameManager Instance { get; private set; }

    private void Awake()
    {
        Instance = this;
    }

    private void Start()
    {
        // シーンに配置されているアイテムの数を数えます。
        _totalCount = FindObjectsByType<Pickup>(FindObjectsSortMode.None).Length;
        _clearMessage.SetActive(false);
        UpdateScoreText();
    }

    private void Update()
    {
        // クリア後に R キーを押すと、最初からやり直します。
        // 特定のキーを案内しているため、入力アクションではなくキーボードを直接読み取ります（第 14 章）。
        Keyboard keyboard = Keyboard.current;
        if (_isCleared && keyboard != null && keyboard.rKey.wasPressedThisFrame)
        {
            Restart();
        }
    }

    private void OnDestroy()
    {
        // シーンを読み込み直すとこのオブジェクトは破棄されるため、参照を消しておきます。
        if (Instance == this)
        {
            Instance = null;
        }
    }

    // アイテムが取得されたときに Pickup から呼ばれます。
    public void CollectPickup()
    {
        if (_isCleared)
        {
            return;
        }

        _collectedCount++;
        UpdateScoreText();

        if (_collectedCount >= _totalCount)
        {
            _isCleared = true;
            _clearMessage.SetActive(true);
        }
    }

    public void Restart()
    {
        // 現在のシーンを読み込み直します。
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

    private void UpdateScoreText()
    {
        _scoreText.text = $"Score: {_collectedCount} / {_totalCount}";
    }
}
