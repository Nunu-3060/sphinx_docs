"""本文で使う図を生成する.

Sphinx のビルド開始時に conf.py から main() が呼び出される。
examples フォルダのモジュールを使うため、単独で実行する場合は
環境変数 PYTHONPATH に examples フォルダを追加すること。
"""

from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

import bgm_example
import envelope
import sequencer
import sound_effects
import waveforms
from wav_io import SAMPLE_RATE, Signal

OUT_DIR = Path(__file__).resolve().parent.parent / "images"

plt.switch_backend("Agg")  # 画面に表示せず、ファイルにだけ描画する
plt.rcParams["font.family"] = ["Meiryo", "Yu Gothic", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]


def save(fig: Figure, name: str) -> None:
    """図を PNG で保存して閉じる."""
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"{name}.png", dpi=110)
    plt.close(fig)


def time_axis(num_samples: int) -> Signal:
    """サンプル番号を時刻 [ミリ秒] に変換する."""
    return np.arange(num_samples) / SAMPLE_RATE * 1000.0


def fig_waveforms() -> None:
    """4 種類の基本波形."""
    freq = 440.0
    n = int(SAMPLE_RATE * 2 / freq)  # 2 周期分
    phase = waveforms.phase_from_frequency(freq, n)
    items: list[tuple[str, Signal]] = [
        ("正弦波", waveforms.sine_wave(phase)),
        ("矩形波（デューティ比 50 %）", waveforms.pulse_wave(phase, 0.5)),
        ("三角波（4 bit）", waveforms.triangle_wave(phase)),
        ("ノイズ", waveforms.noise_wave(n / SAMPLE_RATE, 8)),
    ]
    fig, axes = plt.subplots(4, 1, figsize=(7, 7), sharex=True)
    for ax, (title, signal), color in zip(axes, items, COLORS):
        ax.plot(time_axis(n), signal, color=color, drawstyle="steps-post")
        ax.set_title(title)
        ax.set_ylim(-1.3, 1.3)
        ax.set_ylabel("振幅")
    axes[-1].set_xlabel("時間 [ms]（440 Hz の 2 周期分）")
    save(fig, "waveforms")


def fig_sound_wave() -> None:
    """周波数と振幅の違い."""
    t = np.linspace(0.0, 0.01, 1000)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
    axes[0].plot(t * 1000, np.sin(2 * np.pi * 200 * t), label="200 Hz")
    axes[0].plot(t * 1000, np.sin(2 * np.pi * 400 * t), label="400 Hz", color=COLORS[1])
    axes[0].set_title("周波数の違い（音の高さ）")
    axes[1].plot(t * 1000, np.sin(2 * np.pi * 200 * t), label="振幅 1.0")
    axes[1].plot(t * 1000, 0.4 * np.sin(2 * np.pi * 200 * t), label="振幅 0.4", color=COLORS[1])
    axes[1].set_title("振幅の違い（音の大きさ）")
    for ax in axes:
        ax.set_xlabel("時間 [ms]")
        ax.legend(loc="upper right", fontsize=8)
    axes[0].set_ylabel("振幅")
    save(fig, "sound_wave")


def fig_harmonics() -> None:
    """奇数倍音を足していくと矩形波に近づく様子."""
    t = np.linspace(0.0, 2.0, 2000)  # 2 周期
    fig, ax = plt.subplots(figsize=(7, 3.2))
    for count, color in zip((1, 3, 10), COLORS):
        signal = np.zeros_like(t)
        for k in range(count):
            n = 2 * k + 1
            signal += 4.0 / np.pi * np.sin(2 * np.pi * n * t) / n
        ax.plot(t, signal, color=color, label=f"第 {2 * count - 1} 倍音まで")
    ax.plot(t, np.where(np.mod(t, 1.0) < 0.5, 1.0, -1.0), color="black", linestyle="--", label="矩形波")
    ax.set_xlabel("時間 [周期]")
    ax.set_ylabel("振幅")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "harmonics")


