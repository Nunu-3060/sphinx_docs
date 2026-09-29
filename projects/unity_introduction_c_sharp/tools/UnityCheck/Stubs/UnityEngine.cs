// サンプルコードの検査用に、UnityEngine の API のうち本書で使う部分だけを最小限に再現したスタブです。
// Unity の実際の動作（描画、物理演算、フレームの進行など）は再現していません。
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

namespace UnityEngine
{
    public class Object
    {
        private bool _destroyed;

        public string name { get; set; } = "";

        public static bool operator ==(Object x, Object y)
        {
            bool xNull = x is null || x._destroyed;
            bool yNull = y is null || y._destroyed;
            if (xNull || yNull)
            {
                return xNull && yNull;
            }
            return ReferenceEquals(x, y);
        }

        public static bool operator !=(Object x, Object y)
        {
            return !(x == y);
        }

        public static implicit operator bool(Object obj)
        {
            return obj != null;
        }

        public override bool Equals(object other)
        {
            return other is Object obj && this == obj;
        }

        public override int GetHashCode()
        {
            return base.GetHashCode();
        }

        public static void Destroy(Object obj, float t = 0f)
        {
            if (obj is object)
            {
                obj._destroyed = true;
            }
        }

        public static T Instantiate<T>(T original, Vector3 position, Quaternion rotation) where T : Object
        {
            return original;
        }

        public static T[] FindObjectsByType<T>(FindObjectsSortMode sortMode) where T : Object
        {
            return new T[0];
        }
    }

    public enum FindObjectsSortMode
    {
        None,
        InstanceID,
    }

    public enum PrimitiveType
    {
        Sphere,
        Capsule,
        Cylinder,
        Cube,
        Plane,
        Quad,
    }

    public sealed class GameObject : Object
    {
        public GameObject()
        {
            transform = new Transform();
        }

        public Transform transform { get; }

        public bool activeSelf { get; private set; } = true;

        public void SetActive(bool value)
        {
            activeSelf = value;
        }

        public bool CompareTag(string tag)
        {
            return false;
        }

        public static GameObject CreatePrimitive(PrimitiveType type)
        {
            return new GameObject { name = type.ToString() };
        }
    }

    public class Component : Object
    {
        private Transform _transform;

        public Transform transform => _transform ?? (_transform = this as Transform ?? new Transform());

        public GameObject gameObject { get; } = null;

        public T GetComponent<T>()
        {
            return default;
        }

        public bool TryGetComponent<T>(out T component)
        {
            component = default;
            return false;
        }

        public bool CompareTag(string tag)
        {
            return false;
        }
    }

    public class Behaviour : Component
    {
        public bool enabled { get; set; } = true;
    }

    public class MonoBehaviour : Behaviour
    {
        public CancellationToken destroyCancellationToken => CancellationToken.None;

        public Coroutine StartCoroutine(IEnumerator routine)
        {
            return new Coroutine();
        }

        public void StopCoroutine(Coroutine routine)
        {
        }
    }

    public class ScriptableObject : Object
    {
    }

    public sealed class Coroutine
    {
    }

    public class YieldInstruction
    {
    }

    public sealed class WaitForSeconds : YieldInstruction
    {
        public WaitForSeconds(float seconds)
        {
        }
    }

    public class Transform : Component
    {
        private readonly List<Transform> _children = new List<Transform>();

        public Vector3 position { get; set; }

        public Quaternion rotation { get; set; } = Quaternion.identity;

        public Vector3 localScale { get; set; } = new Vector3(1f, 1f, 1f);

        public Vector3 forward => Vector3.forward;

        public Transform parent { get; private set; }

        public int childCount => _children.Count;

        public void SetParent(Transform newParent)
        {
            parent = newParent;
            newParent._children.Add(this);
        }

        public void Rotate(float xAngle, float yAngle, float zAngle)
        {
        }

        public void Rotate(Vector3 eulers)
        {
        }
    }

    public class Renderer : Component
    {
        public bool enabled { get; set; } = true;

        public Material material { get; set; } = new Material();
    }

    public class Material : Object
    {
        public Color color { get; set; }
    }

    public class Collider : Component
    {
    }

    public enum ForceMode
    {
        Force = 0,
        Acceleration = 5,
        Impulse = 1,
        VelocityChange = 2,
    }

    public class Rigidbody : Component
    {
        public float mass { get; set; } = 1f;

        public Vector3 linearVelocity { get; set; }

