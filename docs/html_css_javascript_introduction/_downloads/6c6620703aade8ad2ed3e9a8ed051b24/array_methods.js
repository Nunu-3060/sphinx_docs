// 配列のメソッド
// compare_python.py に、同じ処理を Python で書いた例がある。

const numbers = [1, 2, 3, 4, 5, 6];

console.log("===== map: 各要素を変換する =====");
// Python: [n * n for n in numbers]
const squares = numbers.map((n) => n * n);
console.log(squares); // [1, 4, 9, 16, 25, 36]

console.log("===== filter: 条件に合う要素だけを残す =====");
// Python: [n for n in numbers if n % 2 == 0]
const evens = numbers.filter((n) => n % 2 === 0);
console.log(evens); // [2, 4, 6]

console.log("===== reduce: 要素を 1 つの値にまとめる =====");
// Python: sum(numbers)
const total = numbers.reduce((sum, n) => sum + n, 0);
console.log(total); // 21

console.log("===== メソッドチェーン =====");
// Python: sum(n * n for n in numbers if n % 2 == 0)
const sumOfEvenSquares = numbers
  .filter((n) => n % 2 === 0)
  .map((n) => n * n)
  .reduce((sum, n) => sum + n, 0);
console.log(sumOfEvenSquares); // 56

console.log("===== find / some / every / includes =====");
console.log(numbers.find((n) => n > 3)); // 4 (最初に条件を満たす要素)
console.log(numbers.some((n) => n > 5)); // true  (Python: any(...))
console.log(numbers.every((n) => n > 0)); // true  (Python: all(...))
console.log(numbers.includes(3)); // true  (Python: 3 in numbers)

console.log("===== 追加・削除・結合 =====");
const list = [1, 2, 3];
list.push(4); // 末尾に追加 (Python: list.append(4))
const last = list.pop(); // 末尾を取り出す (Python: list.pop())
console.log(list, last); // [1, 2, 3] 4
console.log(list.slice(1)); // [2, 3] (Python: list[1:])
console.log([...list, ...[10, 20]]); // [1, 2, 3, 10, 20] (スプレッド構文)
console.log(list.join(", ")); // "1, 2, 3" (Python: ", ".join(...))
console.log(list.length); // 3 (Python: len(list))

console.log("===== sort の注意点 =====");
// 引数なしの sort は要素を文字列として比較する
console.log([10, 9, 1, 100].sort()); // [1, 10, 100, 9]
// 数値として並べるには比較関数を渡す
console.log([10, 9, 1, 100].sort((a, b) => a - b)); // [1, 9, 10, 100]

console.log("===== オブジェクトの配列 =====");
const users = [
  { name: "山田", age: 30 },
  { name: "佐藤", age: 25 },
  { name: "鈴木", age: 35 },
];
const names = users.filter((u) => u.age >= 30).map((u) => u.name);
console.log(names); // ["山田", "鈴木"]

// Object.entries で [キー, 値] の配列に変換する (Python: dict.items())
const prices = { apple: 100, banana: 80 };
for (const [key, value] of Object.entries(prices)) {
  console.log(`${key}: ${value} 円`);
}
