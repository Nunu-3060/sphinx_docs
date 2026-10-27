"""本文で使う図(PNG、GIF)を生成するスクリプト。

SPH や格子ボルツマン法の計算には数分かかるため、図はビルド時ではなく
このスクリプトで事前に生成し、source/images/ に保存しておく。
計算には examples/ のサンプルコードをそのまま使う。

実行方法(プロジェクトのルートで実行する)::

    python source/_scripts/generate_figures.py            # すべての図を生成する
    python source/_scripts/generate_figures.py sph lbm    # 指定した章の図だけを生成する
"""
import sys
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402
from matplotlib.artist import Artist  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle  # noqa: E402
from PIL import Image, ImageSequence  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "source" / "images"
sys.path.insert(0, str(ROOT / "examples"))

import advection_1d  # noqa: E402
import cavity_flow  # noqa: E402
import collision  # noqa: E402
import diffusion_1d  # noqa: E402
import integrators  # noqa: E402
import lbm_karman  # noqa: E402
import neighbor_search  # noqa: E402
import particle_system  # noqa: E402
import projectile  # noqa: E402
import sph_dam_break  # noqa: E402
import spring_mass  # noqa: E402
import stable_fluids  # noqa: E402

plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
plt.rcParams["figure.dpi"] = 100
plt.rcParams["savefig.dpi"] = 100
plt.rcParams["axes.unicode_minus"] = False


def shrink_gif(name: str, colors: int = 48, every: int = 1) -> None:
    """GIF の色数を減らし(every > 1 ならフレームも間引き)、ファイルサイズを小さくする。"""
    path = OUT / name
    with Image.open(path) as im:
        duration = im.info.get("duration", 66) * every
        frames = []
        for k, frame in enumerate(ImageSequence.Iterator(im)):
            if k % every == 0:
                frames.append(frame.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=duration, loop=0, optimize=True)
    print(f"  {name} ({path.stat().st_size // 1024} KB)")


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print(f"  {name}")


# ---------------------------------------------------------------- 第 2 章
def fig_integrators() -> None:
    dt, n_steps = 0.1, 300
    t = np.arange(n_steps + 1) * dt
    fig, (ax_x, ax_e) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    ax_x.plot(t, np.cos(t), "k--", label="厳密解")
    for name, stepper in integrators.METHODS.items():
        xs, vs = integrators.simulate(stepper, 1.0, 0.0, dt, n_steps)
        ax_x.plot(t, xs, label=name)
        ax_e.plot(t, integrators.energy(xs, vs), label=name)
        print(f"    {name}: E(t=30) = {integrators.energy(xs, vs)[-1]:.4f}")
    ax_x.set_ylabel("位置 x")
    ax_x.set_ylim(-3.5, 3.5)
    ax_x.legend(loc="upper left", ncol=4)
    ax_e.axhline(0.5, color="k", ls="--", lw=1)
    ax_e.set_xlabel("時刻 t")
    ax_e.set_ylabel("エネルギー E")
    ax_e.set_ylim(0.0, 2.0)
    save(fig, "integrators.png")

    # 時間刻み幅と誤差の関係(収束次数)
    dts = np.array([0.2, 0.1, 0.05, 0.025, 0.0125])
    fig, ax = plt.subplots(figsize=(6, 4))
    for name, stepper in integrators.METHODS.items():
        errors = []
        for dt_i in dts:
            n = round(10.0 / dt_i)
            xs, _ = integrators.simulate(stepper, 1.0, 0.0, float(dt_i), n)
            errors.append(abs(xs[-1] - np.cos(10.0)))
        ax.loglog(dts, errors, "o-", label=name)
        print(f"    {name}: errors = {[f'{e:.2e}' for e in errors]}")
    ax.loglog(dts, 0.5 * dts, "k:", lw=1, label="傾き 1")
    ax.loglog(dts, 0.05 * dts**2, "k--", lw=1, label="傾き 2")
    ax.set_xlabel("時間刻み幅 Δt")
    ax.set_ylabel("t = 10 における位置の誤差")
    ax.legend()
    save(fig, "integrators_order.png")


