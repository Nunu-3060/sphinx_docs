using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Playables;

/// <summary>
/// Timeline のカットシーンをスクリプトから再生し、Signal と再生終了を受け取るサンプル。
/// </summary>
/// <remarks>
/// 使い方:
/// 1. Playable Director を持つ GameObject にこのスクリプトを追加し、Director に Playable Director を指定する。
/// 2. Playable Director の Play On Awake を無効にしておく。
/// 3. Timeline の Signal Track に Signal Emitter を置き、Signal Receiver の Reaction に
///    このスクリプトの OnCutsceneSignal を登録する。
/// Enter キーでカットシーンを再生する。
/// </remarks>
public class CutsceneController : MonoBehaviour
{
    [SerializeField]
    private PlayableDirector director;

    private void OnEnable()
    {
        if (director != null)
        {
            director.stopped += OnDirectorStopped;
        }
    }

    private void OnDisable()
    {
        if (director != null)
        {
            director.stopped -= OnDirectorStopped;
        }
    }

    private void Update()
    {
        Keyboard keyboard = Keyboard.current;
        if (keyboard == null || director == null)
        {
            return;
        }

        if (keyboard.enterKey.wasPressedThisFrame && director.state != PlayState.Playing)
        {
            director.time = 0d;
            director.Play();
        }
    }

    /// <summary>
    /// Signal Receiver から呼び出されるメソッド。
    /// </summary>
    public void OnCutsceneSignal()
    {
        Debug.Log($"Signal を受信した（再生位置 {director.time:F2} 秒）");
    }

    /// <summary>
    /// Timeline の再生が停止したときに呼び出される。
    /// </summary>
    private void OnDirectorStopped(PlayableDirector stoppedDirector)
    {
        Debug.Log("カットシーンの再生が終了した");
    }
}
