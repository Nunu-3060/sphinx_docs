// 第 16 章 物理演算と衝突判定
// 衝突（Collision）とトリガー（Trigger）のイベントを Console ウィンドウに表示するスクリプトです。
// 使い方: Rigidbody と Collider を持つ GameObject にアタッチします。
//         トリガーを試すときは、相手の Collider の Is Trigger にチェックを入れます。
using UnityEngine;

public class CollisionReporter : MonoBehaviour
{
    // ---- 衝突: どちらの Collider も Is Trigger がオフのとき ----
    private void OnCollisionEnter(Collision collision)
    {
        // relativeVelocity は、ぶつかった瞬間の 2 つの物体の相対速度です。
        Debug.Log($"{collision.gameObject.name} に衝突した（相対速度: {collision.relativeVelocity.magnitude:F2} m/s）");
    }

    private void OnCollisionExit(Collision collision)
    {
        Debug.Log($"{collision.gameObject.name} から離れた。");
    }

    // ---- トリガー: どちらかの Collider の Is Trigger がオンのとき ----
    private void OnTriggerEnter(Collider other)
    {
        // タグの比較には、tag == "..." ではなく CompareTag を使います。
        if (other.CompareTag("Player"))
        {
            Debug.Log("プレイヤーが範囲に入った。");
        }
        else
        {
            Debug.Log($"{other.name} が範囲に入った。");
        }
    }

    private void OnTriggerExit(Collider other)
    {
        Debug.Log($"{other.name} が範囲から出た。");
    }
}
