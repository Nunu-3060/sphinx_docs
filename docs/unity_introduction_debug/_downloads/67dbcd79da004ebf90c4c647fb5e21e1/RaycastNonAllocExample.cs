using UnityEngine;

/// <summary>
/// Physics.RaycastAll の代わりに Physics.RaycastNonAlloc を使い、
/// GC アロケーションを発生させずに複数の衝突を取得するサンプルです。
/// </summary>
public class RaycastNonAllocExample : MonoBehaviour
{
    [SerializeField]
    private float maxDistance = 20f;

    [SerializeField, Tooltip("Ray が当たる対象のレイヤー")]
    private LayerMask targetLayers = ~0;

    // 結果を受け取る配列は、フィールドとして一度だけ確保して使い回します。
    // 取得できる衝突の数は、この配列の長さが上限になります。
    private readonly RaycastHit[] hits = new RaycastHit[16];

    // 同じ警告を毎フレーム出力しないためのフラグです。
    private bool hasWarned;

    private void Update()
    {
        // 悪い例: RaycastAll は呼び出すたびに新しい配列を生成します。
        // RaycastHit[] allHits = Physics.RaycastAll(transform.position, transform.forward, maxDistance, targetLayers);

        // 良い例: 戻り値は実際に配列へ書き込まれた衝突の数です。
        int hitCount = Physics.RaycastNonAlloc(
            transform.position, transform.forward, hits, maxDistance, targetLayers);

        // 配列の長さではなく、hitCount までを処理します。
        // 結果は距離の順に並んでいるとは限らないことにも注意してください。
        for (int i = 0; i < hitCount; i++)
        {
            Debug.DrawLine(transform.position, hits[i].point, Color.red);
        }

        if (hitCount == hits.Length && !hasWarned)
        {
            // 配列がいっぱいの場合、取得しきれなかった衝突がある可能性があります。
            Debug.LogWarning("衝突の数が配列の長さに達しました。配列を大きくすることを検討してください。", this);
            hasWarned = true;
        }
    }
}
