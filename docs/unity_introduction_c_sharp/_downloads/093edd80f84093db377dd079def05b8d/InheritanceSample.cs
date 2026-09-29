// 第 8 章 継承とポリモーフィズム
// Enemy を継承したクラスと、IDamageable を実装したクラスをまとめて扱うスクリプトです。
// 使い方: 同じフォルダーの IDamageable.cs、Enemy.cs、Slime.cs、Dragon.cs、Barrel.cs と一緒にプロジェクトに置き、
//         シーン内の GameObject にアタッチして Play ボタンを押します。
using System.Collections.Generic;
using UnityEngine;

public class InheritanceSample : MonoBehaviour
{
    private void Start()
    {
        // Slime も Dragon も Enemy の一種なので、List<Enemy> にまとめて入れられます。
        List<Enemy> enemies = new List<Enemy> { new Slime(), new Dragon() };

        // 同じ Cry() の呼び出しでも、実際のクラスに応じて異なる処理が実行されます（ポリモーフィズム）。
        foreach (Enemy enemy in enemies)
        {
            Debug.Log($"{enemy.Name}「{enemy.Cry()}」（攻撃力: {enemy.AttackPower}）");
        }

        // 継承関係のないクラスどうしでも、同じインターフェイスを実装していれば同じように扱えます。
        Slime slime = new Slime();
        Barrel barrel = new Barrel();
        IDamageable[] targets = { slime, barrel };
        foreach (IDamageable target in targets)
        {
            target.TakeDamage(5);
        }
        Debug.Log($"スライムの HP: {slime.Hp}, たるが壊れた: {barrel.IsBroken}");

        // is 演算子で、実際の型を調べて変換できます。
        foreach (IDamageable target in targets)
        {
            if (target is Enemy enemy)
            {
                Debug.Log($"{enemy.Name}は敵です。");
            }
        }
    }
}
