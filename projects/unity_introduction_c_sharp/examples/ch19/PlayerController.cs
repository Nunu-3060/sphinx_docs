// 第 19 章 簡単なゲームを作る
// 入力に応じてボールを転がすプレイヤーのスクリプトです。
// 使い方: Player という名前の Sphere にアタッチします（Rigidbody は自動で追加されます）。
//         Sphere の Tag は Player に設定します。
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Rigidbody))]
public class PlayerController : MonoBehaviour
{
    [Tooltip("転がす力の大きさ")]
    [SerializeField] private float _force = 10f;

    [Tooltip("この高さより下に落ちたら、ゲームをやり直す")]
    [SerializeField] private float _fallLimit = -10f;

    private Rigidbody _rigidbody;
    private InputAction _moveAction;
    private Vector2 _moveInput;

    private void Awake()
    {
        _rigidbody = GetComponent<Rigidbody>();
        _moveAction = InputSystem.actions.FindAction("Move");
    }

    private void Update()
    {
        // 入力は Update で読み取り、フィールドに保存しておきます。
        _moveInput = _moveAction.ReadValue<Vector2>();

        if (transform.position.y < _fallLimit)
        {
            GameManager.Instance.Restart();
        }
    }

    private void FixedUpdate()
    {
        // 入力の上下を Z 方向（奥・手前）、左右を X 方向に割り当てて、力を加えます。
        Vector3 direction = new Vector3(_moveInput.x, 0f, _moveInput.y);
        _rigidbody.AddForce(direction * _force);
    }
}
