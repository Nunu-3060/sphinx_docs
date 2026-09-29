using System;
using UnityEngine;
using UnityEngine.Events;

namespace UnityIntroduction.Chapter08
{
    /// <summary>
    /// 体力を管理し、変化したときと 0 になったときにイベントで通知します。
    /// </summary>
    public class Health : MonoBehaviour
    {
        [SerializeField, Min(1)]
        private int _maxHealth = 3;

        [SerializeField, Tooltip("体力が 0 になったときに呼ばれる処理（Inspector で設定します）")]
        private UnityEvent _died = new UnityEvent();

        /// <summary>
        /// 体力が変化したときに、変化後の体力を引数として発生します。
        /// </summary>
        public event Action<int> HealthChanged;

        /// <summary>
        /// 現在の体力です。
        /// </summary>
        public int CurrentHealth { get; private set; }

        private void Awake()
        {
            CurrentHealth = _maxHealth;
        }

        /// <summary>
        /// 指定した量のダメージを与えます。
        /// </summary>
        /// <param name="amount">ダメージ量（1 以上。0 以下の場合は何もしません）</param>
        public void TakeDamage(int amount)
        {
            if (CurrentHealth <= 0 || amount <= 0)
            {
                return;
            }

            CurrentHealth = Mathf.Max(CurrentHealth - amount, 0);
            HealthChanged?.Invoke(CurrentHealth);

            if (CurrentHealth == 0)
            {
                _died.Invoke();
            }
        }

        [ContextMenu("1 ダメージを与える")]
        private void TakeOneDamage()
        {
            TakeDamage(1);
        }
    }
}
