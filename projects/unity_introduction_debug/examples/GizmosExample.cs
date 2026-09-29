using UnityEngine;

/// <summary>
/// Debug.DrawRay と Gizmos を使って、目に見えない情報を Scene ビューに表示するサンプルです。
/// </summary>
public class GizmosExample : MonoBehaviour
{
    [SerializeField]
    private float searchRadius = 5f;

    [SerializeField]
    private float rayLength = 10f;

    private void Update()
    {
        // 前方に Ray を飛ばし、何かに当たったかどうかで線の色を変えます。
        Vector3 origin = transform.position;
        Vector3 direction = transform.forward;
        bool isHit = Physics.Raycast(origin, direction, out RaycastHit hit, rayLength);

        Color color = isHit ? Color.red : Color.green;
        float length = isHit ? hit.distance : rayLength;

        // Debug.DrawRay で描いた線は 1 フレームだけ表示されます。
        // Scene ビューに表示され、Game ビューでも Gizmos ボタンを有効にすると表示されます。
        Debug.DrawRay(origin, direction * length, color);
    }

    /// <summary>
    /// 常に呼び出されるギズモの描画処理です。再生していないときも呼び出されます。
    /// </summary>
    private void OnDrawGizmos()
    {
        // 索敵範囲を黄色いワイヤーフレームの球で表示します。
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, searchRadius);
    }

    /// <summary>
    /// この GameObject を選択しているときだけ呼び出されるギズモの描画処理です。
    /// </summary>
    private void OnDrawGizmosSelected()
    {
        // Ray の最大距離を水色の線で表示します。
        Gizmos.color = Color.cyan;
        Gizmos.DrawLine(transform.position, transform.position + transform.forward * rayLength);
    }
}
