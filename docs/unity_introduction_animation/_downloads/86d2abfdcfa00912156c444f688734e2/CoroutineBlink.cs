using System.Collections;
using UnityEngine;

/// <summary>
/// コルーチンを使って、Renderer の表示と非表示を一定間隔で切り替えるサンプル。
/// </summary>
/// <remarks>
/// 使い方: Mesh Renderer などの Renderer を持つ GameObject に追加して再生する。
/// 被ダメージ時の点滅演出などに応用できる。
/// </remarks>
[RequireComponent(typeof(Renderer))]
public class CoroutineBlink : MonoBehaviour
{
    [Tooltip("表示と非表示を切り替える間隔（秒）")]
    [Min(0.01f)]
    [SerializeField]
    private float interval = 0.1f;

    [Tooltip("点滅させる回数")]
    [Min(1)]
    [SerializeField]
    private int blinkCount = 10;

    private Renderer targetRenderer;

    private void Awake()
    {
        targetRenderer = GetComponent<Renderer>();
    }

    private void Start()
    {
        StartCoroutine(Blink());
    }

    private IEnumerator Blink()
    {
        // 同じ待ち時間を繰り返し使うため、WaitForSeconds を 1 つだけ作って再利用する。
        WaitForSeconds wait = new WaitForSeconds(interval);

        for (int i = 0; i < blinkCount; i++)
        {
            targetRenderer.enabled = false;
            yield return wait;
            targetRenderer.enabled = true;
            yield return wait;
        }
    }
}
