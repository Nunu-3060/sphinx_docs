簡単な実践プロジェクト
======================

はじめに
--------

ここまで、Rust の文法や設計思想を章ごとに個別に学んできました。本章では、それらの知識を組み合わせて、実際に動くひとつのコマンドラインツールを最初から最後まで作り上げます。

題材は ``wordcount`` という名前のシンプルな CLI ツールです。テキストファイルを読み込み、行数・単語数を数え、出現頻度の高い単語トップNを表示します。Python であれば数行のスクリプトで書けてしまう処理ですが、あえて Rust らしい書き方(``Result`` によるエラーハンドリング、``HashMap`` を使った集計、モジュール分割、イテレータの活用)を意識しながら実装していきます。

プロジェクトの概要
-------------------

``wordcount`` の仕様は次のとおりです。

- コマンドライン引数でテキストファイルのパスを受け取る
- オプションで表示件数(トップN)を指定できる(省略時は5件)
- ファイルの行数と単語数を数えて表示する
- 出現回数の多い単語を、回数の多い順に表示する

処理の中心となる「集計」のロジックは ``counter`` というモジュールに分離し、``main.rs`` は引数の処理と結果の表示に専念させます。これは実際の Rust プロジェクトでもよく見られる、「入出力を扱う層」と「ロジックを扱う層」を分離する設計です。

Cargo プロジェクトの作成
-------------------------

まず、``cargo new wordcount`` で新しいバイナリプロジェクトを作成します。生成される ``Cargo.toml`` は次のようになります。

.. code-block:: toml

   [package]
   name = "wordcount"
   version = "0.1.0"
   edition = "2024"

   [dependencies]

今回は標準ライブラリのみで実装するため、``[dependencies]`` に外部クレートを追加する必要はありません。実務では、コマンドライン引数の解析に ``clap`` のようなクレートを使うことが多いですが、まずは ``std::env::args`` を直接使う方法から理解しておくと、外部クレートが内部で何をしているかを見通しやすくなります。

コマンドライン引数の受け取り
----------------------------

``std::env::args`` を使うと、コマンドライン引数を ``String`` のイテレータとして取得できます。1番目の要素(インデックス0)は慣習的に実行ファイル自身のパスですが、これは呼び出し元次第であり必ず保証されているわけではありません。通常、実際の引数は2番目以降になります。

引数が不足している場合は、エラーメッセージを ``Err`` として返し、呼び出し元にその処理を委ねます。これは、Python で異常時に例外を送出し、呼び出し元でまとめてハンドリングするのに近い考え方です。

ファイル読み込みとエラーハンドリング
-------------------------------------

ファイルの読み込みには ``std::fs::read_to_string`` を使います。この関数はファイルが存在しない場合や読み取り権限がない場合に ``Err`` になる ``Result<String, std::io::Error>`` 型を返すため、 ``?`` 演算子を使ってエラーを呼び出し元に伝播させます。

``main`` 関数自体はエラーを返す型にせず、実際の処理を ``run`` という別関数に切り出し、``main`` からは ``run`` の戻り値を確認してエラーメッセージを表示する形にしています。これは、``main`` 関数の戻り値を ``Result`` にすることもできますが、終了コードやエラーメッセージの出し方を細かく制御したい場合によく使われる書き方です。

単語カウント処理のモジュール分割
----------------------------------

単語の集計処理は ``src/counter.rs`` という別ファイルに切り出し、 ``main.rs`` から ``mod counter;`` で読み込みます。集計結果は ``Stats`` という構造体にまとめ、行数・単語数・ ``HashMap<String, u32>`` による単語ごとの出現回数を保持します。

単語を数える際には、単純に空白で区切るだけでなく、記号を取り除いて小文字に統一する「正規化」を行うことで、 ``"Rust."`` と ``"rust"`` を同じ単語として数えられるようにしています。正規化は、``chars()`` で1文字ずつのイテレータに変換し、 ``filter`` で英数字だけを残し、``collect::<String>()`` で ``String`` に組み立て直し(``::<String>`` はコンパイラに「``String`` として集めてほしい」と伝えるための型注釈で、「ターボフィッシュ」と呼ばれる記法です)、最後に ``to_lowercase`` で小文字化する、という流れで実装します。

出現回数を数える部分では ``HashMap`` の ``entry`` というメソッドを使います。``word_freq.entry(word)`` は、そのキーが既にあれば既存の値への参照を、無ければ ``or_insert(0)`` で指定した初期値(ここでは0)を挿入したうえでその値への可変参照を返します。返ってきた参照に対して ``*... += 1`` とすることで、「初出なら0から、既出ならその値に1を足す」という処理を1行で書けます。これは Python の ``dict.setdefault(word, 0)`` や ``collections.Counter`` が内部でやっていることに近い処理です。

頻出単語トップNの算出
------------------------

