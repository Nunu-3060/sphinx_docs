using UnityEngine;

namespace UnityIntroduction.Chapter07
{
    /// <summary>
    /// GameObject を一定の速度で移動させます。
    /// </summary>
    public class Mover : MonoBehaviour
    {
        [SerializeField, Tooltip("1 秒あたりの移動量（m/s）")]
        private Vector3 _velocity = new Vector3(1f, 0f, 0f);

        private void Update()
        {
            // Time.deltaTime（前のフレームからの経過秒数）を掛けると、
            // フレームレートに関係なく 1 秒あたり _velocity だけ移動します。
            transform.position += _velocity * Time.deltaTime;
        }
    }
}
