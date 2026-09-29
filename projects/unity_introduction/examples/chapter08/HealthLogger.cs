using UnityEngine;

namespace UnityIntroduction.Chapter08
{
    /// <summary>
    /// Health の HealthChanged イベントを購読し、体力の変化をログに表示します。
    /// </summary>
    public class HealthLogger : MonoBehaviour
    {
        [SerializeField]
        private Health _health;

        private void OnEnable()
        {
            if (_health != null)
            {
                _health.HealthChanged += OnHealthChanged;
            }
        }

        private void OnDisable()
        {
            // 購読したイベントは必ず解除します。
            if (_health != null)
            {
                _health.HealthChanged -= OnHealthChanged;
            }
        }

        private void OnHealthChanged(int currentHealth)
        {
            Debug.Log($"残りの体力: {currentHealth}");
        }
    }
}
