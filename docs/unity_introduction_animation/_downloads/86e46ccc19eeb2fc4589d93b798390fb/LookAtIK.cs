using UnityEngine;

/// <summary>
/// Humanoid キャラクターの視線と右手を、IK で指定したターゲットへ向けるサンプル。
/// </summary>
/// <remarks>
/// 使い方:
/// 1. Avatar が Humanoid に設定されたキャラクターにこのスクリプトを追加する。
/// 2. Animator Controller のレイヤー設定で IK Pass を有効にする（無効だと OnAnimatorIK が呼ばれない）。
/// 3. Look Target と Right Hand Target に、シーン上の空の GameObject などを指定する。
/// </remarks>
[RequireComponent(typeof(Animator))]
public class LookAtIK : MonoBehaviour
{
    [Header("視線")]
    [SerializeField]
    private Transform lookTarget;

    [Tooltip("視線 IK 全体の影響度（0 で無効、1 で最大）")]
    [Range(0f, 1f)]
    [SerializeField]
    private float lookWeight = 1f;

    [Tooltip("体の向きへの影響度")]
    [Range(0f, 1f)]
    [SerializeField]
    private float bodyWeight = 0.2f;

    [Tooltip("頭の向きへの影響度")]
    [Range(0f, 1f)]
    [SerializeField]
    private float headWeight = 0.8f;

    [Header("右手")]
    [SerializeField]
    private Transform rightHandTarget;

    [Range(0f, 1f)]
    [SerializeField]
    private float rightHandWeight = 1f;

    private Animator animator;

    private void Awake()
    {
        animator = GetComponent<Animator>();
    }

    private void OnAnimatorIK(int layerIndex)
    {
        if (lookTarget != null)
        {
            // 引数は順に、全体・体・頭・目の影響度、および可動範囲の制限の強さ。
            animator.SetLookAtWeight(lookWeight, bodyWeight, headWeight, 1f, 0.5f);
            animator.SetLookAtPosition(lookTarget.position);
        }
        else
        {
            animator.SetLookAtWeight(0f);
        }

        if (rightHandTarget != null)
        {
            animator.SetIKPositionWeight(AvatarIKGoal.RightHand, rightHandWeight);
            animator.SetIKRotationWeight(AvatarIKGoal.RightHand, rightHandWeight);
            animator.SetIKPosition(AvatarIKGoal.RightHand, rightHandTarget.position);
            animator.SetIKRotation(AvatarIKGoal.RightHand, rightHandTarget.rotation);
        }
        else
        {
            animator.SetIKPositionWeight(AvatarIKGoal.RightHand, 0f);
            animator.SetIKRotationWeight(AvatarIKGoal.RightHand, 0f);
        }
    }
}
