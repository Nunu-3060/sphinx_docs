// 第 14 章 入力処理
// プロジェクト全体の入力アクション（Project-wide Actions）を使って移動とジャンプの入力を読み取るスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play モード中に WASD キー、矢印キー、ゲームパッドの左スティックなどで操作します。
//         Unity 6 で作成したプロジェクトに最初から用意されている入力アクション（Move、Jump）を使います。
using UnityEngine;
using UnityEngine.InputSystem;

public class ActionInputSample : MonoBehaviour
{
    [SerializeField] private float _speed = 3f;

    private InputAction _moveAction;
    private InputAction _jumpAction;

    private void Awake()
    {
        // Project Settings の Input System Package で設定されている入力アクションから、名前で検索します。
        _moveAction = InputSystem.actions.FindAction("Move");
        _jumpAction = InputSystem.actions.FindAction("Jump");
    }

    private void Update()
    {
        // Move は Vector2 の値を返します。x が左右、y が上下（前後）の入力です。
        Vector2 input = _moveAction.ReadValue<Vector2>();

        // 2 次元の入力を、3 次元空間の X 方向と Z 方向の移動に割り当てます。
        Vector3 direction = new Vector3(input.x, 0f, input.y);
        transform.position += direction * _speed * Time.deltaTime;

        if (_jumpAction.WasPressedThisFrame())
        {
            Debug.Log("ジャンプの入力があった。");
        }
    }
}
