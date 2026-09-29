using UnityEngine;
using UnityEngine.InputSystem;

/// <summary>
/// クリックしたオブジェクトの表面に、ヒットエフェクトのプレハブを生成するサンプル。
/// シーン内の空の GameObject にアタッチして使う。
/// </summary>
/// <remarks>
/// ヒットエフェクトのプレハブは、次のように設定しておく。
/// ・Main モジュールの Looping を無効にし、Stop Action を Destroy にする（再生が終わったら自動で削除するため）。
/// ・パーティクルがローカル座標の Z 軸の正の向きに飛ぶようにする（面の法線の向きに飛ばすため）。
/// クリックの対象にするオブジェクトには、コライダーが必要である。
/// </remarks>
public class HitEffectSpawner : MonoBehaviour
{
    [SerializeField, Tooltip("生成するヒットエフェクトのプレハブ")]
    private ParticleSystem _hitEffectPrefab;

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

        // カメラからマウスの位置に向かうレイを飛ばし、当たったコライダーを調べる。
        Ray ray = _camera.ScreenPointToRay(mouse.position.ReadValue());
        if (Physics.Raycast(ray, out RaycastHit hit, _maxDistance))
        {
            // エフェクトの Z 軸が、当たった面の法線の向きになるように回転させる。
            Quaternion rotation = Quaternion.LookRotation(hit.normal);
            Instantiate(_hitEffectPrefab, hit.point, rotation);
        }
    }
}