# ---------------------------------------------------------------- 第 3 章
def fig_particles() -> None:
    pos0 = np.array([0.0, 0.0])
    vel0 = np.array([10.0, 10.0])
    dt, t_end = 0.01, 2.0
    t = np.linspace(0.0, t_end, round(t_end / dt) + 1)
    fig, (ax_fly, ax_bounce) = plt.subplots(1, 2, figsize=(11, 4))
    for drag in (0.0, 0.5, 1.0):
        traj = projectile.simulate_flight(pos0, vel0, drag, dt, t_end)
        ax_fly.plot(traj[:, 0], traj[:, 1], label=f"b = {drag}")
        if drag > 0.0:
            exact = projectile.analytic_flight(pos0, vel0, drag, t)
            ax_fly.plot(exact[:, 0], exact[:, 1], "k--", lw=1)
            print(f"    b = {drag}: max error = {np.abs(traj - exact).max():.4f} m")
    ax_fly.set_xlabel("x [m]")
    ax_fly.set_ylabel("y [m]")
    ax_fly.set_ylim(0.0, 6.0)
    ax_fly.legend()
    ax_fly.set_title("空気抵抗の有無による軌道の違い(破線は厳密解)")
    heights = projectile.simulate_bounce(height=2.0, restitution=0.8, dt=0.001, t_end=4.0)
    ax_bounce.plot(np.linspace(0.0, 4.0, heights.size), heights)
    ax_bounce.set_xlabel("時刻 t [s]")
    ax_bounce.set_ylabel("高さ y [m]")
    ax_bounce.set_title("床で跳ね返るボール(反発係数 0.8)")
    save(fig, "projectile.png")

    rng = np.random.default_rng(1)
    p = particle_system.create_particles(3000)
    for _ in range(240):
        particle_system.emit(p, 15, rng)
        particle_system.update(p, 1.0 / 60.0)
    fig, ax = plt.subplots(figsize=(6, 4))
    alive = p.alive
    sc = ax.scatter(p.pos[alive, 0], p.pos[alive, 1], s=3, c=p.age[alive], cmap="viridis_r", vmin=0.0, vmax=3.0)
    fig.colorbar(sc, ax=ax, label="発生してからの時間 [s]")
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(0.0, 4.0)
    ax.set_aspect("equal")
    ax.set_title("パーティクルシステムによる噴水")
    save(fig, "fountain.png")

    for n in (1_000, 10_000, 100_000):
        t_loop, t_numpy = particle_system.benchmark(n)
        print(f"    N = {n}: loop {t_loop * 1e3:.3f} ms, numpy {t_numpy * 1e3:.3f} ms, ratio {t_loop / t_numpy:.0f}")


