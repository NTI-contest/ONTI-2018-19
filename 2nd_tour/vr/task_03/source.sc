using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class AutoBallControl : BallControl
{
    private int colCount;
    private int rowCount;
    private int currentPath = 0, currentVertex = 0;
    private float width = 0;
    private float height = 0;

    private readonly List<List<int>> g = new List<List<int>>();
    private readonly List<List<List<int>>> paths = new List<List<List<int>>>();
    private readonly List<List<int>> sequences = new List<List<int>>();

    private const float Step = 0.751f;
    private List<int> visitOrder;

    private int GetVertex(int column, int row)
    {
        return column * rowCount + row;
    }

    private List<int> GetPath(int u, int v)
    {
        var dists = new List<int>();
        dists.AddRange(Enumerable.Repeat(0, colCount * rowCount));
        var prev = new List<int>();
        prev.AddRange(Enumerable.Repeat(0, colCount * rowCount));
        for (var i = 0; i < dists.Count; ++i)
            dists[i] = 10000000;
        dists[u] = 0;
        prev[u] = -1;

        var q = new Queue<int>();
        q.Enqueue(u);
        while (q.Count > 0) {
            var w = q.Dequeue();
            for (var i = 0; i < g[w].Count; ++i) {
                if (dists[g[w][i]] > dists[w] + 1) {
                    dists[g[w][i]] = dists[w] + 1;
                    prev[g[w][i]] = w;
                    q.Enqueue(g[w][i]);
                }
            }
        }

        var path = new List<int>();
        var t = v;
        while (t != -1) {
            path.Add(t);
            t = prev[t];
        }

        path.Reverse();
        return path;
    }

    public override void SetMaze()
    {
        width = MazeDescription.CellWidth;
        height = MazeDescription.CellHeight;

        var maxCol = 0;
        var maxRow = 0;
        foreach (var cell in MazeDescription.Cells) {
            maxCol = Math.Max(cell.Column, maxCol);
            maxRow = Math.Max(cell.Row, maxRow);
        }

        rowCount = maxRow + 1;
        colCount = maxCol + 1;

        var c = new List<int>();
        for (var i = 0; i < colCount * rowCount; ++i)
            g.Add(new List<int>());
        foreach (var cell in MazeDescription.Cells) {
            var v = GetVertex(cell.Column, cell.Row);
            if (cell.CanMoveRight) {
                var u = GetVertex(cell.Column + 1, cell.Row);
                g[v].Add(u);
                g[u].Add(v);
            }

            if (cell.CanMoveForward) {
                var u = GetVertex(cell.Column, cell.Row + 1);
                g[v].Add(u);
                g[u].Add(v);
            }

            if (cell.HasCoin || cell.Row == 0 && cell.Column == 0)
                c.Add(v);
        }

        for (var i = 0; i < c.Count; ++i) {
            paths.Add(new List<List<int>>());
            for (var j = 0; j < c.Count; ++j)
                paths[i].Add(new List<int>());
        }

        for (var i = 0; i < c.Count; ++i) {
            for (var j = 0; j < c.Count; ++j) {
                if (i == j) continue; // TODO
                var path = GetPath(c[i], c[j]);
                paths[i][j] = path;
            }
        }

        visitOrder = GetBestPathOrder();
    }

    private KeyValuePair<int, int> GetRowColumn(int vertex)
    {
        return new KeyValuePair<int, int>(vertex % rowCount, vertex / rowCount);
    }

    private List<int> GetBestPathOrder()
    {
        var visited = new List<bool>();
        visited.AddRange(Enumerable.Repeat(false, paths.Count));
        visited[0] = true;
        var initialSequence = new Stack<int>();
        initialSequence.Push(0);
        GenerateAllPathOrderVariants(visited, initialSequence);

        List<int> bestPathOrder = null;
        var bestCost = 0;
        foreach (var sequence in sequences) {
            var cost = 0;
            for (var j = 0; j < sequence.Count - 1; ++j)
                cost += paths[sequence[j]][sequence[j + 1]].Count;

            if (bestPathOrder == null || cost < bestCost) {
                bestCost = cost;
                bestPathOrder = sequence;
            }
        }
        Debug.Assert(bestPathOrder != null);

        return bestPathOrder;
    }

    private static List<int> PathStackToList(IEnumerable<int> pathStack)
    {
        var clonedStack = new Stack<int>(new Stack<int>(pathStack));
        var path = new List<int>();
        while (clonedStack.Count > 0)
            path.Add(clonedStack.Pop());
        path.Reverse();
        return path;
    }

    private void GenerateAllPathOrderVariants(IList<bool> visited, Stack<int> sequence)
    {
        if (sequence.Count == visited.Count) {
            sequences.Add(PathStackToList(sequence));
            return;
        }

        for (var i = 0; i < paths.Count; ++i) {
            if (!visited[i]) {
                visited[i] = true;
                sequence.Push(i);
                GenerateAllPathOrderVariants(visited, sequence);
                sequence.Pop();
                visited[i] = false;
            }
        }
    }

    private void DebugPrintPath()
    {
        for (var i = 0; i < paths.Count - 1; ++i) {
            for (var j = 0; j < paths[i][i + 1].Count; ++j) {
                var rowCol = GetRowColumn(paths[i][i + 1][j]);
            }
        }
    }

    public override int GetMove(float x, float y)
    {
        if (currentPath == paths.Count - 1)
            return 0;
        var path = paths[visitOrder[currentPath]][visitOrder[currentPath + 1]];
        var rowCol = GetRowColumn(path[currentVertex]);
        var targetY = rowCol.Key * height;
        var targetX = rowCol.Value * width;

        var dx = x - targetX;
        var dy = y - targetY;
        if (dx * dx + dy * dy < Step * Step) {
            if (path[currentVertex] == path[path.Count - 1]) {
                ++currentPath;
                currentVertex = 0;
            }
            else
                ++currentVertex;
        }

        if (Math.Abs(dx) > Math.Abs(dy))
            return dx > 0 ? MoveTypeLeft : MoveTypeRight;
        return dy > 0 ? MoveTypeBottom : MoveTypeTop;
    }
}



