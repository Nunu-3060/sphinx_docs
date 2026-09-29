ジェネリクスとトレイト
======================

同じような処理を、扱う型だけを変えて何度も書いた経験はないでしょうか。Python では動的型付けのおかげで、型を気にせず同じ関数をさまざまな型に対して使い回せます。Rust では、コンパイル時に型が確定している必要がありますが、その代わりに「ジェネリクス」と「トレイト」という仕組みで、型に依存しない再利用可能なコードを安全に書くことができます。

ジェネリクスによる関数のパラメータ化
--------------------------------------

ジェネリクスとは、具体的な型の代わりに ``T`` のような型パラメータを使い、関数や構造体を複数の型に対応させる仕組みです。次の例は、スライスの中から最大値を求める関数です。

.. code-block:: rust

    fn largest<T: PartialOrd>(list: &[T]) -> &T {
        let mut result = &list[0];

        for item in list {
            if item > result {
                result = item;
            }
        }

        result
    }

    fn main() {
        let numbers = vec![34, 50, 25, 100, 65];
        println!("最大値: {}", largest(&numbers));

        let chars = vec!['y', 'm', 'a', 'q'];
        println!("最大値: {}", largest(&chars));
    }

``<T: PartialOrd>`` の部分がトレイト境界です。「``T`` は何らかの型だが、 ``PartialOrd`` (大小比較ができること) を実装している型に限る」という制約を表しています。この境界がないと、``item > result`` という比較演算がすべての型に対して定義されているとは限らないため、コンパイルエラーになります。

ジェネリクスによる構造体のパラメータ化
----------------------------------------

構造体もジェネリックにできます。

.. code-block:: rust

    struct Point<T> {
        x: T,
        y: T,
    }

    fn main() {
        let integer_point = Point { x: 5, y: 10 };
        let float_point = Point { x: 1.0, y: 4.0 };

        println!("{} , {}", integer_point.x, float_point.y);
    }

``Point<T>`` は、``x`` と ``y`` が同じ型であればどんな型でも受け入れられる構造体です。実行時に型ごとの分岐をするのではなく、コンパイル時に型ごとの専用コードが生成されるため、実行速度への影響はほとんどありません。

トレイトの定義と実装
--------------------

トレイトは、複数の型が共通して持つべき振る舞い(メソッド)を定義する仕組みで、Rust における「インターフェース」に相当します。

.. code-block:: rust

    trait Summary {
        fn summarize(&self) -> String;
    }

    struct Article {
        title: String,
        content: String,
    }

    impl Summary for Article {
        fn summarize(&self) -> String {
            let preview: String = self.content.chars().take(10).collect();
            format!("{}: {}", self.title, preview)
        }
    }

    fn main() {
        let article = Article {
            title: String::from("Rust入門"),
            content: String::from("今日はトレイトについて学びます。"),
        };

        println!("{}", article.summarize());
    }

``trait Summary`` でメソッドの「シグネチャ」だけを宣言し、 ``impl Summary for Article`` で実際の処理を実装します。1つの型に対して複数のトレイトを実装することもできます。

.. admonition:: 注意: 文字列のスライスと文字境界
   :class: warning

   上の例で ``&self.content[..10]`` のように文字列をバイト単位でスライスしなかったのには理由があります。Rust の ``String`` は UTF-8 でエンコードされており、日本語などのマルチバイト文字は1文字が3〜4バイトを占めます。``&content[..10]`` のようにバイトオフセットでスライスすると、そのオフセットがちょうど文字の境界と一致しない限り ``byte index 10 is not a char boundary`` という実行時パニックになります。Python の文字列スライス(``content[:10]``)は文字(コードポイント)単位で安全に切り出せますが、Rust では文字数で切り出したい場合、上の例のように ``chars()`` イテレータを使って文字単位で処理する必要があります。

トレイト境界(トレイト制約)
------------------------------

ジェネリックな関数の引数に、特定のトレイトを実装した型だけを受け付けたい場合、トレイト境界を使います。

.. code-block:: rust

    fn notify<T: Summary>(item: &T) {
        println!("速報! {}", item.summarize());
    }

この ``notify`` は、``impl Trait`` という構文を使って次のように短く書くこともできます。``fn notify<T: Summary>(item: &T)`` の糖衣構文で、単一の引数であればほぼ同じ意味です。

.. code-block:: rust

    fn notify(item: &impl Summary) {
        println!("速報! {}", item.summarize());
    }

ただし、この2つの書き方は引数が2つ以上になると意味が変わってきます。``fn f<T: Summary>(a: &T, b: &T)`` はジェネリック型パラメータ ``T`` を1つしか持たないため、``a`` と ``b`` は必ず同じ具体的な型でなければなりません。一方 ``fn f(a: &impl Summary, b: &impl Summary)`` は、``impl Summary`` がそれぞれ独立した匿名の型パラメータとして扱われるため、``a`` と ``b`` に異なる型を渡すことができます。

ここまで見てきたジェネリクスや ``impl Trait`` は、コンパイル時に具体的な型ごとの専用コードが生成される「静的ディスパッチ」という方式です。``T`` に入りうる型はコンパイル時にすべて確定しているため、この処理を「単相化(モノモーフィゼーション)」と呼びます。実行時のコストはほとんどありませんが、型の数だけコードが複製されるため、バイナリのサイズは大きくなりがちです。

これに対して、``&dyn Summary`` や ``Box<dyn Summary>`` のように「トレイトオブジェクト」を使う方法は「動的ディスパッチ」と呼ばれ、実際にどの型のメソッドを呼び出すかは、実行時に「vテーブル」と呼ばれる仕組みを介して決定されます。生成されるコードは1つで済むためバイナリは小さくなりますが、実行時にわずかなコストがかかります。``dyn`` やトレイトオブジェクトの詳細については、スマートポインタの章で詳しく扱います。

