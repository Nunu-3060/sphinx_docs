using UnityEngine;
using UnityEngine.InputSystem;

namespace UnityIntroduction.RollABall
{
    /// <summary>
    /// 入力に応じてボールに力を加えて転がします。
    /// </summary>
    [RequireComponent(typeof(Rigidbody))]
    public class PlayerController : MonoBehaviour
    {
        [SerializeField, Tooltip("ボールに加える力の大きさ（N）")]
        private float _moveForce = 10f;

        private Rigidbody _rigidbody;
        private InputAction _moveAction;
        private Vector2 _moveInput;
        private bool _canMove = true;

        private void Awake()
        {
            _rigidbody = GetComponent<Rigidbody>();

            // プロジェクト全体のアクション（Project-wide Actions）から Move アクションを取得します。
            _moveAction = InputSystem.actions.FindAction("Player/Move", throwIfNotFound: true);
        }

        private void Update()
        {
            // 入力は毎フレーム呼ばれる Update で読み取ります。
            _moveInput = _canMove ? _moveAction.ReadValue<Vector2>() : Vector2.zero;
        }

        private void FixedUpdate()
        {
            // 物理演算への力の追加は、物理演算の更新に合わせて呼ばれる FixedUpdate で行います。
            // 入力の上下（y）を、ワールド座標の前後（z）に対応させます。
            var force = new Vector3(_moveInput.x, 0f, _moveInput.y) * _moveForce;
            _rigidbody.AddForce(force);
        }

        /// <summary>
        /// 操作を受け付けないようにし、ボールをその場で止めます。
        /// </summary>
        public void StopMoving()
        {
            _canMove = false;
            _moveInput = Vector2.zero;
            _rigidbody.linearVelocity = Vector3.zero;
            _rigidbody.angularVelocity = Vector3.zero;
        }
    }
}
