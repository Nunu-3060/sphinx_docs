using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

namespace EditorIntro.EditorScripts
{
    /// <summary>
    /// 第 11 章のサンプルです。
    /// Project Settings ウィンドウに「Editor Intro > Batch Rename」ページを追加します。
    /// </summary>
    public static class BatchRenameSettingsProvider
    {
        // SettingsProvider 属性を付けた static メソッドが返すページが、設定ウィンドウに登録されます。
        [SettingsProvider]
        public static SettingsProvider CreateProvider()
        {
            // 第 1 引数はページのパス、第 2 引数は表示先（Project Settings か Preferences か）です。
            return new SettingsProvider("Project/Editor Intro/Batch Rename", SettingsScope.Project)
            {
                label = "Batch Rename",
                activateHandler = (searchContext, rootElement) => CreateGUI(rootElement),

                // 設定ウィンドウの検索欄に入力されたとき、このページを候補にするキーワードです。
                keywords = new HashSet<string> { "Rename", "Prefix", "Digits" },
            };
        }

        private static void CreateGUI(VisualElement rootElement)
        {
            var settings = BatchRenameSettings.instance;

            var container = new VisualElement();
            container.style.paddingLeft = 10;
            container.style.paddingTop = 2;
            rootElement.Add(container);

            var title = new Label("Batch Rename");
            title.style.fontSize = 19;
            title.style.unityFontStyleAndWeight = FontStyle.Bold;
            title.style.marginBottom = 8;
            container.Add(title);

            var prefixField = new TextField("接頭辞") { value = settings.Prefix };
            prefixField.RegisterValueChangedCallback(evt =>
            {
                settings.Prefix = evt.newValue;
                settings.SaveSettings();
            });
            container.Add(prefixField);

            var startNumberField = new IntegerField("開始番号") { value = settings.StartNumber };
            startNumberField.RegisterValueChangedCallback(evt =>
            {
                settings.StartNumber = evt.newValue;

                // 範囲外の値は設定側で補正されるため、補正後の値を表示し直します。
                startNumberField.SetValueWithoutNotify(settings.StartNumber);
                settings.SaveSettings();
            });
            container.Add(startNumberField);

            var digitsField = new SliderInt("桁数", BatchRenameSettings.MinDigits, BatchRenameSettings.MaxDigits)
            {
                value = settings.Digits,
                showInputField = true,
            };
            digitsField.RegisterValueChangedCallback(evt =>
            {
                settings.Digits = evt.newValue;
                digitsField.SetValueWithoutNotify(settings.Digits);
                settings.SaveSettings();
            });
            container.Add(digitsField);
        }
    }
}
