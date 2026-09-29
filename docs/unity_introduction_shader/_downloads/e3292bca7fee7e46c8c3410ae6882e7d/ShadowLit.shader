// 第 11 章：影を落とし（ShadowCaster パス）、
// 影を受ける（シャドウマップの参照）シェーダー。
// ライティングは第 9 章の BlinnPhong.shader と同じ計算に、影の減衰を加えたもの。
Shader "Introduction/Chapter11/ShadowLit"
{
    Properties
    {
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        _SpecularColor ("Specular Color", Color) = (1, 1, 1, 1)
        _Shininess ("Shininess", Range(1, 256)) = 32
    }

    SubShader
    {
        Tags
        {
            "RenderType" = "Opaque"
            "Queue" = "Geometry"
            "RenderPipeline" = "UniversalPipeline"
        }

        // HLSLINCLUDE の内容は、このサブシェーダーのすべてのパスの先頭に挿入される。
        // SRP Batcher に対応させるには、
        // すべてのパスで UnityPerMaterial の内容を同じにする必要がある。
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

        CBUFFER_START(UnityPerMaterial)
            half4 _BaseColor;
            half4 _SpecularColor;
            float _Shininess;
        CBUFFER_END
        ENDHLSL

        // 1 つ目のパス：画面に色を描画する
        Pass
        {
            Name "ForwardLit"
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            // メインライトの影を受けるためのキーワード。
            // URP Asset の影の設定に応じて、URP がこのうち 1 つを有効にする。
            #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE
            // ソフトシャドウ（影の輪郭をぼかす処理）のためのキーワード
            #pragma multi_compile_fragment _ _SHADOWS_SOFT _SHADOWS_SOFT_LOW _SHADOWS_SOFT_MEDIUM _SHADOWS_SOFT_HIGH

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
            };

            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionWS = TransformObjectToWorld(input.positionOS.xyz);
                output.positionCS = TransformWorldToHClip(output.positionWS);
                output.normalWS = TransformObjectToWorldNormal(input.normalOS);
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
                float3 normalWS = normalize(input.normalWS);
                float3 viewDirWS = GetWorldSpaceNormalizeViewDir(input.positionWS);

                // ワールド空間の位置を、シャドウマップを参照するための座標に変換する
                float4 shadowCoord = TransformWorldToShadowCoord(input.positionWS);
                // 引数に shadowCoord を渡すと、
                // mainLight.shadowAttenuation に影の情報が入る
                // （0：完全に影の中、1：影の外）
                Light mainLight = GetMainLight(shadowCoord);
                half3 lightColor = mainLight.color * mainLight.shadowAttenuation;

                half3 ambient = SampleSH(normalWS) * _BaseColor.rgb;

                half nDotL = saturate(dot(normalWS, mainLight.direction));
                half3 diffuse = _BaseColor.rgb * lightColor * nDotL;

                float3 halfDirWS = normalize(mainLight.direction + viewDirWS);
                half nDotH = saturate(dot(normalWS, halfDirWS));
                half3 specular = _SpecularColor.rgb * lightColor * pow(nDotH, _Shininess);

                return half4(ambient + diffuse + specular, 1.0);
            }
            ENDHLSL
        }

        // 2 つ目のパス：シャドウマップに深度を書き込み、ほかのオブジェクトに影を落とす
        Pass
        {
            Name "ShadowCaster"
            Tags { "LightMode" = "ShadowCaster" }

            ZWrite On
            ZTest LEqual
            // 色は書き込まない
            ColorMask 0

            HLSLPROGRAM
            #pragma vertex ShadowVert
            #pragma fragment ShadowFrag

            // ポイントライトとスポットライトの影を描画するときに、
            // URP が有効にするキーワード
            #pragma multi_compile_vertex _ _CASTING_PUNCTUAL_LIGHT_SHADOW

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Shadows.hlsl"

            // 影を描画しているライトの向きと位置。URP が値を設定する。
            float3 _LightDirection;
            float3 _LightPosition;

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
            };

            Varyings ShadowVert(Attributes input)
            {
                Varyings output;
                float3 positionWS = TransformObjectToWorld(input.positionOS.xyz);
                float3 normalWS = TransformObjectToWorldNormal(input.normalOS);

            #if defined(_CASTING_PUNCTUAL_LIGHT_SHADOW)
                float3 lightDirectionWS = normalize(_LightPosition - positionWS);
            #else
                float3 lightDirectionWS = _LightDirection;
            #endif

                // シャドウアクネ（表面に縞模様の影が出る現象）を防ぐため、
                // 位置を少しずらす
                positionWS = ApplyShadowBias(positionWS, normalWS, lightDirectionWS);
                output.positionCS = TransformWorldToHClip(positionWS);

                // ライトの近くでクリップ面より手前に出た頂点を、
                // クリップ面の位置に押し戻す
            #if UNITY_REVERSED_Z
                output.positionCS.z = min(output.positionCS.z, UNITY_NEAR_CLIP_VALUE);
            #else
                output.positionCS.z = max(output.positionCS.z, UNITY_NEAR_CLIP_VALUE);
            #endif
                return output;
            }

            half4 ShadowFrag(Varyings input) : SV_Target
            {
                // 深度だけが必要なため、色は何を返してもよい
                return 0;
            }
            ENDHLSL
        }

        // 3 つ目のパス：深度テクスチャーに深度を書き込む。
        // カメラの深度テクスチャーを使う機能（Depth Priming や、
        // 深度を使うエフェクトなど）で必要になる。
        Pass
        {
            Name "DepthOnly"
            Tags { "LightMode" = "DepthOnly" }

            ZWrite On
            ColorMask R

            HLSLPROGRAM
            #pragma vertex DepthVert
            #pragma fragment DepthFrag

            struct Attributes
            {
                float4 positionOS : POSITION;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
            };

            Varyings DepthVert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                return output;
            }

            half DepthFrag(Varyings input) : SV_Target
            {
                return input.positionCS.z;
            }
            ENDHLSL
        }
    }
}
