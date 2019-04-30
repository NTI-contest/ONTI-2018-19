using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;

public class MazeSpawner : MonoBehaviour
{
  public GameObject Floor;
  public GameObject Wall;
  public GameObject Pillar;
  public GameObject GoalPrefab;

  public bool ReadMazeDataFromFile;

  public int SeedValue;
  public int Rows;
  public int Cols;
  public int Coins;
  public int BallEnergy;

  private void ReadInputFile()
  {
  if (ReadMazeDataFromFile) {
  var args = File.ReadAllText("input.txt").Split(' ');
  MazeDescription.SeedValue = int.Parse(args[0]);
  MazeDescription.Rows = int.Parse(args[1]);
  MazeDescription.Cols = int.Parse(args[2]);
  MazeDescription.Coins = int.Parse(args[3]);
  MazeDescription.BallEnergy = int.Parse(args[4]);
  }
  else {
  MazeDescription.SeedValue = SeedValue;
  MazeDescription.Rows = Rows;
  MazeDescription.Cols = Cols;
  MazeDescription.Coins = Coins;
  MazeDescription.BallEnergy = BallEnergy;
  }
  }

  private void Awake()
  {
  ReadInputFile();
  MazeDescription.PillarPrefab = Pillar;
  MazeDescription.WallPrefab = Wall;
  MazeDescription.CoinPrefab = GoalPrefab;

  if (MazeDescription.IsConsoleRun()) {
  var mainCamera = GameObject.FindGameObjectWithTag("MainCamera");
  if (mainCamera != null)
  mainCamera.SetActive(true);
  }

  Random.InitState(MazeDescription.SeedValue);

  var mazeDescriptionCells = new List<MazeDescriptionCell>();
  var cellsWithCoinIndexes = new List<int>();
  var mMazeGenerator = new TreeMazeGenerator(MazeDescription.Rows,
  MazeDescription.Cols);
  mMazeGenerator.GenerateMaze();
  for (var row = 0; row < MazeDescription.Rows; ++row) {
  for (var column = 0; column < MazeDescription.Cols; ++column) {
  var x = column * MazeDescription.CellWidth;
  var z = row * MazeDescription.CellHeight;
  var cell = mMazeGenerator.GetMazeCell(row, column);

  var floor = Instantiate(Floor, new Vector3(x, 0, z), Quaternion.Euler(0, 0, 0));
  floor.transform.parent = transform;

  if (cell.WallRight) {
  var wall = Instantiate(Wall, new Vector3(x + MazeDescription.CellWidth / 2, 0, z) + 
  Wall.transform.position, Quaternion.Euler(0, 90, 0));
  wall.transform.parent = transform;
  }
  if (cell.WallFront) {
  var wall = Instantiate(Wall, new Vector3(x, 0, z + MazeDescription.CellHeight / 2) + 
  Wall.transform.position, Quaternion.Euler(0, 0, 0));
  wall.transform.parent = transform;
  }
  if (cell.WallLeft) {
  var wall = Instantiate(Wall, new Vector3(x - MazeDescription.CellWidth / 2, 0, z) + 
  Wall.transform.position, Quaternion.Euler(0, 270, 0));
  wall.transform.parent = transform;
  }
  if (cell.WallBack) {
  var wall = Instantiate(Wall, new Vector3(x, 0, z - MazeDescription.CellHeight / 2) + 
  Wall.transform.position, Quaternion.Euler(0, 180, 0));
  wall.transform.parent = transform;
  }

  var mazeDescriptionCell = new MazeDescriptionCell {
  Row = row,
  Column = column,
  CanMoveBackward = !cell.WallBack,
  CanMoveLeft = !cell.WallLeft,
  CanMoveRight = !cell.WallRight,
  CanMoveForward = !cell.WallFront,
  HasCoin = false,
  };
  if (cell.IsGoal)
  cellsWithCoinIndexes.Add(mazeDescriptionCells.Count);
  mazeDescriptionCells.Add(mazeDescriptionCell);
  }
  }

  Debug.Assert(cellsWithCoinIndexes.Count >= MazeDescription.Coins);
  cellsWithCoinIndexes = cellsWithCoinIndexes.OrderBy(x => Random.value).ToList();
  for (var i = 0; i < MazeDescription.Coins; ++i) {
  var cell = mazeDescriptionCells[cellsWithCoinIndexes[i]];
  cell.HasCoin = true;
  var x = cell.Column * MazeDescription.CellWidth;
  var z = cell.Row * MazeDescription.CellHeight;
  var coin = Instantiate(GoalPrefab, new Vector3(x, 1, z), Quaternion.Euler(0, 0, 0));
  coin.transform.parent = transform;
  }

  if (Pillar != null) {
  for (var row = 0; row <= MazeDescription.Rows; ++row) {
  for (var column = 0; column <= MazeDescription.Cols; ++column) {
  var x = column * MazeDescription.CellWidth;
  var z = row * MazeDescription.CellHeight;
  var pillar = Instantiate(Pillar, new Vector3(x - MazeDescription.CellWidth / 2, 0, 
  z - MazeDescription.CellHeight / 2), Quaternion.identity);
  pillar.transform.parent = transform;
  }
  }
  }

  MazeDescription.Cells = mazeDescriptionCells;
  }
}