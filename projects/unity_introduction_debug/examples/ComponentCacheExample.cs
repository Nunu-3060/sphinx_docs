using UnityEngine;

/// <summary>
/// GetComponent の結果をキャッシュ（フィールドに保存）して使い回すサンプルです。
/// </summary>
/// <remarks>
/// RequireComponent 属性により、このコンポーネントを追加すると Rigidbody も自動的に追加されます。
/// </remarks>
[RequireComponent(typeof(Rigidbody))]
public class ComponentCacheExample : MonoBehaviour
{
    [SerializeField]
    private float upwardForce = 5f;

    private Rigidbody cachedRigidbody;

    private void Awake()
    {
        // 自分自身のコンポーネントの取得は Awake で 1 回だけ行い、結果をフィールドに保存します。
        cachedRigidbody = GetComponent<Rigidbody>();
    }

    private void FixedUpdate()
    {
        // 悪い例: 毎回 GetComponent を呼び出すと、そのたびに検索のコストがかかります。
        // GetComponent<Rigidbody>().AddForce(Vector3.up * upwardForce);

        // 良い例: 保存しておいた参照を使います。
        cachedRigidbody.AddForce(Vector3.up * upwardForce);
    }

    private void OnCollisionEnter(Collision collision)
    {
        // 他のオブジェクトのコンポーネントを取得する場合は TryGetComponent が便利です。
        // コンポーネントが見つかったかどうかを戻り値で判定でき、
        // 見つからなかった場合もエディター上で GC アロケーションが発生しません。
        if (collision.gameObject.TryGetComponent(out Rigidbody otherRigidbody))
        {
            Debug.Log($"{otherRigidbody.name} と衝突しました。", this);
        }
    }
}
