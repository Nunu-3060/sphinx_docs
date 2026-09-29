// 第 11 章 イベント関数とライフサイクル
// 主なイベント関数が呼ばれた順番を Console ウィンドウに表示するスクリプトです。
// 使い方: シーン内の GameObject にアタッチして Play ボタンを押します。
//         Play モード中に Inspector ウィンドウでコンポーネントのチェックを外したり、Play モードを終了したりして、
//         OnDisable や OnDestroy が呼ばれる様子も確認してください。
using UnityEngine;

public class LifecycleLogger : MonoBehaviour
{
    // 毎フレーム呼ばれる関数は、最初の 1 回だけ表示するためのフラグです。
    private bool _isFirstFixedUpdate = true;
    private bool _isFirstUpdate = true;
    private bool _isFirstLateUpdate = true;

    private void Awake()
    {
        Debug.Log("Awake: インスタンスが作られた直後に 1 回");
    }

    private void OnEnable()
    {
        Debug.Log("OnEnable: 有効になるたびに");
    }

    private void Start()
    {
        Debug.Log("Start: 最初の Update の直前に 1 回");
    }

    private void FixedUpdate()
    {
        if (_isFirstFixedUpdate)
        {
            Debug.Log($"FixedUpdate: 一定間隔（{Time.fixedDeltaTime} 秒）ごと");
            _isFirstFixedUpdate = false;
        }
    }

    private void Update()
    {
        if (_isFirstUpdate)
        {
            Debug.Log("Update: 毎フレーム");
            _isFirstUpdate = false;
        }
    }

    private void LateUpdate()
    {
        if (_isFirstLateUpdate)
        {
            Debug.Log("LateUpdate: 毎フレーム、すべての Update の後");
            _isFirstLateUpdate = false;
        }
    }

    private void OnDisable()
    {
        Debug.Log("OnDisable: 無効になるたびに");
    }

    private void OnDestroy()
    {
        Debug.Log("OnDestroy: 破棄される直前に 1 回");
    }
}
