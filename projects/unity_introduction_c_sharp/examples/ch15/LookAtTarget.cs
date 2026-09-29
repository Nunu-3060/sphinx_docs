// 第 15 章 ベクトルと移動・回転
// 目標のオブジェクトの方向へ滑らかに向きを変え、一定の距離まで近づくスクリプトです。
// 使い方: シーンに Cube を作成してアタッチし、Target にシーン内の別の GameObject を設定します。
using UnityEngine;

public class LookAtTarget : MonoBehaviour
{
    [SerializeField] private Transform _target;

    [Tooltip("1 秒あたりに回転する最大の角度（度）")]
    [SerializeField] private float _turnSpeed = 180f;

    [Tooltip("1 秒あたりに進む距離（m）")]
    [SerializeField] private float _moveSpeed = 2f;

    [Tooltip("目標にこの距離まで近づいたら止まる")]
    [SerializeField] private float _stopDistance = 1.5f;

    private void Update()
    {
        if (_target == null)
        {
            return;
        }

        // 自分から目標へ向かうベクトル（目標の位置 - 自分の位置）
        Vector3 toTarget = _target.position - transform.position;
        toTarget.y = 0f;    // 上下には傾かないように、水平方向の成分だけを使います。

        if (toTarget.sqrMagnitude < 0.0001f)
        {
            return;
        }

        // 目標の方向を向く回転を求め、現在の回転から少しずつ近づけます。
        Quaternion targetRotation = Quaternion.LookRotation(toTarget);
        transform.rotation = Quaternion.RotateTowards(transform.rotation, targetRotation, _turnSpeed * Time.deltaTime);

        // 十分に離れていれば、自分の正面（transform.forward）の方向へ進みます。
        if (toTarget.magnitude > _stopDistance)
        {
            transform.position += transform.forward * _moveSpeed * Time.deltaTime;
        }
    }
}
