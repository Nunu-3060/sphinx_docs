エラーハンドリング
==================

プログラムを書いていると、ファイルが見つからない、ネットワーク接続が切れる、入力値が不正であるなど、さまざまな「失敗」に遭遇します。Python では主に ``try``/``except`` を使って実行時に例外を捕捉しますが、Rust ではエラーを「回復不能なエラー」と「回復可能なエラー」の2種類に分けて考え、それぞれ異なる方法で扱います。本章ではこの2つの仕組みと、エラーを扱う際によく使われる構文を学びます。

回復不能なエラー: panic! マクロ
----------------------------------

プログラムがこれ以上正常に処理を続けられない致命的な状況では、 ``panic!`` マクロを使って処理を強制的に停止させます。配列の範囲外アクセスをしたときや、``panic!("メッセージ")`` を明示的に呼び出したときに発生します。

.. code-block:: rust

    fn main() {
        let v = vec![1, 2, 3];

        // 範囲外アクセスは panic を引き起こす
        println!("{}", v[99]);
    }

このコードを実行すると、Rust はエラーメッセージと発生箇所を表示してプロセスを異常終了させます。``panic!`` は、バグの検出やそれ以上処理を続けても安全ではない状況のためのものであり、あらかじめ起こりうると分かっているエラーの処理には使いません。

回復可能なエラー: Result<T, E>
----------------------------------

ファイルが存在しない、数値のパースに失敗したなど、あらかじめ想定できるエラーには ``Result<T, E>`` という列挙型を使います。定義は次のようになっています。

.. code-block:: rust

    enum Result<T, E> {
        Ok(T),
        Err(E),
    }

処理が成功すれば ``Ok`` に成功値を、失敗すれば ``Err`` にエラー値を包んで返します。例えば標準ライブラリの ``File::open`` は ``Result<File, std::io::Error>`` を返します。

.. code-block:: rust

    use std::fs::File;

    fn main() {
        let result = File::open("hello.txt");

        let _file = match result {
            Ok(file) => file,
            Err(error) => {
                panic!("ファイルを開けませんでした: {:?}", error);
            }
        };
    }

match による Result の処理
----------------------------------

``Result`` は列挙型なので、``match`` 式を使って ``Ok``/``Err`` のそれぞれの場合に応じた処理を書くのが基本です。エラーの種類によって挙動を変えたい場合は、``Err`` 側でさらに ``match`` することもできます。

.. code-block:: rust

    use std::fs::File;
    use std::io::ErrorKind;

    fn main() {
        let result = File::open("hello.txt");

        let _file = match result {
            Ok(file) => file,
            Err(error) => match error.kind() {
                ErrorKind::NotFound => {
                    panic!("ファイルが見つかりません: {:?}", error);
                }
                other_error => {
                    panic!("ファイルを開けませんでした: {:?}", other_error);
                }
            },
        };
    }

unwrap と expect の使い方と注意点
----------------------------------

毎回 ``match`` を書くのは冗長に感じられることがあります。 ``Result<T, E>`` には ``unwrap`` メソッドと ``expect`` メソッドが用意されており、``Ok`` の場合は中身を取り出し、``Err`` の場合はその場で ``panic!`` します。

.. code-block:: rust

    use std::fs::File;

    fn main() {
        // Err の場合、デフォルトのメッセージで panic する
        let _file1 = File::open("hello.txt").unwrap();

        // Err の場合、指定したメッセージで panic する
        let _file2 = File::open("hello.txt")
            .expect("hello.txt を開けませんでした");
    }

``expect`` はメッセージを自分で指定できるため、``unwrap`` よりもデバッグしやすくなります。ただし、どちらもエラー時にプログラムを即座に終了させるため、プロトタイピングや「失敗しないと分かっている」場面以外では多用すべきではありません。本番のコードでは、後述する ``?`` 演算子や ``match`` を使って適切にエラーを処理することが推奨されます。

? 演算子によるエラーの伝播
----------------------------------

エラーが起きた関数の中では処理しきれず、呼び出し元にエラーを「伝播」させたい場合がよくあります。そのために使うのが ``?`` 演算子です。

