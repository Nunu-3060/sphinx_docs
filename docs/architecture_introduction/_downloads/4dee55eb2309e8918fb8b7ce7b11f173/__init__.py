"""循環 import を解消したパッケージの例.

依存の向きを customers ← orders ← reports の一方向にそろえました。
パッケージの利用者向けに、公開する名前をここで import し、__all__ に
列挙します。

実行方法（examples フォルダーで実行します）::

    python -m ch09_circular_good.main
"""

from .customers import Customer
from .orders import Order
from .reports import total_spent

__all__ = ["Customer", "Order", "total_spent"]
