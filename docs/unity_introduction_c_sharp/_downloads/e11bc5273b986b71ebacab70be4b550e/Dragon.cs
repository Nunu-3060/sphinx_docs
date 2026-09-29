// 第 8 章 継承とポリモーフィズム
// Enemy を継承した「ドラゴン」クラスです。
public class Dragon : Enemy
{
    public Dragon() : base("ドラゴン", 200)
    {
    }

    public override int AttackPower => 40;

    // Cry は override していないため、Enemy の Cry がそのまま使われます。
}
