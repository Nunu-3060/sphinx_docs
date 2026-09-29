// 第 4 章 制御構文
// if 文、switch 文、switch 式、条件演算子で処理を分岐させるスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Inspector ウィンドウで Score と Weapon の値を変えて試します。
using UnityEngine;

public class ControlFlowSample : MonoBehaviour
{
    [SerializeField] private int _score = 72;
    [SerializeField] private string _weapon = "Sword";

    private void Start()
    {
        // ---- if 文 ----
        // 上の条件から順に判定し、最初に当てはまったブロックだけが実行されます。
        if (_score >= 80)
        {
            Debug.Log("評価: A");
        }
        else if (_score >= 60)
        {
            Debug.Log("評価: B");
        }
        else
        {
            Debug.Log("評価: C");
        }

        // ---- switch 文 ----
        // 値が一致する case のブロックが実行されます。どれにも一致しなければ default が実行されます。
        switch (_weapon)
        {
            case "Sword":
                Debug.Log("剣で攻撃した。");
                break;
            case "Bow":
                Debug.Log("弓で攻撃した。");
                break;
            default:
                Debug.Log("素手で攻撃した。");
                break;
        }

        // ---- switch 式 ----
        // 条件に応じて値を 1 つ選ぶときは、switch 式を使うと簡潔に書けます。
        int damage = _weapon switch
        {
            "Sword" => 10,
            "Bow" => 7,
            _ => 1,
        };
        Debug.Log($"ダメージ: {damage}");

        // ---- 条件演算子 ----
        // 条件 ? 条件が true のときの値 : 条件が false のときの値
        string result = _score >= 60 ? "合格" : "不合格";
        Debug.Log($"判定: {result}");
    }
}
