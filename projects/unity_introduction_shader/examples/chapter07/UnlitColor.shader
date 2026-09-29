// 第 7 章：オブジェクトを 1 色で塗りつぶすだけの、最も簡単な URP 用シェーダー。
Shader "Introduction/Chapter07/UnlitColor"
{
    // マテリアルの Inspector ウィンドウに表示するプロパティ
    Properties
    {
        // [MainColor] を付けると、C# の Material.color でこの色を読み書きできる
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
    }

    SubShader
    {
        // RenderPipeline を指定し、URP のときだけこのサブシェーダーを使うようにする
        Tags
        {
            "RenderType" = "Opaque"
            "Queue" = "Geometry"
            "RenderPipeline" = "UniversalPipeline"
        }

        Pass
        {
            Name "Unlit"
            // URP の Forward / Forward+ レンダリングで描画されるパス
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            // 頂点シェーダーとフラグメントシェーダーとして使う関数の名前
            #pragma vertex Vert
            #pragma fragment Frag

            // 座標変換の関数などをまとめた URP のライブラリ
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            // 頂点シェーダーへの入力（メッシュの頂点データ）
            struct Attributes
            {
                float4 positionOS : POSITION; // オブジェクト空間の位置
            };

            // 頂点シェーダーからフラグメントシェーダーへ渡すデータ
            struct Varyings
            {
                float4 positionCS : SV_POSITION; // クリップ空間の位置
            };

            // SRP Batcher に対応させるため、
            // マテリアルのプロパティは UnityPerMaterial にまとめる
            CBUFFER_START(UnityPerMaterial)
                half4 _BaseColor;
            CBUFFER_END

            // 頂点シェーダー：頂点ごとに 1 回呼ばれ、頂点の位置をクリップ空間に変換する
            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                return output;
            }

            // フラグメントシェーダー：ピクセルごとに 1 回呼ばれ、そのピクセルの色を返す
            half4 Frag(Varyings input) : SV_Target
            {
                return _BaseColor;
            }
            ENDHLSL
        }
    }
}
