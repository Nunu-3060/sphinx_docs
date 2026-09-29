using System;
using UnityEngine;

/// <summary>
/// Debug クラスによるログ出力の基本を示すサンプルです。
/// 任意の GameObject に追加して再生すると、Console ウィンドウにログが出力されます。
/// </summary>
public class LogExample : MonoBehaviour
{
    [SerializeField]
    private int hitPoint = 100;

    private void Start()
    {
        // 通常のログです。Console ウィンドウに白いアイコンで表示されます。
        Debug.Log("ゲームを開始しました。");

        // 警告です。黄色いアイコンで表示されます。
        if (hitPoint > 1000)
        {
            Debug.LogWarning("HP の初期値が大きすぎる可能性があります。");
        }

        // 第 2 引数に this を渡すと、Console ウィンドウでこのログをクリックしたときに
        // この GameObject が Hierarchy ウィンドウでハイライトされます。
        Debug.Log($"{name} の HP は {hitPoint} です。", this);

        // 条件が false のときだけエラーとして出力します。
        // Debug.Assert はエディターと Development Build でのみ実行されます。
        Debug.Assert(hitPoint > 0, "HP は 1 以上である必要があります。", this);
    }

    /// <summary>
    /// Inspector ウィンドウでこのコンポーネントを右クリックし、
    /// メニューから「エラーを出力する」を選ぶと実行されます。
    /// </summary>
    [ContextMenu("エラーを出力する")]
    private void OutputError()
    {
        // エラーです。赤いアイコンで表示されます。
        Debug.LogError("エラーのテストです。", this);
    }

    /// <summary>
    /// Inspector ウィンドウでこのコンポーネントを右クリックし、
    /// メニューから「例外を出力する」を選ぶと実行されます。
    /// </summary>
    [ContextMenu("例外を出力する")]
    private void OutputException()
    {
        try
        {
            int[] values = new int[3];

            // 配列の範囲外にアクセスするため、例外が発生します。
            values[5] = 1;
        }
        catch (IndexOutOfRangeException e)
        {
            // 例外を無視せず、スタックトレース付きで出力します。
            Debug.LogException(e, this);
        }
    }
}