.. code-block:: rust

    use std::fs::File;
    use std::io::{self, Read};

    fn read_username_from_file() -> Result<String, io::Error> {
        let mut file = File::open("hello.txt")?;
        let mut username = String::new();
        file.read_to_string(&mut username)?;
        Ok(username)
    }

``?`` は、対象の ``Result`` が ``Ok`` であれば中身の値を取り出して処理を続け、``Err`` であればその ``Err`` をそのまま関数の戻り値として即座に ``return`` します。これにより、``match`` を何段も書かずに簡潔にエラーを伝播できます。

``?`` 演算子を使うには、それを使う関数自身の戻り値が ``Result`` (または ``Option``)になっている必要があります。``main`` 関数でも、戻り値を ``Result<(), E>`` にすれば ``?`` を利用できます。

.. code-block:: rust

    use std::error::Error;
    use std::fs::File;

    fn main() -> Result<(), Box<dyn Error>> {
        let _file = File::open("hello.txt")?;
        Ok(())
    }

``dyn`` (トレイトオブジェクト) や ``Box`` (スマートポインタ) については、スマートポインタの章で詳しく説明します。ここでは「``main`` から ``?`` を使うための定型句」と捉えておけば十分です。

``Option<T>`` を返す関数でも同様に ``?`` を使えます。``Some`` であれば中身を取り出して処理を続け、``None`` であれば即座に ``None`` を返します。

.. code-block:: rust

    fn first_char_uppercase(text: &str) -> Option<char> {
        let first = text.chars().next()?;
        Some(first.to_ascii_uppercase())
    }

    fn main() {
        println!("{:?}", first_char_uppercase("rust")); // Some('R')
        println!("{:?}", first_char_uppercase(""));      // None
    }

独自のエラー型
----------------------------------

実務のコードでは、``Box<dyn Error>`` で済ませず、自分のプログラム専用のエラー型を定義することもよくあります。複数の失敗パターンを1つの ``enum`` にまとめ、``std::fmt::Display`` を実装してエラーメッセージを組み立てられるようにするのが基本的なパターンです。

.. code-block:: rust

    use std::fmt;

    #[derive(Debug)]
    enum AppError {
        NotFound(String),
        InvalidInput(String),
    }

    impl fmt::Display for AppError {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            match self {
                AppError::NotFound(name) => write!(f, "{} が見つかりません", name),
                AppError::InvalidInput(msg) => write!(f, "入力が不正です: {}", msg),
            }
        }
    }

    impl std::error::Error for AppError {}

    fn find_user(id: u32) -> Result<String, AppError> {
        if id == 0 {
            return Err(AppError::NotFound(String::from("ユーザー")));
        }
        Ok(String::from("Alice"))
    }

    fn main() {
        match find_user(0) {
            Ok(name) => println!("見つかりました: {}", name),
            Err(error) => println!("エラー: {}", error),
        }
    }

``impl std::error::Error for AppError {}`` のように、``Display`` だけでなく ``std::error::Error`` トレイトも実装しておくのが、独自のエラー型としては「完成形」となる慣習的なパターンです。``Error`` トレイト自体にはメソッドの実装義務がほとんどありませんが、これを実装しておくことで、例えば ``AppError`` を ``Box<dyn Error>`` に変換して先ほどの ``?`` 演算子でまとめて扱えるようになるなど、標準ライブラリやエコシステムのエラー処理の仕組みと連携しやすくなります。

なお、``?`` 演算子は、対象の ``Err`` の型と関数の戻り値のエラー型が異なっていても、内部で ``From::from`` を呼び出して自動的に型変換を行ってくれます。異なる種類のエラー(例えば ``std::io::Error`` と独自のエラー型)を1つの関数の中で ``?`` を使ってまとめて扱いたいときは、独自のエラー型に対して ``From<io::Error>`` を実装しておくと、``?`` だけで変換までしてくれるようになります。

