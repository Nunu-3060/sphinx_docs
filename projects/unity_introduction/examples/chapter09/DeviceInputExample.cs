using UnityEngine;
using UnityEngine.InputSystem;

namespace UnityIntroduction.Chapter09
{
    /// <summary>
    /// Input Actions を使わず、キーボード、マウス、ゲームパッドの状態を直接読み取ります。
    /// </summary>
    /// <remarks>
    /// 動作確認やデバッグ用の簡単な処理に向いた方法です。
    /// ゲーム本体の操作には Input Actions を使うことをお勧めします。
    /// </remarks>
    public class DeviceInputExample : MonoBehaviour
    {
        private void Update()
        {
            // デバイスが接続されていない場合、current は null になります。
            Keyboard keyboard = Keyboard.current;
            if (keyboard != null && keyboard.spaceKey.wasPressedThisFrame)
            {
                Debug.Log("スペースキーが押されました。");
            }

            Mouse mouse = Mouse.current;
            if (mouse != null && mouse.leftButton.wasPressedThisFrame)
            {
                Vector2 position = mouse.position.ReadValue();
                Debug.Log($"左クリックされました。画面上の位置: {position}");
            }

            Gamepad gamepad = Gamepad.current;
            if (gamepad != null && gamepad.buttonSouth.wasPressedThisFrame)
            {
                Debug.Log("ゲームパッドの下側のボタンが押されました。");
            }
        }
    }
}
