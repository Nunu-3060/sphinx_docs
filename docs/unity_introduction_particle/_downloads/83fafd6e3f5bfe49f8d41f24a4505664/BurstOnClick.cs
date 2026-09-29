using UnityEngine;
using UnityEngine.InputSystem;

/// <summary>
/// マウスの左ボタンをクリックした位置に、パーティクルをまとめて放出するサンプル。
/// Particle System を持つ GameObject にアタッチして使う。
/// </summary>
/// <remarks>
/// Particle System は次のように設定しておく。
/// ・Main モジュールの Simulation Space を World にする（移動したときに放出済みのパーティクルが付いてこないようにするため）。
/// ・Emission モジュールを無効にする（スクリプトから放出するときだけパーティクルを出すため）。
/// </remarks>
[RequireComponent(typeof(ParticleSystem))]
public class BurstOnClick : MonoBehaviour
{
    [SerializeField, Tooltip("1 回のクリックで放出するパーティクルの数")]
    private int _count = 30;

    [SerializeField, Tooltip("カメラから放出位置までの距離")]
    private float _distance = 10f;

    private ParticleSystem _particleSystem;
    private Camera _camera;

    private void Awake()
    {
        _particleSystem = GetComponent<ParticleSystem>();
        _camera = Camera.main;
    }

    private void Update()
    {
        Mouse mouse = Mouse.current;
        if (mouse == null || !mouse.leftButton.wasPressedThisFrame)
        {
            return;
        }

        // マウスの位置（スクリーン座標）を、カメラから _distance だけ離れたワールド座標に変換する。
        Vector2 screenPosition = mouse.position.ReadValue();
        Vector3 worldPosition = _camera.ScreenToWorldPoint(
            new Vector3(screenPosition.x, screenPosition.y, _distance));

        // Particle System をクリックした位置に移動してから放出する。
        transform.position = worldPosition;
        _particleSystem.Emit(_count);
    }
}
