using UnityEngine;
using UnityEngine.InputSystem;

/// <summary>
/// キーボード入力に応じて Animator の Speed パラメーターを更新し、
/// Blend Tree で待機・歩行・走行を切り替えるサンプル。
/// </summary>
/// <remarks>
/// 使い方:
/// 1. Animator Controller に Float 型のパラメーター "Speed" を追加する。
/// 2. Speed で待機（0）・歩行（0.5）・走行（1）をブレンドする 1D の Blend Tree を作る。
/// 3. Animator コンポーネントを持つ GameObject にこのスクリプトを追加する。
/// W / A / S / D キーで移動し、Shift キーを押している間は走る。
/// 入力には Input System パッケージを使用する。
/// </remarks>
[RequireComponent(typeof(Animator))]
public class PlayerAnimatorController : MonoBehaviour
{
    // パラメーター名は文字列ではなくハッシュ値で指定すると、毎フレームの文字列処理を省ける。
    private static readonly int SpeedHash = Animator.StringToHash("Speed");

    [Tooltip("Speed の値が目標値に近づくまでの時間（秒）。大きいほど滑らかに変化する。")]
    [Min(0f)]
    [SerializeField]
    private float speedDampTime = 0.1f;

    [Tooltip("移動方向へ向きを変える速さ（度/秒）")]
    [SerializeField]
    private float turnSpeed = 720f;

    private Animator animator;

    private void Awake()
    {
        animator = GetComponent<Animator>();
    }

    private void Update()
    {
        Vector2 input = ReadMoveInput();
        bool isRunning = Keyboard.current != null && Keyboard.current.leftShiftKey.isPressed;

        // 入力の大きさ（0 から 1）に、歩行なら 0.5、走行なら 1 を掛けて Speed とする。
        float targetSpeed = input.magnitude * (isRunning ? 1f : 0.5f);

        // dampTime を指定すると、値が急に変わらず徐々に目標値へ近づく。
        animator.SetFloat(SpeedHash, targetSpeed, speedDampTime, Time.deltaTime);

        // 入力がある間は、キャラクターを入力方向へ向ける。
        if (input.sqrMagnitude > 0.01f)
        {
            Vector3 direction = new Vector3(input.x, 0f, input.y);
            Quaternion targetRotation = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.RotateTowards(
                transform.rotation,
                targetRotation,
                turnSpeed * Time.deltaTime);
        }
    }

    /// <summary>
    /// W / A / S / D キーの入力を、長さ 1 以下の 2 次元ベクトルとして返す。
    /// </summary>
    private static Vector2 ReadMoveInput()
    {
        Keyboard keyboard = Keyboard.current;
        if (keyboard == null)
        {
            return Vector2.zero;
        }

        Vector2 input = Vector2.zero;
        if (keyboard.wKey.isPressed)
        {
            input.y += 1f;
        }

        if (keyboard.sKey.isPressed)
        {
            input.y -= 1f;
        }

        if (keyboard.dKey.isPressed)
        {
            input.x += 1f;
        }

        if (keyboard.aKey.isPressed)
        {
            input.x -= 1f;
        }

        // 斜め入力で長さが 1 を超えないようにする。
        return Vector2.ClampMagnitude(input, 1f);
    }
}
