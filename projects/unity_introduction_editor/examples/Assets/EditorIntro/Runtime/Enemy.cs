using UnityEngine;

namespace EditorIntro
{
    /// <summary>
    /// 第 6 章のカスタムエディター（EnemyEditor）で表示するコンポーネントです。
    /// </summary>
    public class Enemy : MonoBehaviour
    {
        [SerializeField] private string enemyName = "Slime";

        [Min(1)]
        [SerializeField] private int maxHp = 100;

        [Min(0)]
        [SerializeField] private int hp = 100;

        [Min(0f)]
        [SerializeField] private float moveSpeed = 2f;

        public string EnemyName => enemyName;
        public int MaxHp => maxHp;
        public int Hp => hp;
        public float MoveSpeed => moveSpeed;
    }
}
