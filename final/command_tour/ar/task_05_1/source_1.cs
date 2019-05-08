
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