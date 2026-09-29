// 第 19 章 簡単なゲームを作る
// プレイヤーが触れると取得されるアイテムのスクリプトです。
// 使い方: Is Trigger にチェックを入れた Collider を持つ Cube にアタッチし、プレハブにして複数配置します。
using UnityEngine;

public class Pickup : MonoBehaviour
{
    [Tooltip("X、Y、Z 軸それぞれの 1 秒あたりの回転角度（度）")]
    [SerializeField] private Vector3 _rotationSpeed = new Vector3(15f, 30f, 45f);

    // 見た目をわかりやすくするため、アイテムを回転させます。
    private void Update()
    {
        transform.Rotate(_rotationSpeed * Time.deltaTime);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player"))
        {
            return;
        }

        GameManager.Instance.CollectPickup();
        Destroy(gameObject);
    }
}
