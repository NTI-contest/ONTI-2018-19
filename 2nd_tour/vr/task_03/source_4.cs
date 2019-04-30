using System;
using System.Collections.Generic;
using UnityEngine;
using Random = UnityEngine.Random;

public class TreeMazeGenerator
{
  private struct CellToVisit
  {
    public readonly int Row;
    public readonly int Column;
    public readonly Direction MoveMade;

    public CellToVisit(int row, int column, Direction move)
    {
      Row = row;
      Column = column;
      MoveMade = move;
    }
  }

  private int RowCount { get; set; }
  private int ColumnCount { get; set; }

  private readonly MazeCell[, ] mMaze;
  private readonly List<CellToVisit> mCellsToVisit = new List<CellToVisit> ();

  public TreeMazeGenerator(int rows, int columns)
  {
    RowCount = Mathf.Abs(rows);
    if (RowCount == 0)
      RowCount = 1;
    ColumnCount = Mathf.Abs(columns);
    if (ColumnCount == 0)
      ColumnCount = 1;

    mMaze = new MazeCell[rows, columns];
    for (var row = 0; row < rows; ++row)
    for (var column = 0; column < columns; ++column)
      mMaze[row, column] = new MazeCell();
  }

  public MazeCell GetMazeCell(int row, int column)
  {
    if (row >= 0 && column >= 0 && row < RowCount && column < ColumnCount)
      return mMaze[row, column];
    throw new ArgumentOutOfRangeException();
  }

  public void GenerateMaze ()
  {
    var movesAvailable = new Direction[4];
    mCellsToVisit.Add(new CellToVisit(Random.Range(0, RowCount), 
    Random.Range(0, ColumnCount), Direction.Start));
    while (mCellsToVisit.Count > 0) {
      var movesAvailableCount = 0;
      var ctv = mCellsToVisit[mCellsToVisit.Count - 1];

      //check move right
      if (ctv.Column + 1 < ColumnCount 
        && !GetMazeCell(ctv.Row, ctv.Column + 1).IsVisited 
        && !IsCellInList(ctv.Row, ctv.Column + 1)) {
        movesAvailable[movesAvailableCount] = Direction.Right;
        ++movesAvailableCount;
      }
      else if (!GetMazeCell(ctv.Row, ctv.Column).IsVisited && 
        ctv.MoveMade != Direction.Left) {
        GetMazeCell(ctv.Row, ctv.Column).WallRight = true;
        if (ctv.Column + 1 < ColumnCount)
          GetMazeCell(ctv.Row,ctv.Column+1).WallLeft = true;
      }

      //check move forward
      if (ctv.Row + 1 < RowCount 
        && !GetMazeCell(ctv.Row + 1, ctv.Column).IsVisited 
        && !IsCellInList(ctv.Row + 1, ctv.Column)){
        movesAvailable[movesAvailableCount] = Direction.Front;
        ++movesAvailableCount;
      }
      else if (!GetMazeCell(ctv.Row, ctv.Column).IsVisited 
        && ctv.MoveMade != Direction.Back) {
        GetMazeCell(ctv.Row, ctv.Column).WallFront = true;
        if (ctv.Row + 1 < RowCount)
          GetMazeCell(ctv.Row+1,ctv.Column).WallBack = true;
      }

      //check move left
      if(ctv.Column > 0 && ctv.Column - 1 >= 0 
        && !GetMazeCell(ctv.Row, ctv.Column - 1).IsVisited 
        && !IsCellInList(ctv.Row, ctv.Column - 1)){
        movesAvailable[movesAvailableCount] = Direction.Left;
        ++movesAvailableCount;
      }
      else if (!GetMazeCell(ctv.Row, ctv.Column).IsVisited 
        && ctv.MoveMade != Direction.Right){
        GetMazeCell(ctv.Row, ctv.Column).WallLeft = true;
        if (ctv.Column > 0 && ctv.Column - 1 >= 0)
          GetMazeCell(ctv.Row, ctv.Column - 1).WallRight = true;
      }

      //check move backward
      if (ctv.Row > 0 && ctv.Row - 1 >= 0 && !GetMazeCell(ctv.Row - 1, ctv.Column).IsVisited && 
        !IsCellInList(ctv.Row - 1, ctv.Column)) {
        movesAvailable[movesAvailableCount] = Direction.Back;
        ++movesAvailableCount;
      }
      else if (!GetMazeCell(ctv.Row, ctv.Column).IsVisited 
        && ctv.MoveMade != Direction.Front) {
        GetMazeCell(ctv.Row, ctv.Column).WallBack = true;
        if (ctv.Row > 0 && ctv.Row - 1 >= 0)
          GetMazeCell(ctv.Row - 1, ctv.Column).WallFront = true;
      }

      if (!GetMazeCell(ctv.Row, ctv.Column).IsVisited && movesAvailableCount == 0)
        GetMazeCell(ctv.Row, ctv.Column).IsGoal = true;
      GetMazeCell(ctv.Row, ctv.Column).IsVisited = true;

      if (movesAvailableCount > 0) {
        switch (movesAvailable[Random.Range(0, movesAvailableCount)]) {
        case Direction.Start:
          break;
        case Direction.Right:
          mCellsToVisit.Add(new CellToVisit(ctv.Row, ctv.Column + 1, Direction.Right));
          break;
        case Direction.Front:
          mCellsToVisit.Add(new CellToVisit(ctv.Row + 1, ctv.Column, Direction.Front));
          break;
        case Direction.Left:
          mCellsToVisit.Add(new CellToVisit(ctv.Row, ctv.Column - 1, Direction.Left));
          break;
        case Direction.Back:
          mCellsToVisit.Add(new CellToVisit(ctv.Row - 1, ctv.Column, Direction.Back));
          break;
        default:
          throw new ArgumentOutOfRangeException();
        }
      }
      else
        mCellsToVisit.Remove(ctv);
    }
  }

  private bool IsCellInList(int row, int column)
  {
    return mCellsToVisit.FindIndex(other => other.Row == row 
    && other.Column == column) >= 0;
  }
}