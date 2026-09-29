// 第 18 章 Unity 固有の注意点
// 敵の種類ごとのパラメーターを保存する ScriptableObject です。
// 使い方: Project ウィンドウで右クリックし、Create > Samples > Enemy Data を選んでアセットを作成します。
using UnityEngine;

[CreateAssetMenu(fileName = "EnemyData", menuName = "Samples/Enemy Data")]
public class EnemyData : ScriptableObject
{
    [SerializeField] private string _displayName = "スライム";
    [SerializeField] private int _maxHp = 10;
    [SerializeField] private float _moveSpeed = 1f;

    // ゲーム中に書き換えられないよう、外部には読み取り専用のプロパティとして公開します。
    public string DisplayName => _displayName;

    public int MaxHp => _maxHp;

    public float MoveSpeed => _moveSpeed;
}
