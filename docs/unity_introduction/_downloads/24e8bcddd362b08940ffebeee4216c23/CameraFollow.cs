using UnityEngine;

namespace UnityIntroduction.RollABall
{
    /// <summary>
    /// 対象との位置関係を保ったまま、カメラを対象に追従させます。
    /// </summary>
    public class CameraFollow : MonoBehaviour
    {
        [SerializeField, Tooltip("追従する対象")]
        private Transform _target;

        private Vector3 _offset;

        private void Start()
        {
            // 再生開始時のカメラと対象の位置の差を覚えておきます。
            _offset = transform.position - _target.position;
        }

        private void LateUpdate()
        {
            // 対象の移動が終わった後の LateUpdate でカメラを動かすと、表示のずれを防げます。
            transform.position = _target.position + _offset;
        }
    }
}
