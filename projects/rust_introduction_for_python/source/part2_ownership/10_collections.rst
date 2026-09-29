コレクション
============

実際のプログラムでは、単一の値だけでなく複数の値をまとめて扱う場面がほとんどです。Rust の標準ライブラリには、複数の値をまとめて扱うための「コレクション」型がいくつか用意されています。本章では、その中でも特によく使われる ``Vec<T>``、``String``/ ``&str``、``HashMap<K, V>`` を扱います。これらのデータもすべて、これまで学んだ所有権と借用のルールに従って管理されます。

Vec<T>: 可変長配列
----------------------------------------

``Vec<T>`` (通称「ベクタ」)は、同じ型 ``T`` の値を可変長で並べて格納できるコレクションです。Python の ``list`` に近い役割を果たします。

.. code-block:: rust

    fn main() {
        let mut v: Vec<i32> = Vec::new(); // 空の Vec を作る(この後 push するため型注釈は省略可能)

        v.push(1);
        v.push(2);
        v.push(3);

        println!("{:?}", v); // [1, 2, 3]
    }

初期値がある場合は ``vec!`` マクロを使うと簡潔に書けます。

.. code-block:: rust

    fn main() {
        let v = vec![1, 2, 3]; // 型は i32 が推論される
        println!("{:?}", v);
    }

要素へのアクセスには、添字によるインデックスアクセスと ``get`` メソッドの2通りの方法があります。

.. code-block:: rust

    fn main() {
        let v = vec![1, 2, 3, 4, 5];

        let third: &i32 = &v[2]; // インデックスアクセス(範囲外だとパニックする)
        println!("3番目の要素: {}", third);

        match v.get(2) { // get は Option<&T> を返すので安全に扱える
            Some(value) => println!("3番目の要素: {}", value),
            None => println!("要素がありません"),
        }

        match v.get(100) { // 範囲外でもパニックせず None が返る
            Some(value) => println!("100番目の要素: {}", value),
            None => println!("そんな要素はありません"),
        }
    }

このほかにもよく使うメソッドがいくつかあります。``len`` は要素数を、``is_empty`` は要素が1つも無いかどうかを、``pop`` は末尾の要素を取り除いて返し、``contains`` は指定した値が含まれているかどうかを調べます。

.. code-block:: rust

    fn main() {
        let mut v = vec![1, 2, 3];

        println!("要素数: {}", v.len());       // 3
        println!("空か: {}", v.is_empty());    // false

        let last = v.pop(); // 末尾を取り除いて返す(戻り値は Option<T>)
        println!("{:?}", last); // Some(3)
        println!("{:?}", v);    // [1, 2]

        println!("{}", v.contains(&2)); // true
    }

``for`` ループを使うと、``Vec`` の全要素を順番に取り出すことができます。

.. code-block:: rust

    fn main() {
        let v = vec![100, 32, 57];

        for i in &v { // 不変参照でイテレーションする
            println!("{}", i);
        }

        let mut v2 = vec![100, 32, 57];
        for i in &mut v2 { // 可変参照でイテレーションすれば要素を書き換えられる
            *i += 50;
        }
        println!("{:?}", v2); // [150, 82, 107]
    }

String と文字列スライス &str
----------------------------------------

Rust には文字列を扱う型が主に2つあります。所有権を持つ ``String`` と、文字列データを借用する文字列スライス ``&str`` です。この2つの違いは、Rust を学ぶうえで所有権の考え方が最も具体的に現れる場所の1つです。

``String`` はヒープ上に確保された、伸長可能・所有権を持つ文字列型です。

.. code-block:: rust

    fn main() {
        let mut s = String::from("hello");
        s.push_str(", world"); // 文字列を末尾に追加する(所有しているので変更可能)

        println!("{}", s);
    }

文字列同士を連結する方法としては、``+`` 演算子を使うこともできます。

.. code-block:: rust

    fn main() {
        let s1 = String::from("Hello, ");
        let s2 = String::from("world!");
        let s3 = s1 + &s2; // s1 の所有権はここで消費され、以後 s1 は使えなくなる

        println!("{}", s3);
    }

