// 第 8 章 継承とポリモーフィズム
// Enemy を継承した「スライム」クラスです。
public class Slime : Enemy
{
    // base(...) で基底クラス（Enemy）のコンストラクターを呼び出します。
    public Slime() : base("スライム", 10)
    {
    }

    public override int AttackPower => 2;

    public override string Cry()
    {
        return "ぷるぷる";
    }
}
