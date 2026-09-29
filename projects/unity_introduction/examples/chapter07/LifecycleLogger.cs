using UnityEngine;

namespace UnityIntroduction.Chapter07
{
    /// <summary>
    /// イベント関数が呼ばれた順番を Console ウィンドウに表示します。
    /// </summary>
    /// <remarks>
    /// Update などの毎フレーム呼ばれるイベント関数は、ログが大量に出ないように
    /// 最初の 1 回だけ表示します。
    /// </remarks>
    public class LifecycleLogger : MonoBehaviour
    {
        private bool _hasLoggedFixedUpdate;
        private bool _hasLoggedUpdate;
        private bool _hasLoggedLateUpdate;

        private void Awake()
        {
            Log(nameof(Awake));
        }

        private void OnEnable()
        {
            Log(nameof(OnEnable));
        }

        private void Start()
        {
            Log(nameof(Start));
        }

        private void FixedUpdate()
        {
            if (!_hasLoggedFixedUpdate)
            {
                Log(nameof(FixedUpdate));
                _hasLoggedFixedUpdate = true;
            }
        }

        private void Update()
        {
            if (!_hasLoggedUpdate)
            {
                Log(nameof(Update));
                _hasLoggedUpdate = true;
            }
        }

        private void LateUpdate()
        {
            if (!_hasLoggedLateUpdate)
            {
                Log(nameof(LateUpdate));
                _hasLoggedLateUpdate = true;
            }
        }

        private void OnDisable()
        {
            Log(nameof(OnDisable));
        }

        private void OnDestroy()
        {
            Log(nameof(OnDestroy));
        }

        private static void Log(string eventName)
        {
            // Time.frameCount はゲームの開始からのフレーム数です。
            Debug.Log($"フレーム {Time.frameCount}: {eventName}");
        }
    }
}