# ---------------------------------------------------------------- 第 4 章
def fig_interactions() -> None:
    rope = spring_mass.Rope()
    print(f"    critical dt = {spring_mass.critical_time_step(rope) * 1e3:.3f} ms")
    frames = spring_mass.simulate(rope, dt=0.0005, t_end=1.2, n_frames=13)
    fig, ax = plt.subplots(figsize=(6, 5))
    cmap = plt.get_cmap("viridis")
    for k, fr in enumerate(frames):
        ax.plot(fr[:, 0], fr[:, 1], "o-", ms=3, lw=1, color=cmap(k / (len(frames) - 1)))
    ax.set_aspect("equal")
    ax.set_title("ロープの形の変化(0.1 s ごと、紫 → 黄)")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    save(fig, "rope.png")
    for dt in (0.004, 0.0045, 0.005):
        fr = spring_mass.simulate(rope, dt=dt, t_end=3.0, n_frames=31)
        print(f"    dt = {dt}: diverged = {bool(np.isnan(fr).any())}")

    model = collision.ContactModel()
    print(f"    contact time = {model.contact_time * 1e3:.3f} ms, damping = {model.damping:.4f}")
    for e in (0.9, 0.5, 0.1):
        m = collision.ContactModel(restitution=e)
        e20 = collision.measure_restitution(m, m.contact_time / 20.0)
        e100 = collision.measure_restitution(m, m.contact_time / 100.0)
        print(f"    e = {e}: dt=tc/20 -> {e20:.3f}, dt=tc/100 -> {e100:.3f}")

    box = 0.6
    dt = model.contact_time / 20.0
    pos, vel = collision.initial_state(12, model, box)
    fig, axs = plt.subplots(1, 4, figsize=(14, 5.4))
    times = (0.0, 0.3, 0.6, 2.0)
    t = 0.0
    for ax, t_snap in zip(axs, times):
        while t < t_snap - 0.5 * dt:
            collision.step(pos, vel, model, box, dt)
            t += dt
        for x, y in pos:
            ax.add_patch(Circle((x, y), model.radius, fc="tab:blue", ec="k", lw=0.5))
        ax.set_xlim(0.0, box)
        ax.set_ylim(0.0, 0.9)
        ax.set_aspect("equal")
        ax.set_title(f"t = {t_snap} s")
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, "collision.png")

    # セル分割法の説明図
    rng = np.random.default_rng(3)
    pts = rng.uniform(0.0, 5.0, (60, 2))
    target = np.array([2.4, 2.6])
    fig, ax = plt.subplots(figsize=(5, 5))
    for k in range(6):
        ax.axhline(k, color="gray", lw=0.8)
        ax.axvline(k, color="gray", lw=0.8)
    ax.add_patch(Rectangle((1.0, 1.0), 3.0, 3.0, fc="tab:orange", alpha=0.2))
    ax.add_patch(Circle(tuple(target), 1.0, fill=False, ec="tab:red", lw=1.5))
    in_cells = np.all((pts >= 1.0) & (pts < 4.0), axis=1)
    close = np.linalg.norm(pts - target, axis=1) < 1.0
    ax.scatter(pts[~in_cells, 0], pts[~in_cells, 1], s=12, c="lightgray")
    ax.scatter(pts[in_cells & ~close, 0], pts[in_cells & ~close, 1], s=12, c="tab:blue", label="候補(距離を計算する)")
    ax.scatter(pts[close, 0], pts[close, 1], s=18, c="tab:red", label="近傍(距離が半径未満)")
    ax.scatter(*target, s=60, c="k", marker="*", label="注目する粒子")
    ax.set_xlim(0.0, 5.0)
    ax.set_ylim(0.0, 5.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=1, fontsize=9)
    ax.set_title("セル分割法(セルの一辺 = 探索半径)")
    save(fig, "cell_list.png")

    sizes = [250, 500, 1000, 2000, 4000]
    results = [neighbor_search.measure(n) for n in sizes]
    for n, (tb, tc) in zip(sizes, results):
        print(f"    N = {n}: brute {tb * 1e3:.2f} ms, cell {tc * 1e3:.2f} ms")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(sizes, [r[0] * 1e3 for r in results], "o-", label="総当たり法")
    ax.loglog(sizes, [r[1] * 1e3 for r in results], "s-", label="セル分割法")
    ax.set_xlabel("粒子数 N")
    ax.set_ylabel("計算時間 [ms]")
    ax.legend()
    save(fig, "neighbor_benchmark.png")


# ---------------------------------------------------------------- 第 5 章
def fig_viewpoints() -> None:
    def velocity(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # 説明用の渦状の速度場
        return -(y - 2.0) + 0.6, (x - 2.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8))
    gx, gy = np.meshgrid(np.linspace(0.25, 3.75, 8), np.linspace(0.25, 3.75, 8))
    u, v = velocity(gx, gy)
    ax1.quiver(gx, gy, u, v, color="tab:blue")
    ax1.scatter(gx, gy, s=6, c="k")
    ax1.set_title("オイラー的視点\n空間に固定した点で速度を観測する")

    pts = np.array([[1.0, 2.0], [2.0, 3.4], [3.2, 1.5], [2.6, 2.4], [1.4, 1.0], [0.6, 3.0], [3.4, 3.2], [2.0, 0.5]])
    dt = 0.01
    for p0 in pts:
        path = [p0.copy()]
        p = p0.copy()
        for _ in range(100):
            du, dv = velocity(np.array(p[0]), np.array(p[1]))
            p = p + dt * np.array([float(du), float(dv)])
            path.append(p.copy())
        arr = np.array(path)
        ax2.plot(arr[:, 0], arr[:, 1], "-", color="tab:orange")
        ax2.scatter(*arr[0], s=30, c="tab:gray")
        ax2.scatter(*arr[-1], s=40, c="tab:orange")
    ax2.set_title("ラグランジュ的視点\n流体とともに動く粒子を追跡する")
    for ax in (ax1, ax2):
        ax.set_xlim(0.0, 4.0)
        ax.set_ylim(0.0, 4.0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, "viewpoints.png")