``HashMap`` は要素の順序を保証しないため、出現回数順に並べ替えるには一度 ``Vec`` に集める必要があります。 ``iter()`` でイテレータを作り、``map`` でタプルに変換します。このとき ``word.clone()`` としているのは、``word_freq`` が持つ ``String`` の所有権そのものを奪ってしまうと元の ``HashMap`` が壊れてしまうため、キーの複製を作って新しい ``Vec`` 側に持たせているためです(所有権の章で学んだ「借用で済むところは借用、複製が必要なら明示的に ``clone``」という考え方の実践例です)。 ``collect()`` で ``Vec`` にまとめたあと、``sort_by`` に比較用のクロージャを渡して並べ替えます。 ``b.1.cmp(&a.1)`` は出現回数(2番目の要素)を降順に比較する指定で、``.then_with(|| a.0.cmp(&b.0))`` は出現回数が同じだった場合に単語の辞書順で順序を安定させるための追加条件です(``cmp`` は大小関係を表す ``Ordering`` という列挙型を返し、``then_with`` はその結果が「等しい」だったときだけ次の比較を評価します)。最後に ``truncate(n)`` で、並べ替え済みの ``Vec`` の先頭 ``n`` 件より後ろの要素をすべて切り捨て、トップN件だけを残します。

このように「``HashMap`` の中身をイテレータ経由で ``Vec`` に集め、並べ替えて上位だけを取り出す」という流れは、集計処理を書く際に非常によく使われるパターンです。

完成したコードの動作
---------------------

以上を踏まえた完成版のコードは次のとおりです。まず ``src/main.rs`` です。

.. code-block:: rust

   use std::env;
   use std::error::Error;
   use std::fs;
   use std::process;

   mod counter;

   fn main() {
       if let Err(e) = run() {
           eprintln!("エラー: {}", e);
           process::exit(1);
       }
   }

   fn run() -> Result<(), Box<dyn Error>> {
       let args: Vec<String> = env::args().collect();

       if args.len() < 2 {
           return Err("使い方: wordcount <ファイルパス> [表示件数]".into());
       }

       let file_path = &args[1];

       // 表示件数はオプション引数。指定がなければ5件とする。
       let top_n: usize = match args.get(2) {
           Some(s) => s.parse()?,
           None => 5,
       };

       // ファイルを読み込む。失敗した場合は `?` でエラーを呼び出し元に伝える。
       let contents = fs::read_to_string(file_path)?;

       let stats = counter::analyze(&contents);

       println!("ファイル: {}", file_path);
       println!("行数: {}", stats.line_count);
       println!("単語数: {}", stats.word_count);
       println!("異なり語数: {}", stats.unique_word_count());
       println!();
       println!("頻出単語トップ{}", top_n);

       let ranking = counter::top_words(&stats.word_freq, top_n);
       for (rank, (word, count)) in ranking.iter().enumerate() {
           println!("{:2}. {:<15} {}", rank + 1, word, count);
       }

       Ok(())
   }

続いて、集計ロジックをまとめた ``src/counter.rs`` です。

.. code-block:: rust

   use std::collections::HashMap;

   /// テキスト全体の集計結果を保持する構造体
   pub struct Stats {
       pub line_count: usize,
       pub word_count: usize,
       pub word_freq: HashMap<String, u32>,
   }

   impl Stats {
       /// 集計された単語の異なり数(ユニークな単語数)を返す
       pub fn unique_word_count(&self) -> usize {
           self.word_freq.len()
       }
   }

   /// テキストを解析し、行数・単語数・単語ごとの出現回数を集計する
   pub fn analyze(text: &str) -> Stats {
       let line_count = text.lines().count();

       let mut word_freq: HashMap<String, u32> = HashMap::new();
       let mut word_count = 0;

       for line in text.lines() {
           for raw_word in line.split_whitespace() {
               let word = normalize(raw_word);
               if word.is_empty() {
                   continue;
               }
               word_count += 1;
               *word_freq.entry(word).or_insert(0) += 1;
           }
       }

       Stats {
           line_count,
           word_count,
           word_freq,
       }
   }

   /// 単語から記号を取り除き、小文字に統一する
   fn normalize(word: &str) -> String {
       word.chars()
           .filter(|c| c.is_alphanumeric())
           .collect::<String>()
           .to_lowercase()
   }

   /// 出現回数が多い順にトップN件の単語を取得する
   pub fn top_words(word_freq: &HashMap<String, u32>, n: usize) -> Vec<(String, u32)> {
       let mut words: Vec<(String, u32)> = word_freq
           .iter()
           .map(|(word, count)| (word.clone(), *count))
           .collect();

       // 出現回数の降順、同数の場合は単語の辞書順で安定させる
       words.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0)));
       words.truncate(n);
       words
   }

   #[cfg(test)]
   mod tests {
       use super::*;

       #[test]
       fn analyze_counts_lines_and_words() {
           let text = "Rust is great.\nRust is fast.\n";
           let stats = analyze(text);

           assert_eq!(stats.line_count, 2);
           assert_eq!(stats.word_count, 6);
           assert_eq!(stats.word_freq.get("rust"), Some(&2));
       }

       #[test]
       fn top_words_returns_most_frequent_first() {
           let mut freq = HashMap::new();
           freq.insert(String::from("rust"), 3);
           freq.insert(String::from("is"), 2);
           freq.insert(String::from("great"), 1);

           let top = top_words(&freq, 2);

           assert_eq!(top, vec![
               (String::from("rust"), 3),
               (String::from("is"), 2),
           ]);
       }
   }

