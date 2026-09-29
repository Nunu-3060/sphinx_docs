using UnityEngine;

/// <summary>
/// AnimationCurve を使って GameObject を上下に弾ませるサンプル。
/// </summary>
/// <remarks>
/// 使い方: GameObject に追加して再生する。Inspector ウィンドウで Height Curve をクリックすると
/// カーブエディターが開き、再生中でも形を変更して動きの変化を確認できる。
/// </remarks>
public class CurveMover : MonoBehaviour
{
    [Tooltip("横軸が時間の割合（0 から 1）、縦軸が高さの倍率のカーブ")]
    [SerializeField]
    private AnimationCurve heightCurve = new AnimationCurve(
        new Keyframe(0f, 0f),
        new Keyframe(0.5f, 1f),
        new Keyframe(1f, 0f));

    [Tooltip("最大の高さ（メートル）")]
    [SerializeField]
    private float height = 2f;

    [Tooltip("1 回の跳ねにかける時間（秒）")]
    [Min(0.01f)]
    [SerializeField]
    private float duration = 1f;

    private Vector3 basePosition;

    private void Start()
    {
        // 開始時の位置を基準にする。
        basePosition = transform.position;
    }

    private void Update()
    {
        // Mathf.Repeat は 0 から duration までの値を繰り返す。
        float t = Mathf.Repeat(Time.time, duration) / duration;

        transform.position = basePosition + (Vector3.up * (heightCurve.Evaluate(t) * height));
    }
}
