// 第 19 章 簡単なゲームを作る
// プレイヤーとの位置関係を保ったまま、カメラを追従させるスクリプトです。
// 使い方: Main Camera にアタッチし、Target に Player を設定します。
using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    [SerializeField] private Transform _target;

    // ゲーム開始時のカメラとプレイヤーの位置の差です。
    private Vector3 _offset;

    private void Start()
    {
        _offset = transform.position - _target.position;
    }

    // プレイヤーの移動がすべて終わった後にカメラを動かすため、LateUpdate を使います。
    private void LateUpdate()
    {
        transform.position = _target.position + _offset;
    }
}
