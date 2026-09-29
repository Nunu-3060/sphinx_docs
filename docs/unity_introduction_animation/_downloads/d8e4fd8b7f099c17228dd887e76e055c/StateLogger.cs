using UnityEngine;

/// <summary>
/// ステートに入ったときと出たときに、Console ウィンドウへログを出力する StateMachineBehaviour。
/// </summary>
/// <remarks>
/// 使い方: Animator ウィンドウでステートを選択し、Inspector ウィンドウの Add Behaviour から
/// StateLogger を追加する。
/// </remarks>
public class StateLogger : StateMachineBehaviour
{
    [Tooltip("ログに表示するステートの名前")]
    [SerializeField]
    private string label = "State";

    public override void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        Debug.Log($"[{animator.name}] {label} に入った（レイヤー {layerIndex}）");
    }

    public override void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        // normalizedTime は 1 回分の再生を 1 とした再生位置。ループするステートでは 1 を超える。
        Debug.Log($"[{animator.name}] {label} から出た（再生位置 {stateInfo.normalizedTime:F2}）");
    }
}
