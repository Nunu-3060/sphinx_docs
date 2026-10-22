"""第 9 章「データの扱い方」の悪い例。"""

visit_count = 0


def visit() -> None:
    global visit_count
    visit_count += 1


def add_tag(tag: str, tags: list[str] = []) -> list[str]:
    tags.append(tag)
    return tags


def describe_book(book: tuple[str, int, bool]) -> str:
    if book[2]:
        return book[0] + "（" + str(book[1]) + "円）は貸し出しできる"
    return book[0] + "（" + str(book[1]) + "円）は貸し出し中である"


def status_message(status: str) -> str:
    if status == "shipped":
        return "発送済み"
    if status == "delivered":
        return "配達済み"
    return "不明な状態"


if __name__ == "__main__":
    visit()
    visit()
    print(visit_count)
    print(add_tag("Python"))
    print(add_tag("入門"))
    print(describe_book(("Python 入門", 2000, True)))
    print(status_message("shiped"))