``+`` 演算子は左辺の ``String`` の所有権を消費してしまう点に注意してください(右辺は参照 ``&s2`` を渡すだけなので所有権は移動しません)。なお ``&s2`` は ``&String`` ですが、Rust の「デリファレンス型強制(deref coercion)」によって自動的に ``&str`` に変換されるため、本来 ``&str`` を期待する ``+`` の右辺にそのまま渡すことができます。所有権を消費せずに複数の文字列から新しい ``String`` を組み立てたい場合は、``format!`` マクロが便利です。``format!`` は ``println!`` と同じ書式指定が使えますが、標準出力には表示せず、結果を新しい ``String`` として返します。

.. code-block:: rust

    fn main() {
        let s1 = String::from("Hello");
        let s2 = String::from("world");
        let s3 = format!("{}, {}!", s1, s2); // s1, s2 の所有権は消費されない

        println!("{}", s3);
        println!("{} {}", s1, s2); // s1, s2 はまだ有効
    }

``format!`` はここまでの章でもすでに何度か登場していますが、文字列を組み立てる手段として ``+`` と合わせてあらためて整理しておきましょう。

対して ``&str`` は、``String`` の一部、または文字列リテラルへの借用です。文字列リテラル(``"hello"`` のように直接書いた文字列)は実は ``&'static str`` という型で、プログラムのバイナリに埋め込まれた文字列データへの参照です。

.. code-block:: rust

    fn main() {
        let s = String::from("hello world");

        let hello: &str = &s[0..5];  // "hello" という s を借用したスライス
        let world: &str = &s[6..11]; // "world"

        println!("{} {}", hello, world);
    }

なお、スライスは文字列に限った特別な機能ではなく、Rust におけるより一般的な概念です。``&[T]`` という形で ``Vec<T>`` や配列の一部を借用する「スライス」も存在し、``&str`` はその文字列版(``&[u8]`` に相当するバイト列への参照)にあたる一例だと考えると理解しやすいでしょう。

.. admonition:: 注意: 文字列のスライスと文字境界
   :class: warning

   ``&s[0..5]`` のようなスライスの範囲は、文字数ではなくバイト数で指定する必要があります。英数字であれば1文字が1バイトなので問題になりませんが、日本語などのマルチバイト文字を含む文字列を文字の区切り(バイト境界)ではない位置でスライスしようとすると、実行時にパニックが発生します。マルチバイト文字列を安全に扱う方法については、後の「ジェネリクスとトレイト」の章で詳しく説明します。

関数の引数として文字列を受け取る場合、所有権を要求しない ``&str`` を受け取るようにしておくと、``String`` と文字列リテラルの両方を受け取れて柔軟です。

.. code-block:: rust

    fn first_word(s: &str) -> &str {
        let bytes = s.as_bytes();

        for (i, &item) in bytes.iter().enumerate() {
            if item == b' ' {
                return &s[0..i];
            }
        }

        s
    }

    fn main() {
        let my_string = String::from("hello world");
        println!("{}", first_word(&my_string)); // String からも呼べる

        let my_literal = "hello world";
        println!("{}", first_word(my_literal)); // 文字列リテラルからも呼べる
    }

大まかな使い分けの目安として、「文字列を新しく作る・保持する・書き換える」場合は ``String`` を、「既にある文字列を一時的に読み取るだけ」の場合は ``&str`` を使う、と覚えておくとよいでしょう。

HashMap<K, V>
----------------------------------------

キーと値の組を格納する ``HashMap<K, V>`` は、Python の ``dict`` に近いコレクションです。``Vec`` と違い標準の prelude には含まれていないため、使う際は ``use`` 文でインポートする必要があります。

.. code-block:: rust

    use std::collections::HashMap;

    fn main() {
        let mut scores = HashMap::new();

        scores.insert(String::from("Blue"), 10);
        scores.insert(String::from("Yellow"), 50);

        println!("{:?}", scores);
    }

値を取得するには ``get`` メソッドを使います。キーが存在するとは限らないため、 ``get`` は ``Option<&V>`` を返します。

.. code-block:: rust

    use std::collections::HashMap;

    fn main() {
        let mut scores = HashMap::new();
        scores.insert(String::from("Blue"), 10);

        let team_name = String::from("Blue");
        match scores.get(&team_name) {
            Some(score) => println!("スコア: {}", score),
            None => println!("そのチームは登録されていません"),
        }

        match scores.get("Red") {
            Some(score) => println!("スコア: {}", score),
            None => println!("そのチームは登録されていません"), // こちらが実行される
        }
    }

