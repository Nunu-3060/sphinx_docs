using UnityEngine;

/// <summary>
/// Animation Event から呼び出され、足音を再生するサンプル。
/// </summary>
/// <remarks>
/// 使い方:
/// 1. Animator コンポーネントを持つ GameObject に、このスクリプトと AudioSource を追加する。
/// 2. 歩行の Animation Clip で、足が地面に着くフレームに Animation Event を追加する。
/// 3. Animation Event の Function に OnFootstep を指定し、String に "Left" または "Right" を入力する。
/// </remarks>
[RequireComponent(typeof(AudioSource))]
public class FootstepEvent : MonoBehaviour
{
    [SerializeField]
    private AudioClip footstepClip;

    private AudioSource audioSource;

    private void Awake()
    {
        audioSource = GetComponent<AudioSource>();
    }

    /// <summary>
    /// Animation Event から呼び出されるメソッド。
    /// </summary>
    /// <param name="foot">どちらの足かを表す文字列（Animation Event の String に入力した値）。</param>
    public void OnFootstep(string foot)
    {
        if (footstepClip == null)
        {
            return;
        }

        audioSource.PlayOneShot(footstepClip);
        Debug.Log($"足音: {foot}");
    }
}
