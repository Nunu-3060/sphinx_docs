using UnityEngine;

/// <summary>
/// Dissolve シェーダーの _Threshold を時間とともに変化させ、
/// オブジェクトが消えたり現れたりするようにする。
/// </summary>
[RequireComponent(typeof(Renderer))]
public class DissolveAnimator : MonoBehaviour
{
    private static readonly int ThresholdId = Shader.PropertyToID("_Threshold");

    [Tooltip("完全に消えるまでの秒数")]
    [SerializeField] private float _duration = 3.0f;

    private Material _material;

    private void Start()
    {
        _material = GetComponent<Renderer>().material;
    }

    private void Update()
    {
        // 0（消えていない）と 1（すべて消えた）の間を往復させる
        float threshold = Mathf.PingPong(Time.time / _duration, 1.0f);
        _material.SetFloat(ThresholdId, threshold);
    }

    private void OnDestroy()
    {
        Destroy(_material);
    }
}
