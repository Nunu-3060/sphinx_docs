using System;
using UnityEngine;

namespace EditorIntro
{
    /// <summary>
    /// 最小値と最大値の組を表す型です。
    /// 第 7 章の MinMaxRangeDrawer で、Inspector ウィンドウの表示をカスタマイズします。
    /// </summary>
    [Serializable]
    public struct MinMaxRange
    {
        [SerializeField] private float min;
        [SerializeField] private float max;

        public MinMaxRange(float min, float max)
        {
            this.min = min;
            this.max = max;
        }

        public float Min => min;
        public float Max => max;

        /// <summary>min 以上 max 以下の乱数を返します。</summary>
        public float GetRandomValue()
        {
            return UnityEngine.Random.Range(min, max);
        }
    }
}
