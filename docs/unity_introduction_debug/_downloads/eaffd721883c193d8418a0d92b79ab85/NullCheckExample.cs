using System.Collections;
using UnityEngine;

/// <summary>
/// 破棄された UnityEngine.Object を null と比較したときの挙動を確認するサンプルです。
/// </summary>
/// <remarks>
/// Inspector ウィンドウで Target に破棄してもよい GameObject を設定してから再生してください。
/// bool の値は Console ウィンドウに True または False と表示されます。
/// </remarks>
public class NullCheckExample : MonoBehaviour
{
    [SerializeField]
    private GameObject target;

    // Start の戻り値を IEnumerator にすると、Start をコルーチンとして実行できます。
    private IEnumerator Start()
    {
        if (target == null)
        {
            Debug.LogWarning("Target が設定されていません。", this);
            yield break;
        }

        Destroy(target);

        // Destroy は即座にはオブジェクトを破棄しません。
        // 実際の破棄は現在のフレームの Update 処理が終わった後に行われるため、ここでは False です。
        Debug.Log($"Destroy の直後: target == null は {target == null}");

        // 次のフレームまで待ちます。
        yield return null;

        // 破棄された UnityEngine.Object は、== 演算子で null と比較すると True になります。
        Debug.Log($"1 フレーム後: target == null は {target == null}");

        // is null は == 演算子を使わずに C# の参照を直接調べるため、False になります。
        Debug.Log($"1 フレーム後: target is null は {target is null}");

        try
        {
            // ?. 演算子も == 演算子を使わないため、破棄済みのオブジェクトにアクセスしてしまい、
            // MissingReferenceException が発生します。
            string targetName = target?.name;
            Debug.Log(targetName);
        }
        catch (MissingReferenceException e)
        {
            Debug.LogException(e, this);
        }

        // UnityEngine.Object の null チェックには == / != 演算子か、bool への暗黙の変換を使います。
        if (target != null)
        {
            Debug.Log("この行は実行されません。");
        }
    }
}
