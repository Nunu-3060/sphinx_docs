using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// パーティクルが衝突した位置に、別の Particle System で水しぶきを出すサンプル。
/// 衝突するパーティクルを出す Particle System にアタッチして使う。
/// </summary>
/// <remarks>
/// アタッチする Particle System は、次のように設定しておく。
/// ・Collision モジュールを有効にし、Type を World にする。
/// ・Collision モジュールの Send Collision Messages を有効にする。
/// 水しぶき用の Particle System は、Simulation Space を World にし、Emission モジュールを無効にしておく。
/// </remarks>
[RequireComponent(typeof(ParticleSystem))]
public class ParticleCollisionHandler : MonoBehaviour
{
    [SerializeField, Tooltip("衝突した位置に放出する Particle System")]
    private ParticleSystem _splashEffect;

    [SerializeField, Tooltip("1 回の衝突で放出するパーティクルの数")]
    private int _splashCount = 5;

    private ParticleSystem _particleSystem;

    // 衝突の情報を受け取るリスト。毎回作り直さないように使い回す。
    private readonly List<ParticleCollisionEvent> _collisionEvents = new List<ParticleCollisionEvent>();

    private void Awake()
    {
        _particleSystem = GetComponent<ParticleSystem>();
    }

    // パーティクルがコライダーに衝突したときに、Unity から呼ばれる。
    // other は、衝突した相手の GameObject である。
    private void OnParticleCollision(GameObject other)
    {
        if (_splashEffect == null)
        {
            return;
        }

        // other との衝突の情報を取得する。戻り値は衝突の数である。
        int count = _particleSystem.GetCollisionEvents(other, _collisionEvents);

        for (int i = 0; i < count; i++)
        {
            // intersection は、衝突した位置（ワールド座標）である。
            // applyShapeToPosition を true にすると、Shape モジュールの形の分だけ位置をばらつかせる。
            ParticleSystem.EmitParams emitParams = new ParticleSystem.EmitParams
            {
                position = _collisionEvents[i].intersection,
                applyShapeToPosition = true,
            };

            _splashEffect.Emit(emitParams, _splashCount);
        }
    }
}
