// 第 7 章 クラスとオブジェクト
// キャラクターの名前と HP を管理するクラスです。MonoBehaviour を継承しない、普通の C# のクラスです。
// ClassSample.cs から利用します。
using UnityEngine;

public class Character
{
    // フィールド: クラスの外から直接書き換えられないように private にします。
    private int _hp;

    // コンストラクター: new でインスタンスを作るときに 1 回だけ呼ばれます。
    public Character(string name, int maxHp)
    {
        Name = name;
        MaxHp = maxHp;
        _hp = maxHp;
        CreatedCount++;
    }

    // static プロパティ: インスタンスごとではなく、クラス全体で 1 つだけ存在します。
    public static int CreatedCount { get; private set; }

    // 読み取り専用の自動実装プロパティ: 値を設定できるのはコンストラクターの中だけです。
    public string Name { get; }

    public int MaxHp { get; }

    // 値の範囲を制限するプロパティ: クラスの外からは読み取りだけができます。
    public int Hp
    {
        get { return _hp; }
        private set { _hp = Mathf.Clamp(value, 0, MaxHp); }
    }

    // 計算結果を返すだけのプロパティ
    public bool IsAlive => Hp > 0;

    public void TakeDamage(int amount)
    {
        Hp -= amount;
    }

    public void Heal(int amount)
    {
        Hp += amount;
    }
}
