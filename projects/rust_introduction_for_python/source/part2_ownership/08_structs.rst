構造体
======

Rust で複数の関連するデータをひとまとめにして扱いたいときに使うのが「構造体(struct)」です。構造体は、名前付きのフィールドを持つ独自のデータ型を定義する仕組みで、Python のクラスの「データを保持する部分」に近い役割を果たします。

構造体の定義とインスタンス化
----------------------------------------

構造体は ``struct`` キーワードで定義します。各フィールドには名前と型を指定します。

.. code-block:: rust

    struct User {
        username: String,
        email: String,
        active: bool,
        sign_in_count: u64,
    }

    fn main() {
        let user1 = User {
            username: String::from("someusername123"),
            email: String::from("someone@example.com"),
            active: true,
            sign_in_count: 1,
        };

        println!("{} さんのメールアドレス: {}", user1.username, user1.email);
    }

なお、ここでは ``username`` や ``email`` のフィールドに ``String`` のような所有権を持つ型を使っています。フィールドに ``&str`` のような参照を持たせることも可能ですが、その場合はライフタイム注釈が必要になります。今の段階ではフィールドには ``String`` のような所有権を持つ型を使うのがシンプルで、参照をフィールドに持たせる方法は後の「ライフタイム」の章で説明します。

``user1`` 自体を ``println!("{:?}", user1)`` のようにそのまま ``{:?}`` で表示したい場合は、構造体定義の直前に ``#[derive(Debug)]`` という注釈を付けておく必要があります(詳細は後の章で扱います)。

``derive`` にはほかにもよく使われるものがあります。例えば ``Clone`` を指定するとインスタンスを複製できるようになり(``clone`` メソッドが使えるようになります)、``PartialEq`` を指定すると ``==`` 演算子でインスタンス同士を比較できるようになります。``#[derive(Debug, Clone, PartialEq)]`` のように、複数のトレイトをまとめて指定することもできます。

.. code-block:: rust

    #[derive(Debug, Clone, PartialEq)]
    struct Point {
        x: i32,
        y: i32,
    }

    fn main() {
        let p1 = Point { x: 1, y: 2 };
        let p2 = p1.clone();

        println!("{}", p1 == p2); // true: フィールドの値がすべて等しいので等しいと判定される
    }

``derive`` できるトレイトの詳しい一覧や、それぞれがどのような仕組みで動いているかは、後の「ジェネリクスとトレイト」の章で扱います。

フィールドの値には ``.`` でアクセスします。インスタンスを ``mut`` として宣言すれば、フィールドの値を書き換えることもできます(構造体は一部のフィールドだけを可変にすることはできず、インスタンス全体が可変か不変かのどちらかです)。

.. code-block:: rust

    fn main() {
        let mut user1 = User {
            username: String::from("someusername123"),
            email: String::from("someone@example.com"),
            active: true,
            sign_in_count: 1,
        };

        user1.email = String::from("another@example.com");
    }

関数の引数名とフィールド名が一致している場合は、フィールド初期化省略記法を使ってより簡潔に書くことができます。

.. code-block:: rust

    fn build_user(email: String, username: String) -> User {
        User {
            username, // username: username, と同じ意味
            email,    // email: email, と同じ意味
            active: true,
            sign_in_count: 1,
        }
    }

既存のインスタンスの値の大部分を再利用しつつ、一部のフィールドだけ変更した新しいインスタンスを作りたい場合は、構造体更新記法(``..``)が便利です。

.. code-block:: rust

    fn main() {
        let user1 = build_user(
            String::from("someone@example.com"),
            String::from("someusername123"),
        );

        let user2 = User {
            email: String::from("another@example.com"),
            ..user1 // 残りのフィールドは user1 と同じ値を使う
        };

        println!("{}", user2.username);
    }

なお ``..user1`` はフィールドの値をコピーまたはムーブするため、``String`` のように ``Copy`` を実装していないフィールドが含まれる場合、``user1`` はこの後まるごとは使えなくなる点に注意してください。

impl ブロックとメソッド
----------------------------------------

構造体にひもづく振る舞い(メソッド)は、構造体定義とは別に ``impl`` ブロックの中で定義します。

.. code-block:: rust

    struct Rectangle {
        width: u32,
        height: u32,
    }

    impl Rectangle {
        // &self を受け取るのでインスタンスを借用するメソッド
        fn area(&self) -> u32 {
            self.width * self.height
        }

        // &mut self を受け取るので、値を書き換えるメソッド
        fn double_width(&mut self) {
            self.width *= 2;
        }
    }

    fn main() {
        let mut rect = Rectangle { width: 30, height: 50 };

        println!("面積: {}", rect.area());

        rect.double_width();
        println!("2倍後の面積: {}", rect.area());
    }

