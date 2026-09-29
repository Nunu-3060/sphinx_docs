// 第 13 章 GameObject とコンポーネントの操作
// 一定時間ごとにプレハブからオブジェクトを生成し、一定時間後に破棄するスクリプトです。
// 使い方: 空の GameObject にアタッチし、Prefab にプレハブを Project ウィンドウからドラッグして設定します。
using UnityEngine;

public class Spawner : MonoBehaviour
{
    [SerializeField] private GameObject _prefab;

    [Tooltip("生成する間隔（秒）")]
    [SerializeField] private float _interval = 1f;

    [Tooltip("生成したオブジェクトを破棄するまでの時間（秒）")]
    [SerializeField] private float _lifetime = 3f;

    [Tooltip("生成する範囲（このオブジェクトを中心とした X 方向と Z 方向の半径）")]
    [SerializeField] private float _range = 5f;

    // 前回生成してからの経過時間です。
    private float _elapsed;

    private void Update()
    {
        _elapsed += Time.deltaTime;
        if (_elapsed < _interval)
        {
            return;
        }
        _elapsed = 0f;

        // Random.Range(最小値, 最大値) で、範囲内のランダムな値を得ます。
        Vector3 offset = new Vector3(Random.Range(-_range, _range), 0f, Random.Range(-_range, _range));

        // Instantiate で、プレハブを複製してシーンに生成します。
        GameObject spawned = Instantiate(_prefab, transform.position + offset, Quaternion.identity);

        // Destroy の第 2 引数に秒数を指定すると、その時間が経ってから破棄されます。
        Destroy(spawned, _lifetime);
    }
}
