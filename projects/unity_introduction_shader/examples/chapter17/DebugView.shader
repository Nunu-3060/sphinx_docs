// 第 17 章：法線や UV 座標を色として表示し、
// シェーダーの中の値を目で確かめるためのシェーダー。
Shader "Introduction/Chapter17/DebugView"
{
    Properties
    {
        // マテリアルの Inspector でドロップダウンから表示内容を選ぶ。
        // 選んだ項目に応じて、_MODE_NORMAL などのキーワードのうち 1 つが有効になる。
        [KeywordEnum(Normal, UV, Depth)] _Mode ("Mode", Float) = 0
        // Depth モードで白になる距離（カメラからの距離）
        _MaxDistance ("Max Distance", Float) = 20
    }

    SubShader
    {
        Tags
        {
            "RenderType" = "Opaque"
            "Queue" = "Geometry"
            "RenderPipeline" = "UniversalPipeline"
        }

        Pass
        {
            Name "DebugView"
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            // マテリアルで選ばれたキーワードのバリアントだけがビルドに含まれる
            #pragma shader_feature_local_fragment _MODE_NORMAL _MODE_UV _MODE_DEPTH

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float2 uv : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
                float2 uv : TEXCOORD2;
            };

            CBUFFER_START(UnityPerMaterial)
                float _MaxDistance;
            CBUFFER_END

            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionWS = TransformObjectToWorld(input.positionOS.xyz);
                output.positionCS = TransformWorldToHClip(output.positionWS);
                output.normalWS = TransformObjectToWorldNormal(input.normalOS);
                output.uv = input.uv;
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
            #if defined(_MODE_UV)
                // U を赤、V を緑で表示する。frac で 0 ～ 1 の範囲に収め、
                // タイリングの繰り返しも見えるようにする。
                return half4(frac(input.uv), 0.0, 1.0);
            #elif defined(_MODE_DEPTH)
                // カメラからの距離を、近いほど黒、遠いほど白で表示する
                float distanceToCamera = length(GetCameraPositionWS() - input.positionWS);
                return half4(saturate(distanceToCamera / _MaxDistance).xxx, 1.0);
            #else
                // 法線の各成分（-1 ～ 1）を 0 ～ 1 に変換して、xyz を RGB として表示する
                float3 normalWS = normalize(input.normalWS);
                return half4(normalWS * 0.5 + 0.5, 1.0);
            #endif
            }
            ENDHLSL
        }
    }
}
