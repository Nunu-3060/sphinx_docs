using UnityEngine;
using UnityEngine.InputSystem;

namespace UnityIntroduction.Chapter09
{
    /// <summary>
    /// Input Actions の Move で移動し、Jump でログを表示します。
    /// </summary>
    /// <remarks>
    /// Inspector で、InputSystem_Actions アセットの Player/Move と Player/Jump を指定してください。
    /// </remarks>
    public class InputActionMover : MonoBehaviour
    {
        [SerializeField]
        private InputActionReference _moveAction;

        [SerializeField]
        private InputActionReference _jumpAction;

        [SerializeField, Tooltip("1 秒あたりの移動量（m/s）")]
        private float _speed = 3f;

        private void OnEnable()
        {
            // アクションは有効にしないと入力を受け取りません。
            // プロジェクト全体のアクション（Project-wide Actions）は最初から有効ですが、
            // 明示的に有効にしても問題ありません。
            _moveAction.action.Enable();
            _jumpAction.action.Enable();

            // ボタンが押されたときに呼ばれるメソッドを登録します。
            _jumpAction.action.performed += OnJumpPerformed;
        }

        private void OnDisable()
        {
            _jumpAction.action.performed -= OnJumpPerformed;
        }

        private void Update()
        {
            // Move アクションは WASD キーや左スティックの入力を Vector2 で返します。
            Vector2 input = _moveAction.action.ReadValue<Vector2>();
            var direction = new Vector3(input.x, 0f, input.y);
            transform.Translate(direction * _speed * Time.deltaTime, Space.World);
        }

        private void OnJumpPerformed(InputAction.CallbackContext context)
        {
            Debug.Log("Jump が押されました。");
        }
    }
}
