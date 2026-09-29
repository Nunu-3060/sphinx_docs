// 第 9 章 C# の発展的な機能
// 例外処理（try、catch、finally）と、null を扱うための演算子を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using System;
using UnityEngine;

public class ExceptionSample : MonoBehaviour
{
    private void Start()
    {
        // ---- 例外処理 ----
        try
        {
            int value = int.Parse("abc");
            Debug.Log($"変換結果: {value}");    // 例外が発生するので、この行は実行されない
        }
        catch (FormatException e)
        {
            Debug.Log($"数値に変換できなかった: {e.GetType().Name}");
        }
        finally
        {
            Debug.Log("finally ブロックは、例外の有無にかかわらず実行される。");
        }

        // 失敗することが予想できる処理は、例外を使わずに TryParse で書くのが一般的です。
        if (int.TryParse("123", out int parsed))
        {
            Debug.Log($"TryParse の結果: {parsed}");
        }

        // ---- null 許容値型 ----
        // int? は「int の値」か「値なし（null）」のどちらかを持てる型です。
        int? bestTime = null;
        Debug.Log($"記録あり: {bestTime.HasValue}");

        // ?? 演算子: 左辺が null のときに右辺の値を使います。
        int displayTime = bestTime ?? 999;
        Debug.Log($"表示する記録: {displayTime}");

        // ---- null 条件演算子 ----
        // ?. は、左辺が null ならメンバーにアクセスせずに null を返します。
        string playerName = null;
        int? length = playerName?.Length;
        Debug.Log($"名前の長さ: {length ?? 0}");
    }
}
