using UnityEngine;

/// <summary>
/// 指定した時間をかけて、開始位置・開始角度から終了位置・終了角度へ補間するサンプル。
/// </summary>
/// <remarks>
/// 使い方: GameObject に追加し、Inspector ウィンドウで開始と終了の値、所要時間を設定して再生する。
/// 位置は Vector3.Lerp、回転は Quaternion.Slerp で補間する。
/// </remarks>
public class LerpMover : MonoBehaviour
{
    [Header("位置")]
    [SerializeField]
    private Vector3 startPosition = Vector3.zero;

    [SerializeField]
    private Vector3 endPosition = new Vector3(5f, 0f, 0f);

    [Header("回転（オイラー角で指定）")]
    [SerializeField]
    private Vector3 startEulerAngles = Vector3.zero;

    [SerializeField]
    private Vector3 endEulerAngles = new Vector3(0f, 180f, 0f);

    [Tooltip("開始から終了までにかける時間（秒）")]
    [Min(0.01f)]
    [SerializeField]
    private float duration = 2f;

    private float elapsedTime;

    private void Update()
    {
        elapsedTime += Time.deltaTime;

        // 経過時間を 0 から 1 の割合に変換する。1 を超えないように制限する。
        float t = Mathf.Clamp01(elapsedTime / duration);

        transform.position = Vector3.Lerp(startPosition, endPosition, t);
        transform.rotation = Quaternion.Slerp(
            Quaternion.Euler(startEulerAngles),
            Quaternion.Euler(endEulerAngles),
            t);
    }
}
