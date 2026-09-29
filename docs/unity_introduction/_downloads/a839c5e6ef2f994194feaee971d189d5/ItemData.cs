using UnityEngine;

namespace UnityIntroduction.Chapter08
{
    /// <summary>
    /// アイテムの設定値をまとめた ScriptableObject です。
    /// </summary>
    /// <remarks>
    /// Project ウィンドウで右クリックし、
    /// Create &gt; Unity Introduction &gt; Item Data からアセットを作成できます。
    /// </remarks>
    [CreateAssetMenu(fileName = "NewItemData", menuName = "Unity Introduction/Item Data")]
    public class ItemData : ScriptableObject
    {
        [SerializeField]
        private string _displayName = "新しいアイテム";

        [SerializeField, TextArea]
        private string _description = "";

        [SerializeField, Min(0)]
        private int _price = 100;

        [SerializeField]
        private Sprite _icon;

        public string DisplayName => _displayName;

        public string Description => _description;

        public int Price => _price;

        public Sprite Icon => _icon;
    }
}
