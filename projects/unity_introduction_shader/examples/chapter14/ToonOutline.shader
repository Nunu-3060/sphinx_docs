// 第 14 章：陰影をはっきり 2 段階に分けるトゥーンシェーディングと、
// 輪郭線を描画するシェーダー。
Shader "Introduction/Chapter14/ToonOutline"
{
    Properties
    {
        [MainColor] _BaseColor ("Base Color", Color) = (1, 0.6, 0.5, 1)
        _ShadeColor ("Shade Color", Color) = (0.5, 0.3, 0.4, 1)
        // 明るい部分と暗い部分の境目の位置（N・L の値）
        _ShadeThreshold ("Shade Threshold", Range(-1, 1)) = 0
        // 境目をぼかす幅（0 でくっきり分かれる）
        _ShadeSmoothness ("Shade Smoothness", Range(0, 0.5)) = 0.02
        _OutlineColor ("Outline Color", Color) = (0.1, 0.05, 0.05, 1)
        // 輪郭線の太さ（オブジェクト空間の単位）
        _OutlineWidth ("Outline Width", Range(0, 0.1)) = 0.02
    }

    SubShader
    {
        Tags
        {
            "RenderType" = "Opaque"
            "Queue" = "Geometry"
            "RenderPipeline" = "UniversalPipeline"
        }

        // 2 つのパスで UnityPerMaterial の内容をそろえるため、共通部分にまとめる
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

        CBUFFER_START(UnityPerMaterial)
            half4 _BaseColor;
            half4 _ShadeColor;
            half _ShadeThreshold;
            half _ShadeSmoothness;
            half4 _OutlineColor;
            float _OutlineWidth;
        CBUFFER_END
        ENDHLSL

        // 1 つ目のパス：トゥーンシェーディングで本体を描画する
        Pass
        {
            Name "Toon"
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 normalWS : TEXCOORD0;
            };

            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                output.normalWS = TransformObjectToWorldNormal(input.normalOS);
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
                float3 normalWS = normalize(input.normalWS);
                Light mainLight = GetMainLight();

                // Lambert と異なり、N・L を 0 ～ 1 に切り詰めずに使う（-1 ～ 1）
                half nDotL = dot(normalWS, mainLight.direction);
                // しきい値の前後で 0 から 1 に急に変わる値を作る
                half lit = smoothstep(
                    _ShadeThreshold - _ShadeSmoothness,
                    _ShadeThreshold + _ShadeSmoothness,
                    nDotL);

                half3 color = lerp(_ShadeColor.rgb, _BaseColor.rgb, lit) * mainLight.color;
                return half4(color, 1.0);
            }
            ENDHLSL
        }

        // 2 つ目のパス：法線方向に膨らませたメッシュの裏面だけを描画して、輪郭線にする
        Pass
        {
            Name "Outline"
            // URP は、LightMode が SRPDefaultUnlit のパスも、
            // UniversalForward のパスと同じタイミングで描画する
            Tags { "LightMode" = "SRPDefaultUnlit" }

            // 表面を描画せず、裏面だけを描画する
            Cull Front

            HLSLPROGRAM
            #pragma vertex OutlineVert
            #pragma fragment OutlineFrag

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
            };

            Varyings OutlineVert(Attributes input)
            {
                Varyings output;
                // 頂点を法線方向に押し出す
                float3 offset = normalize(input.normalOS) * _OutlineWidth;
                float3 positionOS = input.positionOS.xyz + offset;
                output.positionCS = TransformObjectToHClip(positionOS);
                return output;
            }

            half4 OutlineFrag(Varyings input) : SV_Target
            {
                return _OutlineColor;
            }
            ENDHLSL
        }
    }
}
