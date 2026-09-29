// 第 17 章 コルーチンと非同期処理
// コルーチンを使って、1 秒ごとにカウントダウンを表示するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using System.Collections;
using UnityEngine;

public class CountdownCoroutine : MonoBehaviour
{
    [SerializeField] private int _count = 3;

    private void Start()
    {
        // StartCoroutine でコルーチンを開始します。
        StartCoroutine(Countdown());
    }

    // コルーチンは、戻り値の型を IEnumerator にしたメソッドです。
    private IEnumerator Countdown()
    {
        for (int i = _count; i > 0; i--)
        {
            Debug.Log(i);

            // yield return で処理を中断し、1 秒後にこの続きから再開します。
            yield return new WaitForSeconds(1f);
        }
        Debug.Log("スタート！");
    }
}
