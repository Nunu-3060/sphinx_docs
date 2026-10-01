"""ヘキサゴナルアーキテクチャで構成した ToDo アプリの例.

中心にドメイン（domain）とアプリケーション（service）を置き、外部との
やり取りはポート（ports）を通して行います。アダプター（adapters）は
ポートに依存しますが、中心の側はアダプターを知りません。

実行方法（examples フォルダーで実行します）::

    python -m ch11_hexagonal.main
"""
