using UnityEngine;
using UnityEngine.InputSystem;

/// <summary>
/// 第 10 章の HitEffectSpawner を、EffectPool を使う形に書き換えたサンプル。
/// シーン内の空の GameObject にアタッチし、EffectPool を設定して使う。
/// </summary>
public class PooledHitEffectSpawner : MonoBehaviour
{
    [SerializeField, Tooltip("エフェクトを取り出すプール")]
    private EffectPool _effectPool;

    [SerializeField, Tooltip("レイの最大距離")]
    private float _maxDistance = 100f;

    private Camera _camera;

    private void Awake()
    {
        _camera = Camera.main;
    }

    private void Update()
    {
        Mouse mouse = Mouse.current;
        if (mouse == null || !mouse.leftButton.wasPressedThisFrame)
        {
            return;
        }

        Ray ray = _camera.ScreenPointToRay(mouse.position.ReadValue());
        if (Physics.Raycast(ray, out RaycastHit hit, _maxDistance))
        {
            // Instantiate の代わりに、プールからエフェクトを取り出して再生する。
            Quaternion rotation = Quaternion.LookRotation(hit.normal);
            _effectPool.Play(hit.point, rotation);
        }
    }
}
