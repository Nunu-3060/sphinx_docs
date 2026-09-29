using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.VFX;

/// <summary>
/// C# から VFX Graph のプロパティとイベントを操作するサンプル。
/// Visual Effect コンポーネントを持つ GameObject にアタッチして使う。
/// </summary>
/// <remarks>
/// VFX Graph の Blackboard に、次のプロパティとイベントを用意しておく。
/// ・Float 型のプロパティ SpawnRate（Exposed を有効にする）
/// ・Color 型のプロパティ ParticleColor（Exposed を有効にする）
/// ・イベント OnBurst（Event コンテキストの名前）
/// 操作方法：
/// ・上矢印キー、下矢印キー：SpawnRate を増減する。
/// ・R キー：ParticleColor をランダムに変える。
/// ・Space キー：OnBurst イベントを送る。
/// ・P キー、S キー：再生（OnPlay）と停止（OnStop）のイベントを送る。
/// </remarks>
[RequireComponent(typeof(VisualEffect))]
public class VisualEffectController : MonoBehaviour
{
    // プロパティの名前から ID を作っておくと、文字列で指定するより処理が速い。
    private static readonly int SpawnRateId = Shader.PropertyToID("SpawnRate");
    private static readonly int ParticleColorId = Shader.PropertyToID("ParticleColor");

    private const string BurstEventName = "OnBurst";

    [SerializeField, Tooltip("キーを 1 回押したときの SpawnRate の変化量")]
    private float _rateStep = 100f;

    [SerializeField, Tooltip("SpawnRate の上限")]
    private float _maxRate = 10000f;

    private VisualEffect _visualEffect;

    private void Awake()
    {
        _visualEffect = GetComponent<VisualEffect>();
    }

    private void Update()
    {
        Keyboard keyboard = Keyboard.current;
        if (keyboard == null)
        {
            return;
        }

        if (keyboard.upArrowKey.wasPressedThisFrame)
        {
            ChangeSpawnRate(_rateStep);
        }

        if (keyboard.downArrowKey.wasPressedThisFrame)
        {
            ChangeSpawnRate(-_rateStep);
        }

        if (keyboard.rKey.wasPressedThisFrame && _visualEffect.HasVector4(ParticleColorId))
        {
            // Color 型のプロパティは、C# からは Vector4 として設定する。
            Color color = Random.ColorHSV(0f, 1f, 0.8f, 1f, 1f, 1f);
            _visualEffect.SetVector4(ParticleColorId, color);
        }

        if (keyboard.spaceKey.wasPressedThisFrame)
        {
            _visualEffect.SendEvent(BurstEventName);
        }

        if (keyboard.pKey.wasPressedThisFrame)
        {
            // Play は OnPlay イベントを送る。
            _visualEffect.Play();
        }

        if (keyboard.sKey.wasPressedThisFrame)
        {
            // Stop は OnStop イベントを送る。放出済みのパーティクルは消えない。
            _visualEffect.Stop();
        }
    }

    private void ChangeSpawnRate(float delta)
    {
        // グラフにプロパティがない場合は何もしない。
        if (!_visualEffect.HasFloat(SpawnRateId))
        {
            return;
        }

        float rate = _visualEffect.GetFloat(SpawnRateId) + delta;
        _visualEffect.SetFloat(SpawnRateId, Mathf.Clamp(rate, 0f, _maxRate));
    }
}
