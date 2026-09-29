using System.Diagnostics;
using UnityEngine;

/// <summary>
/// リリースビルドでログ出力を呼び出し箇所ごと取り除くためのラッパークラスです。
/// </summary>
/// <remarks>
/// <para>
/// [Conditional] 属性が付いたメソッドは、指定したシンボルがどれも定義されていない場合、
/// 呼び出し箇所ごとコンパイル結果から削除されます。
/// このとき、引数に渡す文字列の生成処理も実行されません。
/// </para>
/// <para>
/// UNITY_EDITOR はエディター上で常に定義されるシンボルです。
/// ENABLE_LOG は独自のシンボルで、ビルドでもログを出力したい場合に
/// Project Settings の Player > Other Settings > Scripting Define Symbols で定義します。
/// </para>
/// <para>
/// 使用例: DebugLogger.Log($"スコア: {score}", this);
/// </para>
/// </remarks>
public static class DebugLogger
{
    // System.Diagnostics にも Debug クラスがあるため、UnityEngine.Debug と明記しています。

    [Conditional("UNITY_EDITOR")]
    [Conditional("ENABLE_LOG")]
    public static void Log(object message, Object context = null)
    {
        UnityEngine.Debug.Log(message, context);
    }

    [Conditional("UNITY_EDITOR")]
    [Conditional("ENABLE_LOG")]
    public static void LogWarning(object message, Object context = null)
    {
        UnityEngine.Debug.LogWarning(message, context);
    }

    // エラーは製品版でも原因の調査に必要になることが多いため、
    // このクラスには含めず、UnityEngine.Debug.LogError を直接使います。
}
