// ===== 定数と状態 =====
const STORAGE_KEY = "todo-app-items";

// タスクの配列。各要素は { id, text, done } の形のオブジェクト
let todos = loadTodos();

const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");
const count = document.querySelector("#todo-count");
const clearDoneButton = document.querySelector("#clear-done-button");

// ===== 保存と読み込み =====
function loadTodos() {
  const json = localStorage.getItem(STORAGE_KEY);
  if (json === null) {
    return [];
  }
  try {
    return JSON.parse(json);
  } catch {
    // 保存内容が壊れている場合は空の一覧から始める
    return [];
  }
}

function saveTodos() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

// ===== 描画 =====
// 状態 (todos) から画面を作り直す。状態を変えたら必ず update を呼ぶ
function createTodoItem(todo) {
  const item = document.createElement("li");
  item.className = "todo-item";
  item.classList.toggle("done", todo.done);
  item.dataset.id = todo.id; // data-id 属性として要素に ID を持たせる

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.className = "toggle-checkbox";
  checkbox.checked = todo.done;
  checkbox.setAttribute("aria-label", "完了");

  const text = document.createElement("span");
  text.className = "todo-text";
  text.textContent = todo.text; // innerHTML は使わない (XSS 対策)

  const deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.className = "delete-button";
  deleteButton.textContent = "削除";

  item.append(checkbox, text, deleteButton);
  return item;
}

function render() {
  list.replaceChildren(...todos.map(createTodoItem));
  const remaining = todos.filter((todo) => !todo.done).length;
  count.textContent = `未完了 ${remaining} 件 / 全 ${todos.length} 件`;
}

function update() {
  saveTodos();
  render();
}

// ===== 操作 =====
function addTodo(text) {
  todos.push({ id: Date.now().toString(), text, done: false });
  update();
}

function toggleTodo(id) {
  todos = todos.map((todo) =>
    todo.id === id ? { ...todo, done: !todo.done } : todo,
  );
  update();
}

function deleteTodo(id) {
  todos = todos.filter((todo) => todo.id !== id);
  update();
}

function clearDone() {
  todos = todos.filter((todo) => !todo.done);
  update();
}

// ===== イベントの登録 =====
form.addEventListener("submit", (event) => {
  event.preventDefault(); // ページ遷移を止める
  const text = input.value.trim();
  if (text === "") {
    return;
  }
  addTodo(text);
  input.value = "";
  input.focus();
});

// 各 li にリスナーを付ける代わりに、親の ul でまとめて受け取る (イベント委譲)
list.addEventListener("click", (event) => {
  const item = event.target.closest(".todo-item");
  if (item === null) {
    return;
  }
  const id = item.dataset.id;

  if (event.target.classList.contains("toggle-checkbox")) {
    toggleTodo(id);
  } else if (event.target.classList.contains("delete-button")) {
    deleteTodo(id);
  }
});

clearDoneButton.addEventListener("click", clearDone);

// ===== 初期表示 =====
render();
