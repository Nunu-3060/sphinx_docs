"""Shadertoy 形式のフラグメントシェーダーをブラウザーで実行するビューアー。

``mainImage`` 関数を定義した GLSL ファイルを読み込み、WebGL2 で実行する
単一の HTML ファイルを生成して既定のブラウザーで開く。
Python の標準ライブラリだけで動作する。

使い方::

    python shader_viewer.py ../shaders/02_first_sphere.frag

生成される HTML は、次の uniform 変数を Shadertoy と同じ意味で提供する。

* ``iResolution`` (vec3): 描画領域の解像度 [px]
* ``iTime`` (float): 開始からの経過時間 [s]
* ``iTimeDelta`` (float): 前フレームからの経過時間 [s]
* ``iFrame`` (int): フレーム番号
* ``iMouse`` (vec4): xy はドラッグ中のマウス座標、zw はクリックした座標
  (ボタンを離すと zw の符号が負になる)
* ``iChannel0`` (sampler2D): Buffer A の描画結果 (複数パスの場合)
* ``iChannelResolution`` (vec3[4]): 各チャンネルの解像度 [px]

複数パスの描画
    ファイルの中に ``// ==== Buffer A ====`` と ``// ==== Image ====`` の行を
    置くと、それぞれの行から次の区切りまでを Buffer A と Image のパスとして
    扱う。Buffer A の ``iChannel0`` には Buffer A 自身の前のフレームの結果が、
    Image の ``iChannel0`` には Buffer A の今のフレームの結果が入る。
    Buffer A は 32 ビット浮動小数点数のテクスチャに描画される。
    ``// ==== Common ====`` の行から次の区切りまでのコードは、Shadertoy の
    Common のタブと同じく、すべてのパスの先頭に加えられる。

URL のフラグメントで、次のパラメーターを指定できる。

* ``#t=2.5``: ``iTime`` を 2.5 秒に固定する。
* ``#frame=0``: ``iFrame`` を 0 に固定する。
* ``#frames=16``: 読み込み直後に 16 フレームだけを描画して止める。
  ``iFrame`` は 0〜15 になる。描画の速さによらず同じ結果が得られる。

パラメーターは ``#t=2.5&frames=16`` のように ``&`` でつなげて指定する。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import webbrowser
from pathlib import Path
from string import Template

# 複数パスの区切りの行。例: "// ==== Buffer A ===="
PASS_MARKER = re.compile(r"^// ==== (Common|Buffer A|Image) ====",
                         re.MULTILINE)

HTML_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<style>
html, body { margin: 0; height: 100%; background: #000; overflow: hidden; }
canvas { display: block; width: 100%; height: 100%; }
#error {
  position: absolute; top: 0; left: 0; right: 0; margin: 0; padding: 1em;
  color: #fff; background: rgba(160, 0, 0, 0.85);
  font: 14px/1.4 monospace; white-space: pre-wrap; display: none;
}
</style>
</head>
<body>
<canvas id="canvas"></canvas>
<pre id="error"></pre>
<script>
"use strict";
// [{name: "Buffer A" | "Image", source: GLSL, line: ファイル中の開始行}]
const PASSES = $passes;

const HEADER = [
  "#version 300 es",
  "precision highp float;",
  "precision highp int;",
  "uniform vec3 iResolution;",
  "uniform float iTime;",
  "uniform float iTimeDelta;",
  "uniform int iFrame;",
  "uniform vec4 iMouse;",
  "uniform sampler2D iChannel0;",
  "uniform vec3 iChannelResolution[4];",
  "out vec4 shadertoyOutColor;"
].join("\\n");

// Image のパスでは不透明度を 1 にする。Buffer A では 4 成分をそのまま残す
function footer(passName) {
  return [
    "",
    "void main() {",
    "  mainImage(shadertoyOutColor, gl_FragCoord.xy);",
    passName === "Image" ? "  shadertoyOutColor.a = 1.0;" : "",
    "}"
  ].join("\\n");
}

const VERTEX_SOURCE = [
  "#version 300 es",
  "in vec2 position;",
  "void main() { gl_Position = vec4(position, 0.0, 1.0); }"
].join("\\n");

function showError(message) {
  const element = document.getElementById("error");
  element.textContent = message;
  element.style.display = "block";
  document.title = "ERROR: " + document.title;
}

function compile(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    throw new Error(gl.getShaderInfoLog(shader));
  }
  return shader;
}

// パスのプログラムを作る。Common のコードがあれば先頭に加える。
// #line でエラーの行番号をファイルの行番号に合わせる
function createProgram(gl, pass) {
  const program = gl.createProgram();
  let source = HEADER;
  if (pass.common) {
    source += "\\n#line " + pass.commonLine + "\\n" + pass.common;
  }
  source += "\\n#line " + pass.line + "\\n" + pass.source + footer(pass.name);
  gl.attachShader(program, compile(gl, gl.VERTEX_SHADER, VERTEX_SOURCE));
  gl.attachShader(program, compile(gl, gl.FRAGMENT_SHADER, source));
  gl.bindAttribLocation(program, 0, "position");
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    throw new Error(gl.getProgramInfoLog(program));
  }
  const uniforms = {};
  for (const name of ["iResolution", "iTime", "iTimeDelta", "iFrame",
                      "iMouse", "iChannel0", "iChannelResolution"]) {
    uniforms[name] = gl.getUniformLocation(program, name);
  }
  return {name: pass.name, program: program, uniforms: uniforms};
}

// URL のフラグメント (#t=2.5&frames=16 など) から数値のパラメーターを読む
function hashParameter(name) {
  const pattern = new RegExp("(?:^#|&)" + name + "=([0-9.]+)");
  const match = pattern.exec(location.hash);
  return match ? parseFloat(match[1]) : null;
}

function run() {
  const canvas = document.getElementById("canvas");
  const gl = canvas.getContext("webgl2", {preserveDrawingBuffer: true});
  if (!gl) {
    showError("WebGL2 is not supported by this browser.");
    return;
  }

  let passes;
  try {
    passes = PASSES.map((pass) => createProgram(gl, pass));
  } catch (e) {
    showError("Shader compile error:\\n" + e.message);
    return;
  }
  const bufferPass = passes.find((pass) => pass.name === "Buffer A");
  const imagePass = passes.find((pass) => pass.name === "Image");

  // 浮動小数点数のテクスチャへの描画に対応していなければ 8 ビットで代用する
  const floatBuffer = gl.getExtension("EXT_color_buffer_float") !== null;

  // 画面全体を覆う 2 つの三角形
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(
    [-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

  // Buffer A の描画先。前のフレームを読みながら次のフレームを書くため 2 枚使う
  let targets = [];
  function createTarget(width, height) {
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);
    if (floatBuffer) {
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA32F, width, height, 0,
                    gl.RGBA, gl.FLOAT, null);
    } else {
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, width, height, 0,
                    gl.RGBA, gl.UNSIGNED_BYTE, null);
    }
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    const framebuffer = gl.createFramebuffer();
    gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0,
                            gl.TEXTURE_2D, texture, 0);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    return {texture: texture, framebuffer: framebuffer};
  }

  // iMouse: xy はドラッグ中の座標、zw はクリック位置 (離すと負)
  const mouse = [0, 0, 0, 0];
  let dragging = false;
  function mousePosition(event) {
    const rect = canvas.getBoundingClientRect();
    const scale = canvas.width / rect.width;
    return [(event.clientX - rect.left) * scale,
            (rect.bottom - event.clientY) * scale];
  }
  canvas.addEventListener("mousedown", (event) => {
    const [x, y] = mousePosition(event);
    dragging = true;
    mouse[0] = x; mouse[1] = y; mouse[2] = x; mouse[3] = y;
  });
  canvas.addEventListener("mousemove", (event) => {
    if (!dragging) { return; }
    const [x, y] = mousePosition(event);
    mouse[0] = x; mouse[1] = y;
  });
  window.addEventListener("mouseup", () => {
    dragging = false;
    mouse[2] = -Math.abs(mouse[2]); mouse[3] = -Math.abs(mouse[3]);
  });

  function drawPass(pass, width, height, time, timeDelta, frame, channel) {
    gl.useProgram(pass.program);
    const u = pass.uniforms;
    gl.uniform3f(u.iResolution, width, height, 1);
    gl.uniform1f(u.iTime, time);
    gl.uniform1f(u.iTimeDelta, timeDelta);
    gl.uniform1i(u.iFrame, frame);
    gl.uniform4fv(u.iMouse, mouse);
    gl.uniform3fv(u.iChannelResolution,
                  [width, height, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, channel);
    gl.uniform1i(u.iChannel0, 0);
    gl.viewport(0, 0, width, height);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  }

  // 1 フレームを描画する
  function renderFrame(time, timeDelta, frame) {
    const ratio = window.devicePixelRatio || 1;
    const width = Math.max(1, Math.floor(canvas.clientWidth * ratio));
    const height = Math.max(1, Math.floor(canvas.clientHeight * ratio));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
      targets = [];
    }
    if (bufferPass && targets.length === 0) {
      targets = [createTarget(width, height), createTarget(width, height)];
    }
    let latest = null;
    if (bufferPass) {
      // targets[0] (前のフレーム) を読み、targets[1] に書いてから入れ替える
      gl.bindFramebuffer(gl.FRAMEBUFFER, targets[1].framebuffer);
      drawPass(bufferPass, width, height, time, timeDelta, frame,
               targets[0].texture);
      targets.reverse();
      latest = targets[0].texture;
    }
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    drawPass(imagePass, width, height, time, timeDelta, frame, latest);
  }

  const fixedTime = hashParameter("t");
  const fixedFrame = hashParameter("frame");
  const frameCount = hashParameter("frames");

  if (frameCount !== null) {
    // 指定したフレーム数だけを続けて描画して止める (撮影用)。
    // 画面の大きさが変わったときは、最初から描画し直す
    const renderFixedFrames = () => {
      const time = fixedTime !== null ? fixedTime : 0;
      targets = [];
      for (let frame = 0; frame < frameCount; frame++) {
        renderFrame(time, 1 / 60, frame);
      }
      gl.finish();
    };
    new ResizeObserver(renderFixedFrames).observe(canvas);
    return;
  }

  const startTime = performance.now();
  let previousTime = 0;
  let frame = 0;
  function loop(now) {
    const time = fixedTime !== null ? fixedTime : (now - startTime) / 1000;
    renderFrame(time, time - previousTime,
                fixedFrame !== null ? fixedFrame : frame);
    previousTime = time;
    frame += 1;
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
}

run();
</script>
</body>
</html>
""")


