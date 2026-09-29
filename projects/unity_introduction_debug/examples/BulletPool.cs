using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Pool;

/// <summary>
/// ObjectPool&lt;T&gt; を使って弾の GameObject を使い回すサンプルです。
/// </summary>
/// <remarks>
/// Inspector ウィンドウの Bullet Prefab に、弾として使うプレハブ（例: 小さな Sphere）を設定してください。
/// 再生すると、一定間隔で前方に弾を発射し続けます。
/// 弾は一定時間後に破棄されるのではなく、非表示にしてプールに戻され、次の発射で再利用されます。
/// </remarks>
public class BulletPool : MonoBehaviour
{
    [SerializeField]
    private GameObject bulletPrefab;

    [SerializeField, Tooltip("発射間隔（秒）")]
    private float fireInterval = 0.1f;

    [SerializeField, Tooltip("弾の速さ（単位/秒）")]
    private float bulletSpeed = 20f;

    [SerializeField, Tooltip("弾が消えるまでの時間（秒）")]
    private float bulletLifetime = 2f;

    [SerializeField, Tooltip("最初に確保するプールの容量")]
    private int defaultCapacity = 20;

    [SerializeField, Tooltip("プールに保持する弾の最大数。超えた分は破棄されます。")]
    private int maxSize = 100;

    /// <summary>
    /// 発射中の弾の情報です。
    /// </summary>
    private struct ActiveBullet
    {
        public GameObject GameObject;
        public float ReleaseTime;
    }

    private readonly List<ActiveBullet> activeBullets = new List<ActiveBullet>();
    private ObjectPool<GameObject> pool;
    private float nextFireTime;

    private void Awake()
    {
        pool = new ObjectPool<GameObject>(
            createFunc: CreateBullet,
            actionOnGet: bullet => bullet.SetActive(true),
            actionOnRelease: bullet => bullet.SetActive(false),
            actionOnDestroy: bullet => Destroy(bullet),
            collectionCheck: true,
            defaultCapacity: defaultCapacity,
            maxSize: maxSize);
    }

    private void Update()
    {
        if (Time.time >= nextFireTime)
        {
            Fire();
            nextFireTime = Time.time + fireInterval;
        }

        MoveAndReleaseBullets();
    }

    /// <summary>
    /// プールが空のときに呼び出され、新しい弾を生成します。
    /// </summary>
    private GameObject CreateBullet()
    {
        return Instantiate(bulletPrefab);
    }

    private void Fire()
    {
        // Instantiate の代わりに、プールから弾を取り出します。
        GameObject bullet = pool.Get();

        // 再利用される弾には前回の状態が残っているため、取り出すたびに位置と向きを設定し直します。
        bullet.transform.SetPositionAndRotation(transform.position, transform.rotation);

        activeBullets.Add(new ActiveBullet
        {
            GameObject = bullet,
            ReleaseTime = Time.time + bulletLifetime,
        });
    }

    private void MoveAndReleaseBullets()
    {
        // 要素を削除しながら走査するため、末尾から処理します。
        for (int i = activeBullets.Count - 1; i >= 0; i--)
        {
            ActiveBullet activeBullet = activeBullets[i];

            if (Time.time >= activeBullet.ReleaseTime)
            {
                // Destroy の代わりに、プールへ戻します。
                pool.Release(activeBullet.GameObject);
                activeBullets.RemoveAt(i);
                continue;
            }

            Transform bulletTransform = activeBullet.GameObject.transform;
            bulletTransform.position += bulletTransform.forward * (bulletSpeed * Time.deltaTime);
        }
    }

    private void OnDestroy()
    {
        // プールに保持している弾をすべて破棄します。発射中の弾も破棄します。
        foreach (ActiveBullet activeBullet in activeBullets)
        {
            Destroy(activeBullet.GameObject);
        }

        activeBullets.Clear();
        pool?.Clear();
    }
}
