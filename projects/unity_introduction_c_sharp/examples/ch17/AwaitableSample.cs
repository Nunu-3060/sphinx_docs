// 第 17 章 コルーチンと非同期処理
// async と await（Awaitable）を使って、CountdownCoroutine.cs と同じカウントダウンを書いたスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using System;
using UnityEngine;

public class AwaitableSample : MonoBehaviour
{
    [SerializeField] private int _count = 3;

    // Start は、戻り値の型を Awaitable にして async メソッドにすることができます。
    private async Awaitable Start()
    {
        try
        {
            for (int i = _count; i > 0; i--)
            {
                Debug.Log(i);

                // 1 秒待ってから続きを実行します。
                // destroyCancellationToken を渡すと、待っている間にこのオブジェクトが破棄されたときに処理が中止されます。
                await Awaitable.WaitForSecondsAsync(1f, destroyCancellationToken);
            }
            Debug.Log("スタート！");
        }
        catch (OperationCanceledException)
        {
            // 処理が中止されたときは、ここに来ます。
            Debug.Log("カウントダウンが中止された。");
        }
    }
}
