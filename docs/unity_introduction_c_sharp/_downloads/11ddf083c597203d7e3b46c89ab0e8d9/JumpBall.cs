// 第 16 章 物理演算と衝突判定
// ジャンプの入力（入力アクションの Jump）で Rigidbody に力を加えてジャンプさせるスクリプトです。
// 使い方: 床となる Plane と、その上に Sphere を作成し、Sphere にこのスクリプトをアタッチします（Rigidbody は自動で追加されます）。
using UnityEngine;
using UnityEngine.InputSystem;

// RequireComponent を付けると、このスクリプトをアタッチしたときに Rigidbody も自動で追加されます。
[RequireComponent(typeof(Rigidbody))]
public class JumpBall : MonoBehaviour
{
    [SerializeField] private float _jumpForce = 5f;

    private Rigidbody _rigidbody;
    private InputAction _jumpAction;
    private bool _jumpRequested;
    private bool _isGrounded;

    private void Awake()
    {
        _rigidbody = GetComponent<Rigidbody>();
        _jumpAction = InputSystem.actions.FindAction("Jump");
    }

    // 入力は Update で読み取ります（FixedUpdate では押された瞬間を取りこぼすことがあるため）。
    private void Update()
    {
        if (_jumpAction.WasPressedThisFrame() && _isGrounded)
        {
            _jumpRequested = true;
        }
    }

    // 物理演算に関わる処理は FixedUpdate で行います。
    private void FixedUpdate()
    {
        if (_jumpRequested)
        {
            // ForceMode.Impulse は、質量を考慮した瞬間的な力（撃力）を加えます。
            _rigidbody.AddForce(Vector3.up * _jumpForce, ForceMode.Impulse);
            _jumpRequested = false;
            _isGrounded = false;
        }
    }

    // ほかの Collider とぶつかっている間、毎回の物理演算の更新ごとに呼ばれます。
    private void OnCollisionStay(Collision collision)
    {
        // 接触点の法線（面に垂直な向き）が上向きなら、床の上に立っていると判断します。
        for (int i = 0; i < collision.contactCount; i++)
        {
            ContactPoint contact = collision.GetContact(i);
            if (contact.normal.y > 0.5f)
            {
                _isGrounded = true;
                return;
            }
        }
    }

    private void OnCollisionExit(Collision collision)
    {
        _isGrounded = false;
    }
}
