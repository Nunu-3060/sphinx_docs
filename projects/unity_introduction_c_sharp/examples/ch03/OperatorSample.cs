// 第 3 章 演算子と式
// 算術演算子、代入演算子、比較演算子、論理演算子の動きを確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using UnityEngine;

public class OperatorSample : MonoBehaviour
{
    private void Start()
    {
        // ---- 算術演算子 ----
        int a = 7;
        int b = 2;
        Debug.Log($"a + b = {a + b}");
        Debug.Log($"a - b = {a - b}");
        Debug.Log($"a * b = {a * b}");
        Debug.Log($"a / b = {a / b}");
        Debug.Log($"a % b = {a % b}");

        // 整数どうしの割り算では、小数部分が切り捨てられます。
        // 小数の結果が欲しいときは、どちらかを float に変換します。
        Debug.Log($"(float)a / b = {(float)a / b}");

        // 負の数の割り算は 0 の方向へ切り捨てられ、余りの符号は割られる数と同じになります。
        Debug.Log($"-7 / 2 = {-7 / 2}");
        Debug.Log($"-7 % 2 = {-7 % 2}");

        // 掛け算は足し算より先に計算されます。かっこで順序を変えられます。
        Debug.Log($"2 + 3 * 4 = {2 + 3 * 4}");
        Debug.Log($"(2 + 3) * 4 = {(2 + 3) * 4}");

        // ---- 代入演算子とインクリメント ----
        int hp = 100;
        hp -= 25;   // hp = hp - 25 と同じ
        hp *= 2;    // hp = hp * 2 と同じ
        Debug.Log($"hp = {hp}");

        int count = 0;
        count++;    // count = count + 1 と同じ
        count++;
        Debug.Log($"count = {count}");

        // ---- 比較演算子と論理演算子 ----
        int age = 15;
        bool hasTicket = true;
        Debug.Log($"age >= 18: {age >= 18}");
        Debug.Log($"チケットがあり、かつ 12 歳以上: {hasTicket && age >= 12}");
        Debug.Log($"18 歳以上、またはチケットがある: {age >= 18 || hasTicket}");
        Debug.Log($"チケットがない: {!hasTicket}");

        // ---- 小数の誤差 ----
        // 小数は 2 進数で近似して保存されるため、わずかな誤差が生じることがあります。
        float x = 0.1f + 0.6f;
        Debug.Log($"0.1f + 0.6f == 0.7f: {x == 0.7f}");

        // float どうしがほぼ等しいかを調べるには Mathf.Approximately を使います。
        Debug.Log($"Mathf.Approximately(x, 0.7f): {Mathf.Approximately(x, 0.7f)}");
    }
}
