using UnityEngine;

namespace UnityIntroduction.Chapter10
{
    /// <summary>
    /// 衝突イベントとトリガーイベントの発生をログに表示します。
    /// </summary>
    /// <remarks>
    /// イベントを受け取るには、衝突する 2 つの GameObject の両方に Collider があり、
    /// 少なくとも一方に Rigidbody が付いている必要があります。
    /// 衝突イベントの場合は、少なくとも一方の Rigidbody の Is Kinematic が無効である必要があります。
    /// </remarks>
    public class CollisionReporter : MonoBehaviour
    {
        private void OnCollisionEnter(Collision collision)
        {
            // relativeVelocity は衝突した瞬間の相対速度です。
            float speed = collision.relativeVelocity.magnitude;
            Debug.Log($"{collision.gameObject.name} と衝突しました（相対速度 {speed:F2} m/s）。");
        }

        private void OnCollisionExit(Collision collision)
        {
            Debug.Log($"{collision.gameObject.name} から離れました。");
        }

        private void OnTriggerEnter(Collider other)
        {
            Debug.Log($"{other.gameObject.name} がトリガーに入りました。");
        }

        private void OnTriggerExit(Collider other)
        {
            Debug.Log($"{other.gameObject.name} がトリガーから出ました。");
        }
    }
}
