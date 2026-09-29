// 第 9 章 C# の発展的な機能
// 列挙型（enum）の定義と使い方を確認するスクリプトです。
// 使い方: シーン内の GameObject にアタッチし、Inspector ウィンドウで State の値を変えて試します。
using UnityEngine;

public class EnumSample : MonoBehaviour
{
    // ゲームの状態を表す列挙型です。クラスの中に定義することもできます。
    public enum GameState
    {
        Title,
        Playing,
        GameOver,
    }

    // 列挙型のフィールドは、Inspector ウィンドウではドロップダウンで表示されます。
    [SerializeField] private GameState _state = GameState.Playing;

    private void Start()
    {
        Debug.Log($"現在の状態: {_state}");

        // 列挙型の値は、内部的には 0 から始まる整数です。
        Debug.Log($"GameOver の整数値: {(int)GameState.GameOver}");

        string message = _state switch
        {
            GameState.Title => "タイトル画面を表示する。",
            GameState.Playing => "ゲームを進める。",
            GameState.GameOver => "ゲームオーバー画面を表示する。",
            _ => "不明な状態。",
        };
        Debug.Log(message);
    }
}
