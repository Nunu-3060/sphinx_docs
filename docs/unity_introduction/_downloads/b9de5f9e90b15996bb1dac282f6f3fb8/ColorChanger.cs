using UnityEngine;

namespace UnityIntroduction.Chapter07
{
    /// <summary>
    /// 同じ GameObject にある Renderer の色を、2 色の間で往復させます。
    /// </summary>
    [RequireComponent(typeof(MeshRenderer))]
    public class ColorChanger : MonoBehaviour
    {
        [SerializeField]
        private Color _colorA = Color.white;

        [SerializeField]
        private Color _colorB = Color.red;

        [SerializeField, Tooltip("1 往復にかかる秒数")]
        private float _period = 2f;

        private Renderer _renderer;

        private void Awake()
        {
            // 同じ GameObject に付いている Renderer を取得して保持します。
            // 毎フレーム GetComponent を呼ぶより効率的です。
            _renderer = GetComponent<Renderer>();
        }

        private void Update()
        {
            // Mathf.PingPong は 0 から 1 までを往復する値を返します。
            float t = Mathf.PingPong(Time.time * 2f / _period, 1f);

            // material にアクセスすると、この Renderer 専用のマテリアルが複製されます。
            _renderer.material.color = Color.Lerp(_colorA, _colorB, t);
        }
    }
}
