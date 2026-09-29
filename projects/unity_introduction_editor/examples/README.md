# Unity エディター拡張入門 サンプルコード

「Unity エディター拡張入門」で使用するサンプルコードです。

## 動作環境

- Unity 6（6000.0 LTS）

## 使い方

1. Unity で新しいプロジェクトを作成するか、既存のプロジェクトを開きます。
2. このフォルダーの `Assets/EditorIntro` フォルダーを、プロジェクトの `Assets` フォルダーの直下にコピーします。
3. コンパイルが終わると、メニューバーに「Tools > Editor Intro」が追加されます。

`Assets/EditorIntro` 以外の場所に置く場合は、`Editor/SampleWindow.cs` の `UxmlPath` を変更してください。

## フォルダー構成

| フォルダー | 内容 |
| --- | --- |
| `Assets/EditorIntro/Runtime` | ゲームオブジェクトに追加するコンポーネントなど（ビルドに含まれる） |
| `Assets/EditorIntro/Editor` | エディター拡張のスクリプト（ビルドに含まれない） |
| `Assets/EditorIntro/Editor/UI` | EditorWindow で使う UXML と USS |

## コードの検査

`.editorconfig` に書式と命名規則を定義しています。次のコマンドで書式を検査できます。

```
dotnet format whitespace examples --folder --verify-no-changes
```
