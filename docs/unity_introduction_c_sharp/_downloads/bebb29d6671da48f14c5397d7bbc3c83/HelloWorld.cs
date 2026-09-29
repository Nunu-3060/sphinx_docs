// 第 1 章 開発環境の準備
// Console ウィンドウに「Hello, Unity!」と表示するだけの、最初のスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押します。
using UnityEngine;

public class HelloWorld : MonoBehaviour
{
    // Start は、最初の Update が呼ばれる直前に 1 回だけ呼ばれます。
    private void Start()
    {
        Debug.Log("Hello, Unity!");
    }
}
