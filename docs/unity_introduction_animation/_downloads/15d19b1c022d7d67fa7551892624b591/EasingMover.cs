using UnityEngine;

/// <summary>
/// イージング関数を使って 2 点間を往復させるサンプル。
/// </summary>
/// <remarks>
/// 使い方: GameObject に追加し、Inspector ウィンドウで Easing を切り替えながら再生して、
/// 動きの違いを確認する。
/// </remarks>
public class EasingMover : MonoBehaviour
{
    /// <summary>
    /// 使用するイージング関数の種類。
    /// </summary>
    public enum EasingType
    {
        /// <summary>等速で動く。</summary>
        Linear,

        /// <summary>ゆっくり動き出し、だんだん速くなる。</summary>
        EaseIn,

        /// <summary>速く動き出し、だんだん遅くなる。</summary>
        EaseOut,

        /// <summary>ゆっくり動き出し、ゆっくり止まる。</summary>
        SmoothStep,
    }

    [SerializeField]
    private EasingType easing = EasingType.SmoothStep;

    [SerializeField]
    private Vector3 startPosition = Vector3.zero;

    [SerializeField]
    private Vector3 endPosition = new Vector3(5f, 0f, 0f);

    [Tooltip("片道にかける時間（秒）")]
    [Min(0.01f)]
    [SerializeField]
    private float duration = 1.5f;

    private void Update()
    {
        // Mathf.PingPong は 0 → duration → 0 → ... と往復する値を返す。
        float t = Mathf.PingPong(Time.time, duration) / duration;

        transform.position = Vector3.LerpUnclamped(startPosition, endPosition, Evaluate(easing, t));
    }

    /// <summary>
    /// 0 から 1 の値 t を、イージング関数で変換した値を返す。
    /// </summary>
    private static float Evaluate(EasingType type, float t)
    {
        switch (type)
        {
            case EasingType.EaseIn:
                // f(t) = t^2
                return t * t;
            case EasingType.EaseOut:
                // f(t) = 1 - (1 - t)^2
                return 1f - ((1f - t) * (1f - t));
            case EasingType.SmoothStep:
                // f(t) = 3t^2 - 2t^3
                return t * t * (3f - (2f * t));
            case EasingType.Linear:
            default:
                return t;
        }
    }
}
