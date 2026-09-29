// JavaScript の基本文法
// js_basics.html をブラウザで開き、開発者ツールのコンソールで結果を確認する。

console.log("===== 変数宣言 =====");
const PI = 3.14159; // 再代入できない
let count = 0; // 再代入できる
count += 1;
console.log(PI, count);

console.log("===== データ型 =====");
console.log(typeof 42); // "number" (整数と小数の区別はない)
console.log(typeof "text"); // "string"
console.log(typeof true); // "boolean"
console.log(typeof undefined); // "undefined"
console.log(typeof null); // "object" (歴史的な経緯による仕様)
console.log(typeof [1, 2, 3]); // "object" (配列もオブジェクト)
console.log(0.1 + 0.2); // 0.30000000000000004 (Python と同じく浮動小数点数)
console.log(7 / 2); // 3.5 (整数どうしでも小数になる)
console.log(Math.floor(7 / 2)); // 3 (Python の 7 // 2 に相当)

console.log("===== == と === =====");
console.log(1 == "1"); // true  (型を変換してから比較する)
console.log(1 === "1"); // false (型も含めて比較する)
console.log(null == undefined); // true
console.log(null === undefined); // false
console.log("5" * 2); // 10 (文字列が数値に変換される)
console.log("5" + 2); // "52" (数値が文字列に変換される)

console.log("===== 条件分岐 =====");
const score = 75;
if (score >= 80) {
  console.log("優");
} else if (score >= 60) {
  console.log("良");
} else {
  console.log("可");
}

// 三項演算子 (Python の "良" if score >= 60 else "可" に相当)
const result = score >= 60 ? "合格" : "不合格";
console.log(result);

console.log("===== ループ =====");
for (let i = 0; i < 3; i++) {
  console.log(`i = ${i}`);
}

const fruits = ["apple", "banana", "cherry"];
// for...of は値を順に取り出す (Python の for fruit in fruits に相当)
for (const fruit of fruits) {
  console.log(fruit);
}
// for...in はキー (配列では添字の文字列) を取り出す
for (const index in fruits) {
  console.log(index, typeof index); // "0" "string" ...
}

console.log("===== 関数 =====");
// 関数宣言
function add(a, b) {
  return a + b;
}

// アロー関数とデフォルト引数
const greet = (name = "ゲスト") => `こんにちは、${name} さん`;

console.log(add(2, 3)); // 5
console.log(greet()); // "こんにちは、ゲスト さん"
console.log(greet("山田")); // "こんにちは、山田 さん"
console.log(add(1)); // NaN (足りない引数は undefined になり、エラーにならない)

console.log("===== オブジェクトと JSON =====");
const user = { name: "山田", age: 30, tags: ["admin", "dev"] };
console.log(user.name, user["age"]);
user.email = "yamada@example.com"; // const でもプロパティは変更できる

// 分割代入 (Python のアンパックに近い)
const { name, age } = user;
console.log(name, age);

const json = JSON.stringify(user); // オブジェクト → JSON 文字列
console.log(json);
const parsed = JSON.parse(json); // JSON 文字列 → オブジェクト
console.log(parsed.tags[0]); // "admin"

console.log("===== スコープとクロージャ =====");
function makeCounter() {
  let value = 0; // 外から直接は参照できない
  return () => {
    value += 1;
    return value;
  };
}
const counter = makeCounter();
console.log(counter(), counter(), counter()); // 1 2 3

console.log("===== クラス =====");
class Animal {
  constructor(name) {
    this.name = name; // Python の self.name = name に相当
  }

  speak() {
    return `${this.name} が鳴いた`;
  }
}

class Dog extends Animal {
  speak() {
    return `${super.speak()}: ワン`;
  }
}
console.log(new Dog("ポチ").speak()); // "ポチ が鳴いた: ワン"

console.log("===== 例外処理 =====");
function divide(a, b) {
  if (b === 0) {
    throw new Error("0 で割ることはできない");
  }
  return a / b;
}

try {
  divide(1, 0);
} catch (error) {
  console.log(`エラー: ${error.message}`);
} finally {
  console.log("finally は必ず実行される");
}
console.log(1 / 0); // Infinity (JavaScript では例外にならない)