キーがすでに存在するかどうかを調べたり、値を削除したりするには ``contains_key`` や ``remove`` を使います。

.. code-block:: rust

    use std::collections::HashMap;

    fn main() {
        let mut scores = HashMap::new();
        scores.insert(String::from("Blue"), 10);

        println!("{}", scores.contains_key("Blue")); // true

        scores.remove("Blue");
        println!("{}", scores.contains_key("Blue")); // false
    }

「キーが存在すれば既存の値を、無ければ指定した値を挿入してから返す」という処理は、``entry`` メソッドと ``or_insert`` を組み合わせるとまとめて書けます。これは Python の ``dict.setdefault`` に近い働きをします。

.. code-block:: rust

    use std::collections::HashMap;

    fn main() {
        let mut word_count: HashMap<&str, i32> = HashMap::new();

        for word in "hello world hello rust".split_whitespace() {
            let count = word_count.entry(word).or_insert(0); // 無ければ0を挿入し、その値への可変参照を返す
            *count += 1;
        }

        println!("{:?}", word_count); // {"hello": 2, "world": 1, "rust": 1} (順序は不定)
    }

なお ``String`` のようにヒープデータを持つ値を ``insert`` で ``HashMap`` に渡すと、その値の所有権は ``HashMap`` に移動(ムーブ)します。挿入後に元の変数を使おうとするとコンパイルエラーになる点にも注意してください。

.. code-block:: rust

    use std::collections::HashMap;

    fn main() {
        let key = String::from("Blue");
        let value = String::from("初期値");

        let mut map = HashMap::new();
        map.insert(key, value); // key と value の所有権が map に移動する

        // println!("{}", key); // ※これはコンパイルエラーになります
    }

.. admonition:: Python 経験者向けメモ
   :class: tip

   おおまかな対応関係としては、``Vec<T>`` ≒ Python の ``list``、``HashMap<K, V>`` ≒ Python の ``dict`` と考えると理解しやすいです。ただし Python の ``list`` は異なる型の値を自由に混在させられるのに対し、``Vec<T>`` は原則として同じ型 ``T`` の値しか格納できません。

   もう1つの大きな違いは文字列の扱いです。Python の文字列は ``str`` 型1種類しかありませんが、Rust には所有権を持つ ``String`` と、借用した文字列スライス ``&str`` という2つの型があります。これは「所有権」という Rust 特有の概念が、最も日常的によく使う文字列というデータ型にも現れている例です。最初は ``String`` と ``&str`` のどちらを使うべきか迷うかもしれませんが、「保持するなら ``String``、一時的に読むだけなら ``&str``」という原則を覚えておけば、多くの場面で正しく判断できます。

まとめ
------

- ``Vec<T>`` は同じ型の値を可変長で格納するコレクションで、Python の ``list`` に近いものです
- ``Vec`` の要素には ``v[i]`` によるインデックスアクセスと、``Option`` を返す安全な ``get`` メソッドの2通りの方法でアクセスできます
- ``Vec`` には ``len``/``is_empty``/``pop``/``contains`` といった便利なメソッドも用意されています
- ``String`` は所有権を持つ文字列、``&str`` は文字列を借用したスライスであり、用途に応じて使い分けます
- 文字列の連結には所有権を消費する ``+`` 演算子と、所有権を消費せず新しい ``String`` を組み立てる ``format!`` マクロが使えます
- 文字列のスライスはバイト単位で指定するため、日本語などのマルチバイト文字を境界でない位置で切り出すと実行時にパニックします
- ``HashMap<K, V>`` はキーと値の組を格納するコレクションで、Python の ``dict`` に近いものです
- ``HashMap`` の ``get`` は ``Option<&V>`` を返すため、キーが存在しない場合も安全に処理でき、``contains_key``/``remove`` でキーの有無の確認や削除もできます
- ``entry``/``or_insert`` を使うと、キーが無ければ値を挿入し、あれば既存の値を返す処理をまとめて書けます(Python の ``dict.setdefault`` に近い)
