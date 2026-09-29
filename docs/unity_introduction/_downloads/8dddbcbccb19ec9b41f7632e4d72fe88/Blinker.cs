using System.Collections;
using UnityEngine;

namespace UnityIntroduction.Chapter08
{
    /// <summary>
    /// コルーチンを使って、Renderer の表示と非表示を一定間隔で切り替えます。
    /// </summary>
    [RequireComponent(typeof(MeshRenderer))]
    public class Blinker : MonoBehaviour
    {
        [SerializeField, Tooltip("点滅する回数")]
        private int _blinkCount = 5;

        [SerializeField, Tooltip("表示を切り替える間隔（秒）")]
        private float _interval = 0.2f;

        private Renderer _renderer;

        private void Awake()
        {
            _renderer = GetComponent<Renderer>();
        }

        private void Start()
        {
            StartCoroutine(BlinkRoutine());
        }

        private IEnumerator BlinkRoutine()
        {
            // WaitForSeconds は毎回生成せず、使い回すことができます。
            var wait = new WaitForSeconds(_interval);

            for (int i = 0; i < _blinkCount; i++)
            {
                _renderer.enabled = false;
                yield return wait;

                _renderer.enabled = true;
                yield return wait;
            }

            Debug.Log("点滅が終わりました。");
        }
    }
}
