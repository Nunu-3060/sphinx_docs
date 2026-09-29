// 第 7 章 クラスとオブジェクト
// Character クラスのインスタンスを作って使い、クラス（参照型）と構造体（値型）の違いを確認するスクリプトです。
// 使い方: Character.cs と同じプロジェクトに置き、シーン内の GameObject にアタッチして Play ボタンを押します。
using UnityEngine;

public class ClassSample : MonoBehaviour
{
    private void Start()
    {
        // new でインスタンスを作ります。
        Character hero = new Character("勇者", 30);
        Character slime = new Character("スライム", 8);

        hero.TakeDamage(12);
        Debug.Log($"{hero.Name}: HP {hero.Hp} / {hero.MaxHp}");

        // Hp は MaxHp を超えないように制限されています。
        hero.Heal(100);
        Debug.Log($"{hero.Name}: HP {hero.Hp} / {hero.MaxHp}");

        // Hp は 0 未満にもなりません。
        slime.TakeDamage(20);
        Debug.Log($"{slime.Name}: HP {slime.Hp}, 生存: {slime.IsAlive}");

        // static メンバーは「クラス名.メンバー名」で使います。
        Debug.Log($"作成したキャラクターの数: {Character.CreatedCount}");

        // ---- クラスは参照型 ----
        // 代入するとインスタンスへの参照がコピーされ、2 つの変数が同じインスタンスを指します。
        Character sameHero = hero;
        sameHero.TakeDamage(5);
        Debug.Log($"hero.Hp = {hero.Hp}, sameHero.Hp = {sameHero.Hp}");

        // ---- 構造体は値型 ----
        // Vector3 は構造体です。代入すると値そのものがコピーされるため、コピー先を変えても元の値は変わりません。
        Vector3 original = new Vector3(1f, 2f, 3f);
        Vector3 copy = original;
        copy.x = 10f;
        Debug.Log($"original.x = {original.x}, copy.x = {copy.x}");
    }
}
