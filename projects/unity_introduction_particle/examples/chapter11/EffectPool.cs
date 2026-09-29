using UnityEngine;
using UnityEngine.Pool;

/// <summary>
/// エフェクトを使い回すためのオブジェクトプール。
/// シーン内の空の GameObject にアタッチし、PooledEffect を付けたプレハブを設定して使う。
/// </summary>
public class EffectPool : MonoBehaviour
{
    [SerializeField, Tooltip("使い回すエフェクトのプレハブ（PooledEffect を付けておく）")]
    private PooledEffect _effectPrefab;

    [SerializeField, Tooltip("最初に確保するリストの大きさ")]
    private int _defaultCapacity = 10;

    [SerializeField, Tooltip("プールに保持するエフェクトの最大数")]
    private int _maxSize = 50;

    private ObjectPool<PooledEffect> _pool;

    private void Awake()
    {
        _pool = new ObjectPool<PooledEffect>(
            CreateEffect,
            OnGetEffect,
            OnReleaseEffect,
            OnDestroyEffect,
            true,
            _defaultCapacity,
            _maxSize);
    }

    /// <summary>
    /// 指定した位置と向きでエフェクトを再生する。
    /// </summary>
    public void Play(Vector3 position, Quaternion rotation)
    {
        // プールに空きがあればそれを使い、なければ新しく生成する。
        PooledEffect effect = _pool.Get();
        effect.transform.SetPositionAndRotation(position, rotation);
        effect.Play();
    }

    // プールに空きがないときに呼ばれ、新しいエフェクトを生成する。
    private PooledEffect CreateEffect()
    {
        PooledEffect effect = Instantiate(_effectPrefab, transform);
        effect.SetPool(_pool);
        return effect;
    }

    // プールから取り出すときに呼ばれる。
    private void OnGetEffect(PooledEffect effect)
    {
        effect.gameObject.SetActive(true);
    }

    // プールに戻すときに呼ばれる。
    private void OnReleaseEffect(PooledEffect effect)
    {
        effect.gameObject.SetActive(false);
    }

    // プールがいっぱいで戻せないときに呼ばれ、エフェクトを削除する。
    private void OnDestroyEffect(PooledEffect effect)
    {
        Destroy(effect.gameObject);
    }
}
