using System;
using UnityEngine;

namespace UnityIntroduction.RollABall
{
    /// <summary>
    /// プレイヤーが触れると回収されるアイテムです。
    /// </summary>
    /// <remarks>
    /// Collider（Box Collider など）を付け、Is Trigger を有効にしておきます。
    /// Collider は抽象クラスなので、RequireComponent で自動的に追加されることはありません。
    /// </remarks>
    [RequireComponent(typeof(Collider))]
    public class Pickup : MonoBehaviour
    {
        [SerializeField, Tooltip("回収したときに生成するエフェクト（省略可）")]
        private ParticleSystem _effectPrefab;

        [SerializeField, Tooltip("回収したときに再生する効果音（省略可）")]
        private AudioClip _sound;

        /// <summary>
        /// いずれかの Pickup が回収されたときに発生します。
        /// </summary>
        /// <remarks>
        /// static なイベントなので、Pickup を 1 つずつ参照しなくても購読できます。
        /// </remarks>
        public static event Action<Pickup> Collected;

        private void OnTriggerEnter(Collider other)
        {
            if (!other.CompareTag("Player"))
            {
                return;
            }

            if (_effectPrefab != null)
            {
                Instantiate(_effectPrefab, transform.position, Quaternion.identity);
            }

            if (_sound != null)
            {
                // この GameObject はすぐに破棄されるため、再生用の AudioSource を一時的に生成する
                // PlayClipAtPoint を使います。PlayClipAtPoint の音は 3D サウンドになるので、
                // カメラの位置で再生して、距離によって音が小さくならないようにします。
                AudioSource.PlayClipAtPoint(_sound, Camera.main.transform.position);
            }

            Collected?.Invoke(this);
            Destroy(gameObject);
        }
    }
}
