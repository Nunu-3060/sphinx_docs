using Unity.Profiling;
using UnityEngine;

/// <summary>
/// ProfilerMarker を使って、任意の処理区間を Profiler に表示するサンプルです。
/// </summary>
/// <remarks>
/// 再生中に Profiler ウィンドウの CPU Usage モジュールを開き、
/// 「ProfilerMarkerExample.」で始まる項目を探してください。
/// ProfilerMarker の計測処理は、Development Build ではないビルドでは自動的に取り除かれます。
/// </remarks>
public class ProfilerMarkerExample : MonoBehaviour
{
    // マーカーは生成にコストがかかるため、static readonly フィールドとして一度だけ生成します。
    private static readonly ProfilerMarker s_CalculateMarker =
        new ProfilerMarker("ProfilerMarkerExample.Calculate");

    private static readonly ProfilerMarker s_ApplyMarker =
        new ProfilerMarker("ProfilerMarkerExample.Apply");

    [SerializeField, Tooltip("1 フレームあたりの計算回数。増やすと処理が重くなります。")]
    private int iterationCount = 100000;

    private float result;

    private void Update()
    {
        // using ブロックを使う方法です。ブロックを抜けると自動的に計測が終了します。
        using (s_CalculateMarker.Auto())
        {
            result = Calculate();
        }

        // Begin と End を明示的に呼び出す方法です。End の呼び出し忘れに注意してください。
        s_ApplyMarker.Begin();
        transform.localScale = Vector3.one * (1f + Mathf.Abs(result) * 0.0001f);
        s_ApplyMarker.End();
    }

    /// <summary>
    /// 計測対象とする、意図的に重くした処理です。
    /// </summary>
    private float Calculate()
    {
        float sum = 0f;
        for (int i = 0; i < iterationCount; i++)
        {
            sum += Mathf.Sin(i * 0.001f);
        }

        return sum;
    }
}
