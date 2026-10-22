"""第 8 章: 描画に依存しないロジックの単体テスト。

examples ディレクトリで次のように実行する。
    pytest
"""

from main import SCREEN_H, SCREEN_W, Enemy, EnemyC, Entity, overlaps


def test_overlapping_entities_collide() -> None:
    a = Entity(0, 0, 16, 16)
    b = Entity(8, 8, 16, 16)
    assert overlaps(a, b)
    assert overlaps(b, a)


def test_touching_edges_do_not_collide() -> None:
    # a の右端 (x = 16) と b の左端がちょうど接しているだけなら当たらない
    a = Entity(0, 0, 16, 16)
    b = Entity(16, 0, 16, 16)
    assert not overlaps(a, b)


def test_margin_shrinks_hitbox() -> None:
    # 画像は重なっていても、当たり判定を縮めると当たらなくなる
    a = Entity(0, 0, 16, 16, margin=5)
    b = Entity(12, 12, 16, 16, margin=2)
    assert overlaps(Entity(0, 0, 16, 16), Entity(12, 12, 16, 16))
    assert not overlaps(a, b)


def test_hitbox_is_centered() -> None:
    assert Entity(10, 20, 16, 16, margin=5).hitbox() == (15, 25, 6, 6)


def test_is_outside() -> None:
    assert not Entity(0, 0, 16, 16).is_outside()
    assert Entity(-17, 0, 16, 16).is_outside()
    assert Entity(0, SCREEN_H + 1, 16, 16).is_outside()
    assert Entity(SCREEN_W + 1, 0, 16, 16).is_outside()


def test_enemy_is_destroyed_when_hp_reaches_zero() -> None:
    enemy = Enemy(0, 0, level=0)
    assert enemy.damage()
    assert not enemy.alive


def test_tough_enemy_survives_first_hits() -> None:
    enemy = EnemyC(0, 0, level=0)
    for _ in range(EnemyC.HP - 1):
        assert not enemy.damage()
        assert enemy.alive
    assert enemy.damage()
    assert not enemy.alive
