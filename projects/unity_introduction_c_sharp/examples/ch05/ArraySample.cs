// 第 5 章 配列とコレクション
// 配列の作成、要素へのアクセス、for 文と foreach 文による列挙を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using UnityEngine;

public class ArraySample : MonoBehaviour
{
    private void Start()
    {
        // 要素数 3 の配列を作成します。int の要素は最初は 0 です。
        int[] scores = new int[3];
        scores[0] = 80;
        scores[1] = 65;
        scores[2] = 92;
        Debug.Log($"要素数: {scores.Length}, 先頭: {scores[0]}, 末尾: {scores[scores.Length - 1]}");

        // 作成と同時に要素を指定することもできます。
        string[] items = { "薬草", "毒消し", "鍵" };

        // for 文では、インデックス（添字）を使って要素にアクセスします。
        for (int i = 0; i < items.Length; i++)
        {
            Debug.Log($"items[{i}] = {items[i]}");
        }

        // foreach 文では、先頭から順に要素を 1 つずつ取り出します。
        int total = 0;
        foreach (int score in scores)
        {
            total += score;
        }
        Debug.Log($"合計点: {total}");

        // 2 次元配列（3 行 4 列）。マップのマス目などを表すのに使えます。
        int[,] map = new int[3, 4];
        map[1, 2] = 5;
        Debug.Log($"行数: {map.GetLength(0)}, 列数: {map.GetLength(1)}, map[1, 2] = {map[1, 2]}");
    }
}
