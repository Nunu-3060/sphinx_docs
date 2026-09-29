using UnityEditor;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 10 章のサンプルです。
    /// 「Sprites」フォルダーに追加されたテクスチャーを、自動的にスプライトとしてインポートします。
    /// </summary>
    public class TextureImportProcessor : AssetPostprocessor
    {
        // テクスチャーのインポート処理の直前に呼ばれます。
        private void OnPreprocessTexture()
        {
            // .meta ファイルが無い（初めてインポートされる）ときだけ設定します。
            // こうしておくと、ユーザーが後から Inspector ウィンドウで変更した設定を上書きしません。
            if (!assetImporter.importSettingsMissing)
            {
                return;
            }

            // パスに「/Sprites/」を含むテクスチャーだけを対象にします。
            if (!assetPath.Contains("/Sprites/"))
            {
                return;
            }

            var importer = (TextureImporter)assetImporter;
            importer.textureType = TextureImporterType.Sprite;
            importer.spriteImportMode = SpriteImportMode.Single;
        }
    }
}
