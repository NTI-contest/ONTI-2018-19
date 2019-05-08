using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class GridGenerator : MonoBehaviour
{
   // Use this for initialization
   public Transform[] points;
   public Transform itemsParent;
   public List<float> distance;
   public LineRenderer lr, lrCells;
   public Vector2Int cellsCount;
   public Vector2 cellSize;

   public List<GridObject> gridObject = new List<GridObject>();

   private readonly Vector3[] _vertix = new Vector3[4];

   private const double Tolerance = 0.00001;

   private void Start()
   {
       foreach (var item in gridObject)
       {
           item.obj = Instantiate(item.scriptable.prefab, itemsParent);
       }
   }

   public void AddItem(GridChildScriptable item, Vector2Int pos)
   {
       var g = new GridObject(item, pos);
       g.obj = Instantiate(g.scriptable.prefab, itemsParent);
       gridObject.Add(g);
       UpdateChild();
   }

   private void Update()
   {
       GenerateGrid();
   }

   private static float Distance(Vector3 A, Vector3 B, Vector3 C)
   {
       var S = B - A;
       var D = C - A;
       var H = new Vector3(D.y * S.z - D.z * S.y, D.x * S.z - D.z * S.x, D.x * S.y - D.y * S.x);
       return Vector3.Distance(Vector3.zero, H) / Vector3.Distance(Vector3.zero, S);
   }

   private static Vector3 Project(Vector3 A, Vector3 S, Vector3 B)
   {
       float Lam = -(S.x * (A.x - B.x) + S.y * (A.y - B.y) + S.z * (A.z - B.z)) / (S.x * S.x + S.y * S.y + S.z * S.z);
       return new Vector3(Lam * S.x + A.x, Lam * S.y + A.y, Lam * S.z + A.z);
   }

   private void UpdateDistance()
   {
       for (int i = 0; i < points.Length; i++)
       {
           distance[i] = Vector3.Distance(points[i].position, points[(i + 1) % 4].position);
       }
   }

   private void GenerateGrid()
   {
       UpdateDistance();
       int l0 = distance.FindIndex(x => Math.Abs(x - distance.Max()) < Tolerance);
       _vertix[0] = points[l0].position;
       _vertix[1] = points[(l0 + 1) % 4].position;
       Vector3 delta = points[l0].position - points[(l0 + 1) % 4].position;

       if (Distance(points[l0].position, points[(l0 + 1) % 4].position, points[(l0 + 2) % 4].position) <
           Distance(points[l0].position, points[(l0 + 1) % 4].position, points[(l0 + 3) % 4].position)
       )
       {
           _vertix[2] = Project(points[(l0 + 2) % 4].position, delta, points[(l0 + 1) % 4].position);
           _vertix[3] = Project(points[(l0 + 2) % 4].position, delta, points[l0].position);
       }
       else
       {
           _vertix[2] = Project(points[(l0 + 3) % 4].position, delta, points[(l0 + 1) % 4].position);
           _vertix[3] = Project(points[(l0 + 3) % 4].position, delta, points[l0].position);
       }

       for (int i = l0; i < 3; i++)
       {
           Vector3 t = _vertix[0];
           _vertix[0] = _vertix[1];
           _vertix[1] = _vertix[2];
           _vertix[2] = _vertix[3];
           _vertix[3] = t;
       }

       lr.SetPositions(_vertix);
       DrawCells(_vertix);

       UpdateChild();
   }

   private void DrawCells(Vector3[] p)
   {
       var lrPoints = new List<Vector3>();
       for (int i = 0; i < cellsCount.x; i++)
       {
           lrPoints.Add(Vector3.Lerp(p[0], p[1], (float) i / cellsCount.x));
           lrPoints.Add(Vector3.Lerp(p[3], p[2], (float) i / cellsCount.x));
           i++;
           lrPoints.Add(Vector3.Lerp(p[3], p[2], (float) i / cellsCount.x));
           lrPoints.Add(Vector3.Lerp(p[0], p[1], (float) i / cellsCount.x));
       }

       for (int i = 0; i < cellsCount.y; i++)
       {
           lrPoints.Add(Vector3.Lerp(p[1], p[2], (float) i / cellsCount.y));
           lrPoints.Add(Vector3.Lerp(p[0], p[3], (float) i / cellsCount.y));
           i++;
           lrPoints.Add(Vector3.Lerp(p[0], p[3], (float) i / cellsCount.y));
           lrPoints.Add(Vector3.Lerp(p[1], p[2], (float) i / cellsCount.y));
       }

       cellSize.x = Vector3.Distance(p[0], p[3]) / cellsCount.x;
       cellSize.y = Vector3.Distance(p[0], p[1]) / cellsCount.y;
       lrCells.positionCount = lrPoints.Count;
       lrCells.SetPositions(lrPoints.ToArray());
   }

   private static Vector3 MultiplyVector(Vector3 a, Vector3 b)
   {
       return new Vector3(a.y * b.z - a.z * b.y, -a.x * b.z + b.x * a.z, a.x * b.y - b.x * a.y);
   }

   private void UpdateChild()
   {
       itemsParent.transform.position = _vertix[0];
       itemsParent.transform.LookAt(_vertix[1], MultiplyVector(_vertix[1], _vertix[2]));
       foreach (var item in gridObject)
       {
           if (!(System.Math.Abs(item.scriptable.scale.x) > Tolerance) ||
               !(System.Math.Abs(item.scriptable.scale.y) > Tolerance) || cellsCount.x == 0 ||
               cellsCount.y == 0) continue;
           var pos = Vector3.zero;
           pos.x = cellSize.x * item.gridPos.x + cellSize.x / 2;
           pos.z = cellSize.y * item.gridPos.y + cellSize.y / 2;
           item.obj.transform.localPosition = pos;
           item.obj.transform.localScale =
               Vector3.one * Mathf.Min(cellSize.x / item.scriptable.scale.x,
                   cellSize.y / item.scriptable.scale.y);
       }
   }
}



