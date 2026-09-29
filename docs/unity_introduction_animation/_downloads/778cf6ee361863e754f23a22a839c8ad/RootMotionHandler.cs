using UnityEngine;

/// <summary>
/// Root Motion による移動量を CharacterController に渡し、重力も加えて移動させるサンプル。
/// </summary>
/// <remarks>
/// 使い方: Animator と CharacterController を持つキャラクターに追加する。
/// OnAnimatorMove を定義すると、Animator の Apply Root Motion の表示が
/// Handled by Script になり、Root Motion の適用はこのスクリプトが担当する。
/// </remarks>
[RequireComponent(typeof(Animator))]
[RequireComponent(typeof(CharacterController))]
public class RootMotionHandler : MonoBehaviour
{
    [Tooltip("接地中に下向きへ加え続ける速度。地面から浮かないようにするための値。")]
    [SerializeField]
    private float groundedVerticalSpeed = -1f;

    private Animator animator;
    private CharacterController characterController;
    private float verticalSpeed;

    private void Awake()
    {
        animator = GetComponent<Animator>();
        characterController = GetComponent<CharacterController>();
    }

    private void OnAnimatorMove()
    {
        // アニメーションが今回のフレームで動かそうとした移動量と回転量
        Vector3 deltaPosition = animator.deltaPosition;
        Quaternion deltaRotation = animator.deltaRotation;

        // 垂直方向の移動は、アニメーションではなく重力で決める。
        if (characterController.isGrounded && verticalSpeed < 0f)
        {
            verticalSpeed = groundedVerticalSpeed;
        }
        else
        {
            verticalSpeed += Physics.gravity.y * Time.deltaTime;
        }

        deltaPosition.y = verticalSpeed * Time.deltaTime;

        characterController.Move(deltaPosition);
        transform.rotation *= deltaRotation;
    }
}
