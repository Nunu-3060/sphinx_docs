// 第 10 章：法線マップで表面の細かい凹凸を表現するシェーダー。
// ライティングは第 9 章の環境光と拡散反射（Lambert）を使う。
Shader "Introduction/Chapter10/NormalMap"
{
    Properties
    {
        [MainTexture] _BaseMap ("Base Map", 2D) = "white" {}
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        // [Normal] を付けると、
        // 法線マップ以外のテクスチャーを設定したときに警告が表示される。
        // [NoScaleOffset] を付けると、
        // Tiling と Offset の入力欄が表示されなくなる（Base Map と同じ UV を使うため）。
        // "bump" は、法線マップが未設定のときに凹凸なしとして扱われる既定のテクスチャー。
        [Normal][NoScaleOffset] _NormalMap ("Normal Map", 2D) = "bump" {}
        // 凹凸の強さ（0 で凹凸なし）
        _NormalScale ("Normal Scale", Range(0, 2)) = 1
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
            Name "NormalMap"
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
                float4 tangentOS : TANGENT; // xyz：接線、w：従法線の向き（1 または -1）
                float2 uv : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
                float3 tangentWS : TEXCOORD2;
                float3 bitangentWS : TEXCOORD3;
            };

            TEXTURE2D(_BaseMap);
            SAMPLER(sampler_BaseMap);
            TEXTURE2D(_NormalMap);
            SAMPLER(sampler_NormalMap);

            CBUFFER_START(UnityPerMaterial)
                float4 _BaseMap_ST;
                half4 _BaseColor;
                half _NormalScale;
            CBUFFER_END

            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                output.uv = TRANSFORM_TEX(input.uv, _BaseMap);

                // 法線、接線、従法線をワールド空間に変換する。
                // 従法線は、法線と接線の外積に tangentOS.w を掛けて求められる。
                VertexNormalInputs normalInputs =
                    GetVertexNormalInputs(input.normalOS, input.tangentOS);
                output.normalWS = normalInputs.normalWS;
                output.tangentWS = normalInputs.tangentWS;
                output.bitangentWS = normalInputs.bitangentWS;
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
                // 法線マップから接空間の法線を取り出す。
                // テクスチャーの 0 ～ 1 の値を -1 ～ 1 のベクトルに戻す処理も、
                // この関数が行う。
                half4 packedNormal = SAMPLE_TEXTURE2D(_NormalMap, sampler_NormalMap, input.uv);
                half3 normalTS = UnpackNormalScale(packedNormal, _NormalScale);

                // TBN 行列（接線、従法線、法線を行に並べた行列）で、
                // 接空間からワールド空間に変換する
                half3x3 tangentToWorld =
                    half3x3(input.tangentWS, input.bitangentWS, input.normalWS);
                float3 normalWS = normalize(TransformTangentToWorld(normalTS, tangentToWorld));

                half3 baseMapColor = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, input.uv).rgb;
                half3 albedo = baseMapColor * _BaseColor.rgb;
                Light mainLight = GetMainLight();

                half3 ambient = SampleSH(normalWS) * albedo;
                half nDotL = saturate(dot(normalWS, mainLight.direction));
                half3 diffuse = albedo * mainLight.color * nDotL;

                return half4(ambient + diffuse, 1.0);
            }
            ENDHLSL
        }
    }
}
