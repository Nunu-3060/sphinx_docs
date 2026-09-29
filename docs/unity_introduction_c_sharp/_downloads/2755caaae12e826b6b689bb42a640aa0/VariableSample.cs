// 第 2 章 変数と型
// 変数の宣言、型変換、var、定数の使い方を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using UnityEngine;

public class VariableSample : MonoBehaviour
{
    // const を付けたフィールドは、後から値を変更できない定数になります。
    private const int MaxLevel = 99;

    private void Start()
    {
        // 代表的な型の変数を宣言し、同時に初期値を代入します。
        int hp = 100;
        float speed = 3.5f;
        bool isAlive = true;
        char rank = 'A';
        string playerName = "Alice";
        Debug.Log($"名前: {playerName}, HP: {hp}, 速さ: {speed}, 生存: {isAlive}, ランク: {rank}");

        // 変数の値は後から変更できます。
        hp = hp - 30;
        Debug.Log($"ダメージ後の HP: {hp}");

        // int から float への変換は情報が失われないため、自動で行われます（暗黙的な型変換）。
        int coins = 7;
        float coinsAsFloat = coins;
        Debug.Log($"coinsAsFloat: {coinsAsFloat}");

        // float から int への変換にはキャストが必要です（明示的な型変換）。小数部分は切り捨てられます。
        // Mathf.RoundToInt は最も近い整数に丸めます。
        float distance = 9.8f;
        int truncated = (int)distance;
        int rounded = Mathf.RoundToInt(distance);
        Debug.Log($"切り捨て: {truncated}, 丸め: {rounded}");

        // 文字列を数値に変換するには int.Parse などを使います。
        int score = int.Parse("250");
        Debug.Log($"score + 1 = {score + 1}");

        // 文字列と数値を + でつなぐと、文字列として連結されます。
        Debug.Log("score: " + score);

        // var を使うと、右辺の値から型が推論されます（ここでは int になります）。
        var level = 5;
        Debug.Log($"level の型: {level.GetType().Name}");

        Debug.Log($"最大レベル: {MaxLevel}");
    }
}
