// 第 18 章 Unity 固有の注意点
// EnemyData（ScriptableObject）のパラメーターを使う敵のコンポーネントです。
// 使い方: 敵の GameObject にアタッチし、Data に EnemyData のアセットを Project ウィンドウからドラッグして設定します。
//         同じ EnemyData を複数の敵で共有できます。
using UnityEngine;

public class EnemyStatus : MonoBehaviour
{
    [SerializeField] private EnemyData _data;

    // HP のように敵ごとに変化する値は、ScriptableObject ではなくコンポーネント側に持たせます。
    private int _currentHp;

    private void Start()
    {
        _currentHp = _data.MaxHp;
        Debug.Log($"{_data.DisplayName} が現れた（HP: {_currentHp}, 速さ: {_data.MoveSpeed}）");
    }
}