        public void AddForce(Vector3 force, ForceMode mode = ForceMode.Force)
        {
        }
    }

    public struct ContactPoint
    {
        public Vector3 normal { get; set; }
    }

    public class Collision
    {
        public GameObject gameObject { get; } = new GameObject();

        public Vector3 relativeVelocity { get; }

        public int contactCount => 0;

        public ContactPoint GetContact(int index)
        {
            return default;
        }
    }

    public struct Color
    {
        public float r;
        public float g;
        public float b;
        public float a;

        public Color(float r, float g, float b, float a = 1f)
        {
            this.r = r;
            this.g = g;
            this.b = b;
            this.a = a;
        }

        public static Color red => new Color(1f, 0f, 0f);

        public static Color green => new Color(0f, 1f, 0f);
    }

    public struct Vector2
    {
        public float x;
        public float y;

        public Vector2(float x, float y)
        {
            this.x = x;
            this.y = y;
        }

        public override string ToString()
        {
            return string.Format(CultureInfo.InvariantCulture, "({0:F2}, {1:F2})", x, y);
        }
    }

    public struct Vector3
    {
        public float x;
        public float y;
        public float z;

        public Vector3(float x, float y, float z)
        {
            this.x = x;
            this.y = y;
            this.z = z;
        }

        public static Vector3 zero => new Vector3(0f, 0f, 0f);

        public static Vector3 forward => new Vector3(0f, 0f, 1f);

        public static Vector3 back => new Vector3(0f, 0f, -1f);

        public static Vector3 right => new Vector3(1f, 0f, 0f);

        public static Vector3 up => new Vector3(0f, 1f, 0f);

        public float sqrMagnitude => x * x + y * y + z * z;

        public float magnitude => (float)Math.Sqrt(sqrMagnitude);

        public Vector3 normalized
        {
            get
            {
                float m = magnitude;
                return m > 1e-5f ? this / m : zero;
            }
        }

        public static Vector3 operator +(Vector3 a, Vector3 b) => new Vector3(a.x + b.x, a.y + b.y, a.z + b.z);

        public static Vector3 operator -(Vector3 a, Vector3 b) => new Vector3(a.x - b.x, a.y - b.y, a.z - b.z);

        public static Vector3 operator *(Vector3 a, float d) => new Vector3(a.x * d, a.y * d, a.z * d);

        public static Vector3 operator *(float d, Vector3 a) => a * d;

        public static Vector3 operator /(Vector3 a, float d) => new Vector3(a.x / d, a.y / d, a.z / d);

        public static float Distance(Vector3 a, Vector3 b) => (a - b).magnitude;

        public static float Dot(Vector3 a, Vector3 b) => a.x * b.x + a.y * b.y + a.z * b.z;

        public static Vector3 Cross(Vector3 a, Vector3 b)
        {
            return new Vector3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
        }

        public static Vector3 Lerp(Vector3 a, Vector3 b, float t)
        {
            t = Mathf.Clamp01(t);
            return a + (b - a) * t;
        }

        public override string ToString()
        {
            return string.Format(CultureInfo.InvariantCulture, "({0:F2}, {1:F2}, {2:F2})", x, y, z);
        }
    }

    public struct Quaternion
    {
        public float x;
        public float y;
        public float z;
        public float w;

        public static Quaternion identity => new Quaternion { w = 1f };

        public static Quaternion Euler(float x, float y, float z) => identity;

        public static Quaternion LookRotation(Vector3 forward) => identity;

        public static Quaternion RotateTowards(Quaternion from, Quaternion to, float maxDegreesDelta) => to;
    }

    public static class Mathf
    {
        public const float Epsilon = 1.401298E-45f;

        public static int Clamp(int value, int min, int max) => Math.Min(Math.Max(value, min), max);

        public static float Clamp01(float value) => Math.Min(Math.Max(value, 0f), 1f);

        public static int RoundToInt(float f) => (int)Math.Round(f);

        // Unity の実装と同じ判定式です。
        public static bool Approximately(float a, float b)
        {
            return Math.Abs(b - a) < Math.Max(0.000001f * Math.Max(Math.Abs(a), Math.Abs(b)), Epsilon * 8f);
        }
    }

    public static class Random
    {
        private static readonly System.Random Generator = new System.Random();

        public static float Range(float minInclusive, float maxInclusive)
        {
            return minInclusive + (float)Generator.NextDouble() * (maxInclusive - minInclusive);
        }
    }

