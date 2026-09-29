using UnityEngine;

namespace EditorIntro
{
    /// <summary>
    /// 第 7 章のサンプルです。
    /// 自作の PropertyDrawer と DecoratorDrawer が適用されるフィールドを持ちます。
    /// </summary>
    public class DrawerExample : MonoBehaviour
    {
        // NoteAttribute → NoteDrawer（DecoratorDrawer）で補足説明を表示します。
        // MinMaxRange 型 → MinMaxRangeDrawer（PropertyDrawer）で表示します。
        [Note("敵が出現する間隔（秒）を、最小値と最大値で指定します。")]
        [SerializeField] private MinMaxRange spawnInterval = new MinMaxRange(1f, 3f);

        // TagSelectorAttribute → TagSelectorDrawer（PropertyDrawer）で表示します。
        [TagSelector]
        [SerializeField] private string targetTag = "Player";

        public MinMaxRange SpawnInterval => spawnInterval;
        public string TargetTag => targetTag;
    }
}