def split_passes(source: str) -> list[dict[str, str | int]]:
    """シェーダーのソースコードをパスごとに分ける。

    区切りの行が無ければ、全体を 1 つの Image パスとして扱う。
    Common の区切りがあれば、そのコードを各パスの common に入れる。

    Args:
        source: GLSL のソースコード。

    Returns:
        パスのリスト (Common は含まない)。各要素は name (パスの名前)、
        source (パスのソースコード)、line (ファイル中の開始行、1 始まり)、
        common (Common のコード)、commonLine (Common の開始行) を持つ。
    """
    markers = list(PASS_MARKER.finditer(source))
    if not markers:
        return [{"name": "Image", "source": source, "line": 1,
                 "common": "", "commonLine": 1}]
    sections: list[dict[str, str | int]] = []
    for index, marker in enumerate(markers):
        end = (markers[index + 1].start() if index + 1 < len(markers)
               else len(source))
        sections.append({
            "name": marker.group(1),
            "source": source[marker.start():end],
            "line": source.count("\n", 0, marker.start()) + 1,
        })
    names = [s["name"] for s in sections]
    if names.count("Image") != 1 or len(set(names)) != len(names):
        raise ValueError("Image のパスがちょうど 1 つ必要である")

    common = next((s for s in sections if s["name"] == "Common"), None)
    passes = [s for s in sections if s["name"] != "Common"]
    for p in passes:
        p["common"] = common["source"] if common else ""
        p["commonLine"] = common["line"] if common else 1
    return passes


