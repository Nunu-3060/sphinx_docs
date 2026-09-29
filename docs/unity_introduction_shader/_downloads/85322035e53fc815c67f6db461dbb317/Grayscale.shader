// 第 15 章：画面全体をグレースケール（白黒）にするポストエフェクト用のシェーダー。
// Full Screen Pass Renderer Feature の Pass Material に設定して使う。
Shader "Introduction/Chapter15/Grayscale"
{
    Properties
    {
        // 0 で元の色、1 で完全な白黒
        _Intensity ("Intensity", Range(0, 1)) = 1
    }

    SubShader
    {
        Tags
        {
            "RenderType" = "Opaque"
            "RenderPipeline" = "UniversalPipeline"
        }

        // 画面全体を覆う三角形を描くだけなので、深度とカリングは使わない
        ZWrite Off
        ZTest Always
        Cull Off

        Pass
        {
            Name "Grayscale"

            HLSLPROGRAM
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            // 全画面描画用の頂点シェーダー Vert と、
            // 画面の色が入ったテクスチャー _BlitTexture が定義されている
            #include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"

            #pragma vertex Vert
            #pragma fragment GrayscaleFrag

            CBUFFER_START(UnityPerMaterial)
                half _Intensity;
            CBUFFER_END

            half4 GrayscaleFrag(Varyings input) : SV_Target
            {
                UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input);

                // レンダリング済みの画面の色を読み取る
                half4 color =
                    SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_LinearClamp, input.texcoord);

                // 人の目は緑に敏感で青に鈍感なため、
                // 重みを付けて輝度を求める（ITU-R BT.709 の係数）
                half luminance = dot(color.rgb, half3(0.2126, 0.7152, 0.0722));

                color.rgb = lerp(color.rgb, luminance.xxx, _Intensity);
                return color;
            }
            ENDHLSL
        }
    }
}
