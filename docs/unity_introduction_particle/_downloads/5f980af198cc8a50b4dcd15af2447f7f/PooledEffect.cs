using UnityEngine;
using UnityEngine.Pool;

/// <summary>
/// EffectPool で使い回すエフェクト。
/// エフェクトのプレハブのルートの GameObject（Particle System を持つもの）にアタッチして使う。
/// </summary>
/// <remarks>
/// プレハブの Main モジュールは、Looping と Play On Awake を無効にしておく。
/// 再生が終わると、自分をプールに戻す。
/// </remarks>
[RequireComponent(typeof(ParticleSystem))]
public class PooledEffect : MonoBehaviour
{
    private ParticleSystem _particleSystem;
    private IObjectPool<PooledEffect> _pool;

    private void Awake()
    {
        _particleSystem = GetComponent<ParticleSystem>();

        // 再生が終わったときに OnParticleSystemStopped が呼ばれるようにする。
        ParticleSystem.MainModule main = _particleSystem.main;
        main.stopAction = ParticleSystemStopAction.Callback;
    }

    /// <summary>
    /// 戻り先のプールを設定する。
    /// </summary>
    public void SetPool(IObjectPool<PooledEffect> pool)
    {
        _pool = pool;
    }

    /// <summary>
    /// エフェクトを最初から再生する。
    /// </summary>
    public void Play()
    {
        _particleSystem.Play(true);
    }

    // Stop Action が Callback のとき、すべてのパーティクルが消えて再生が終わると、Unity から呼ばれる。
    private void OnParticleSystemStopped()
    {
        if (_pool != null)
        {
            _pool.Release(this);
        }
        else
        {
            // プールを使わずに生成された場合は、そのまま削除する。
            Destroy(gameObject);
        }
    }
}