# ---------------------------------------------------------------- 第 6 章
def fig_advection_diffusion() -> None:
    c, nx = 1.0, 200
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    x, _ = advection_1d.solve(advection_1d.upwind, nx, c, 0.5, 0.0)
    ax1.plot(x, advection_1d.exact_solution(x, 1.0, c), "k--", label="厳密解")
    for name, scheme in (("風上差分", advection_1d.upwind), ("ラックス-ヴェンドロフ法", advection_1d.lax_wendroff)):
        x, u = advection_1d.solve(scheme, nx, c, 0.5, 1.0)
        ax1.plot(x, u, label=name)
        print(f"    {name}: max {u.max():.3f}, min {u.min():.3f}")
    ax1.set_title("t = 1(1 周後)、クーラン数 0.5")
    ax1.set_xlabel("x")
    ax1.set_ylabel("u")
    ax1.legend(fontsize=9)
    t_end = 0.05
    ax2.plot(x, advection_1d.exact_solution(x, t_end, c), "k--", label="厳密解")
    x, u = advection_1d.solve(advection_1d.ftcs, nx, c, 0.5, t_end)
    ax2.plot(x, u, label="FTCS 法(クーラン数 0.5)")
    x, u = advection_1d.solve(advection_1d.upwind, nx, c, 1.2, t_end)
    ax2.plot(x, u, label="風上差分(クーラン数 1.2)")
    ax2.set_ylim(-2.0, 3.0)
    ax2.set_title(f"t = {t_end}")
    ax2.set_xlabel("x")
    ax2.legend(fontsize=9)
    save(fig, "advection.png")
    x, u = advection_1d.solve(advection_1d.upwind, nx, c, 1.0, 1.0)
    print(f"    upwind CFL=1: error {np.abs(u - advection_1d.exact_solution(x, 1.0, c)).max():.2e}")

    nu, nx = 1.0, 51
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    x_fine = np.linspace(0.0, 1.0, 400)
    for t in (0.0, 0.005, 0.02, 0.05):
        ax1.plot(x_fine, diffusion_1d.exact_solution(x_fine, t, nu), "k--", lw=1)
        x, u = diffusion_1d.solve(nx, nu, 0.4, t)
        ax1.plot(x, u, "o", ms=3, label=f"t = {t}")
    ax1.set_title("拡散数 r = 0.4(破線は厳密解)")
    ax1.set_xlabel("x")
    ax1.set_ylabel("u")
    ax1.legend()
    t_end = 0.045
    ax2.plot(x_fine, diffusion_1d.exact_solution(x_fine, t_end, nu), "k--", lw=1, label="厳密解")
    for r in (0.5, 0.55):
        x, u = diffusion_1d.solve(nx, nu, r, t_end)
        ax2.plot(x, u, "o-", ms=3, label=f"r = {r}")
    ax2.set_ylim(-0.2, 1.0)
    ax2.set_title(f"t = {t_end}")
    ax2.set_xlabel("x")
    ax2.legend()
    save(fig, "diffusion.png")


