// 第 8 章 継承とポリモーフィズム
// すべての敵に共通する性質をまとめた抽象クラスです。
// abstract クラスは new でインスタンスを作れず、継承して使います。
public abstract class Enemy : IDamageable
{
    // protected: このクラスと、このクラスを継承したクラスからだけ呼び出せます。
    protected Enemy(string name, int hp)
    {
        Name = name;
        Hp = hp;
    }

    public string Name { get; }

    public int Hp { get; private set; }

    // abstract プロパティ: 中身は派生クラスで必ず定義します。
    public abstract int AttackPower { get; }

    // virtual メソッド: 派生クラスで必要に応じて上書き（override）できます。
    public virtual string Cry()
    {
        return "……";
    }

    public void TakeDamage(int amount)
    {
        Hp -= amount;
        if (Hp < 0)
        {
            Hp = 0;
        }
    }
}
