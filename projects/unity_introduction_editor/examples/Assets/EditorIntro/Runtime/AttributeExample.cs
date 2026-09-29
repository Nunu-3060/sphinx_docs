using UnityEngine;

namespace EditorIntro
{
    /// <summary>
    /// 第 4 章のサンプルです。
    /// 属性を付けるだけで Inspector ウィンドウの表示を調整できることを示します。
    /// </summary>
    public class AttributeExample : MonoBehaviour
    {
        public enum Difficulty
        {
            // InspectorName 属性で、Inspector ウィンドウに表示する名前を変更できます。
            [InspectorName("かんたん")] Easy,
            [InspectorName("ふつう")] Normal,
            [InspectorName("むずかしい")] Hard,
        }

        [Header("基本情報")]
        [Tooltip("キャラクターの名前です。マウスカーソルを重ねると、この説明が表示されます。")]
        [SerializeField] private string characterName = "Hero";

        [Min(1)]
        [SerializeField] private int level = 1;

        [SerializeField] private Difficulty difficulty = Difficulty.Normal;

        [Space(12)]
        [Header("能力値")]
        [Range(0f, 100f)]
        [SerializeField] private float hitRate = 80f;

        [Range(1, 10)]
        [SerializeField] private int attackCount = 1;

        [Header("説明文")]
        [TextArea(2, 5)]
        [SerializeField] private string profile = "";

        // public フィールドは SerializeField 属性を付けなくても保存・表示されます。
        public Color themeColor = Color.white;

        // HideInInspector 属性を付けると、保存はされますが表示されません。
        [HideInInspector] public int hiddenValue;

        public string CharacterName => characterName;
        public int Level => level;
        public Difficulty CurrentDifficulty => difficulty;
        public float HitRate => hitRate;
        public int AttackCount => attackCount;
        public string Profile => profile;
    }
}
