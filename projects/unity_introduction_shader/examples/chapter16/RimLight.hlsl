// 第 16 章：Shader Graph の Custom Function ノードから呼び出す、リムライトの計算。
// ノードの Type を File にし、Source にこのファイル、Name に RimLight を指定する。

// インクルードガード：同じファイルが複数回読み込まれても、
// 関数が重複して定義されないようにする
#ifndef INTRODUCTION_RIM_LIGHT_INCLUDED
#define INTRODUCTION_RIM_LIGHT_INCLUDED

// 関数名の末尾の _float は、ノードの Precision が Float のときに使われることを表す。
// 戻り値は使わず、out 引数がノードの出力ポートになる。
void RimLight_float(float3 Normal, float3 ViewDir, float Power, out float Out)
{
    float nDotV = saturate(dot(normalize(Normal), normalize(ViewDir)));
    Out = pow(1.0 - nDotV, Power);
}

// Precision が Half のときに使われる版
void RimLight_half(half3 Normal, half3 ViewDir, half Power, out half Out)
{
    half nDotV = saturate(dot(normalize(Normal), normalize(ViewDir)));
    Out = pow(1.0 - nDotV, Power);
}

#endif
