using UnityEngine;

namespace UnityIntroduction.Chapter07
{
    /// <summary>
    /// 一定の間隔で Prefab を生成し、一定時間後に破棄します。
    /// </summary>
    public class Spawner : MonoBehaviour
    {
        [SerializeField, Tooltip("生成する Prefab")]
        private GameObject _prefab;

        [SerializeField, Tooltip("生成する間隔（秒）")]
        private float _interval = 1f;

        [SerializeField, Tooltip("生成してから破棄するまでの時間（秒）")]
        private float _lifetime = 3f;

        private float _elapsed;

        private void Start()
        {
            if (_prefab == null)
            {
                Debug.LogWarning("Prefab が設定されていません。", this);
                enabled = false;
            }
        }

        private void Update()
        {
            _elapsed += Time.deltaTime;
            if (_elapsed < _interval)
            {
                return;
            }

            _elapsed -= _interval;

            // 自分の位置から半径 1 m 以内のランダムな位置に生成します。
            Vector3 position = transform.position + Random.insideUnitSphere;
            GameObject instance = Instantiate(_prefab, position, Quaternion.identity);

            // 第 2 引数に秒数を渡すと、その時間が経過した後に破棄されます。
            Destroy(instance, _lifetime);
        }
    }
}
