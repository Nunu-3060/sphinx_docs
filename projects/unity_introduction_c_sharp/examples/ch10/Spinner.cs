// 第 10 章 Unity スクリプトの基本
// アタッチした GameObject を、Y 軸を中心に回転させ続けるコンポーネントです。
// 使い方: シーンに Cube を作成してアタッチし、Play ボタンを押します。
//         回転の速さは Inspector ウィンドウの Degrees Per Second で変更できます。
using UnityEngine;

public class Spinner : MonoBehaviour
{
    // 1 秒あたりに回転する角度（度）です。
    [SerializeField] private float _degreesPerSecond = 90f;

    // Update は毎フレーム 1 回呼ばれます。
    private void Update()
    {
        // transform は、このコンポーネントがアタッチされている GameObject の Transform です。
        // Time.deltaTime を掛けると、フレームレートに関係なく 1 秒あたり一定の角度で回転します（第 11 章）。
        transform.Rotate(0f, _degreesPerSecond * Time.deltaTime, 0f);
    }
}
