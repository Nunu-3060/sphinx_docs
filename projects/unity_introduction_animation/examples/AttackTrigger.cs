using UnityEngine;
using UnityEngine.InputSystem;

/// <summary>
/// Trigger 型パラメーターによる遷移と、CrossFade による直接遷移を比較するサンプル。
/// </summary>
/// <remarks>
/// 使い方:
/// 1. Animator Controller に Trigger 型のパラメーター "Attack" を追加する。
/// 2. 待機ステートから "Attack" ステートへ、条件 Attack の遷移を作る。
/// 3. "Hit" ステートを作る（遷移は不要）。
/// 4. Animator コンポーネントを持つ GameObject にこのスクリプトを追加する。
/// Space キーで攻撃し、H キーで被ダメージのモーションへ直接切り替える。
/// </remarks>
[RequireComponent(typeof(Animator))]
public class AttackTrigger : MonoBehaviour
{
    private static readonly int AttackTriggerHash = Animator.StringToHash("Attack");
    private static readonly int AttackStateHash = Animator.StringToHash("Attack");
    private static readonly int HitStateHash = Animator.StringToHash("Hit");

    private const int BaseLayer = 0;

    [Tooltip("CrossFade で切り替える時間（秒）")]
    [Min(0f)]
    [SerializeField]
    private float hitFadeDuration = 0.1f;

    private Animator animator;

    private void Awake()
    {
        animator = GetComponent<Animator>();
    }

    private void Update()
    {
        Keyboard keyboard = Keyboard.current;
        if (keyboard == null)
        {
            return;
        }

        if (keyboard.spaceKey.wasPressedThisFrame && !IsAttacking())
        {
            // 遷移条件は Animator Controller 側で定義しておき、スクリプトは合図だけを送る。
            animator.SetTrigger(AttackTriggerHash);
        }

        if (keyboard.hKey.wasPressedThisFrame)
        {
            // 遷移を定義していないステートへも、スクリプトから直接切り替えられる。
            // CrossFadeInFixedTime は切り替え時間を秒で指定する。
            animator.CrossFadeInFixedTime(HitStateHash, hitFadeDuration, BaseLayer);

            // 被ダメージ中に古い攻撃入力が残らないよう、Trigger を解除しておく。
            animator.ResetTrigger(AttackTriggerHash);
        }
    }

    /// <summary>
    /// 攻撃ステートの再生中、または攻撃ステートへの遷移中であれば true を返す。
    /// </summary>
    private bool IsAttacking()
    {
        AnimatorStateInfo current = animator.GetCurrentAnimatorStateInfo(BaseLayer);
        if (current.shortNameHash == AttackStateHash)
        {
            return true;
        }

        if (animator.IsInTransition(BaseLayer))
        {
            AnimatorStateInfo next = animator.GetNextAnimatorStateInfo(BaseLayer);
            return next.shortNameHash == AttackStateHash;
        }

        return false;
    }
}