引数や型パラメータが増えて読みにくくなる場合は、``where`` 句を使って書くこともできます。

.. code-block:: rust

    use std::fmt::Display;

    fn some_function<T, U>(t: &T, u: &U) -> i32
    where
        T: Display,
        U: Clone,
    {
        println!("{}", t);
        let _u2 = u.clone();
        42
    }

デフォルト実装
--------------

トレイトのメソッドには、あらかじめデフォルトの実装を与えておくこともできます。実装側で必要なメソッドだけを上書きすればよいため、共通の振る舞いを何度も書く必要がなくなります。ここでは先ほどの ``Summary`` と混同しないよう、``Announcement`` という別のトレイトとして定義し直します。

.. code-block:: rust

    trait Announcement {
        fn summarize_author(&self) -> String;

        fn summarize(&self) -> String {
            format!("(続きを読む: {}より)", self.summarize_author())
        }
    }

    struct Tweet {
        username: String,
    }

    impl Announcement for Tweet {
        fn summarize_author(&self) -> String {
            format!("@{}", self.username)
        }
        // summarize はデフォルト実装をそのまま使う
    }

.. admonition:: Python 経験者向けメモ
   :class: tip

   Python のダックタイピングは「それらしいメソッドさえ持っていれば動く」という柔軟な設計です。型を明示的に宣言しなくても、 ``summarize`` というメソッドがあればとりあえず呼び出せてしまい、実際に存在しなければ実行時に ``AttributeError`` になります。

   Rust のトレイトは、これに近い柔軟性を持ちながらも、「このジェネリック型は必ずこのトレイトを実装している」ことをコンパイル時に保証してくれます。役割としては Python の抽象基底クラス(``abc.ABC``)に近く、メソッドの実装漏れや型の取り違えは実行前にコンパイルエラーとして検出されます。

``derive`` できる主なトレイト
--------------------------------

構造体の章で、``#[derive(Debug, Clone, PartialEq)]`` のように書くと、コンパイラがトレイトの実装を自動生成してくれることに触れました。構造体の章で予告した通り、ここで ``derive`` によって自動導出できる代表的なトレイトをまとめて紹介します。

- ``Debug``: ``{:?}`` 形式でのデバッグ出力を可能にします。
- ``Clone``: ``clone()`` メソッドによる値の複製を可能にします。
- ``PartialEq``: ``==``/``!=`` による等価比較を可能にします。
- ``PartialOrd``: ``<``/``>`` などによる大小比較を可能にします。
- ``Copy``: 値をムーブではなくコピーで扱えるようにします。整数や浮動小数点数のような単純な型でよく使われます。
- ``Default``: ``Default::default()`` で、その型の「既定値」を生成できるようにします。
- ``Hash``: ``HashMap`` や ``HashSet`` のキーとして使えるようにします。

.. code-block:: rust

    #[derive(Debug, Clone, Copy, PartialEq, PartialOrd, Default, Hash)]
    struct Score {
        value: i32,
    }

    fn main() {
        let a = Score { value: 10 };
        let b = a; // Copy が導出されているのでムーブではなくコピーされる

        println!("{:?}", a);                       // Score { value: 10 }
        println!("{}", a == b);                     // true
        println!("{}", a < Score { value: 20 });    // true
        println!("{:?}", Score::default());         // Score { value: 0 }
    }

これらのトレイトは、フィールドがすべて対応するトレイトを実装している場合にのみ導出できます。例えば ``String`` を含む構造体には ``Copy`` を導出できません。

関連型(Associated Types)
------------------------------

トレイトの中には、メソッドのシグネチャだけでなく「型」そのものを宣言できるものがあります。これを関連型と呼びます。代表例が、後のイテレータの章で扱う ``Iterator`` トレイトです。

.. code-block:: rust

    trait Iterator {
        type Item;

        fn next(&mut self) -> Option<Self::Item>;
    }

``type Item;`` の部分が関連型の宣言で、``impl Iterator for SomeType`` する側が「自分にとっての ``Item`` は具体的に何の型か」を決めます。関連型はジェネリクスの型パラメータ ``<T>`` と似た役割を果たしますが、``T`` が呼び出し側で自由に選べるのに対し、関連型は1つのトレイト実装につき1種類の型に固定される点が異なります。``next`` メソッドのように、そのトレイト自身の定義の中で「この型」を指し示したい場合に使われる仕組みだと考えるとよいでしょう。

まとめ
------

- ジェネリクスを使うと、型パラメータ ``T`` によって関数や構造体を複数の型に対応させられます。
- トレイトは ``trait`` で宣言し、``impl Trait for Type`` で型ごとの実装を与えます。
- トレイト境界(``<T: Trait>`` や ``where`` 句)によって、ジェネリックな型が特定の振る舞いを持つことをコンパイル時に保証できます。
- トレイトにはデフォルト実装を与えられ、実装側は必要な部分だけを上書きできます。
- Rust のトレイトは Python のダックタイピングに近い柔軟性を持ちつつ、型の安全性をコンパイル時に確保する仕組みです。
- ``derive`` を使うと、``Debug``/``Clone``/``PartialEq`` に加えて、``PartialOrd`` (大小比較)、``Copy`` (コピー可能にする)、``Default`` (既定値の生成)、``Hash`` (``HashMap`` のキーに利用) なども自動導出できます。
- 関連型(``type Item;`` など)を使うと、トレイトの定義の中で「実装ごとに決まる型」を表現できます。
