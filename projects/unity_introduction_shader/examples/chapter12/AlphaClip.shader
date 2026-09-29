// 第 12 章：アルファテストで、
// アルファが一定の値より小さいピクセルを描画しないシェーダー。
// 葉や金網のように、「完全に見える部分」と「完全に透明な部分」だけがあるものに使う。
Shader "Introduction/Chapter12/AlphaClip"
{
    Properties
    {
        [MainTexture] _BaseMap ("Base Map", 2D) = "white" {}
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        // アルファがこの値より小さいピクセルは描画しない
        _Cutoff ("Alpha Cutoff", Range(0, 1)) = 0.5
    }

    SubShader
    {
        // 不透明なオブジェクトと同じく深度を書き込むが、
        // 描画順は不透明なオブジェクトのあとにする
        Tags
        {
            "RenderType" = "TransparentCutout"
            "Queue" = "AlphaTest"
            "RenderPipeline" = "UniversalPipeline"
        }

        Pass
        {
            Name "AlphaClip"
            Tags { "LightMode" = "UniversalForward" }

            // 板ポリゴンの裏側も描画する
            Cull Off

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float2 uv : TEXCOORD0;
            };

            TEXTURE2D(_BaseMap);
            SAMPLER(sampler_BaseMap);

            CBUFFER_START(UnityPerMaterial)
                float4 _BaseMap_ST;
                half4 _BaseColor;
                half _Cutoff;
            CBUFFER_END

            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                output.uv = TRANSFORM_TEX(input.uv, _BaseMap);
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
                half4 color = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, input.uv) * _BaseColor;
                // clip は、引数が負のときにこのピクセルを破棄する
                // （破棄されたピクセルには、色も深度も書き込まれない）
                clip(color.a - _Cutoff);
                return half4(color.rgb, 1.0);
            }
            ENDHLSL
        }
    }
}
