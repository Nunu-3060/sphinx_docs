// 第 13 章：オブジェクトがいつもカメラの方を向くようにする（ビルボード）シェーダー。
// XY 平面上に作られた Quad メッシュに使う。
Shader "Introduction/Chapter13/Billboard"
{
    Properties
    {
        [MainTexture] _BaseMap ("Base Map", 2D) = "white" {}
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        _Cutoff ("Alpha Cutoff", Range(0, 1)) = 0.5
    }

    SubShader
    {
        // DisableBatching：
        // 複数のメッシュが 1 つにまとめられるとオブジェクトの中心が分からなくなるため、
        // バッチングを無効にする
        Tags
        {
            "RenderType" = "TransparentCutout"
            "Queue" = "AlphaTest"
            "RenderPipeline" = "UniversalPipeline"
            "DisableBatching" = "True"
        }

        Pass
        {
            Name "Billboard"
            Tags { "LightMode" = "UniversalForward" }

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

                // オブジェクトの中心（原点）をビュー空間に変換する
                float3 centerWS = TransformObjectToWorld(float3(0.0, 0.0, 0.0));
                float3 centerVS = TransformWorldToView(centerWS);

                // ビュー空間では x 軸が画面の右、y 軸が画面の上を向いている。
                // 中心から頂点の xy 分だけずらすと、頂点が常に画面と平行な面に並ぶ。
                // ワールド行列を通らないため、Transform の Scale は反映されない。
                float3 positionVS = centerVS + float3(input.positionOS.xy, 0.0);

                output.positionCS = TransformWViewToHClip(positionVS);
                output.uv = TRANSFORM_TEX(input.uv, _BaseMap);
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
                half4 color = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, input.uv) * _BaseColor;
                clip(color.a - _Cutoff);
                return half4(color.rgb, 1.0);
            }
            ENDHLSL
        }
    }
}
