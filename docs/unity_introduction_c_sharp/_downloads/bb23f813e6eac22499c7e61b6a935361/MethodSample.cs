// 第 6 章 メソッド
// メソッドの定義と呼び出し、オーバーロード、既定値付き引数、ref と out を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using UnityEngine;

public class MethodSample : MonoBehaviour
{
    private void Start()
    {
        // 戻り値のあるメソッドを呼び出します。
        int sum = Add(3, 4);
        Debug.Log($"Add(3, 4) = {sum}");

        // オーバーロード: 引数の型によって、呼び出されるメソッドが変わります。
        Debug.Log($"Add(1.5f, 2.25f) = {Add(1.5f, 2.25f)}");

        // 既定値付き引数と名前付き引数
        Greet("Alice");
        Greet("Bob", "おはよう");
        Greet(greeting: "こんばんは", name: "Carol");

        // ref: 呼び出し元の変数そのものを書き換えます。
        int level = 1;
        LevelUp(ref level);
        Debug.Log($"level = {level}");

        // out: メソッドから 2 つ目以降の結果を受け取ります。
        if (TryDivide(10, 3, out int quotient, out int remainder))
        {
            Debug.Log($"10 ÷ 3 = {quotient} 余り {remainder}");
        }

        // 受け取る必要のない out 引数は _ で捨てられます。
        if (!TryDivide(10, 0, out _, out _))
        {
            Debug.Log("0 では割れない。");
        }

        Debug.Log($"Square(5) = {Square(5)}");
    }

    // 2 つの int を足した結果を返します。
    private int Add(int x, int y)
    {
        return x + y;
    }

    // 名前が同じで、引数の型が違うメソッド（オーバーロード）です。
    private float Add(float x, float y)
    {
        return x + y;
    }

    // 戻り値のないメソッドには void と書きます。greeting を省略すると "こんにちは" になります。
    private void Greet(string name, string greeting = "こんにちは")
    {
        Debug.Log($"{greeting}、{name}");
    }

    private void LevelUp(ref int level)
    {
        level++;
    }

    // 割り算の商と余りを out 引数で返します。割れないときは false を返します。
    private bool TryDivide(int dividend, int divisor, out int quotient, out int remainder)
    {
        if (divisor == 0)
        {
            quotient = 0;
            remainder = 0;
            return false;
        }
        quotient = dividend / divisor;
        remainder = dividend % divisor;
        return true;
    }

    // 処理が 1 つの式だけのメソッドは、=> を使って短く書けます（式形式のメンバー）。
    private int Square(int x) => x * x;
}
