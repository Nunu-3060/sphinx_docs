列挙型とパターンマッチング
==========================

複数の候補の中からいずれか1つの状態を取りうるデータを表現したいとき、Rust では「列挙型(enum)」を使います。列挙型は Python のクラスや辞書だけでは表現しづらい「いくつかの決まったパターンのうちどれか1つ」という関係を、型として明確に表現できます。

enum の定義とバリアント
----------------------------------------

``enum`` キーワードで列挙型を定義し、取りうる値の候補を「バリアント(variant)」として列挙します。

.. code-block:: rust

    enum IpAddrKind {
        V4,
        V6,
    }

    fn main() {
        let four = IpAddrKind::V4;
        let six = IpAddrKind::V6;
    }

Rust の列挙型の強力な点は、各バリアントにデータを持たせられることです。バリアントごとに異なる種類・数のデータを持たせることもできます。

.. code-block:: rust

    enum IpAddr {
        V4(u8, u8, u8, u8),
        V6(String),
    }

    fn main() {
        let home = IpAddr::V4(127, 0, 0, 1);
        let loopback = IpAddr::V6(String::from("::1"));
    }

構造体のような名前付きフィールドを含む、より複雑なデータを持たせることも可能です。

.. code-block:: rust

    enum Message {
        Quit,                       // データを持たないバリアント
        Move { x: i32, y: i32 },    // 構造体のような名前付きフィールドを持つ
        Write(String),              // 文字列を1つ持つ
        ChangeColor(i32, i32, i32), // 値を3つ持つ
    }

match によるパターンマッチング
----------------------------------------

列挙型の値がどのバリアントであるかによって処理を分けるには、``match`` 式を使います。 ``match`` は Python の ``if``/``elif`` の連鎖や辞書によるディスパッチに近い役割を果たしますが、大きな違いとして「すべてのバリアントを網羅しているか」をコンパイラがチェックしてくれます。

.. code-block:: rust

    enum Coin {
        Penny,
        Nickel,
        Dime,
        Quarter,
    }

    fn value_in_cents(coin: Coin) -> u8 {
        match coin {
            Coin::Penny => 1,
            Coin::Nickel => 5,
            Coin::Dime => 10,
            Coin::Quarter => 25,
        }
    }

    fn main() {
        println!("{}", value_in_cents(Coin::Dime));
    }

もし ``match`` の中で ``Coin`` のバリアントのどれか1つでも処理し忘れると、コンパイルエラーになります。この「網羅性チェック(exhaustiveness checking)」により、うっかり1つのケースを処理し忘れるバグをコンパイル時に防げます。

複数のバリアントに対して同じ処理を行いたい場合は、``|`` を使って1つのアームにまとめて書くこともできます。

.. code-block:: rust

    fn describe_coin(coin: Coin) -> String {
        match coin {
            Coin::Penny => String::from("1セント硬貨です"),
            Coin::Nickel | Coin::Dime => String::from("5セント硬貨か10セント硬貨です"),
            Coin::Quarter => String::from("25セント硬貨です"),
        }
    }

    fn main() {
        println!("{}", describe_coin(Coin::Dime));
    }

バリアントがデータを持つ場合、``match`` のパターンでそのデータを取り出すこともできます。

.. code-block:: rust

    fn main() {
        let msg = Message::Move { x: 10, y: 20 };

        match msg {
            Message::Quit => println!("Quit"),
            Message::Move { x, y } => println!("Move to ({}, {})", x, y),
            Message::Write(text) => println!("Write: {}", text),
            Message::ChangeColor(r, g, b) => println!("Color: ({}, {}, {})", r, g, b),
        }
    }

すべてのケースを個別に書く必要がない場合は、``_`` を使って「それ以外すべて」を表すこともできます。

.. code-block:: rust

    fn main() {
        let coin = Coin::Dime;

        match coin {
            Coin::Quarter => println!("25セント"),
            _ => println!("それ以外"),
        }
    }

impl による enum へのメソッド定義
----------------------------------------

構造体と同様、``enum`` にも ``impl`` ブロックでメソッドを定義できます。メソッドの中で ``self`` に対して ``match`` を使えば、バリアントごとに異なる処理を行うメソッドを自然に書くことができます。

.. code-block:: rust

    enum Message {
        Quit,
        Write(String),
    }

    impl Message {
        fn call(&self) {
            match self {
                Message::Quit => println!("終了します"),
                Message::Write(text) => println!("メッセージ: {}", text),
            }
        }
    }

    fn main() {
        let m = Message::Write(String::from("こんにちは"));
        m.call();
    }

なお ``call`` は ``&self`` を受け取るため、``match self`` でマッチした ``self`` も参照です。そのため ``Message::Write(text)`` にマッチした ``text`` は ``String`` ではなく ``&String`` として束縛され(この自動的な調整は「マッチ・エルゴノミクス」と呼ばれます)、所有権はムーブされません。

Option<T> による値の有無の表現
----------------------------------------

多くの言語には「値が無い」ことを表す ``null`` や ``None`` がありますが、Rust には ``null`` がありません。代わりに、標準ライブラリで定義されている ``Option<T>`` という列挙型を使って「値があるかもしれないし、無いかもしれない」ことを型として表現します。

