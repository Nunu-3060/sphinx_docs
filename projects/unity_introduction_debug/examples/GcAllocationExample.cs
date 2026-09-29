using System.Collections.Generic;
using System.Linq;
using Unity.Profiling;
using UnityEngine;

/// <summary>
/// GC アロケーションが発生するコードと、発生しないように改善したコードを比較するサンプルです。
/// </summary>
/// <remarks>
/// 再生中に Profiler ウィンドウの CPU Usage モジュールを開き、
/// 「GcAllocationExample.Tick」の GC Alloc 列を確認してください。
/// Inspector ウィンドウで Use Optimized Code を切り替えると、値の変化を比較できます。
/// </remarks>
public class GcAllocationExample : MonoBehaviour
{
    private static readonly ProfilerMarker s_TickMarker =
        new ProfilerMarker("GcAllocationExample.Tick");

    [SerializeField, Tooltip("オンにすると改善後のコードを実行します。")]
    private bool useOptimizedCode = false;

    [SerializeField]
    private int valueCount = 1000;

    private int[] values;
    private int score;
    private int lastScore = -1;
    private string scoreText = string.Empty;
    private int evenCount;

    // 改善後のコードで使い回すリストです。
    private readonly List<int> evenValues = new List<int>();

    private void Awake()
    {
        values = new int[valueCount];
        for (int i = 0; i < values.Length; i++)
        {
            values[i] = Random.Range(0, 100);
        }
    }

    private void Update()
    {
        // スコアは 60 フレームごとに増えるものとします。
        if (Time.frameCount % 60 == 0)
        {
            score++;
        }

        using (s_TickMarker.Auto())
        {
            if (useOptimizedCode)
            {
                TickWithoutAllocation();
            }
            else
            {
                TickWithAllocation();
            }
        }
    }

    /// <summary>
    /// 毎フレーム GC アロケーションが発生するコードです。
    /// </summary>
    private void TickWithAllocation()
    {
        // スコアが変わっていなくても、毎フレーム新しい文字列が生成されます。
        scoreText = "Score: " + score;

        // Where は列挙用のオブジェクトを、ToList は新しいリストを毎回生成します。
        List<int> evens = values.Where(v => v % 2 == 0).ToList();
        evenCount = evens.Count;
    }

    /// <summary>
    /// GC アロケーションが発生しないように改善したコードです。
    /// </summary>
    private void TickWithoutAllocation()
    {
        // スコアが変わったときだけ文字列を生成します。
        if (score != lastScore)
        {
            scoreText = "Score: " + score;
            lastScore = score;
        }

        // 新しいリストを作らず、フィールドのリストを Clear して使い回します。
        evenValues.Clear();
        for (int i = 0; i < values.Length; i++)
        {
            if (values[i] % 2 == 0)
            {
                evenValues.Add(values[i]);
            }
        }

        evenCount = evenValues.Count;
    }

    private void OnGUI()
    {
        // 結果を確認するための表示です。計測区間の外なので、比較には影響しません。
        GUILayout.Label($"{scoreText} / 偶数の個数: {evenCount}");
    }
}