なお ``rect.area()`` のように呼び出す際、``area`` が ``&self`` を受け取るメソッドであっても、``rect`` を明示的に ``&rect`` と書く必要はありません。Rust コンパイラがメソッドのシグネチャに合わせて自動的に ``&rect``(必要なら ``&mut rect``)に変換してくれるためで、これは「自動参照(automatic referencing)」と呼ばれる仕組みです。Python には対応する概念がないため、``&self`` の意味を学んだばかりだと不思議に見えるかもしれません。

メソッドの第一引数は常に ``self`` の何らかの形です。``&self`` は不変参照として借用するだけの読み取り専用のメソッド、``&mut self`` は可変参照として借用し値を変更できるメソッドです。``self`` を値として受け取る(参照を付けない)メソッドも定義でき、その場合は呼び出すとインスタンスの所有権がメソッドに移動します(元の変数はそれ以降使えなくなります)。

関連関数
----------------------------------------

``impl`` ブロックの中には、``self`` を引数に取らない関数も定義できます。これは「関連関数(associated function)」と呼ばれ、``StructName::function_name()`` の形式で呼び出します。コンストラクタのように、新しいインスタンスを組み立てて返す用途でよく使われます(標準ライブラリの ``String::new()`` もこの形式の関連関数です)。

.. code-block:: rust

    impl Rectangle {
        // 正方形を作る関連関数(コンストラクタ的な役割)
        fn square(size: u32) -> Self {
            Self {
                width: size,
                height: size,
            }
        }
    }

    fn main() {
        let sq = Rectangle::square(20);
        println!("面積: {}", sq.area());
    }

``Self`` (大文字)は、この ``impl`` ブロックが対象としている型(ここでは ``Rectangle``)の別名として使えるキーワードです。

タプル構造体とユニット構造体
----------------------------------------

フィールドに名前を付けず、型だけを並べた「タプル構造体」も定義できます。

.. code-block:: rust

    struct Color(i32, i32, i32);
    struct Point(i32, i32, i32);

    fn main() {
        let black = Color(0, 0, 0);
        let origin = Point(0, 0, 0);

        println!("black.0 = {}", black.0); // フィールドにはインデックスでアクセスする
    }

さらに、フィールドを一切持たない「ユニット構造体」もあります。値そのものよりも、特定のトレイトを実装するための「型」としての役割だけが必要な場合に使われます。

.. code-block:: rust

    struct AlwaysEqual;

    fn main() {
        let _subject = AlwaysEqual;
    }

.. admonition:: Python 経験者向けメモ
   :class: tip

   Rust の構造体は、Python のクラスにおける「データ + メソッド」という考え方に近いものです。ただし Python ではクラス本体の中にメソッドを書きますが、Rust では構造体のフィールド定義(``struct``)とメソッドの定義(``impl``)が分離しています。同じ型に対して複数の ``impl`` ブロックを書くこともできます。

   もう一つの大きな違いは継承です。Python のクラスはクラス継承によって振る舞いを共有しますが、Rust の構造体には継承の仕組みがありません。代わりに「トレイト(trait)」と呼ばれる仕組みで共通の振る舞いを定義し、複数の型で共有します。トレイトについては後の章で詳しく扱います。

まとめ
------

- ``struct`` はフィールドをまとめて名前を付けた独自のデータ型を定義します
- フィールドには ``String`` など所有権を持つ型を使うのがシンプルで、参照を持たせるにはライフタイム注釈が必要になります(後の「ライフタイム」の章で扱います)
- ``#[derive(Debug, Clone, PartialEq)]`` のように、``Debug`` (``{:?}`` 表示)に加えて ``Clone`` (複製)や ``PartialEq`` (``==`` 比較)などのトレイトをまとめて導出できます
- フィールド初期化省略記法や構造体更新記法(``..``)を使うとインスタンス生成が簡潔に書けます
- メソッドは構造体定義とは別の ``impl`` ブロックで定義し、``&self``/``&mut self``/ ``self`` で借用の仕方(読み取り専用・書き換え可能・所有権を移動)を使い分けます
- ``self`` を引数に取らない関連関数は ``Type::function()`` の形で呼び出し、コンストラクタとしてよく使われます
- タプル構造体やユニット構造体という、フィールド名を持たない・フィールドを持たない構造体もあります
