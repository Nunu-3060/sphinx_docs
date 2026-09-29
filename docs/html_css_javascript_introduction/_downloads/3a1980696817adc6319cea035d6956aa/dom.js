// ===== 要素の取得 =====
// querySelector は CSS セレクターに一致する最初の要素を返す (無ければ null)
const title = document.querySelector("#title");
const list = document.querySelector("#fruit-list");
const link = document.querySelector("#link");

// querySelectorAll は一致するすべての要素を NodeList で返す
const fruits = document.querySelectorAll(".fruit");
console.log(`果物の数: ${fruits.length}`);

// ===== 内容・属性・スタイルの変更 =====
title.textContent = "DOM 操作の例 (JavaScript で書き換え済み)";
link.setAttribute("href", "https://developer.mozilla.org/ja/");
link.textContent = "MDN Web Docs へのリンク (href を書き換え済み)";
title.style.color = "steelblue"; // CSS の color プロパティ

// ===== 要素の作成と追加 =====
const newFruits = ["みかん", "ぶどう", "もも", "メロン"];
let nextIndex = 0;

document.querySelector("#add-button").addEventListener("click", () => {
  const name = newFruits[nextIndex % newFruits.length];
  nextIndex += 1;

  const item = document.createElement("li");
  item.className = "fruit";
  item.textContent = name;
  list.append(item);
});

// ===== クラスの切り替え =====
document.querySelector("#toggle-button").addEventListener("click", () => {
  // querySelectorAll の結果はその時点のもの。追加された要素も含めるため再取得する
  for (const item of list.querySelectorAll(".fruit")) {
    item.classList.toggle("highlight");
  }
});

// ===== 要素の削除 =====
document.querySelector("#remove-button").addEventListener("click", () => {
  const lastItem = list.lastElementChild;
  if (lastItem !== null) {
    lastItem.remove();
  }
});
