// 第 9 章 C# の発展的な機能
// デリゲート（Action と Func）、ラムダ式、イベントを確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using System;
using UnityEngine;

public class DelegateSample : MonoBehaviour
{
    private void Start()
    {
        // ---- Action: 戻り値のないメソッドを入れる変数 ----
        Action<string> say = ShowMessage;
        say("メソッドを変数に入れて呼び出した。");

        // ---- Func: 戻り値のあるメソッドを入れる変数（<> の中の最後の型が戻り値の型）----
        // ラムダ式を使うと、その場でメソッドを定義できます。
        Func<int, int, int> multiply = (x, y) => x * y;
        Debug.Log($"multiply(6, 7) = {multiply(6, 7)}");

        // ---- イベント ----
        ScoreCounter counter = new ScoreCounter();

        // += で、イベントが発生したときに呼び出してほしいメソッドを登録します。
        counter.ScoreChanged += score => Debug.Log($"スコアが {score} になった。");
        counter.ScoreChanged += CheckHighScore;

        counter.Add(50);
        counter.Add(80);

        // -= で登録を解除すると、それ以降は呼び出されません。
        counter.ScoreChanged -= CheckHighScore;
        counter.Add(10);
    }

    private void ShowMessage(string message)
    {
        Debug.Log(message);
    }

    private void CheckHighScore(int score)
    {
        if (score >= 100)
        {
            Debug.Log("ハイスコア達成！");
        }
    }

    // スコアを管理し、スコアが変わったことをイベントで知らせるクラスです。
    // DelegateSample の中でだけ使うため、クラスの中に private なクラスとして定義しています。
    private class ScoreCounter
    {
        public event Action<int> ScoreChanged;

        public int Score { get; private set; }

        public void Add(int points)
        {
            Score += points;

            // 登録されたメソッドがなければ ScoreChanged は null なので、?. で null のときは呼び出さないようにします。
            ScoreChanged?.Invoke(Score);
        }
    }
}
