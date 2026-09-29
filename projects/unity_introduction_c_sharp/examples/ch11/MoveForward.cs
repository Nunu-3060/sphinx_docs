// 第 11 章 イベント関数とライフサイクル
// Time.deltaTime を使って、フレームレートに関係なく一定の速さで前進するスクリプトです。
// 使い方: シーンに Cube を作成してアタッチし、Play ボタンを押します。
using UnityEngine;

public class MoveForward : MonoBehaviour
{
    // 1 秒あたりに進む距離（m）です。
    [SerializeField] private float _speed = 2f;

    private void Update()
    {
        // 移動量 = 速さ × 前のフレームからの経過時間
        // Vector3.forward は (0, 0, 1)、つまりワールド座標の Z 軸の正の向きです。
        transform.position += Vector3.forward * _speed * Time.deltaTime;
    }
}