using UnityEngine;

[CreateAssetMenu(fileName = "GridChild", menuName = "scriptable/GridChild", order = 0)]
public class GridChildScriptable : ScriptableObject
{
   public GameObject prefab;
   public Vector2 scale;
}

using UnityEngine;

[System.Serializable]
public class GridObject
{
   public GridChildScriptable scriptable;
   public Vector2Int gridPos;
   public GameObject obj;

   public GridObject(GridChildScriptable scriptable, Vector2Int gridPos)
   {
       this.scriptable = scriptable;
       this.gridPos = gridPos;
   }
}


Разработано меню, в котором можно посмотреть маршруты прохода других групп. На изображении приведен пример работы приложения для квеста в котором участвуют 4 группы. Можно посмотреть маршрут каждой из них.

Рис.4.4. Меню для выбора визуализации AR-браузером маршрутов и местонахождения для нескольких экскурсионных групп. 



Оценка
Меню для выбора маршрута, который нужно показать — 10 баллов.
Графы прохождения других групп — 35 баллов.


Часть 2.  Добавление сведений о местонахождении экскурсионных групп.
Необходимо добавить в приложение фиксацию текущего положения участника, а также отображать положение своей и других групп с определенной точностью.
Критерии
На выбор отображение групп:
Группа отображается одной точкой — 35 баллов
Отображается каждый участник группы с клеточной точностью — 49 баллов
Отображается каждый участник группы с 1/10 * клеточной точностью — 70 баллов
Прочее:
Отображение участников других групп (баллы за отображение одной группы) — 
Решение
С помощью перевода из глобальных координат в локальные (относительно карты), был реализован алгоритм который с точностью в 1/10 клетки отображает положение группы на карте. Алгоритм заключается в линейном преобразовании координат, относительно верхней левой и нижней правой точек. На малых расстояниях (между крайними точками) он позволяет получать достаточно высокую точность.

Рис.4.5. Визуализация AR-браузером положения одной экскурсионной группы и ее маршрута
Оценка
Отображается каждый участник группы с 1/10 * клеточной точностью – 70 баллов
В приложении есть настройки которые отображают расположение участников других групп.

