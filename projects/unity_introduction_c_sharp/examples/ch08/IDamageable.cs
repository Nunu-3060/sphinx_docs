// 第 8 章 継承とポリモーフィズム
// 「ダメージを受けられるもの」を表すインターフェイスです。
// 実装するクラスは、TakeDamage メソッドを必ず持つことになります。
public interface IDamageable
{
    void TakeDamage(int amount);
}
