using UnityEngine;

namespace UnityIntroduction.Chapter08
{
    /// <summary>
    /// Inspector の表示を整える属性の使用例です。
    /// </summary>
    /// <remarks>
    /// Inspector での見え方を確認するためのクラスです。再生を開始すると、設定した値をログに表示します。
    /// </remarks>
    public class InspectorAttributesExample : MonoBehaviour
    {
        [Header("移動")]
        [SerializeField, Tooltip("1 秒あたりの移動量（m/s）")]
        private float _moveSpeed = 5f;

        [SerializeField, Range(0f, 1f), Tooltip("0 で減速なし、1 で即座に停止")]
        private float _damping = 0.1f;

        [Space(12)]
        [Header("表示")]
        [SerializeField]
        private Color _color = Color.white;

        [SerializeField, TextArea(2, 5)]
        private string _memo = "";

        [SerializeField, Min(0)]
        private int _hitPoints = 10;

        private void Start()
        {
            Debug.Log($"速度: {_moveSpeed}, 減衰: {_damping}, 色: {_color}, 体力: {_hitPoints}, メモ: {_memo}");
        }

        [ContextMenu("値を初期値に戻す")]
        private void ResetValues()
        {
            _moveSpeed = 5f;
            _damping = 0.1f;
            _color = Color.white;
            _memo = "";
            _hitPoints = 10;
        }
    }
}