ここまで見てきたように、独自のエラー型を「きちんと」定義しようとすると ``Display`` や ``Error`` の実装、``From`` による変換など、書くべき定型コードが増えていきます。そのため実務の Rust コードでは、こうした手作業を省くために ``anyhow`` や ``thiserror`` というクレートがデファクトスタンダードとしてよく使われます。アプリケーションのコードでは、``Box<dyn Error>`` を手軽に扱える ``anyhow`` がよく使われ、ライブラリのコードでは ``#[derive(thiserror::Error)]`` によって ``Display``/``Error`` の実装を自動生成できる ``thiserror`` がよく使われます。本書では標準ライブラリの範囲にとどめて解説していますが、実務でエラー処理を書く際にはこれらのクレートの存在を知っておくとよいでしょう。

Result/Option のコンビネータメソッド
--------------------------------------

``match`` や ``unwrap``/``expect``/``?`` 以外にも、``Result``/``Option`` には「コンビネータ」と呼ばれる便利なメソッドが多数用意されています。実務の Rust コードでは、これらのメソッドが ``match`` や ``?`` と同じくらいの頻度で登場します。代表的なものを紹介します。

``unwrap_or`` は、``Err``/``None`` のときに指定したデフォルト値を使います。

.. code-block:: rust

    fn main() {
        let x: Result<i32, &str> = Err("失敗");
        println!("{}", x.unwrap_or(0)); // 0

        let y: Option<i32> = None;
        println!("{}", y.unwrap_or(-1)); // -1
    }

``map`` は、``Ok``/``Some`` の中身だけにクロージャを適用して変換します。``Err``/``None`` の場合は何もせずそのまま伝播します。

.. code-block:: rust

    fn main() {
        let x: Result<i32, &str> = Ok(3);
        let doubled = x.map(|v| v * 2);
        println!("{:?}", doubled); // Ok(6)
    }

``map_err`` は ``map`` とは逆に、``Err`` の中身(エラー値)だけを変換します。異なるエラー型を1つにそろえたいときによく使います。

.. code-block:: rust

    fn main() {
        let x: Result<i32, &str> = Err("not a number");
        let y: Result<i32, String> = x.map_err(|e| format!("パースエラー: {}", e));
        println!("{:?}", y); // Err("パースエラー: not a number")
    }

``and_then`` は、成功した場合に続けて別の ``Result``/``Option`` を返す処理をつなげます。``map`` と違い、渡すクロージャ自身が ``Result``/``Option`` を返す点が特徴です。

.. code-block:: rust

    fn half_if_even(n: i32) -> Option<i32> {
        if n % 2 == 0 {
            Some(n / 2)
        } else {
            None
        }
    }

    fn main() {
        let result = Some(8).and_then(half_if_even).and_then(half_if_even);
        println!("{:?}", result); // Some(2)
    }

.. admonition:: Python 経験者向けメモ
   :class: tip

   Python の ``try``/``except`` は、実行時にコードを動かしてみて例外が発生したら捕まえる、という仕組みです。そのため ``except`` を書き忘れていても文法上のエラーにはならず、実行するまでどんな例外が飛んでくるか分かりません。

   一方 Rust の ``Result<T, E>`` は、関数の戻り値の「型」としてエラーの可能性が表現されます。呼び出し側は戻り値が ``Result`` であることをコンパイラに把握されているため、``match`` や ``?`` などで中身を処理しない限りコンパイルが通りません。つまり Rust では「エラー処理を書き忘れる」ことがコンパイルの段階で発見しやすくなっているのです。

まとめ
------

- 回復不能なエラーには ``panic!`` を使い、プログラムを強制終了させます。
- 回復可能なエラーは ``Result<T, E>`` の ``Ok``/``Err`` で表現します。
- ``match`` を使うと ``Ok``/``Err`` それぞれに応じた処理を書けます。
- ``unwrap``/``expect`` は手軽ですが、失敗時に即座に ``panic!`` するため、本番コードでは多用を避けるべきです。
- ``?`` 演算子を使うと、戻り値が ``Result`` の関数の中でエラーを簡潔に呼び出し元へ伝播できます。
- 複数のエラー種別を ``enum`` にまとめ、``Display`` を実装すれば独自のエラー型を定義できます。``?`` 演算子は ``From::from`` によって型を自動変換してくれます。
- ``unwrap_or``/``map``/``map_err``/``and_then`` などのコンビネータメソッドを使うと、``match`` を書かずに ``Result``/``Option`` を簡潔に処理できます。
