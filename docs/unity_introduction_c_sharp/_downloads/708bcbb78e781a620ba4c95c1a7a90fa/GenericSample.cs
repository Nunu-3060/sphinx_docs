// 第 9 章 C# の発展的な機能
// ジェネリクス（型をパラメーターとして受け取る仕組み）を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using System;
using UnityEngine;

public class GenericSample : MonoBehaviour
{
    private void Start()
    {
        // 同じ Swap メソッドを、int にも string にも使えます。
        int a = 1;
        int b = 2;
        Swap(ref a, ref b);
        Debug.Log($"a = {a}, b = {b}");

        string first = "前";
        string second = "後";
        Swap(ref first, ref second);
        Debug.Log($"first = {first}, second = {second}");

        // 型制約（where T : IComparable<T>）により、大小比較ができる型だけを受け付けます。
        int[] numbers = { 3, 9, 4 };
        string[] fruits = { "りんご", "みかん", "ぶどう" };
        Debug.Log($"最大値: {Max(numbers)}");
        Debug.Log($"辞書順で最後: {Max(fruits)}");
    }

    // T には、呼び出し時に実際の型（int や string など）が当てはめられます。
    private void Swap<T>(ref T x, ref T y)
    {
        T temp = x;
        x = y;
        y = temp;
    }

    private T Max<T>(T[] values) where T : IComparable<T>
    {
        T max = values[0];
        foreach (T value in values)
        {
            if (value.CompareTo(max) > 0)
            {
                max = value;
            }
        }
        return max;
    }
}
