using UnityEngine;

namespace UnityIntroduction.RollABall
{
    /// <summary>
    /// GameObject を一定の速さで回転させ続けます。
    /// </summary>
    public class Rotator : MonoBehaviour
    {
        [SerializeField, Tooltip("各軸まわりの 1 秒あたりの回転角度（度）")]
        private Vector3 _degreesPerSecond = new Vector3(15f, 30f, 45f);

        private void Update()
        {
            transform.Rotate(_degreesPerSecond * Time.deltaTime);
        }
    }
}
