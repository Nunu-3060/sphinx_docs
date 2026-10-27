extends Node
## 配列と辞書の例。


func _ready() -> void:
	print("--- 配列と辞書 ---")
	var items: Array[String] = ["剣", "盾"]  # 要素の型を指定した配列
	items.append("薬草")
	print("持ち物: ", items, "（", items.size(), " 個）")
	print("先頭: ", items[0], "、末尾: ", items[-1])

	var prices: Dictionary[String, int] = {"剣": 100, "盾": 80}  # キーと値の型を指定した辞書
	prices["薬草"] = 10
	for item: String in prices:
		print(item, " は ", prices[item], " G")
	print("鎧の値段: ", prices.get("鎧", -1))

	# 配列や辞書は参照で扱われる。代入しても複製されない。
	var copied := items
	copied.append("鍵")
	print("元の配列も変わる: ", items)
	# 複製が必要なときは duplicate() を使う。
	var cloned := items.duplicate()
	cloned.clear()
	print("duplicate() した配列を消しても元は残る: ", items)
