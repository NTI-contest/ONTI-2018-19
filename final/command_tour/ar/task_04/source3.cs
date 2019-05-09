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