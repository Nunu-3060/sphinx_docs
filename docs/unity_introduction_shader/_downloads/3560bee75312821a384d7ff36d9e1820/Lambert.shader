// 第 9 章：メインライトによる拡散反射（Lambert 反射）だけを計算するシェーダー。
Shader "Introduction/Chapter09/Lambert"
{
    Properties
    {
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
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
            Name "Lambert"
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            // ライトの情報を取得する関数を使うため、Lighting.hlsl を読み込む
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL; // オブジェクト空間の法線
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 normalWS : TEXCOORD0; // ワールド空間の法線
            };

            CBUFFER_START(UnityPerMaterial)
                half4 _BaseColor;
            CBUFFER_END

            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                // 法線は位置とは異なる方法で変換する必要がある（第 3 章を参照）
                output.normalWS = TransformObjectToWorldNormal(input.normalOS);
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
                // 補間された法線は長さが 1 でなくなるため、正規化し直す
                float3 normalWS = normalize(input.normalWS);

                // メインライト（最も明るいディレクショナルライト）の情報を取得する。
                // mainLight.direction は、表面からライトへ向かう単位ベクトル。
                Light mainLight = GetMainLight();

                // Lambert 反射：明るさは法線とライト方向の内積に比例する。
                // 裏側（内積が負）は 0 にする。
                half nDotL = saturate(dot(normalWS, mainLight.direction));
                half3 diffuse = _BaseColor.rgb * mainLight.color * nDotL;

                return half4(diffuse, 1.0);
            }
            ENDHLSL
        }
    }
}
