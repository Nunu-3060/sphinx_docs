// 第 5 章 配列とコレクション
// List<T> と Dictionary<TKey, TValue> の基本的な使い方を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using System.Collections.Generic;
using UnityEngine;

public class CollectionSample : MonoBehaviour
{
    private void Start()
    {
        // ---- List<T>: 要素数を後から変えられるコレクション ----
        List<string> party = new List<string>();
        party.Add("勇者");
        party.Add("魔法使い");
        party.Add("僧侶");
        party.Remove("魔法使い");
        Debug.Log($"人数: {party.Count}, 先頭: {party[0]}");
        bool hasPriest = party.Contains("僧侶");
        Debug.Log($"僧侶がいる: {hasPriest}");

        foreach (string member in party)
        {
            Debug.Log($"メンバー: {member}");
        }

        // ---- Dictionary<TKey, TValue>: キーを指定して値を取り出すコレクション ----
        Dictionary<string, int> prices = new Dictionary<string, int>
        {
            { "薬草", 8 },
            { "毒消し", 10 },
        };

        // キーがなければ追加され、あれば値が上書きされます。
        prices["鍵"] = 50;
        int herbPrice = prices["薬草"];
        Debug.Log($"薬草の値段: {herbPrice}");

        // 存在しないキーを prices["剣"] のように読み取ると例外が発生するため、TryGetValue で確認します。
        if (prices.TryGetValue("剣", out int swordPrice))
        {
            Debug.Log($"剣の値段: {swordPrice}");
        }
        else
        {
            Debug.Log("剣は売っていない。");
        }

        foreach (KeyValuePair<string, int> pair in prices)
        {
            Debug.Log($"{pair.Key}: {pair.Value} G");
        }
    }
}
