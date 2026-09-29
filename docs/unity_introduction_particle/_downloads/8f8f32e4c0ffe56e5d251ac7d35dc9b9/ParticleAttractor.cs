using UnityEngine;

/// <summary>
/// 放出済みのパーティクルを、目標の位置に向かって加速させるサンプル。
/// Particle System を持つ GameObject にアタッチして使う。
/// </summary>
/// <remarks>
/// パーティクルの位置は、Simulation Space で選んだ座標系で表される。
/// このサンプルでは目標の位置をワールド座標で扱うため、Simulation Space を World にしておく。
/// </remarks>
[RequireComponent(typeof(ParticleSystem))]
public class ParticleAttractor : MonoBehaviour
{
    [SerializeField, Tooltip("パーティクルを引き寄せる目標")]
    private Transform _target;

    [SerializeField, Tooltip("目標に向かう加速度の大きさ（m/s²）")]
    private float _acceleration = 5f;

    private ParticleSystem _particleSystem;

    // パーティクルの情報を受け取る配列。毎フレーム作り直さないように使い回す。
    private ParticleSystem.Particle[] _particles;

    private void Awake()
    {
        _particleSystem = GetComponent<ParticleSystem>();

        // 同時に存在できる最大数の分だけ、配列を確保しておく。
        _particles = new ParticleSystem.Particle[_particleSystem.main.maxParticles];
    }

    // Particle System の更新が済んだ後に処理するため、LateUpdate を使う。
    private void LateUpdate()
    {
        if (_target == null)
        {
            return;
        }

        // 現在のパーティクルを配列にコピーする。戻り値はコピーした数である。
        int count = _particleSystem.GetParticles(_particles);

        Vector3 targetPosition = _target.position;
        float deltaTime = Time.deltaTime;

        for (int i = 0; i < count; i++)
        {
            // 目標の方向に、加速度 × 経過時間だけ速度を加える。
            Vector3 direction = (targetPosition - _particles[i].position).normalized;
            _particles[i].velocity += direction * (_acceleration * deltaTime);
        }

        // 変更した配列を Particle System に書き戻す。
        _particleSystem.SetParticles(_particles, count);
    }
}
