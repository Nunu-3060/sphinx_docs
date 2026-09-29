using UnityEngine;
using UnityEngine.InputSystem;

namespace UnityIntroduction.Chapter14
{
    /// <summary>
    /// 入力に応じて Animator Controller のパラメーターを設定します。
    /// </summary>
    /// <remarks>
    /// Animator Controller に、Float 型の Speed と Trigger 型の Jump を用意してください。
    /// </remarks>
    [RequireComponent(typeof(Animator))]
    public class AnimatorParameterDriver : MonoBehaviour
    {
        // パラメーター名を毎回文字列で渡すより、事前にハッシュ値へ変換しておくほうが効率的です。
        private static readonly int SpeedHash = Animator.StringToHash("Speed");
        private static readonly int JumpHash = Animator.StringToHash("Jump");

        private Animator _animator;
        private InputAction _moveAction;
        private InputAction _jumpAction;

        private void Awake()
        {
            _animator = GetComponent<Animator>();

            // プロジェクト全体のアクション（Project-wide Actions）から名前で検索します。
            _moveAction = InputSystem.actions.FindAction("Player/Move", throwIfNotFound: true);
            _jumpAction = InputSystem.actions.FindAction("Player/Jump", throwIfNotFound: true);
        }

        private void Update()
        {
            // 入力の大きさ（0 から 1）を Speed に設定し、待機と歩きのアニメーションを切り替えます。
            float speed = _moveAction.ReadValue<Vector2>().magnitude;
            _animator.SetFloat(SpeedHash, speed);

            if (_jumpAction.WasPressedThisFrame())
            {
                _animator.SetTrigger(JumpHash);
            }
        }
    }
}
