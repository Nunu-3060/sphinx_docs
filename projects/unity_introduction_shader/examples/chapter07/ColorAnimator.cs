using UnityEngine;

/// <summary>
/// マテリアルの _BaseColor プロパティを、C# から時間とともに変化させる。
/// </summary>
[RequireComponent(typeof(Renderer))]
public class ColorAnimator : MonoBehaviour
{
    // プロパティ名を毎フレーム文字列で指定すると検索に時間がかかるため、ID に変換しておく
    private static readonly int BaseColorId = Shader.PropertyToID("_BaseColor");

    [SerializeField] private Color _colorA = Color.red;
    [SerializeField] private Color _colorB = Color.blue;

    [Tooltip("色が A から B に変わるまでの秒数")]
    [SerializeField] private float _duration = 2.0f;

    private Material _material;

    private void Start()
    {
        // Renderer.material は、このオブジェクト専用のマテリアルの複製を返す。
        // 複製を変更しても、同じマテリアルを使うほかのオブジェクトの色は変わらない。
        _material = GetComponent<Renderer>().material;
    }

    private void Update()
    {
        // 0 から 1 までを往復する値を作り、2 つの色を補間する
        float t = Mathf.PingPong(Time.time / _duration, 1.0f);
        _material.SetColor(BaseColorId, Color.Lerp(_colorA, _colorB, t));
    }

    private void OnDestroy()
    {
        // Renderer.material で作られた複製は自動では破棄されないため、自分で破棄する
        Destroy(_material);
    }
}