def fig_sampling() -> None:
    """標本化（サンプリング）と量子化."""
    t = np.linspace(0.0, 1.0, 1000)
    ts = np.linspace(0.0, 1.0, 17)
    analog = np.sin(2 * np.pi * t)
    sampled = np.sin(2 * np.pi * ts)
    levels = 8  # 3 bit
    quantized = np.round((sampled + 1.0) / 2.0 * (levels - 1)) / (levels - 1) * 2.0 - 1.0
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.3), sharey=True)
    axes[0].plot(t, analog, color="gray", label="元の波")
    axes[0].stem(ts, sampled, linefmt="C0-", markerfmt="C0o", basefmt=" ", label="標本")
    axes[0].set_title("標本化: 一定間隔で値を取り出す")
    axes[1].plot(t, analog, color="gray", label="元の波")
    axes[1].step(ts, quantized, where="post", color=COLORS[1], label="量子化後（3 bit = 8 段階）")
    axes[1].plot(ts, quantized, "o", color=COLORS[1])
    for level in np.linspace(-1.0, 1.0, levels):
        axes[1].axhline(level, color="gray", linewidth=0.5, linestyle=":")
    axes[1].set_title("量子化: 値を決められた段階に丸める")
    for ax in axes:
        ax.set_xlabel("時間 [周期]")
        ax.legend(loc="lower left", fontsize=8)
    axes[0].set_ylabel("振幅")
    save(fig, "sampling")


def fig_aliasing() -> None:
    """エイリアシング: 9 Hz の波を 10 Hz で標本化すると 1 Hz に見える."""
    t = np.linspace(0.0, 1.0, 2000)
    ts = np.arange(0.0, 1.0001, 0.1)
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t, np.sin(2 * np.pi * 9 * t), color="gray", label="元の波（9 Hz）")
    ax.plot(t, -np.sin(2 * np.pi * 1 * t), color=COLORS[1], linestyle="--", label="標本から見える波（1 Hz）")
    ax.plot(ts, np.sin(2 * np.pi * 9 * ts), "o", color=COLORS[0], label="標本（10 Hz で標本化）")
    ax.set_xlabel("時間 [秒]")
    ax.set_ylabel("振幅")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "aliasing")


def spectrum(signal: Signal) -> tuple[Signal, Signal]:
    """振幅スペクトルを dB で返す（最大値を 0 dB とする）."""
    windowed = signal * np.hanning(signal.size)
    magnitude = np.abs(np.fft.rfft(windowed))
    freqs = np.fft.rfftfreq(signal.size, 1.0 / SAMPLE_RATE)
    db = 20.0 * np.log10(magnitude / magnitude.max() + 1e-9)
    return freqs, db


def fig_spectra() -> None:
    """各波形のスペクトル（倍音の構成）."""
    freq = 440.0
    n = SAMPLE_RATE // 2
    phase = waveforms.phase_from_frequency(freq, n)
    items: list[tuple[str, Signal]] = [
        ("正弦波", waveforms.sine_wave(phase)),
        ("矩形波（50 %）", waveforms.pulse_wave(phase, 0.5)),
        ("パルス波（25 %）", waveforms.pulse_wave(phase, 0.25)),
        ("三角波（4 bit）", waveforms.triangle_wave(phase)),
    ]
    fig, axes = plt.subplots(4, 1, figsize=(7, 8), sharex=True)
    for ax, (title, signal), color in zip(axes, items, COLORS):
        freqs, db = spectrum(signal)
        ax.plot(freqs, db, color=color, linewidth=0.8)
        ax.set_title(title)
        ax.set_ylim(-80, 5)
        ax.set_xlim(0, 6000)
        ax.set_ylabel("レベル [dB]")
        for k in range(1, 14):
            ax.axvline(freq * k, color="gray", linewidth=0.4, linestyle=":")
    axes[-1].set_xlabel("周波数 [Hz]（点線は 440 Hz の整数倍）")
    save(fig, "spectra")


def fig_duty() -> None:
    """デューティ比の比較."""
    n = int(SAMPLE_RATE * 2 / 440.0)
    phase = waveforms.phase_from_frequency(440.0, n)
    fig, axes = plt.subplots(4, 1, figsize=(7, 5.5), sharex=True)
    for ax, duty, color in zip(axes, (0.125, 0.25, 0.5, 0.75), COLORS):
        ax.plot(time_axis(n), waveforms.pulse_wave(phase, duty), color=color, drawstyle="steps-post")
        ax.set_title(f"デューティ比 {duty * 100:g} %")
        ax.set_ylim(-1.3, 1.3)
        ax.set_yticks([-1, 0, 1])
    axes[-1].set_xlabel("時間 [ms]")
    save(fig, "duty")


def fig_triangle() -> None:
    """4 bit 三角波と理想的な三角波の比較."""
    t = np.linspace(0.0, 1.0, 2000, endpoint=False)
    ideal = 2.0 * np.abs(2.0 * t - 1.0) - 1.0
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t, ideal, color="gray", linestyle="--", label="理想的な三角波")
    ax.plot(t, waveforms.triangle_wave(t), color=COLORS[0], label="4 bit 三角波（32 段の階段）")
    ax.set_xlabel("時間 [周期]")
    ax.set_ylabel("振幅")
    ax.legend(loc="lower right", fontsize=8)
    save(fig, "triangle")


