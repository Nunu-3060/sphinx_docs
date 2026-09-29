// 第 18 章 Unity 固有の注意点
// Destroy した GameObject が「== null」では null と判定されることを確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using System.Collections;
using UnityEngine;

public class NullCheckSample : MonoBehaviour
{
    // Start の戻り値を IEnumerator にすると、Start をコルーチンとして実行できます（第 17 章）。
    private IEnumerator Start()
    {
        // CreatePrimitive は、Cube などの基本的な形状の GameObject をスクリプトから作成します。
        GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);

        // Destroy による破棄は、現在のフレームの Update がすべて終わった後に行われます。
        // そのため、Destroy を呼んだ直後は、まだ破棄されていません。
        Destroy(cube);
        Debug.Log($"Destroy の直後: cube == null は {cube == null}");

        // 次のフレームまで待ちます。
        yield return null;

        // 破棄が完了すると、UnityEngine.Object の == 演算子は、そのオブジェクトを null と等しいと判定します。
        Debug.Log($"1 フレーム後: cube == null は {cube == null}");

        // しかし、変数には C# のオブジェクトが残っているため、本当の null ではありません。
        // is null、?.、?? はこの特別な判定を行わないため、Unity のオブジェクトには使わないでください。
        Debug.Log($"1 フレーム後: cube is null は {cube is null}");
    }
}