Рис.4.6. Визуализация AR-браузером положения нескольких экскурсионных групп и их   маршрутов следования 

Приложение к задаче 4.1 Часть 2. Код-основа для добавления на виртуальную карту сведений о местонахождении групп экскурсантов.

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlaceGroupsScript : MonoBehaviour
{
   private string _code;
   public GameObject groupItem;
   public GameObject map;

   private void Start()
   {
       _code = PlayerPrefs.GetString("code");
       var url = "http://org1.nti-ar.ru/groups";
       StartCoroutine(NetworkUtils.SendRequest<Result>(url, "",
           SystemInfo.deviceUniqueIdentifier, _code, Success, Error));
   }

   private void Success(Result result)
   {
       foreach (var group in result.groups)
       {
           foreach (var location in group.coords)
           {
               var localLocation = GeoUtils.GetPosition(location.latitude, location.longitude);
               var local3Location = new Vector3(localLocation.x, localLocation.y, 0.5f);
               var go = Instantiate(
                   groupItem,
                   local3Location,
                   Quaternion.Euler(0, 0, 0),
                   map.transform
               );
               go.GetComponent<Colorable>().ChangeColor(group.id);
           }
       }
   }

   private void Error(string message, long code)
   {
       Debug.Log("CODE " + code + " ERROR " + message);
   }
}

[Serializable]
public struct Result
{
   public List<GroupLocations> groups;
}

[Serializable]
public struct GroupLocations
{
   public int id;
   public List<Location> coords;
}

Задача 4.2. Разработка AR-навигатора.
Надо создать модуль приложения, отвечающий за отображение моделей достопримечательностей, а также дополнительных объектов взаимодействия. Модели отображаются в “реальном” мире, с учетом положения устройства.

Критерии:
Отображение различных моделей в режиме AR-браузера (т.е. в разных местах открываются разные модели) – 16 баллов.
3Д модели расположены на расстоянии примерно равном расстоянию до объекта на карте – 10 баллов.
На выбор отображение моделей на экране:
Объекты располагаются на экране вне зависимости от положения устройства по центру — 12 баллов.
Объекты располагаются примерно на плоскости земли (с использованием датчиков акселерометра и/или магнитометра и/или гироскопа) — 24 балла.
Предыдущий пункт + модель отображается только тогда, когда в её сторону направлена камера — 36 баллов.

Решение
Реализация отображает разные модели. Так же модели отображаются на расстоянии примерно равном расстоянию до объекта. 
Модель можно увидеть только если место находится в направлении поля зрения камеры пользователя.

Рис.4.7. Работа AR-браузера в режиме AR-навигатора и поиска артефактов
Оценка
Отображаются различные модели в режиме AR-браузера (т.е. в разных местах открываются разные модели) — 16 баллов.
3Д модели расположены на расстоянии примерно равном расстоянию до объекта на карте — 10 баллов.
Модели располагаются примерно на плоскости земли (с использованием датчиков акселерометра и/или магнитометра и/или гироскопа). + модель отображается только тогда, когда в её сторону направлена камера — 36 баллов.

Приложение к задаче 4.2 Код-основа AR-навигатора

using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Serialization;
using UnityEngine.UI;

public class ArPlaceObject : MonoBehaviour
{
   public GameObject objectHolder;
   public Text text;
   [FormerlySerializedAs("jsonFile")] public TextAsset jsonMapAsset;

   private MapPoint _nearestMapPoint;
   private string _lastPointName = "";

   private JsonMap _map;

   private void Start()
   {
       _map = JsonUtility.FromJson<JsonMap>(jsonMapAsset.text);
       UpdateNearestObjectLocation(0, 0);
   }

