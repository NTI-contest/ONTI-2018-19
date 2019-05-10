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
               var localLocation = GeoUtils.GetPosition(location.latitude, 
                                                        location.longitude);
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