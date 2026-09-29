using UnityEngine;

/// <summary>
/// フレームレート（fps）と 1 フレームあたりの処理時間（ms）を画面の左上に表示するサンプルです。
/// </summary>
/// <remarks>
/// 手軽に表示するため、デバッグ用の IMGUI（OnGUI）を使っています。
/// 正確な計測には Profiler を使ってください。
/// </remarks>
public class FpsCounter : MonoBehaviour
{
    [SerializeField, Tooltip("表示を更新する間隔（秒）")]
    private float updateInterval = 0.5f;

    [SerializeField]
    private int fontSize = 32;

    private int frameCount;
    private float elapsedTime;
    private string displayText = string.Empty;
    private GUIStyle style;

    private void Update()
    {
        frameCount++;

        // Time.timeScale の影響を受けないように unscaledDeltaTime を使います。
        elapsedTime += Time.unscaledDeltaTime;

        if (elapsedTime >= updateInterval)
        {
            // 一定時間の平均を求めることで、表示のちらつきを抑えます。
            float fps = frameCount / elapsedTime;
            float frameTimeMs = elapsedTime * 1000f / frameCount;

            // 文字列の生成は GC アロケーションを伴うため、表示の更新時だけ行います。
            displayText = $"{fps:F1} fps ({frameTimeMs:F2} ms)";

            frameCount = 0;
            elapsedTime = 0f;
        }
    }

    private void OnGUI()
    {
        // GUI.skin は OnGUI の中でしか参照できないため、ここで初期化します。
        if (style == null)
        {
            style = new GUIStyle(GUI.skin.label) { fontSize = fontSize };
            style.normal.textColor = Color.white;
        }

        GUI.Label(new Rect(10, 10, 600, fontSize * 1.5f), displayText, style);
    }
}
