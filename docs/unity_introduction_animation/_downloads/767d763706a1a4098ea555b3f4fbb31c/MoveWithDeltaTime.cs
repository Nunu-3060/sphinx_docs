using UnityEngine;

/// <summary>
/// GameObject を一定の速度で移動させるサンプル。
/// </summary>
/// <remarks>
/// 使い方: シーン上の任意の GameObject（Cube など）に追加して再生する。
/// 移動量に Time.deltaTime を掛けているため、フレームレートが変わっても
/// 1 秒あたりの移動距離は変わらない。
/// </remarks>
public class MoveWithDeltaTime : MonoBehaviour
{
    [Tooltip("1 秒あたりの移動量（ワールド座標）")]
    [SerializeField]
    private Vector3 velocity = new Vector3(1f, 0f, 0f);

    private void Update()
    {
        // 移動量 = 速度 × 前フレームからの経過時間（秒）
        transform.position += velocity * Time.deltaTime;
    }
}
