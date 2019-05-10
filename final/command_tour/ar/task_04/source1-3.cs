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