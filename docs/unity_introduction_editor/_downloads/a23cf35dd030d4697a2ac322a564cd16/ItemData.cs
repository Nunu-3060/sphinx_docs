using UnityEngine;

namespace EditorIntro
{
    /// <summary>
    /// 第 10 章のサンプルです。
    /// CreateAssetMenu 属性により、Project ウィンドウの「Create」メニューからアセットを作成できます。
    /// </summary>
    [CreateAssetMenu(fileName = "NewItemData", menuName = "Editor Intro/Item Data")]
    public class ItemData : ScriptableObject
    {
        [SerializeField] private string itemName = "Potion";

        [Min(0)]
        [SerializeField] private int price = 100;

        public string ItemName => itemName;
        public int Price => price;
    }
}
