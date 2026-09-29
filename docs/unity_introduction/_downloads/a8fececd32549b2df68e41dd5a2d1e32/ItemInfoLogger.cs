using UnityEngine;

namespace UnityIntroduction.Chapter08
{
    /// <summary>
    /// Inspector で指定した ItemData の内容をログに表示します。
    /// </summary>
    public class ItemInfoLogger : MonoBehaviour
    {
        [SerializeField]
        private ItemData _item;

        private void Start()
        {
            if (_item == null)
            {
                Debug.LogWarning("ItemData が設定されていません。", this);
                return;
            }

            Debug.Log($"{_item.DisplayName}（{_item.Price} G）: {_item.Description}");
        }
    }
}