    public static class Time
    {
        public static float deltaTime => 1f / 60f;

        public static float fixedDeltaTime => 0.02f;

        public static float time => 0f;
    }

    public static class Debug
    {
        public static void Log(object message) => Write(message);

        public static void Log(object message, Object context) => Write(message);

        public static void LogWarning(object message) => Write(message);

        public static void LogError(object message) => Write(message);

        public static void Assert(bool condition, string message)
        {
            if (!condition)
            {
                Write(message);
            }
        }

        public static void DrawRay(Vector3 start, Vector3 dir, Color color)
        {
        }

        private static void Write(object message)
        {
            Console.WriteLine(message is IFormattable f ? f.ToString(null, CultureInfo.InvariantCulture) : message?.ToString() ?? "Null");
        }
    }

    [AsyncMethodBuilder(typeof(AwaitableMethodBuilder))]
    public class Awaitable
    {
        internal Task InnerTask { get; set; } = Task.CompletedTask;

        public TaskAwaiter GetAwaiter() => InnerTask.GetAwaiter();

        public static Awaitable WaitForSecondsAsync(float seconds, CancellationToken cancellationToken = default)
        {
            return new Awaitable { InnerTask = Task.Delay(TimeSpan.FromSeconds(seconds), cancellationToken) };
        }
    }

    public struct AwaitableMethodBuilder
    {
        private AsyncTaskMethodBuilder _builder;

        public Awaitable Task => new Awaitable { InnerTask = _builder.Task };

        public static AwaitableMethodBuilder Create() => new AwaitableMethodBuilder { _builder = AsyncTaskMethodBuilder.Create() };

        public void Start<TStateMachine>(ref TStateMachine stateMachine) where TStateMachine : IAsyncStateMachine => _builder.Start(ref stateMachine);

        public void SetStateMachine(IAsyncStateMachine stateMachine) => _builder.SetStateMachine(stateMachine);

        public void SetResult() => _builder.SetResult();

        public void SetException(Exception exception) => _builder.SetException(exception);

        public void AwaitOnCompleted<TAwaiter, TStateMachine>(ref TAwaiter awaiter, ref TStateMachine stateMachine)
            where TAwaiter : INotifyCompletion
            where TStateMachine : IAsyncStateMachine
        {
            _builder.AwaitOnCompleted(ref awaiter, ref stateMachine);
        }

        public void AwaitUnsafeOnCompleted<TAwaiter, TStateMachine>(ref TAwaiter awaiter, ref TStateMachine stateMachine)
            where TAwaiter : ICriticalNotifyCompletion
            where TStateMachine : IAsyncStateMachine
        {
            _builder.AwaitUnsafeOnCompleted(ref awaiter, ref stateMachine);
        }
    }

    [AttributeUsage(AttributeTargets.Field)]
    public sealed class SerializeField : Attribute
    {
    }

    [AttributeUsage(AttributeTargets.Field, AllowMultiple = true)]
    public class PropertyAttribute : Attribute
    {
    }

    public sealed class HeaderAttribute : PropertyAttribute
    {
        public HeaderAttribute(string header)
        {
        }
    }

    public sealed class TooltipAttribute : PropertyAttribute
    {
        public TooltipAttribute(string tooltip)
        {
        }
    }

    public sealed class RangeAttribute : PropertyAttribute
    {
        public RangeAttribute(float min, float max)
        {
        }
    }

    public sealed class MinAttribute : PropertyAttribute
    {
        public MinAttribute(float min)
        {
        }
    }

    public sealed class SpaceAttribute : PropertyAttribute
    {
        public SpaceAttribute(float height)
        {
        }
    }

    public sealed class TextAreaAttribute : PropertyAttribute
    {
        public TextAreaAttribute(int minLines, int maxLines)
        {
        }
    }

    [AttributeUsage(AttributeTargets.Class, AllowMultiple = true)]
    public sealed class RequireComponent : Attribute
    {
        public RequireComponent(Type requiredComponent)
        {
        }
    }

    [AttributeUsage(AttributeTargets.Class)]
    public sealed class CreateAssetMenuAttribute : Attribute
    {
        public string fileName { get; set; }

        public string menuName { get; set; }
    }
}

namespace UnityEngine.SceneManagement
{
    public struct Scene
    {
        public string name => "SampleScene";
    }

    public static class SceneManager
    {
        public static Scene GetActiveScene() => default;

        public static void LoadScene(string sceneName)
        {
        }
    }
}
