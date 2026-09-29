// 第 12 章：アルファブレンドで半透明に描画するシェーダー。
Shader "Introduction/Chapter12/Transparent"
{
    Properties
    {
        [MainTexture] _BaseMap ("Base Map", 2D) = "white" {}
        // アルファ（a）の値が不透明度になる（0：完全に透明、1：不透明）
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 0.5)
    }

    SubShader
    {
        // 不透明なオブジェクトをすべて描画したあとに描画するため、
        // Queue を Transparent にする
        Tags
        {
            "RenderType" = "Transparent"
            "Queue" = "Transparent"
            "RenderPipeline" = "UniversalPipeline"
        }

        Pass
        {
            Name "Transparent"
            Tags { "LightMode" = "UniversalForward" }

            // 出力する色 × アルファ + 画面に描かれている色 × (1 - アルファ)
            Blend SrcAlpha OneMinusSrcAlpha
            // 後ろにある半透明のオブジェクトが隠れないように、深度は書き込まない
            ZWrite Off

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
                // テクスチャーのアルファと _BaseColor のアルファを掛けた値が、
                // 最終的な不透明度になる
                return SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, input.uv) * _BaseColor;
            }
            ENDHLSL
        }
    }
}