   private void Update()
   {
       var latitude = GPS.Instance.latitude;
       var longitude = GPS.Instance.longitude;

       UpdateNearestObjectLocation(latitude, longitude);

       if (_nearestMapPoint.name != _lastPointName)
       {
           // Deleting all children exists
           var children = new List<GameObject>();
           foreach (Transform child in objectHolder.transform) children.Add(child.gameObject);
           children.ForEach(Destroy);
          
           // Instantiate new child
           Instantiate(
               Resources.Load<GameObject>("Prefabs/" + _nearestMapPoint.name),
               objectHolder.transform
           );

           _lastPointName = _nearestMapPoint.name;
       }

       var playerPosition = GeoUtils.GetPosition(latitude, longitude);

       var nearestObjectPosition = GeoUtils.GetPosition(
           _nearestMapPoint.coords.latitude,
           _nearestMapPoint.coords.longitude);

       var diff = nearestObjectPosition - playerPosition;

       float x = diff.x / 1513f * 2480f;
       float y = diff.y / 995f * 1640f;

       text.text = "x=" + x + ";y=" + y + "; name=" + _nearestMapPoint.name + "; lat" + latitude + "; lon=" +
                   longitude;

       var objectPosition = new Vector3(x, y, 0.5f);
       objectHolder.transform.position = objectPosition;
   }

   private void UpdateNearestObjectLocation(float latitude, float longitude)
   {
       _nearestMapPoint = _map.all_points[0];
       var currentLocation = new Location(latitude, longitude);
       float shortestDistance = LocationUtils.Hoversine(currentLocation, _nearestMapPoint.coords);

       foreach (var point in _map.all_points)
       {
           var tmpDist = LocationUtils.Hoversine(currentLocation, point.coords);
           if (tmpDist > shortestDistance)
               continue;
           shortestDistance = tmpDist;
           _nearestMapPoint = point;
       }
   }
}


using UnityEngine;
using System.Collections;

public class GyroCamera : MonoBehaviour
{
   // STATE
   private float _initialYAngle = 0f;
   private float _appliedGyroYAngle = 0f;
   private float _calibrationYAngle = 0f;
   private Transform _rawGyroRotation;
   private float _tempSmoothing;

   // SETTINGS
   [SerializeField] private float _smoothing = 0.1f;

   private IEnumerator Start()
   {
       Input.gyro.enabled = true;
       Input.compass.enabled = true;
       Application.targetFrameRate = 60;

       _rawGyroRotation = new GameObject("GyroRaw").transform;
       transform.SetParent(_rawGyroRotation.transform);
       _rawGyroRotation.position = transform.position;
       _rawGyroRotation.rotation = transform.rotation;

       // Wait until gyro is active, then calibrate to reset starting rotation.
       yield return new WaitForSeconds(1);
      
       _initialYAngle = Input.compass.trueHeading;

       StartCoroutine(CalibrateYAngle());
   }

   private void Update()
   {
       ApplyGyroRotation();
       ApplyCalibration();

       transform.rotation = Quaternion.Slerp(transform.rotation, _rawGyroRotation.rotation, _smoothing);
   }

   private IEnumerator CalibrateYAngle()
   {
       _tempSmoothing = _smoothing;
       _smoothing = 1;
       _calibrationYAngle =
           _appliedGyroYAngle - _initialYAngle; // Offsets the y angle in case it wasn't 0 at edit time.
       yield return null;
       _smoothing = _tempSmoothing;
   }

   private void ApplyGyroRotation()
   {
       _rawGyroRotation.rotation = Input.gyro.attitude;
       _rawGyroRotation.Rotate(0f, 0f, 180f, Space.Self); // Swap "handedness" of quaternion from gyro.
       _rawGyroRotation.Rotate(90f, 180f, 0f,
           Space.World); // Rotate to make sense as a camera pointing out the back of your device.
       _appliedGyroYAngle = _rawGyroRotation.eulerAngles.y; // Save the angle around y axis for use in calibration.
   }

   private void ApplyCalibration()
   {
       _rawGyroRotation.Rotate(0f, -_calibrationYAngle, 0f,
           Space.World); // Rotates y angle back however much it deviated when calibrationYAngle was saved.
   }

   public void SetEnabled(bool value)
   {
       enabled = true;
       StartCoroutine(CalibrateYAngle());
   }
}