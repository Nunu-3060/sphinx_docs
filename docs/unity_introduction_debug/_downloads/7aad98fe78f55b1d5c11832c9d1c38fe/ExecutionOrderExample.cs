using UnityEngine;

/// <summary>
/// イベント関数が呼び出される順序を Console ウィンドウに出力するサンプルです。
/// </summary>
/// <remarks>
/// 再生を開始・停止したり、Inspector ウィンドウでコンポーネントや GameObject の
/// 有効・無効を切り替えたりして、出力される順序を確認してください。
/// </remarks>
public class ExecutionOrderExample : MonoBehaviour
{
    private bool isFirstUpdate = true;
    private bool isFirstFixedUpdate = true;
    private bool isFirstLateUpdate = true;

    private void Awake()
    {
        // コンポーネントが無効でも、GameObject が有効であれば呼び出されます。
        Log("Awake");
    }

    private void OnEnable()
    {
        Log("OnEnable");
    }

    private void Start()
    {
        // コンポーネントが有効な場合に限り、最初の Update の直前に 1 回だけ呼び出されます。
        Log("Start");
    }

    private void FixedUpdate()
    {
        // 毎回出力すると Console ウィンドウが埋まってしまうため、最初の 1 回だけ出力します。
        if (isFirstFixedUpdate)
        {
            Log("FixedUpdate（最初の 1 回）");
            isFirstFixedUpdate = false;
        }
    }

    private void Update()
    {
        if (isFirstUpdate)
        {
            Log("Update（最初の 1 回）");
            isFirstUpdate = false;
        }
    }

    private void LateUpdate()
    {
        if (isFirstLateUpdate)
        {
            Log("LateUpdate（最初の 1 回）");
            isFirstLateUpdate = false;
        }
    }

    private void OnDisable()
    {
        Log("OnDisable");
    }

    private void OnDestroy()
    {
        Log("OnDestroy");
    }

    private void Log(string eventName)
    {
        // どのフレームで呼び出されたかが分かるように、フレーム番号も出力します。
        Debug.Log($"[フレーム {Time.frameCount}] {name}: {eventName}", this);
    }
}
