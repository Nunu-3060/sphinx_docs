using System.Collections;
using UnityEngine;

namespace UnityIntroduction.Chapter13
{
    /// <summary>
    /// 効果音の再生と、BGM のフェードアウトを行います。
    /// </summary>
    public class SoundPlayer : MonoBehaviour
    {
        [SerializeField, Tooltip("効果音の再生に使う AudioSource")]
        private AudioSource _sfxSource;

        [SerializeField, Tooltip("BGM の再生に使う AudioSource（Loop を有効にしておきます）")]
        private AudioSource _bgmSource;

        [SerializeField]
        private AudioClip _clickSound;

        /// <summary>
        /// 効果音を再生します。UI のボタンなどから呼び出します。
        /// </summary>
        public void PlayClickSound()
        {
            // PlayOneShot は再生中の音を止めずに重ねて再生します。
            _sfxSource.PlayOneShot(_clickSound);
        }

        /// <summary>
        /// BGM を指定した秒数でフェードアウトして停止します。
        /// </summary>
        public void FadeOutBgm(float duration)
        {
            StartCoroutine(FadeOutRoutine(duration));
        }

        private IEnumerator FadeOutRoutine(float duration)
        {
            float startVolume = _bgmSource.volume;

            for (float elapsed = 0f; elapsed < duration; elapsed += Time.deltaTime)
            {
                _bgmSource.volume = Mathf.Lerp(startVolume, 0f, elapsed / duration);
                yield return null;
            }

            _bgmSource.Stop();

            // 次に再生するときのために音量を戻しておきます。
            _bgmSource.volume = startVolume;
        }
    }
}
