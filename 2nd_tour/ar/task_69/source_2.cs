using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridTransform : MonoBehaviour {

	public GameObject top_left;
	//public GameObject top_right;

	//public GameObject bottom_left;
	public GameObject bottom_right;

	public GameObject grid;
	public static bool transform;
	public static int x_count;
	public static int y_count;


	// Use this for initialization
	void Start () {
		transform = false;

	}
	
	// Update is called once per frame
	void Update () {

		if (transform == true)
		{
			float top_left_x = top_left.transform.position.x;
			float top_left_y = top_left.transform.position.y;
			float top_left_z = top_left.transform.position.z;

			/*float top_right_x = top_right.transform.position.x;
			float top_right_y = top_right.transform.position.y;
			float top_right_z = top_right.transform.position.z;

			float bottom_left_x = bottom_left.transform.position.x;
			float bottom_left_y = bottom_left.transform.position.y;
			float bottom_left_z = bottom_left.transform.position.z;*/

			float bottom_right_x = bottom_right.transform.position.x;
			float bottom_right_y = bottom_right.transform.position.y;
			float bottom_right_z = bottom_right.transform.position.z;

			//Vector3 pos = top_left.transform.position;
			//grid.transform.position = pos;

			float scale_x = Mathf.Abs(top_left_x - bottom_right_x);
			float scale_y = Mathf.Abs(top_left_y - bottom_right_y);
			float scale_z = Mathf.Abs(top_left_z - bottom_right_z);


			float tx = scale_x/x_count;
			float tz = scale_z/y_count;


			grid.transform.localScale = new Vector3(tx, 1, tz);

			float pos_x = ((top_left_x + bottom_right_x)/2);
			 pos_x -= scale_x/2 - (0.5f*tx);

			float pos_y = ((top_left_y + bottom_right_y) / 2);
			// pos_y -= scale_y;

			float pos_z = ((top_left_z + bottom_right_z)/2);
			 pos_z -= scale_z/2 - (0.5f*tz);

			// Vector3 pos = bottom_left.transform.position;
			 grid.transform.localPosition = new Vector3(pos_x,
			  pos_y, pos_z);
			

		/*
		grid.transform.rotation = top_left.transform.rotation;
		
		

		grid.transform.localScale = new Vector3(scale_x, scale_y, 
		scale_z);
		//Vector3 rot = top_left.transform.rotation;*/
	}
}
}