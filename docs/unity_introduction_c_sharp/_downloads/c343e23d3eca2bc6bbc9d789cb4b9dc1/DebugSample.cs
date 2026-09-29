// 第 20 章 デバッグの方法
// Debug クラスのさまざまな機能を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウと Scene ビューを確認します。
using UnityEngine;

public class DebugSample : MonoBehaviour
{
    [SerializeField] private int _hp = 10;

    private void Start()
    {
        // 第 2 引数に GameObject などを渡すと、Console ウィンドウでログを選んだときに、そのオブジェクトが強調表示されます。
        Debug.Log($"{name} の HP: {_hp}", this);

        // 警告（黄色）とエラー（赤色）のログ
        if (_hp < 20)
        {
            Debug.LogWarning("HP が少なくなっている。");
        }
        if (_hp <= 0)
        {
            Debug.LogError("HP が 0 以下になった。");
        }

        // Debug.Assert は、条件が false のときだけエラーのログを表示します。
        Debug.Assert(_hp >= 0, "HP が負の値になっている。");
    }

    private void Update()
    {
        // Scene ビューに、このオブジェクトの正面方向の線を描きます（Game ビューでは、Gizmos を有効にしたときだけ表示されます）。
        Debug.DrawRay(transform.position, transform.forward * 2f, Color.green);
    }
}
