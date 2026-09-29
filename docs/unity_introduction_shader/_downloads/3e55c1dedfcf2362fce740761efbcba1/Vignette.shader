// 第 15 章：画面の周辺を暗くする（ビネット）ポストエフェクト用のシェーダー。
// Full Screen Pass Renderer Feature の Pass Material に設定して使う。
Shader "Introduction/Chapter15/Vignette"
{
    Properties
    {
        _VignetteColor ("Vignette Color", Color) = (0, 0, 0, 1)
        // 画面の中心からこの距離までは暗くしない（画面の高さを 1 とした距離）
        _Radius ("Radius", Range(0, 1)) = 0.4
        // 暗くなり始めてから完全に暗くなるまでの距離
        _Softness ("Softness", Range(0.01, 1)) = 0.4
        _Intensity ("Intensity", Range(0, 1)) = 0.8
    }

    SubShader
    {
        Tags
        {
            "RenderType" = "Opaque"
            "RenderPipeline" = "UniversalPipeline"
        }

        ZWrite Off
        ZTest Always
        Cull Off

        Pass
        {
            Name "Vignette"

            HLSLPROGRAM
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"

            #pragma vertex Vert
            #pragma fragment VignetteFrag

            CBUFFER_START(UnityPerMaterial)
                half4 _VignetteColor;
                float _Radius;
                float _Softness;
                half _Intensity;
            CBUFFER_END

            half4 VignetteFrag(Varyings input) : SV_Target
            {
                UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input);

                half4 color =
                    SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_LinearClamp, input.texcoord);

                // 画面の中心から見た位置。横方向に縦横比を掛け、
                // 周辺が楕円ではなく円形に暗くなるようにする。
                // _ScreenParams.x と _ScreenParams.y には、
                // 描画先の幅と高さ（ピクセル数）が入っている。
                float2 fromCenter = input.texcoord - 0.5;
                fromCenter.x *= _ScreenParams.x / _ScreenParams.y;
                float distanceFromCenter = length(fromCenter);

                // 中心付近は 0、周辺ほど 1 に近づく値
                half vignette = smoothstep(_Radius, _Radius + _Softness, distanceFromCenter);
                vignette *= _Intensity;

                color.rgb = lerp(color.rgb, _VignetteColor.rgb, vignette);
                return color;
            }
            ENDHLSL
        }
    }
}