def fig_keyboard() -> None:
    """鍵盤と音名・周波数の対応（C4 から C5）."""
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.grid(False)
    whites = ["C", "D", "E", "F", "G", "A", "B", "C"]
    for i, name in enumerate(whites):
        octave = 4 if i < 7 else 5
        note = waveforms.note_number(f"{name}{octave}")
        ax.add_patch(Rectangle((i, 0), 1, 3, facecolor="white", edgecolor="black"))
        label = f"{name}{octave}\n{note}\n{waveforms.note_frequency(note):.1f} Hz"
        ax.text(i + 0.5, 0.15, label, ha="center", va="bottom", fontsize=8)
    for i, name in ((0, "C#4"), (1, "D#4"), (3, "F#4"), (4, "G#4"), (5, "A#4")):
        note = waveforms.note_number(name)
        ax.add_patch(Rectangle((i + 0.65, 1.2), 0.7, 1.8, facecolor="black"))
        label = f"{name}\n{note}\n{waveforms.note_frequency(note):.0f}"
        ax.text(i + 1.0, 1.3, label, ha="center", va="bottom", fontsize=7, color="white")
    ax.set_xlim(-0.1, 8.1)
    ax.set_ylim(-0.1, 3.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("鍵盤と音名・MIDI ノート番号・周波数")
    save(fig, "keyboard")


def fig_pulse_timer_error() -> None:
    """矩形波チャンネルのタイマー値による音程のずれ."""
    notes = np.arange(waveforms.note_number("A1"), waveforms.note_number("C8") + 1)
    cents = []
    for note in notes:
        ideal = waveforms.note_frequency(int(note))
        actual = waveforms.pulse_timer_frequency(ideal)
        cents.append(1200.0 * np.log2(actual / ideal))
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(notes, cents, "o-", markersize=3)
    ax.axhline(0.0, color="black", linewidth=0.8)
    ticks = [waveforms.note_number(f"C{octave}") for octave in range(2, 9)]
    ax.set_xticks(ticks, [f"C{octave}" for octave in range(2, 9)])
    ax.set_xlabel("音名")
    ax.set_ylabel("ずれ [セント]")
    ax.set_title("矩形波チャンネルで出せる周波数と 12 平均律とのずれ")
    save(fig, "pulse_timer_error")


def fig_click() -> None:
    """音の途中で切るとクリック音の原因になる."""
    n = int(SAMPLE_RATE * 0.012)
    phase = waveforms.phase_from_frequency(440.0, n)
    raw = waveforms.sine_wave(phase)
    cut = raw.copy()
    cut[int(n * 0.55):] = 0.0
    faded = raw.copy()
    end = int(n * 0.55)
    fade = int(SAMPLE_RATE * 0.004)
    faded[end - fade:end] *= np.linspace(1.0, 0.0, fade)
    faded[end:] = 0.0
    fig, axes = plt.subplots(1, 2, figsize=(9, 3), sharey=True)
    axes[0].plot(time_axis(n), cut, color=COLORS[1])
    axes[0].set_title("途中で急に 0 にした場合")
    axes[1].plot(time_axis(n), faded, color=COLORS[0])
    axes[1].set_title("短いフェードアウトを入れた場合")
    for ax in axes:
        ax.set_xlabel("時間 [ms]")
    axes[0].set_ylabel("振幅")
    save(fig, "click")


def fig_adsr() -> None:
    """ADSR エンベロープ."""
    env = envelope.adsr(0.05, 0.15, 0.6, 0.3, 0.25)
    t = np.arange(env.size) / SAMPLE_RATE
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(t, env, color=COLORS[0])
    for x, label in ((0.025, "A"), (0.125, "D"), (0.35, "S"), (0.625, "R")):
        ax.text(x, 1.05, label, ha="center", fontsize=12)
    for x in (0.05, 0.2, 0.5):
        ax.axvline(x, color="gray", linestyle=":")
    ax.annotate("鍵盤を離す", xy=(0.5, 0.6), xytext=(0.55, 0.85), arrowprops={"arrowstyle": "->"})
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("時間 [秒]")
    ax.set_ylabel("音量")
    save(fig, "adsr")


def fig_nes_decay() -> None:
    """ファミコン風の 16 段階の減衰エンベロープ."""
    fig, ax = plt.subplots(figsize=(7, 3))
    for period, color in zip((2, 8), COLORS):
        env = envelope.nes_decay(0.8, period)
        t = np.arange(env.size) / SAMPLE_RATE
        ax.plot(t, env * 15, color=color, label=f"period = {period}")
    ax.set_xlabel("時間 [秒]")
    ax.set_ylabel("音量（0 から 15）")
    ax.set_yticks(range(0, 16, 3))
    ax.legend(loc="upper right")
    save(fig, "nes_decay")


def fig_pitch_effects() -> None:
    """ピッチスイープ、ビブラート、アルペジオの周波数変化."""
    items: list[tuple[str, Signal]] = [
        ("ピッチスイープ（200 Hz から 1600 Hz）", envelope.exponential_sweep(200.0, 1600.0, 0.4)),
        ("ビブラート（C5、幅 0.3 半音、6 回/秒）", envelope.vibrato(523.25, 1.0, 0.3, 6.0, 0.3)),
        ("アルペジオ（C5 の長三和音、1/60 秒ごと）", envelope.arpeggio(72, [0, 4, 7], 0.2)),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(7, 7))
    for ax, (title, freq), color in zip(axes, items, COLORS):
        t = np.arange(freq.size) / SAMPLE_RATE
        ax.plot(t, freq, color=color)
        ax.set_title(title)
        ax.set_ylabel("周波数 [Hz]")
    axes[-1].set_xlabel("時間 [秒]")
    save(fig, "pitch_effects")


def fig_sfx_spectrograms() -> None:
    """効果音のスペクトログラム."""
    items: list[tuple[str, Callable[[], Signal]]] = [
        ("ジャンプ", sound_effects.jump),
        ("アイテム取得", sound_effects.coin),
        ("レーザー", sound_effects.laser),
        ("爆発", sound_effects.explosion),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(9, 6))
    for ax, (title, func) in zip(axes.flat, items):
        ax.grid(False)
        signal = func()
        with np.errstate(divide="ignore"):  # 無音部分の log10(0) の警告を抑える
            ax.specgram(signal, NFFT=512, Fs=SAMPLE_RATE, noverlap=384, cmap="magma", vmin=-120)
        ax.set_ylim(0, 6000)
        ax.set_title(title)
        ax.set_xlabel("時間 [秒]")
        ax.set_ylabel("周波数 [Hz]")
    save(fig, "sfx_spectrograms")


def fig_pianoroll() -> None:
    """BGM 作例のピアノロール."""
    song = bgm_example.build_song()
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True, gridspec_kw={"height_ratios": [4, 1]})
    for track, color in zip(song.tracks[:3], COLORS):
        events, _ = sequencer.parse(track.score)
        for i, event in enumerate(events):
            note = waveforms.note_number(event.value)
            axes[0].add_patch(Rectangle((event.start, note - 0.4), event.length - 0.15, 0.8,
                                        facecolor=color, label=track.name if i == 0 else None))
    axes[0].set_ylim(waveforms.note_number("E2") - 2, waveforms.note_number("A5") + 2)
    ticks = [waveforms.note_number(f"C{octave}") for octave in range(3, 6)]
    axes[0].set_yticks(ticks, [f"C{octave}" for octave in range(3, 6)])
    axes[0].set_ylabel("音の高さ")
    axes[0].legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=8, ncols=3, frameon=False)
    events, total = sequencer.parse(song.tracks[3].score)
    rows = {"K": 0, "S": 1, "H": 2}
    for event in events:
        axes[1].plot(event.start, rows[event.value], "s", color=COLORS[3])
    axes[1].set_yticks([0, 1, 2], ["K", "S", "H"])
    axes[1].set_ylim(-0.6, 2.6)
    axes[1].set_ylabel("noise")
    axes[1].set_xlim(0, total)
    axes[1].set_xticks(range(0, total + 1, 16), [str(bar + 1) for bar in range(total // 16 + 1)])
    axes[1].set_xlabel("小節")
    for ax in axes:
        for x in range(0, total + 1, 16):
            ax.axvline(x, color="gray", linewidth=0.6)
    save(fig, "pianoroll")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    figures: list[Callable[[], None]] = [
        fig_waveforms, fig_sound_wave, fig_harmonics, fig_sampling, fig_aliasing, fig_spectra, fig_duty,
        fig_triangle, fig_keyboard, fig_pulse_timer_error, fig_click, fig_adsr, fig_nes_decay,
        fig_pitch_effects, fig_sfx_spectrograms, fig_pianoroll,
    ]
    for figure in figures:
        figure()
        print(f"generated: {figure.__name__}")


if __name__ == "__main__":
    main()
