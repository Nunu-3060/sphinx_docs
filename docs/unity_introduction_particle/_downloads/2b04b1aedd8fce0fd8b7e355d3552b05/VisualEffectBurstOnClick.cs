using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.VFX;

/// <summary>
/// クリックした位置を VFX Graph のイベントに添えて送り、その位置にパーティクルを出すサンプル。
/// Visual Effect コンポーネントを持つ GameObject にアタッチして使う。
/// </summary>
/// <remarks>
/// VFX Graph は、次のように作っておく。
/// ・OnClick という名前の Event コンテキストを、Spawn コンテキストの Start に接続する。
/// ・Spawn コンテキストに Single Burst ブロックを追加する。
/// ・Initialize Particle コンテキストに Set Position ブロックを追加し、Source の設定を Source にする。
/// ・Visual Effect を持つ GameObject は原点に置き、回転と拡大縮小をしない（ワールド座標をそのまま使うため）。
/// </remarks>
[RequireComponent(typeof(VisualEffect))]
public class VisualEffectBurstOnClick : MonoBehaviour
{
    private const string ClickEventName = "OnClick";

    // 位置の属性の名前。VFX Graph の組み込みの属性 position に対応する。
    private static readonly int PositionAttributeId = Shader.PropertyToID("position");

    [SerializeField, Tooltip("カメラから放出位置までの距離")]
    private float _distance = 10f;

    private VisualEffect _visualEffect;
    private Camera _camera;

    // イベントに添える属性。毎回作り直さないように使い回す。
    private VFXEventAttribute _eventAttribute;

    private void Awake()
    {
        _visualEffect = GetComponent<VisualEffect>();
        _camera = Camera.main;
        _eventAttribute = _visualEffect.CreateVFXEventAttribute();
    }

    private void Update()
    {
        Mouse mouse = Mouse.current;
        if (mouse == null || !mouse.leftButton.wasPressedThisFrame)
        {
            return;
        }

        Vector2 screenPosition = mouse.position.ReadValue();
        Vector3 worldPosition = _camera.ScreenToWorldPoint(
            new Vector3(screenPosition.x, screenPosition.y, _distance));

        // 位置を属性に設定して、イベントと一緒に送る。
        _eventAttribute.SetVector3(PositionAttributeId, worldPosition);
        _visualEffect.SendEvent(ClickEventName, _eventAttribute);
    }
}
