using UnityEngine;
using UnityEngine.InputSystem;

namespace UnityIntroduction.Chapter11
{
    /// <summary>
    /// スペースキーを押すたびに、Particle System からパーティクルを一度に放出します。
    /// </summary>
    public class ParticleBurst : MonoBehaviour
    {
        [SerializeField]
        private ParticleSystem _particleSystem;

        [SerializeField, Min(1), Tooltip("一度に放出するパーティクルの数")]
        private int _count = 30;

        private void Update()
        {
            Keyboard keyboard = Keyboard.current;
            if (keyboard != null && keyboard.spaceKey.wasPressedThisFrame)
            {
                // Emit は Emission モジュールの設定とは別に、指定した数だけ即座に放出します。
                _particleSystem.Emit(_count);
            }
        }
    }
}
