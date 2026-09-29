using UnityEngine;

namespace UnityIntroduction.Chapter07
{
    /// <summary>
    /// 再生を開始したときに Console ウィンドウへメッセージを表示します。
    /// </summary>
    public class HelloUnity : MonoBehaviour
    {
        private void Start()
        {
            Debug.Log("Hello, Unity!");
        }
    }
}
