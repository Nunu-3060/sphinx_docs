// 非同期処理の例
// async.html をブラウザで開き、開発者ツールのコンソールで結果を確認する。

// ===== イベントループ: 実行順序の確認 =====
console.log("1: 同期処理");
setTimeout(() => console.log("4: setTimeout (待ち時間 0 ms)"), 0);
Promise.resolve().then(() => console.log("3: Promise の then"));
console.log("2: 同期処理");
// 出力順は 1 → 2 → 3 → 4 になる。
// 同期処理がすべて終わってから、Promise のコールバック、setTimeout のコールバックの順に実行される。

// ===== Promise を返す関数 =====
// 指定したミリ秒後に解決される Promise を返す (Python の asyncio.sleep に相当)
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// 名前に応じた点数を 300 ms 後に返す処理 (サーバーへの問い合わせを模したもの)
// 名前が空のときは失敗する
function fetchScore(name) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (name === "") {
        reject(new Error("名前が空です"));
      } else {
        resolve({ name, score: name.length * 10 });
      }
    }, 300);
  });
}

// ===== then / catch による書き方 =====
fetchScore("Alice")
  .then((data) => console.log("then:", data))
  .catch((error) => console.log("catch:", error.message));

// ===== async / await による書き方 =====
async function main() {
  await sleep(1000);
  console.log("----- 1 秒待った -----");

  // await は Promise の完了を待ち、結果を取り出す
  const data = await fetchScore("Bob");
  console.log("await:", data);

  // 失敗した Promise は try...catch で受け取る
  try {
    await fetchScore("");
  } catch (error) {
    console.log("try...catch:", error.message);
  }

  // Promise.all: 複数の処理を並行して実行し、すべての完了を待つ
  // (Python の asyncio.gather に相当)
  const start = performance.now();
  const results = await Promise.all([
    fetchScore("Carol"),
    fetchScore("Dave"),
    fetchScore("Eve"),
  ]);
  const elapsed = Math.round(performance.now() - start);
  console.log("Promise.all:", results);
  console.log(`3 件で約 ${elapsed} ms (順番に待つと約 900 ms かかる)`);
}

main();
