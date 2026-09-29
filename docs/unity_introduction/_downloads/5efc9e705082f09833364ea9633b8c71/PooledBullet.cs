using UnityEngine;
using UnityEngine.Pool;

namespace UnityIntroduction.Chapter18
{
    /// <summary>
    /// まっすぐ飛び、一定時間が経過するとプールに戻る弾です。
    /// </summary>
    public class PooledBullet : MonoBehaviour
    {
        [SerializeField, Tooltip("1 秒あたりの移動量（m/s）")]
        private float _speed = 20f;

        [SerializeField, Tooltip("プールに戻るまでの時間（秒）")]
        private float _lifetime = 2f;

        private IObjectPool<PooledBullet> _pool;
        private float _elapsed;

        /// <summary>
        /// 戻り先のプールを設定します。
        /// </summary>
        public void SetPool(IObjectPool<PooledBullet> pool)
        {
            _pool = pool;
        }

        private void OnEnable()
        {
            // 再利用されるたびに呼ばれるので、ここで状態を初期化します。
            _elapsed = 0f;
        }

        private void Update()
        {
            transform.Translate(Vector3.forward * _speed * Time.deltaTime);

            _elapsed += Time.deltaTime;
            if (_elapsed >= _lifetime)
            {
                // Destroy する代わりにプールへ戻します。
                _pool.Release(this);
            }
        }
    }
}
