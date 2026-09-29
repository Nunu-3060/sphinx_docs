using UnityEngine;
using UnityEngine.InputSystem;

/// <summary>
/// 実行中に Main モジュールと Emission モジュールの値を変更するサンプル。
/// Particle System を持つ GameObject にアタッチして使う。
/// </summary>
/// <remarks>
/// ・上矢印キー、下矢印キー：1 秒あたりの放出数（Rate over Time）を増減する。
/// ・R キー：これから放出するパーティクルの色（Start Color）をランダムに変える。
/// </remarks>
[RequireComponent(typeof(ParticleSystem))]
public class ModifyModules : MonoBehaviour
{
    [SerializeField, Tooltip("キーを 1 回押したときの放出数の変化量")]
    private float _rateStep = 10f;

    [SerializeField, Tooltip("放出数の上限")]
    private float _maxRate = 200f;

    private ParticleSystem _particleSystem;
    private float _rate;

    private void Awake()
    {
        _particleSystem = GetComponent<ParticleSystem>();

        // Inspector で設定した放出数を初期値にする。
        _rate = _particleSystem.emission.rateOverTime.constant;
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
            SetRate(_rate + _rateStep);
        }

        if (keyboard.downArrowKey.wasPressedThisFrame)
        {
            SetRate(_rate - _rateStep);
        }

        if (keyboard.rKey.wasPressedThisFrame)
        {
            SetRandomColor();
        }
    }

    private void SetRate(float rate)
    {
        _rate = Mathf.Clamp(rate, 0f, _maxRate);

        // モジュールは構造体として取得する。
        // 取得した構造体のプロパティに値を代入すると、Particle System に反映される。
        ParticleSystem.EmissionModule emission = _particleSystem.emission;
        emission.rateOverTime = _rate;
    }

    private void SetRandomColor()
    {
        // 色相をランダムにし、彩度と明度は高めにする。
        Color color = Random.ColorHSV(0f, 1f, 0.8f, 1f, 1f, 1f);

        ParticleSystem.MainModule main = _particleSystem.main;
        main.startColor = color;
    }
}