# ---------------------------------------------------------------- 第 7 章
def fig_stable_fluids() -> None:
    # セミラグランジュ法の説明図
    fig, ax = plt.subplots(figsize=(5, 4.2))
    for k in range(6):
        ax.axhline(k, color="gray", lw=0.8)
        ax.axvline(k, color="gray", lw=0.8)
    gx, gy = np.meshgrid(np.arange(5) + 0.5, np.arange(5) + 0.5)
    ax.scatter(gx, gy, s=10, c="gray")
    target = np.array([3.5, 3.5])
    start = np.array([1.75, 2.2])
    ax.add_patch(FancyArrowPatch(tuple(start), tuple(target), connectionstyle="arc3,rad=-0.25",
                                 arrowstyle="-|>", mutation_scale=15, color="tab:blue", lw=1.5))
    ax.add_patch(Rectangle((1.5, 1.5), 1.0, 1.0, fc="tab:orange", alpha=0.25))
    ax.scatter([1.5, 2.5, 1.5, 2.5], [1.5, 1.5, 2.5, 2.5], s=40, c="tab:orange", zorder=3)
    ax.scatter(*start, s=60, c="tab:blue", zorder=3)
    ax.scatter(*target, s=60, c="tab:red", zorder=3)
    ax.annotate("値を求めたい\nセル中心", target, (3.8, 4.3), fontsize=9)
    ax.annotate("出発点\n(4 点から補間)", start, (0.1, 3.1), fontsize=9,
                arrowprops={"arrowstyle": "-", "color": "k", "lw": 0.8})
    ax.set_xlim(0.0, 5.0)
    ax.set_ylim(0.0, 5.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("セミラグランジュ法: 流れを逆にたどる")
    save(fig, "semi_lagrangian.png")

    prm = stable_fluids.Params()
    s = stable_fluids.create_state(prm.n)
    snaps = {50: None, 100: None, 150: None, 200: None}
    gif_frames = []
    for n in range(1, 241):
        stable_fluids.step(s, prm)
        if n in snaps:
            snaps[n] = s.density[1:-1, 1:-1].copy()
        if n % 4 == 0:
            gif_frames.append(s.density[1:-1, 1:-1].copy())
    fig, axs = plt.subplots(1, 4, figsize=(14, 3.8))
    for ax, (n, d) in zip(axs, snaps.items()):
        ax.imshow(d, origin="lower", extent=(0.0, 1.0, 0.0, 1.0), cmap="inferno", vmin=0.0, vmax=1.0)
        ax.set_title(f"t = {n * prm.dt:.1f}")
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, "stable_fluids.png")

    fig, ax = plt.subplots(figsize=(3.6, 3.6))
    image = ax.imshow(gif_frames[0], origin="lower", cmap="inferno", vmin=0.0, vmax=1.0)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()

    def animate(k: int) -> tuple[Artist]:
        image.set_data(gif_frames[k])
        return (image,)

    FuncAnimation(fig, animate, frames=len(gif_frames)).save(OUT / "stable_fluids.gif", writer=PillowWriter(fps=15))
    plt.close(fig)
    shrink_gif("stable_fluids.gif", every=2)

    # 圧力投影の反復回数と、投影後に残る発散の関係
    s = stable_fluids.create_state(prm.n)
    for _ in range(100):
        stable_fluids.step(s, prm)
    stable_fluids.add_forces_and_sources(s, prm)
    u = stable_fluids.advect(stable_fluids.X_VELOCITY, s.u, s.u, s.v, prm.dt)
    v = stable_fluids.advect(stable_fluids.Y_VELOCITY, s.v, s.u, s.v, prm.dt)

    def rms(a: np.ndarray) -> float:
        return float(np.sqrt(np.mean(a**2)))

    before = rms(stable_fluids.divergence(u, v))
    print(f"    divergence before projection: {before:.3f}")
    for it in (10, 50, 200, 1000, 5000):
        uu, vv = stable_fluids.project(u, v, it)
        print(f"    iterations {it}: {rms(stable_fluids.divergence(uu, vv)):.3f}")


