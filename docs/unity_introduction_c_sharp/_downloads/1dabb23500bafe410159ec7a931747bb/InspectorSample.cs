// 第 12 章 Inspector ウィンドウとの連携
// フィールドを Inspector ウィンドウに表示する方法と、表示を整える属性を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Inspector ウィンドウの表示を確認します。
using System;
using System.Collections.Generic;
using UnityEngine;

public class InspectorSample : MonoBehaviour
{
    // public なフィールドは Inspector ウィンドウに表示されますが、ほかのスクリプトからも書き換えられてしまいます。
    public int PublicValue = 1;

    // [SerializeField] を付けると、private のまま Inspector ウィンドウに表示できます（推奨）。
    [Header("移動")]
    [Tooltip("1 秒あたりに進む距離（m）")]
    [SerializeField] private float _moveSpeed = 5f;

    // [Range] を付けると、スライダーで値を設定できます。
    [Range(0f, 1f)]
    [SerializeField] private float _volume = 0.5f;

    [Header("ステータス")]
    [Min(1)]
    [SerializeField] private int _maxHp = 100;

    [Space(10)]
    [TextArea(2, 4)]
    [SerializeField] private string _description = "説明文を入力します。";

    // 配列や List<T> も表示されます。
    [SerializeField] private string[] _tags = { "Player" };

    // [Serializable] を付けたクラスは、フィールドをまとめて表示できます。
    [SerializeField] private List<DropItem> _dropItems = new List<DropItem>();

    // Inspector ウィンドウに表示しない private なフィールドです（[SerializeField] がないため）。
    private int _currentHp;

    // 自動実装プロパティは、[field: SerializeField] を付けると表示できます。
    [field: SerializeField] public int Level { get; private set; } = 1;

    private void Start()
    {
        _currentHp = _maxHp;
        Debug.Log($"速さ: {_moveSpeed}, 音量: {_volume}, HP: {_currentHp}, レベル: {Level}");
        Debug.Log($"説明: {_description}, タグの数: {_tags.Length}, ドロップアイテムの数: {_dropItems.Count}");
    }

    // [Serializable] を付けると、このクラスの public なフィールドと [SerializeField] 付きのフィールドが保存・表示されます。
    [Serializable]
    private class DropItem
    {
        public string Name;

        [Range(0f, 1f)]
        public float Probability;
    }
}
