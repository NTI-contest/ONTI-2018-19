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
       var H = new Vector3(D.y * S.z - D.z * S.y, D.x * S.z - D.z * S.x, 
                           D.x * S.y - D.y * S.x);
       return Vector3.Distance(Vector3.zero, H) / Vector3.Distance(Vector3.zero, S);
   }

   private static Vector3 Project(Vector3 A, Vector3 S, Vector3 B)
   {
       float Lam = -(S.x * (A.x - B.x) + S.y * (A.y - B.y) + S.z * (A.z - B.z)) / 
                   (S.x * S.x + S.y * S.y + S.z * S.z);
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

       if (Distance(points[l0].position, 
                    points[(l0 + 1) % 4].position, 
                    points[(l0 + 2) % 4].position) <
           Distance(points[l0].position, 
                    points[(l0 + 1) % 4].position, 
                    points[(l0 + 3) % 4].position)
       )
       {
           _vertix[2] = Project(points[(l0 + 2) % 4].position, delta, 
                                points[(l0 + 1) % 4].position);
           _vertix[3] = Project(points[(l0 + 2) % 4].position, delta, 
                                points[l0].position);
       }
       else
       {
           _vertix[2] = Project(points[(l0 + 3) % 4].position, delta, 
                                points[(l0 + 1) % 4].position);
           _vertix[3] = Project(points[(l0 + 3) % 4].position, delta, 
                               points[l0].position);
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
       return new Vector3(a.y * b.z - a.z * b.y, -a.x * b.z + b.x * a.z, 
                          a.x * b.y - b.x * a.y);
   }

   private void UpdateChild()
   {
       itemsParent.transform.position = _vertix[0];
       itemsParent.transform.LookAt(_vertix[1], MultiplyVector(_vertix[1], _vertix[2]));
       foreach (var item in gridObject)
       {
           if (!(System.Math.Abs(item.scriptable.scale.x) > Tolerance) ||
               !(System.Math.Abs(item.scriptable.scale.y) > Tolerance) || 
               cellsCount.x == 0 || cellsCount.y == 0) continue;
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