``main.rs`` の最後で結果を表示している部分では、 ``ranking.iter().enumerate()`` を使って「何番目か」という連番と要素を同時に取り出しています。``enumerate()`` はイテレータの各要素に0から始まる添字を付け、 ``(添字, 要素)`` というタプルに変換するアダプタで、Python の ``enumerate(ranking)`` とほぼ同じ役割です。

また ``println!("{:2}. {:<15} {}", rank + 1, word, count)`` の ``{:2}`` や ``{:<15}`` は、値をそのまま埋め込むだけでなく表示幅を指定する書式です。``{:2}`` は最低2桁になるよう右寄せで埋め、``{:<15}`` は左寄せで15文字幅になるよう空白を埋めます。順位や単語の長さがそろっていなくても、出力の列がきれいに揃って見えるようにするための指定です。

``Stats`` 構造体には ``impl`` ブロックでメソッドを1つ追加しています。``unique_word_count`` メソッドは ``&self`` を受け取り、``word_freq`` フィールドの要素数を ``len`` メソッドで数えて返すだけの、単純な読み取り専用メソッドです。構造体にデータをまとめるだけでなく、``impl`` によって振る舞い(メソッド)を持たせる基本形を、この小さな例で復習できます。

``counter.rs`` の末尾には ``#[cfg(test)]`` によるテストモジュールも含めています。``cargo test`` を実行すれば、集計ロジックが期待どおりに動作するかをすぐに確認できます。実際にファイルを用意して ``cargo run -- sample.txt 3`` のように実行すれば、指定したファイルの行数・単語数と、頻出単語トップ3が表示されます。

.. admonition:: Python 経験者向けメモ
   :class: tip

   Python であれば ``collections.Counter`` と ``Counter.most_common(n)`` で数行に書けてしまう処理ですが、Rust では型を明示しながら ``HashMap`` と ``Vec`` を使い分ける必要があります。手間は増えますが、その分「どのデータがどこで、どのような形で扱われているか」がコード上に明確に現れるのが Rust らしいところです。

このプロジェクトで使った概念の振り返り
----------------------------------------

最後に、``wordcount`` の実装で使った概念と、それを学んだ章を振り返っておきましょう。

- **変数・制御フロー・関数(第1部)**: ``run`` 関数や ``normalize`` 関数の定義、``for`` ループによる走査
- **所有権・借用・コレクション(第2部)**: ``&str`` と ``String`` の使い分け、``HashMap`` への借用渡し(``&HashMap<String, u32>``)、``entry``/``or_insert`` による出現回数の集計
- **構造体へのメソッド定義(第2部)**: ``Stats`` 構造体に ``impl`` ブロックで ``unique_word_count`` メソッドを追加し、``word_freq`` フィールドを使った読み取り専用の振る舞いを定義
- **Option<T> とパターンマッチング(第2部)**: ``match args.get(2) { Some(s) => s.parse()?, None => 5 }`` のように、値の有無を型で表す ``Option<T>`` を ``match`` で分岐処理
- **エラーハンドリング(第3部)**: ``Result`` 型と ``?`` 演算子によるエラー伝播、``fs::read_to_string`` の戻り値の扱い
- **エラー型の統一(第3部・第4部)**: ``run`` 関数の戻り値 ``Result<(), Box<dyn Error>>`` に見る、``Box`` というスマートポインタと ``dyn Error`` というトレイトオブジェクトの組み合わせ
- **モジュール(第3部)**: ``mod counter;`` によるファイル分割と ``pub`` によるモジュール間の公開範囲の制御
- **イテレータ(第3部)**: ``lines()``・``split_whitespace()``・ ``chars()``・``map``・``filter``・``collect``・``enumerate``・ ``sort_by`` (と ``Ordering`` の ``then_with``)を組み合わせた集計処理
- **テスト(第4部)**: ``#[cfg(test)]`` と ``#[test]`` による単体テストの記述
- **Cargo(第4部)**: ``cargo new``・``cargo run``・``cargo test`` によるプロジェクトの管理と実行

なお、並行処理や明示的なライフタイム注釈はこのプロジェクトには登場しません。``wordcount`` は単純な逐次実行プログラムであり、借用のスコープも短く単純なため、ライフタイム省略規則がすべて自動的に処理してくれるからです。学んだこと自体が無駄になったわけではなく、必要な場面ではいつでも使える、という位置づけです。

このように、小さな CLI ツールひとつにも、これまで学んだほとんどの概念が自然に登場することが分かります。次章では、ここからさらに学びを広げるための情報を紹介します。
