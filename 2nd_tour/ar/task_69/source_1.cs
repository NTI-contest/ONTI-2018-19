using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class GridMaker : MonoBehaviour {

	public GameObject cell;

	static float widthf;
	static float heightf;

	public InputField xcount;
	public InputField ycount;
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    public void reload()
    {
        Application.LoadLevel("main");
    }
	public void clear(){

		GameObject grid = GameObject.Find("Grid");
		grid.transform.localScale = new Vector3(1,1,1);

		foreach (Transform child in grid.transform)
			{
				GameObject.Destroy(child.gameObject);
			  //child is your child transform
			}

	}

	public void generate(){

		clear();
		string width_str = xcount.text;
		string height_str = ycount.text;


		int width = int.Parse(width_str);
		int height = int.Parse(height_str);

		widthf = 5.0f;
		heightf = 5.0f;

		float genx = 0;
		float geny = 0;
		float genz = 0;

		float x_step = cell.transform.localScale.x;
		float y_step = cell.transform.localScale.z;

		for (int j = 0; j < height; j++)
		{
			genx = 0;
			for (int i = 0; i < width; i++)
			{
					Vector3 pos = new Vector3(genx, genz, geny);
					GameObject new_cell = Instantiate (cell, pos, cell.transform.rotation);
					new_cell.name = "cell" + i.ToString() + j.ToString();
					new_cell.SetActive(true);
					new_cell.transform.parent = GameObject.Find("Grid").transform;
					new_cell.transform.localPosition = pos;
					genx += x_step;
			}
			geny += y_step;

		}
		GridTransform.x_count = width;
		GridTransform.y_count = height;
		GridTransform.transform = true;
		SynFromJson.colorise = true;
	}
}