// 第 9 章：環境光、拡散反射（Lambert）、鏡面反射（Blinn-Phong）を組み合わせたシェーダー。
Shader "Introduction/Chapter09/BlinnPhong"
{
    Properties
    {
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        _SpecularColor ("Specular Color", Color) = (1, 1, 1, 1)
        // 値が大きいほどハイライトが小さく鋭くなる
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

        Pass
        {
            Name "BlinnPhong"
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
                float3 positionWS : TEXCOORD0; // ワールド空間の位置（視線方向の計算に使う）
                float3 normalWS : TEXCOORD1;
            };

            CBUFFER_START(UnityPerMaterial)
                half4 _BaseColor;
                half4 _SpecularColor;
                float _Shininess;
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
                // 表面からカメラへ向かう単位ベクトル
                float3 viewDirWS = GetWorldSpaceNormalizeViewDir(input.positionWS);
                Light mainLight = GetMainLight();

                // 環境光：Lighting ウィンドウの Environment Lighting の設定から、
                // 法線方向の光を取得する
                half3 ambient = SampleSH(normalWS) * _BaseColor.rgb;

                // 拡散反射（Lambert）
                half nDotL = saturate(dot(normalWS, mainLight.direction));
                half3 diffuse = _BaseColor.rgb * mainLight.color * nDotL;

                // 鏡面反射（Blinn-Phong）：
                // ライト方向と視線方向の中間のベクトル（ハーフベクトル）を使う
                float3 halfDirWS = normalize(mainLight.direction + viewDirWS);
                half nDotH = saturate(dot(normalWS, halfDirWS));
                half3 specular = _SpecularColor.rgb * mainLight.color * pow(nDotH, _Shininess);

                return half4(ambient + diffuse + specular, 1.0);
            }
            ENDHLSL
        }
    }
}
