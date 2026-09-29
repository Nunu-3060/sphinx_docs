#version 300 es
precision highp float;

in float vHeight;
out vec4 outColor;

void main() {
    // 低い所は青、高い所は白
    vec3 color = mix(vec3(0.1, 0.3, 0.9), vec3(0.9, 0.95, 1.0), vHeight * 0.5 + 0.5);
    outColor = vec4(color, 1.0);
}
