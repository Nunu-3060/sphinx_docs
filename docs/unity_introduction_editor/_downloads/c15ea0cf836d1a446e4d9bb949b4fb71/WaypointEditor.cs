using UnityEditor;
using UnityEditor.UIElements;
using UnityEngine;
using UnityEngine.UIElements;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 9 章のサンプルです。
    /// Waypoint コンポーネントの各点を、Scene ビュー上のハンドルで移動できるようにします。
    /// </summary>
    [CustomEditor(typeof(Waypoint))]
    public class WaypointEditor : Editor
    {
        // Inspector ウィンドウには、既定の表示をそのまま使います。
        public override VisualElement CreateInspectorGUI()
        {
            var root = new VisualElement();
            InspectorElement.FillDefaultInspector(root, serializedObject, this);
            return root;
        }

        // 対象のゲームオブジェクトを選択している間、Scene ビューの描画時に呼ばれます。
        private void OnSceneGUI()
        {
            var waypoint = (Waypoint)target;
            var transform = waypoint.transform;
            var points = waypoint.Points;
            if (points.Count == 0)
            {
                return;
            }

            // 点はローカル座標で保存されているため、描画用にワールド座標へ変換します。
            var worldPoints = new Vector3[points.Count];
            for (var i = 0; i < points.Count; i++)
            {
                worldPoints[i] = transform.TransformPoint(points[i]);
            }

            // 経路を線で結びます。
            Handles.color = Color.cyan;
            Handles.DrawAAPolyLine(3f, worldPoints);
            if (waypoint.Loop && worldPoints.Length > 2)
            {
                Handles.DrawAAPolyLine(3f, worldPoints[worldPoints.Length - 1], worldPoints[0]);
            }

            // ツールバーの設定が「Local」ならゲームオブジェクトの向きに、「Global」ならワールド座標軸に合わせます。
            var handleRotation = Tools.pivotRotation == PivotRotation.Local
                ? transform.rotation
                : Quaternion.identity;

            for (var i = 0; i < worldPoints.Length; i++)
            {
                Handles.Label(worldPoints[i] + Vector3.up * 0.3f, $"P{i}");

                // BeginChangeCheck と EndChangeCheck の間でハンドルが操作されたかを調べます。
                EditorGUI.BeginChangeCheck();
                var newWorldPoint = Handles.PositionHandle(worldPoints[i], handleRotation);
                if (EditorGUI.EndChangeCheck())
                {
                    // 変更前に Undo.RecordObject を呼び、変更を Undo に記録します。
                    Undo.RecordObject(waypoint, "Move Waypoint");

                    // ワールド座標をローカル座標に戻して保存します。
                    points[i] = transform.InverseTransformPoint(newWorldPoint);

                    // プレハブのインスタンスの場合は、変更をオーバーライドとして記録します。
                    if (PrefabUtility.IsPartOfPrefabInstance(waypoint))
                    {
                        PrefabUtility.RecordPrefabInstancePropertyModifications(waypoint);
                    }
                }
            }
        }
    }
}