.. code-block:: rust

    enum Option<T> {
        Some(T),
        None,
    }

ここで登場する ``<T>`` は、``Some`` が中に持つ値の型を表すプレースホルダーです。このような ``<T>`` の書き方は「ジェネリクス」と呼ばれる仕組みで、詳しくは後の「ジェネリクスとトレイト」の章で説明します。ここでは「``Option<T>`` は ``T`` にどんな型でも入れられる」という程度に理解しておけば十分です。

``Option<T>`` は、値がある場合を表す ``Some(T)`` と、値が無い場合を表す ``None`` という2つのバリアントを持つ列挙型です。``Option``/``Some``/``None`` は標準で常に使えます(prelude に含まれているため ``use`` は不要です)。ただし型によってはこうはいかず、後の「コレクション」の章で登場する ``HashMap`` のように、使う前に ``use`` 文で明示的にインポートしなければならないものもあります。

.. code-block:: rust

    fn main() {
        let some_number = Some(5);       // Option<i32>
        let some_string = Some("文字列"); // Option<&str>
        let absent_number: Option<i32> = None;
    }

重要なのは、``Option<T>`` に包まれた値は、そのままでは中身の型として使うことができない点です。値を取り出すには ``match`` などを使って ``Some`` と ``None`` の両方を必ず処理しなければなりません。

.. code-block:: rust

    fn describe_number(x: Option<i32>) -> String {
        match x {
            Some(n) => format!("値は {} です", n),
            None => String::from("値はありません"),
        }
    }

    fn main() {
        println!("{}", describe_number(Some(7)));
        println!("{}", describe_number(None));
    }

もし ``match`` で ``None`` のケースを書き忘れると、コンパイラがエラーとして教えてくれます。これにより、「値が無いかもしれないことを忘れて処理してしまう」という、他の言語で頻発するバグをコンパイル時に防ぐことができます。

``match`` を使わずに手っ取り早く中身を取り出したいだけの場合、``unwrap`` や ``expect`` というメソッドも用意されています。

.. code-block:: rust

    fn main() {
        let some_number = Some(5);
        println!("{}", some_number.unwrap()); // 5

        let absent_number: Option<i32> = None;
        println!("{}", absent_number.unwrap()); // ここでパニックする
    }

``unwrap`` は ``Some(value)`` であれば ``value`` を返しますが、``None`` の場合はその場でパニック(プログラムの異常終了)を起こします。``expect`` も同様に動作しますが、パニック時に表示するメッセージを指定できる点が異なります。どちらも ``None`` の場合にパニックしてしまうため多用は避けるべきで、より丁寧なエラー処理の方法は後の「エラーハンドリング」の章で扱います。

if let による簡易マッチング
----------------------------------------

``match`` は網羅的である必要がありますが、「特定のパターンのときだけ処理したい」という場面では ``if let`` を使うとより簡潔に書けます。

.. code-block:: rust

    fn main() {
        let some_value = Some(3);

        // match で書くと
        match some_value {
            Some(n) => println!("値は {} です", n),
            _ => {}
        }

        // if let で書くとよりシンプル
        if let Some(n) = some_value {
            println!("値は {} です", n);
        }
    }

``else`` と組み合わせて、パターンに一致しなかった場合の処理を書くこともできます。

.. code-block:: rust

    fn main() {
        let some_value: Option<i32> = None;

        if let Some(n) = some_value {
            println!("値は {} です", n);
        } else {
            println!("値はありませんでした");
        }
    }

.. admonition:: Python 経験者向けメモ
   :class: tip

   Python では「値が無いかもしれない」ことを ``None`` で表現しますが、``None`` かどうかのチェックは実行時まで強制されません。あるコードを書いていて、実行してみて初めて変数が ``None`` だったことに気づき ``AttributeError`` になる、という経験をしたことがある方も多いはずです。

   Rust の ``Option<T>`` は中身の型とは異なる型として扱われるため、``Some`` と ``None`` の両方を処理しない限りコンパイルが通りません。つまり「値が無いケースの処理忘れ」を実行前、コンパイルの段階で必ず検出できます。これは Rust に ``null`` が存在しないことの裏返しでもあり、null 関連のバグを型システムのレベルで防ぐ Rust の代表的な特徴です。

まとめ
------

- ``enum`` は複数の候補(バリアント)のうちどれか1つを表す型で、バリアントごとに異なるデータを持たせることもできます
- 構造体と同様、``enum`` にも ``impl`` ブロックでメソッドを定義でき、メソッド内で ``self`` に対して ``match`` を使えます
- ``match`` はすべてのバリアントを網羅しているかをコンパイラがチェックしてくれるパターンマッチング構文であり、``|`` を使えば複数のバリアントを1つのアームにまとめられます
- Rust には ``null`` が無く、「値が無いかもしれない」ことは ``Option<T>`` (``Some(T)``/``None``)という型で表現します
- ``Option<T>`` の中身を使うには ``Some``/``None`` の両方を処理する必要があり、これによって null 関連のバグをコンパイル時に防げます
- ``unwrap``/``expect`` を使えば ``Option<T>`` から手早く値を取り出せますが、``None`` の場合パニックするため多用は避けます
- 特定の1パターンだけを扱いたい場合は、``match`` より簡潔な ``if let`` が使えます
