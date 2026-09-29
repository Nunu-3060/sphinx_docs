################################################################
第 8 章 継承とポリモーフィズム
################################################################

この章では、既存のクラスをもとに新しいクラスを作る継承と、異なるクラスを同じように扱うためのポリモーフィズム、インターフェイスについて学びます。

継承
================================================================

ゲームには、スライムやドラゴンなど、いろいろな種類の敵が登場します。どの敵も「名前」「HP」「ダメージを受ける処理」を持ちますが、鳴き声や攻撃力は種類ごとに異なります。

このような場合、共通する部分を ``Enemy`` クラスにまとめ、種類ごとに異なる部分だけを ``Slime`` クラスや ``Dragon`` クラスに書きます。あるクラスの性質を引き継いで新しいクラスを作ることを継承と呼びます。

.. code-block:: csharp

   public class Slime : Enemy
   {
       ...
   }

クラス名の後に ``: Enemy`` と書くと、``Slime`` は ``Enemy`` を継承します。継承元の ``Enemy`` を基底クラス、継承した ``Slime`` を派生クラスと呼びます。派生クラスは、基底クラスの ``public`` なメンバーと ``protected`` なメンバーを、自分のメンバーのように使えます。

C# では、1 つのクラスが直接継承できる基底クラスは 1 つだけです。

.. note::

   第 1 章から書いてきた ``public class HelloWorld : MonoBehaviour`` も継承です。``MonoBehaviour`` を継承することで、Unity のコンポーネントとして必要な機能を引き継いでいます。

基底クラスのコンストラクターの呼び出し
----------------------------------------------------------------

派生クラスのコンストラクターでは、``: base(...)`` と書いて、基底クラスのコンストラクターを呼び出せます。

.. code-block:: csharp

   public Slime() : base("スライム", 10)
   {
   }

virtual と override
================================================================

基底クラスのメソッドに ``virtual`` を付けると、派生クラスでそのメソッドの処理を上書きできます。上書きするメソッドには ``override`` を付けます。

.. code-block:: csharp

   // Enemy クラス（基底クラス）
   public virtual string Cry()
   {
       return "……";
   }

   // Slime クラス（派生クラス）
   public override string Cry()
   {
       return "ぷるぷる";
   }

派生クラスで上書きしなかった場合は、基底クラスの処理がそのまま使われます。上書きしたメソッドの中から基底クラスの処理を呼び出したいときは、``base.Cry()`` のように書きます。

abstract
----------------------------------------------------------------

``abstract`` を付けたクラス（抽象クラス）は、``new`` でインスタンスを作れません。継承して使うことを前提にしたクラスです。

抽象クラスには、``abstract`` を付けたメソッドやプロパティを定義できます。これらは中身を持たず、派生クラスで必ず ``override`` して中身を定義しなければなりません。「すべての敵は攻撃力を持つが、その値は種類ごとに決める」という場合は、``AttackPower`` を ``abstract`` プロパティにします。

ポリモーフィズム
================================================================

派生クラスのインスタンスは、基底クラスの型の変数に入れられます。``Slime`` も ``Dragon`` も ``Enemy`` の一種なので、``List<Enemy>`` にまとめて入れられます。

``Enemy`` 型の変数を通して ``Cry()`` を呼び出すと、実際のインスタンスが ``Slime`` なら ``Slime`` の ``Cry()`` が、``Dragon`` なら ``Dragon`` の ``Cry()`` が実行されます。このように、同じ呼び出し方で、実際のクラスに応じた処理が行われる性質をポリモーフィズム（多態性）と呼びます。ポリモーフィズムを使うと、敵の種類が増えても、敵を処理するコードを変更する必要がありません。

インターフェイス
================================================================

インターフェイスは、クラスが持つべきメソッドやプロパティを定めたものです。インターフェイスの名前は、``I`` で始めるのが慣例です。

.. code-block:: csharp

   public interface IDamageable
   {
       void TakeDamage(int amount);
   }

クラス名の後に ``: IDamageable`` と書くと、そのクラスは ``IDamageable`` を実装します。インターフェイスを実装したクラスは、インターフェイスで定められたメンバーをすべて定義しなければなりません。

継承との違いは、次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 項目
     - 継承（クラス）
     - インターフェイス
   * - 直接指定できる数
     - 1 つだけ
     - いくつでも
   * - 処理の中身
     - 基底クラスの処理を引き継げる
     - 原則として、処理は実装するクラスで書く
   * - 向いている場面
     - 「A は B の一種である」という関係
     - 「A は B ができる」という関係

たとえば、たるは敵ではありませんが、攻撃すると壊れます。そこで、``Barrel`` は ``Enemy`` を継承せずに ``IDamageable`` だけを実装します。こうすると、敵とたるを ``IDamageable`` 型としてまとめて扱えます。

is 演算子
----------------------------------------------------------------

``is`` 演算子を使うと、インスタンスが特定の型かどうかを調べられます。``target is Enemy enemy`` と書くと、``target`` が ``Enemy`` であれば ``true`` になり、同時に ``Enemy`` 型に変換した値が変数 ``enemy`` に入ります。

サンプルコード
================================================================

6 つのファイルを同じプロジェクトに置いて使います。``IDamageable``、``Enemy``、``Slime``、``Dragon``、``Barrel`` は ``MonoBehaviour`` を継承していないため、GameObject にアタッチするのは ``InheritanceSample`` だけです。

.. literalinclude:: ../../examples/ch08/IDamageable.cs
   :language: csharp
   :caption: IDamageable.cs

:download:`IDamageable.cs をダウンロード <../../examples/ch08/IDamageable.cs>`

.. literalinclude:: ../../examples/ch08/Enemy.cs
   :language: csharp
   :caption: Enemy.cs

:download:`Enemy.cs をダウンロード <../../examples/ch08/Enemy.cs>`

.. literalinclude:: ../../examples/ch08/Slime.cs
   :language: csharp
   :caption: Slime.cs

:download:`Slime.cs をダウンロード <../../examples/ch08/Slime.cs>`

.. literalinclude:: ../../examples/ch08/Dragon.cs
   :language: csharp
   :caption: Dragon.cs

:download:`Dragon.cs をダウンロード <../../examples/ch08/Dragon.cs>`

.. literalinclude:: ../../examples/ch08/Barrel.cs
   :language: csharp
   :caption: Barrel.cs

:download:`Barrel.cs をダウンロード <../../examples/ch08/Barrel.cs>`

.. literalinclude:: ../../examples/ch08/InheritanceSample.cs
   :language: csharp
   :caption: InheritanceSample.cs

:download:`InheritanceSample.cs をダウンロード <../../examples/ch08/InheritanceSample.cs>`

.. code-block:: text
   :caption: 実行結果

   スライム「ぷるぷる」（攻撃力: 2）
   ドラゴン「……」（攻撃力: 40）
   スライムの HP: 5, たるが壊れた: True
   スライムは敵です。

まとめ
================================================================

* 継承を使うと、基底クラスのメンバーを引き継いだ派生クラスを作れます。
* ``virtual`` を付けたメソッドは、派生クラスで ``override`` して処理を上書きできます。
* ``abstract`` を付けたクラスはインスタンスを作れず、``abstract`` なメンバーは派生クラスで必ず定義します。
* ポリモーフィズムにより、基底クラスの型で扱っても、実際のクラスに応じた処理が行われます。
* インターフェイスは、クラスが持つべきメンバーを定めます。1 つのクラスが複数のインターフェイスを実装できます。
