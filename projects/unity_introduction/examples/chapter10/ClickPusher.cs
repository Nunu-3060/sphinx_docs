using UnityEngine;
using UnityEngine.InputSystem;

namespace UnityIntroduction.Chapter10
{
    /// <summary>
    /// クリックした位置にレイを飛ばし、当たった Rigidbody を押し出します。
    /// </summary>
    public class ClickPusher : MonoBehaviour
    {
        [SerializeField, Tooltip("レイが届く最大距離（m）")]
        private float _maxDistance = 100f;

        [SerializeField, Tooltip("押し出す力積の大きさ（N·s）")]
        private float _pushImpulse = 5f;

        [SerializeField, Tooltip("レイが当たる対象のレイヤー")]
        private LayerMask _targetLayers = ~0;

        private Camera _camera;

        private void Awake()
        {
            // Camera.main は MainCamera タグが付いたカメラを返します。
            _camera = Camera.main;
        }

        private void Update()
        {
            Mouse mouse = Mouse.current;
            if (mouse == null || !mouse.leftButton.wasPressedThisFrame)
            {
                return;
            }

            // 画面上のマウスの位置から、カメラの奥へ向かうレイを作ります。
            Ray ray = _camera.ScreenPointToRay(mouse.position.ReadValue());

            if (!Physics.Raycast(ray, out RaycastHit hit, _maxDistance, _targetLayers))
            {
                return;
            }

            Debug.Log($"{hit.collider.name} に当たりました（距離 {hit.distance:F2} m）。");

            // Rigidbody は UnityEngine.Object なので、?. ではなく != null で判定します。
            if (hit.rigidbody != null)
            {
                hit.rigidbody.AddForceAtPosition(ray.direction * _pushImpulse, hit.point, ForceMode.Impulse);
            }
        }
    }
}
