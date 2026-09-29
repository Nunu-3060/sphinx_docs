using UnityEngine;
using UnityEngine.InputSystem;

/// <summary>
/// キー入力で Particle System の再生、一時停止、停止を切り替えるサンプル。
/// Particle System を持つ GameObject にアタッチして使う。
/// </summary>
[RequireComponent(typeof(ParticleSystem))]
public class ParticlePlayback : MonoBehaviour
{
    private ParticleSystem _particleSystem;

    private void Awake()
    {
        _particleSystem = GetComponent<ParticleSystem>();
    }

    private void Update()
    {
        // キーボードが接続されていない場合は何もしない。
        Keyboard keyboard = Keyboard.current;
        if (keyboard == null)
        {
            return;
        }

        // P キー：再生する。停止中なら最初から、一時停止中なら続きから再生する。
        if (keyboard.pKey.wasPressedThisFrame)
        {
            _particleSystem.Play();
        }

        // Space キー：一時停止する。パーティクルはその場で止まる。
        if (keyboard.spaceKey.wasPressedThisFrame)
        {
            _particleSystem.Pause();
        }

        // S キー：放出を止める。放出済みのパーティクルは寿命が尽きるまで動き続ける。
        if (keyboard.sKey.wasPressedThisFrame)
        {
            _particleSystem.Stop(true, ParticleSystemStopBehavior.StopEmitting);
        }

        // C キー：放出を止め、放出済みのパーティクルもすべて消す。
        if (keyboard.cKey.wasPressedThisFrame)
        {
            _particleSystem.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear);
        }
    }
}
