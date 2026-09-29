using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace UnityIntroduction.Chapter15
{
    /// <summary>
    /// シーンを切り替えます。UI のボタンなどから呼び出して使います。
    /// </summary>
    /// <remarks>
    /// 読み込むシーンは、Build Profiles ウィンドウの Scene List に登録しておく必要があります。
    /// </remarks>
    public class SceneLoader : MonoBehaviour
    {
        /// <summary>
        /// シーンを読み込みます。読み込みが終わるまで、ゲームの処理は止まります。
        /// </summary>
        public void LoadScene(string sceneName)
        {
            SceneManager.LoadScene(sceneName);
        }

        /// <summary>
        /// シーンを非同期で読み込みます。読み込み中もゲームは動き続けます。
        /// </summary>
        public void LoadSceneAsync(string sceneName)
        {
            StartCoroutine(LoadSceneRoutine(sceneName));
        }

        private IEnumerator LoadSceneRoutine(string sceneName)
        {
            AsyncOperation operation = SceneManager.LoadSceneAsync(sceneName);

            while (!operation.isDone)
            {
                // progress は 0 から 1 までの値で、読み込みの進み具合を表します。
                Debug.Log($"読み込み中: {operation.progress * 100f:F0}%");
                yield return null;
            }
        }
    }
}