def build_html(shader_source: str, title: str) -> str:
    """シェーダーのソースコードを埋め込んだ HTML 文字列を返す。

    Args:
        shader_source: ``mainImage`` 関数を含む GLSL のソースコード。
        title: HTML の ``<title>`` に表示する文字列。

    Returns:
        単体で動作する HTML 文字列。
    """
    # "</script>" でスクリプト要素が途切れないように "</" をエスケープする
    passes_literal = json.dumps(split_passes(shader_source))
    passes_literal = passes_literal.replace("</", "<\\/")
    return HTML_TEMPLATE.substitute(title=title, passes=passes_literal)


def write_html(shader_path: Path, output_path: Path) -> Path:
    """GLSL ファイルを読み込み、実行用の HTML ファイルを書き出す。

    Args:
        shader_path: 入力する GLSL ファイルのパス。
        output_path: 出力する HTML ファイルのパス。

    Returns:
        書き出した HTML ファイルのパス。
    """
    source = shader_path.read_text(encoding="utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(source, shader_path.name),
                           encoding="utf-8")
    return output_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="Shadertoy 形式のシェーダーをブラウザーで実行する。")
    parser.add_argument("shader", type=Path,
                        help="mainImage 関数を含む GLSL ファイル")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="出力する HTML ファイル "
                             "(省略時はシェーダーと同じ場所に .html を作成)")
    parser.add_argument("--no-open", action="store_true",
                        help="生成後にブラウザーを開かない")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """エントリーポイント。"""
    args = parse_args(argv)
    shader_path: Path = args.shader
    if not shader_path.is_file():
        print(f"ファイルが見つからない: {shader_path}", file=sys.stderr)
        return 1

    output_path: Path = args.output or shader_path.with_suffix(".html")
    written = write_html(shader_path, output_path)
    print(f"出力: {written}")
    if not args.no_open:
        webbrowser.open(written.resolve().as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