# ---------------------------------------------------------------- 第 8 章
def fig_cavity() -> None:
    results = {n: cavity_flow.solve(n, 0.01, dt=0.002) for n in (21, 41, 81)}
    for n, r in results.items():
        u_c = np.interp(cavity_flow.GHIA_Y, r.y, r.u[:, n // 2])
        print(f"    {n}: steps {r.steps}, max error {np.abs(u_c - cavity_flow.GHIA_U).max():.4f}, "
              f"min u {r.u[:, n // 2].min():.4f}")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    r = results[81]
    speed = np.hypot(r.u, r.v)
    ax1.streamplot(r.x, r.y, r.u, r.v, color=speed, cmap="viridis", density=1.5)
    ax1.set_aspect("equal")
    ax1.set_xlim(0.0, 1.0)
    ax1.set_ylim(0.0, 1.0)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_title("流線(81 × 81、Re = 100)")
    for n, r in results.items():
        ax2.plot(r.u[:, n // 2], r.y, label=f"{n} × {n}")
    ax2.plot(cavity_flow.GHIA_U, cavity_flow.GHIA_Y, "ko", label="Ghia ら(1982)")
    ax2.set_xlabel("u(x = 0.5)")
    ax2.set_ylabel("y")
    ax2.set_title("中心線上の速度の比較")
    ax2.legend()
    save(fig, "cavity.png")


# ---------------------------------------------------------------- 第 9 章
def fig_sph() -> None:
    h = 1.0
    r = np.linspace(0.0, 2.0, 200)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(r, sph_dam_break.kernel(r, h), label="W(r, h)")
    ax.plot(r, sph_dam_break.kernel_derivative(r, h), label="dW/dr")
    ax.axhline(0.0, color="k", lw=0.8)
    ax.set_xlabel("r / h")
    ax.legend()
    ax.set_title("3 次スプラインカーネル(h = 1)")
    save(fig, "sph_kernel.png")

    prm = sph_dam_break.Params()
    s = sph_dam_break.create_state(prm)
    print(f"    fluid {np.count_nonzero(s.is_fluid)}, wall {np.count_nonzero(~s.is_fluid)}, "
          f"mass {s.mass:.4f}, c0 {prm.sound_speed:.2f}")
    snap_times = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4)
    snaps: dict[float, np.ndarray] = {0.0: s.pos.copy()}
    gif_frames = [s.pos[s.is_fluid].copy()]
    times = [0.0]
    fronts = [sph_dam_break.front_position(s)]
    n_total = round(1.6 / prm.dt)
    for n in range(1, n_total + 1):
        sph_dam_break.step(s, prm)
        if n % 100 == 0:
            times.append(s.time)
            fronts.append(sph_dam_break.front_position(s))
        if n % 200 == 0:
            gif_frames.append(s.pos[s.is_fluid].copy())
        for ts in snap_times:
            if n == round(ts / prm.dt):
                snaps[ts] = s.pos.copy()
    wall = s.pos[~s.is_fluid]

    fig, axs = plt.subplots(4, 2, figsize=(11, 10.5))
    for ax, ts in zip(axs.ravel(), snap_times):
        pos = snaps[ts]
        ax.scatter(wall[:, 0], wall[:, 1], s=1, c="gray")
        ax.scatter(pos[s.is_fluid, 0], pos[s.is_fluid, 1], s=2, c="tab:blue")
        ax.set_xlim(-0.1, 1.7)
        ax.set_ylim(-0.1, 1.1)
        ax.set_aspect("equal")
        ax.set_title(f"t = {ts:.1f} s")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, "sph_dam_break.png")

    fig, ax = plt.subplots(figsize=(6, 4))
    t_arr = np.array(times)
    ax.plot(t_arr, fronts, label="SPH")
    ritter = prm.water_width + 2.0 * np.sqrt(9.81 * prm.water_height) * t_arr
    ax.plot(t_arr, ritter, "k--", label="リッターの解(理想化した条件での厳密解)")
    ax.axhline(prm.tank_width, color="gray", lw=0.8)
    ax.set_xlim(0.0, 0.6)
    ax.set_ylim(0.0, 2.0)
    ax.set_xlabel("時刻 t [s]")
    ax.set_ylabel("先端の位置 [m]")
    ax.legend()
    save(fig, "sph_front.png")
    for tt, fr in zip(times, fronts):
        if abs(tt * 10 - round(tt * 10)) < 1e-6 and tt <= 0.6:
            print(f"    t = {tt:.1f}: front {fr:.3f}")

    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.scatter(wall[:, 0], wall[:, 1], s=1, c="gray")
    fluid = ax.scatter(gif_frames[0][:, 0], gif_frames[0][:, 1], s=2, c="tab:blue")
    ax.set_xlim(-0.1, 1.7)
    ax.set_ylim(-0.1, 1.1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()

    def animate(k: int) -> tuple[Artist]:
        fluid.set_offsets(gif_frames[k])
        return (fluid,)

    FuncAnimation(fig, animate, frames=len(gif_frames)).save(OUT / "sph_dam_break.gif", writer=PillowWriter(fps=15))
    plt.close(fig)
    shrink_gif("sph_dam_break.gif", every=2)


# ---------------------------------------------------------------- 第 10 章
def fig_lbm() -> None:
    fig, ax = plt.subplots(figsize=(4, 4))
    for k, (cx, cy) in enumerate(lbm_karman.C):
        if k > 0:
            ax.annotate("", (cx, cy), (0, 0), arrowprops={"arrowstyle": "-|>", "color": "tab:blue", "lw": 1.5})
        dx = 0.15 if cx >= 0 else -0.3
        dy = 0.12 if cy >= 0 else -0.25
        ax.text(cx + dx, cy + dy, str(k), fontsize=12)
    ax.scatter(lbm_karman.C[:, 0], lbm_karman.C[:, 1], s=40, c="k", zorder=3)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.grid(True)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_title("D2Q9 モデルの離散速度")
    save(fig, "d2q9.png")

    prm = lbm_karman.Params()
    print(f"    nu {prm.viscosity:.4f}, tau {prm.tau:.4f}")
    s = lbm_karman.create_state(prm)
    px, py = int(prm.nx / 5 + 6 * prm.radius), prm.ny // 2
    signal = []
    gif_frames = []

    def vort() -> np.ndarray:
        _, ux, uy = lbm_karman.macroscopic(s.f)
        om = lbm_karman.vorticity(ux, uy)
        om[s.obstacle] = np.nan
        return om

    n_total = 24000
    for n in range(1, n_total + 1):
        lbm_karman.step(s, prm)
        _, ux, uy = lbm_karman.macroscopic(s.f[:, py:py + 1, px:px + 1])
        signal.append(float(uy[0, 0]))
        if n > n_total - 6000 and n % 100 == 0:
            gif_frames.append(vort())
    sig = np.array(signal)
    st = lbm_karman.strouhal_number(sig[12000:], prm)
    print(f"    Strouhal number {st:.4f}")

    fig, ax = plt.subplots(figsize=(10, 2.9))
    ax.imshow(gif_frames[-1], origin="lower", cmap="RdBu_r", vmin=-0.02, vmax=0.02)
    ax.contour(s.obstacle, levels=[0.5], colors="k", linewidths=1)
    ax.scatter([px], [py], marker="x", c="k", s=30)
    ax.set_title(f"渦度の分布(ステップ {n_total})。× は速度を記録した点")
    save(fig, "lbm_vorticity.png")

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(np.arange(1, n_total + 1), sig)
    ax.set_xlabel("ステップ数")
    ax.set_ylabel("y 方向の速度(格子単位)")
    ax.set_title("円柱の後流で記録した y 方向の速度")
    save(fig, "lbm_probe.png")

    fig, ax = plt.subplots(figsize=(6.4, 1.9))
    image = ax.imshow(gif_frames[0], origin="lower", cmap="RdBu_r", vmin=-0.02, vmax=0.02)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()

    def animate(k: int) -> tuple[Artist]:
        image.set_data(gif_frames[k])
        return (image,)

    FuncAnimation(fig, animate, frames=len(gif_frames)).save(OUT / "lbm_karman.gif", writer=PillowWriter(fps=12))
    plt.close(fig)
    shrink_gif("lbm_karman.gif", every=2)


TASKS: dict[str, Callable[[], None]] = {
    "integrators": fig_integrators,
    "particles": fig_particles,
    "interactions": fig_interactions,
    "viewpoints": fig_viewpoints,
    "advection": fig_advection_diffusion,
    "stable_fluids": fig_stable_fluids,
    "cavity": fig_cavity,
    "sph": fig_sph,
    "lbm": fig_lbm,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    names = sys.argv[1:] or list(TASKS)
    for name in names:
        print(f"[{name}]")
        TASKS[name]()


if __name__ == "__main__":
    main()
