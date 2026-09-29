// 第 15 章 ベクトルと移動・回転
// ベクトルの長さ、正規化、距離、内積、外積、線形補間を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Play ボタンを押して Console ウィンドウを確認します。
using UnityEngine;

public class VectorSample : MonoBehaviour
{
    private void Start()
    {
        Vector3 a = new Vector3(3f, 0f, 4f);
        Vector3 b = new Vector3(-3f, 0f, 12f);

        // 足し算と引き算は成分ごとに計算されます。
        Debug.Log($"a + b = {a + b}");
        Debug.Log($"a - b = {a - b}");

        // 長さ（大きさ）と、長さを 1 にした向きだけのベクトル（正規化）
        Debug.Log($"a の長さ: {a.magnitude}");
        Debug.Log($"a を正規化: {a.normalized}");

        // 2 点間の距離は (a - b).magnitude と同じです。
        Debug.Log($"a と b の距離: {Vector3.Distance(a, b)}");

        // 内積: 2 つのベクトルの向きがどれだけ揃っているかがわかります。
        // 正規化したベクトルどうしの内積は、同じ向きで 1、直角で 0、逆向きで -1 になります。
        Vector3 forward = Vector3.forward;
        Debug.Log($"前方と前方の内積: {Vector3.Dot(forward, Vector3.forward)}");
        Debug.Log($"前方と右の内積: {Vector3.Dot(forward, Vector3.right)}");
        Debug.Log($"前方と後方の内積: {Vector3.Dot(forward, Vector3.back)}");

        // 外積: 2 つのベクトルの両方に垂直なベクトルが得られます。
        Debug.Log($"右と上の外積: {Vector3.Cross(Vector3.right, Vector3.up)}");

        // 線形補間: t = 0 で開始点、t = 1 で終了点、t = 0.5 でちょうど中間の点になります。
        Debug.Log($"Lerp(0.5): {Vector3.Lerp(Vector3.zero, new Vector3(10f, 0f, 0f), 0.5f)}");
    }
}
