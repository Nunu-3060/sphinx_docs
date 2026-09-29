// 第 4 章 制御構文
// for 文、while 文、do-while 文と、break、continue の動きを確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using UnityEngine;

public class LoopSample : MonoBehaviour
{
    private void Start()
    {
        // ---- for 文: 1 から 10 までの合計 ----
        int sum = 0;
        for (int i = 1; i <= 10; i++)
        {
            sum += i;
        }
        Debug.Log($"1 から 10 までの合計: {sum}");

        // ---- while 文: 条件を満たす間くり返す ----
        int hp = 100;
        int turn = 0;
        while (hp > 0)
        {
            hp -= 30;
            turn++;
        }
        Debug.Log($"{turn} ターンで HP が 0 以下になった（HP: {hp}）");

        // ---- do-while 文: 条件を後で判定するため、最低 1 回は実行される ----
        int tries = 0;
        do
        {
            tries++;
        }
        while (tries < 0);
        Debug.Log($"do-while の実行回数: {tries}");

        // ---- continue と break ----
        // continue は残りの処理を飛ばして次の周回へ進み、break はループそのものを抜けます。
        string log = "";
        for (int i = 1; i <= 10; i++)
        {
            if (i % 2 == 0)
            {
                continue;
            }
            if (i > 7)
            {
                break;
            }
            log += i + " ";
        }
        Debug.Log($"7 までの奇数: {log}");
    }
}
