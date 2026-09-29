// 第 14 章 入力処理
// キーボードとマウスの状態を直接読み取るスクリプトです（Input System パッケージを使用）。
// 使い方: シーン内の GameObject にアタッチし、Play モード中に Game ビューをクリックしてから、
//         矢印キー、スペースキー、マウスの左ボタンを操作します。
using UnityEngine;
using UnityEngine.InputSystem;

public class KeyboardInputSample : MonoBehaviour
{
    [SerializeField] private float _speed = 3f;

    private void Update()
    {
        // 接続されているキーボードとマウスを取得します。接続されていない場合は null になります。
        Keyboard keyboard = Keyboard.current;
        Mouse mouse = Mouse.current;

        if (keyboard != null)
        {
            // isPressed: 押されている間ずっと true
            float horizontal = 0f;
            if (keyboard.leftArrowKey.isPressed)
            {
                horizontal -= 1f;
            }
            if (keyboard.rightArrowKey.isPressed)
            {
                horizontal += 1f;
            }
            transform.position += Vector3.right * horizontal * _speed * Time.deltaTime;

            // wasPressedThisFrame: 押されたフレームだけ true
            if (keyboard.spaceKey.wasPressedThisFrame)
            {
                Debug.Log("スペースキーが押された。");
            }

            // wasReleasedThisFrame: 離されたフレームだけ true
            if (keyboard.spaceKey.wasReleasedThisFrame)
            {
                Debug.Log("スペースキーが離された。");
            }
        }

        if (mouse != null && mouse.leftButton.wasPressedThisFrame)
        {
            // マウスカーソルの位置は、画面の左下を (0, 0) とするピクセル座標です。
            Vector2 position = mouse.position.ReadValue();
            Debug.Log($"クリックした位置: {position}");
        }
    }
}
