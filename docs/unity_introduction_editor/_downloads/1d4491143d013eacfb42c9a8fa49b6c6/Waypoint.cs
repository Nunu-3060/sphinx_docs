using System.Collections.Generic;
using UnityEngine;

namespace EditorIntro
{
    /// <summary>
    /// 第 9 章のサンプルです。
    /// 経路の各点をローカル座標で保持し、Scene ビューにギズモで表示します。
    /// </summary>
    public class Waypoint : MonoBehaviour
    {
        [SerializeField]
        private List<Vector3> points = new List<Vector3>
        {
            new Vector3(0f, 0f, 0f),
            new Vector3(2f, 0f, 0f),
            new Vector3(2f, 0f, 2f),
        };

        [Tooltip("オンにすると、最後の点と最初の点を結びます。")]
        [SerializeField] private bool loop;

        /// <summary>経路の点（ローカル座標）です。</summary>
        public List<Vector3> Points => points;

        public bool Loop => loop;

        // OnDrawGizmos は、ゲームオブジェクトを選択していなくても Scene ビューの描画時に呼ばれます。
        // Gizmos クラスは UnityEngine 名前空間にあるため、ランタイム側のスクリプトに書けます。
        private void OnDrawGizmos()
        {
            Gizmos.color = Color.cyan;
            foreach (var point in points)
            {
                Gizmos.DrawSphere(transform.TransformPoint(point), 0.15f);
            }
        }
    }
}
