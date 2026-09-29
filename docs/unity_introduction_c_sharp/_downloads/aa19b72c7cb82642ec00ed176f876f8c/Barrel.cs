// 第 8 章 継承とポリモーフィズム
// 敵ではないが、壊すことのできる「たる」クラスです。
// Enemy は継承せず、IDamageable インターフェイスだけを実装します。
public class Barrel : IDamageable
{
    public bool IsBroken { get; private set; }

    public void TakeDamage(int amount)
    {
        IsBroken = true;
    }
}
