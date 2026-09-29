// サンプルコードの検査用に、Input System パッケージと TextMeshPro の API のうち本書で使う部分だけを再現したスタブです。
namespace UnityEngine.InputSystem
{
    public static class InputSystem
    {
        public static InputActionAsset actions { get; } = new InputActionAsset();
    }

    public class InputActionAsset : Object
    {
        public InputAction FindAction(string actionNameOrId)
        {
            return new InputAction();
        }
    }

    public class InputAction
    {
        public TValue ReadValue<TValue>() where TValue : struct
        {
            return default;
        }

        public bool WasPressedThisFrame()
        {
            return false;
        }
    }

    public class InputDevice
    {
    }

    public class Keyboard : InputDevice
    {
        public static Keyboard current { get; } = null;

        public Controls.KeyControl leftArrowKey { get; } = new Controls.KeyControl();

        public Controls.KeyControl rightArrowKey { get; } = new Controls.KeyControl();

        public Controls.KeyControl spaceKey { get; } = new Controls.KeyControl();

        public Controls.KeyControl rKey { get; } = new Controls.KeyControl();
    }

    public class Mouse : InputDevice
    {
        public static Mouse current { get; } = null;

        public Controls.ButtonControl leftButton { get; } = new Controls.ButtonControl();

        public Controls.Vector2Control position { get; } = new Controls.Vector2Control();
    }
}

namespace UnityEngine.InputSystem.Controls
{
    public class ButtonControl
    {
        public bool isPressed => false;

        public bool wasPressedThisFrame => false;

        public bool wasReleasedThisFrame => false;
    }

    public class KeyControl : ButtonControl
    {
    }

    public class Vector2Control
    {
        public Vector2 ReadValue() => default;
    }
}

namespace TMPro
{
    public class TextMeshProUGUI : UnityEngine.Component
    {
        public string text { get; set; }
    }
}
