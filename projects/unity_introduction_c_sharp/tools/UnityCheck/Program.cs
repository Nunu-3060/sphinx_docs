// 第 1 部のサンプルコードを Unity なしで実行し、Debug.Log の出力を表示する検査用プログラムです。
// 本文に掲載している「実行結果」が正しいことを確認するために使います。
using System;
using System.Globalization;
using System.Reflection;
using System.Text;

namespace UnityCheck
{
    public static class Program
    {
        private static readonly Type[] _sampleTypes =
        {
            typeof(HelloWorld),
            typeof(VariableSample),
            typeof(OperatorSample),
            typeof(ControlFlowSample),
            typeof(LoopSample),
            typeof(ArraySample),
            typeof(CollectionSample),
            typeof(MethodSample),
            typeof(ClassSample),
            typeof(InheritanceSample),
            typeof(EnumSample),
            typeof(GenericSample),
            typeof(DelegateSample),
            typeof(ExceptionSample),
            typeof(VectorSample),
        };

        public static void Main()
        {
            Console.OutputEncoding = Encoding.UTF8;
            CultureInfo.CurrentCulture = new CultureInfo("ja-JP");

            foreach (Type type in _sampleTypes)
            {
                Console.WriteLine($"==== {type.Name} ====");
                object instance = Activator.CreateInstance(type);
                MethodInfo start = type.GetMethod("Start", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
                start.Invoke(instance, null);
            }
        }
    }
}
