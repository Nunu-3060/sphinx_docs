// 第 17 章 コルーチンと非同期処理
// コルーチンを使って、オブジェクトを一定間隔で点滅させるスクリプトです。
// スペースキーで点滅の開始と停止を切り替えます。
// 使い方: シーンに Cube を作成してアタッチし、Play モード中にスペースキーを押します。
using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;

public class BlinkCoroutine : MonoBehaviour
{
    [SerializeField] private float _interval = 0.2f;

    private Renderer _renderer;

    // 実行中のコルーチンです。停止するときに使います。
    private Coroutine _blinkCoroutine;

    private void Awake()
    {
        _renderer = GetComponent<Renderer>();
    }

    private void Update()
    {
        // 動作確認用の操作なので、入力アクションではなくキーボードを直接読み取ります（第 14 章）。
        Keyboard keyboard = Keyboard.current;
        if (keyboard == null || !keyboard.spaceKey.wasPressedThisFrame)
        {
            return;
        }

        if (_blinkCoroutine == null)
        {
            _blinkCoroutine = StartCoroutine(Blink());
        }
        else
        {
            // StopCoroutine でコルーチンを途中で止めます。
            StopCoroutine(_blinkCoroutine);
            _blinkCoroutine = null;
            _renderer.enabled = true;
        }
    }

    private IEnumerator Blink()
    {
        // 同じ待ち時間を何度も使うので、WaitForSeconds を 1 回だけ作って使い回します。
        WaitForSeconds wait = new WaitForSeconds(_interval);

        // while (true) で無限にくり返しますが、yield return で毎回中断するため、ゲームは止まりません。
        while (true)
        {
            _renderer.enabled = !_renderer.enabled;
            yield return wait;
        }
    }
}
