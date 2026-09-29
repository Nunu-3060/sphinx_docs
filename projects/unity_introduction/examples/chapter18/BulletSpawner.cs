using UnityEngine;
using UnityEngine.Pool;

namespace UnityIntroduction.Chapter18
{
    /// <summary>
    /// オブジェクトプールを使って、弾を一定間隔で発射します。
    /// </summary>
    /// <remarks>
    /// 弾を毎回 Instantiate と Destroy で生成、破棄する代わりに、使い終わった弾を再利用します。
    /// </remarks>
    public class BulletSpawner : MonoBehaviour
    {
        [SerializeField]
        private PooledBullet _bulletPrefab;

        [SerializeField, Tooltip("発射する間隔（秒）")]
        private float _fireInterval = 0.1f;

        private ObjectPool<PooledBullet> _pool;
        private float _elapsed;

        private void Awake()
        {
            _pool = new ObjectPool<PooledBullet>(
                createFunc: CreateBullet,
                actionOnGet: bullet => bullet.gameObject.SetActive(true),
                actionOnRelease: bullet => bullet.gameObject.SetActive(false),
                actionOnDestroy: bullet => Destroy(bullet.gameObject),
                collectionCheck: true,
                defaultCapacity: 20,
                maxSize: 100);
        }

        private void Update()
        {
            _elapsed += Time.deltaTime;
            if (_elapsed < _fireInterval)
            {
                return;
            }

            _elapsed -= _fireInterval;

            // プールから弾を取り出します。空きが無ければ createFunc で新しく生成されます。
            PooledBullet bullet = _pool.Get();
            bullet.transform.SetPositionAndRotation(transform.position, transform.rotation);
        }

        private PooledBullet CreateBullet()
        {
            PooledBullet bullet = Instantiate(_bulletPrefab);
            bullet.SetPool(_pool);
            return bullet;
        }
    }
}
