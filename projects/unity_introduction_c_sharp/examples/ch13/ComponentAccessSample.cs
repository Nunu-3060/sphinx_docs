// 第 13 章 GameObject とコンポーネントの操作
// ほかのコンポーネントの取得、Transform の操作、GameObject の有効・無効の切り替えを確認するスクリプトです。
// 使い方: シーンに Cube を作成してアタッチし、Play ボタンを押します。
//         Target には、シーン内の別の GameObject を Hierarchy ウィンドウからドラッグして設定します。
using UnityEngine;

public class ComponentAccessSample : MonoBehaviour
{
    // ほかの GameObject への参照は、Inspector ウィンドウで設定するのが基本です。
    [SerializeField] private GameObject _target;

    private Renderer _renderer;

    private void Awake()
    {
        // 同じ GameObject にアタッチされているコンポーネントを取得します。
        // 取得したコンポーネントはフィールドに保存しておき、毎フレーム取得し直さないようにします。
        _renderer = GetComponent<Renderer>();
    }

    private void Start()
    {
        // マテリアルの色を変えます。
        _renderer.material.color = Color.red;

        // TryGetComponent は、コンポーネントがあれば true を返し、out 引数に結果を入れます。
        if (TryGetComponent(out Rigidbody body))
        {
            Debug.Log($"Rigidbody の質量: {body.mass}");
        }
        else
        {
            Debug.Log("Rigidbody はアタッチされていない。");
        }

        // transform.position は Vector3（構造体）を返すため、position.y だけを直接書き換えることはできません。
        // いったん変数にコピーし、値を変えてから代入し直します。
        Vector3 position = transform.position;
        position.y += 1f;
        transform.position = position;

        // 回転と拡大縮小も Transform で操作します。
        transform.rotation = Quaternion.Euler(0f, 45f, 0f);
        transform.localScale = new Vector3(2f, 1f, 1f);

        if (_target != null)
        {
            // 親子関係を設定すると、子は親と一緒に移動・回転します。
            _target.transform.SetParent(transform);
            Debug.Log($"{_target.name} の親: {_target.transform.parent.name}, 子の数: {transform.childCount}");
        }
    }

    private void Update()
    {
        // 2 秒ごとに _target の有効・無効を切り替えます。
        // 無効にした GameObject は画面に表示されず、そのコンポーネントの Update も呼ばれなくなります。
        if (_target != null)
        {
            bool shouldBeActive = (int)(Time.time / 2f) % 2 == 0;
            if (_target.activeSelf != shouldBeActive)
            {
                _target.SetActive(shouldBeActive);
            }
        }
    }
}
