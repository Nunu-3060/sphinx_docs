// 第 14 章：オブジェクトの輪郭付近を光らせる（リムライト）シェーダー。
Shader "Introduction/Chapter14/RimLight"
{
    Properties
    {
        [MainColor] _BaseColor ("Base Color", Color) = (0.2, 0.2, 0.3, 1)
        [HDR] _RimColor ("Rim Color", Color) = (0.3, 0.8, 1, 1)
        // 値が大きいほど、光る範囲が輪郭の近くに狭まる
        _RimPower ("Rim Power", Range(0.5, 8)) = 3
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
            Name "RimLight"
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
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

            CBUFFER_START(UnityPerMaterial)
                half4 _BaseColor;
                half4 _RimColor;
                half _RimPower;
            CBUFFER_END

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
                Light mainLight = GetMainLight();

                half3 ambient = SampleSH(normalWS) * _BaseColor.rgb;
                half nDotL = saturate(dot(normalWS, mainLight.direction));
                half3 diffuse = _BaseColor.rgb * mainLight.color * nDotL;

                // 法線と視線が直交する（内積が 0 に近い）輪郭付近ほど、rim が 1 に近づく
                half nDotV = saturate(dot(normalWS, viewDirWS));
                half rim = pow(1.0 - nDotV, _RimPower);
                half3 rimColor = _RimColor.rgb * rim;

                return half4(ambient + diffuse + rimColor, 1.0);
            }
            ENDHLSL
        }
    }
}
