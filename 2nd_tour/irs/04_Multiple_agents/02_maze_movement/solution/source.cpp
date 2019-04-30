// Состояние робота - это пара чисел cell и dir робота
// Количество различных состояний робота для лабиринта размером AxB:
// K_robot = 4*A*B
// Состояние лабиринита - это упорядоченный набор состояний роботов
// Количество различных состояний робота для N роботов:
// K_maze = K_robot^N
// С ограничениями по времени и памяти программа справится с N <= 3

#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <algorithm>
#include <ctime>

using namespace std;

// Выводить ли отладочную информацию?
const bool debug = false;

// Размеры лабиринта
const int height = 8;
const int width = 8;

// Лабиринт
// adj[i] содержит массив вида {U, R, D, L}, где:
// U - номер клетки сверху от i-ой клетки
// R - номер клетки справа от i-ой клетки
// D - номер клетки снизу от i-ой клетки
// L - номер клетки слева от i-ой клетки
// Если с одной из сторон стена, то номер клетки = -1
const int adj[height * width][4] = {{-1, -1, 8, -1}, {-1, 2, 9, -1}, 
    {-1, 3, 10, 1}, {-1, -1, 11, 2}, {-1, 5, 12, -1}, {-1, 6, -1, 4}, 
    {-1, 7, -1, 5}, {-1, -1, 15, 6}, {0, -1, 16, -1}, {1, 10, -1, -1}, 
    {2, -1, -1, 9}, {3, -1, 19, -1}, {4, 13, 20, -1}, {-1, -1, -1, 12}, 
    {-1, 15, 22, -1}, {7, -1, -1, 14}, {8, 17, 24, -1}, 
    {-1, 18, -1, 16}, {-1, 19, 26, 17}, {11, -1, -1, 18}, 
    {12, -1, 28, -1}, {-1, 22, 29, -1}, {14, -1, 30, 21}, 
    {-1, -1, 31, -1}, {16, -1, 32, -1}, {-1, 26, 33, -1}, 
    {18, 27, 34, 25}, {-1, 28, -1, 26}, {20, 29, -1, 27}, 
    {21, 30, -1, 28}, {22, -1, 38, 29}, {23, -1, 39, -1}, 
    {24, -1, 40, -1}, {25, 34, 41, -1}, {26, 35, -1, 33}, 
    {-1, -1, 43, 34}, {-1, 37, 44, -1}, {-1, -1, 45, 36}, 
    {30, -1, 46, -1}, {31, -1, 47, -1}, {32, -1, 48, -1}, 
    {33, -1, -1, -1}, {-1, -1, 50, -1}, {35, -1, 51, -1}, 
    {36, -1, 52, -1}, {37, -1, 53, -1}, {38, -1, 54, -1}, 
    {39, -1, 55, -1}, {40, 49, 56, -1}, {-1, 50, -1, 48}, 
    {42, -1, -1, 49}, {43, -1, 59, -1}, {44, -1, -1, -1}, 
    {45, 54, 61, -1}, {46, 55, 62, 53}, {47, -1, 63, 54}, 
    {48, 57, -1, -1}, {-1, 58, -1, 56}, {-1, 59, -1, 57}, 
    {51, 60, -1, 58}, {-1, 61, -1, 59}, {53, -1, -1, 60},
    {54, 63, -1, -1}, {55, -1, -1, 62}};
// Количество роботов на поле
int robot_count;

// Номер клетки и направление старта роботов
vector <int> cell_start, dir_start;

// Номер клетки и направления финиша роботов
vector <int> cell_finish;

// Количество возможных состояний лабиринта
int state_count = 0;

// used[i] - просмотрено i-ое состояние лабиринта или нет
vector <bool> used;
// used[i] - из какого состояния получили i-ое состояние лабиринта
vector <int> from;
// actions[i] - какое действия совершили роботы, чтобы перейти в i-ое 
// состояние лабиринта
// вместо
vector <char*> actions;

// path[i] - путь для i-ого робота
vector <string> path;

// Состояние лабиринта в которое перешли роботы, когда оказались на точках финиша
int state_finish = -1;

// Переводит символьное представление направления в числовое
// 'U' -> 0
// 'R' -> 1
// 'D' -> 2
// 'L' -> 3
int dir_to_int(char c) {
    if (c == 'U')
        return 0;
    else if (c == 'R')
        return 1;
    else if (c == 'D')
        return 2;
    else if (c == 'L')
        return 3;
    else {
        cerr << "Invalid direction!: " << c << "\n";
        throw(1);
    }
}

// Переводит вектор состоний робота в числовое представление
int state_to_int(vector <pair <int, int>> state) {
    int res = 0;
    for (auto el : state) {
        res *= (4 * height * width);
        res += el.first * 4 + el.second;
    }
    return res;
}

// Переводит числовое представление состояния лабиринта в вектор состояний робота
vector <pair <int, int>> state_to_vector(int state) {
    vector <pair <int, int>> res;
    while (res.size() != robot_count) {
        res.emplace_back(state % (4 * height * width) / 4, state 
            % (4 * height * width) % 4);
        state /= (4 * height * width);
    }
    reverse(res.begin(), res.end());
    return res;
}

// Возвращает следующую комбинация для строки (например FFF -> FFL; FFR -> FLF; 
// RRR -> END)
// (S - бездействовать)
string next_combination(string s) {
    int i = s.size() - 1;
    bool cont = true;
    while (cont && i >= 0) {
        cont = false;
        if (s[i] == 'S')
            s[i] = 'F';
        else if (s[i] == 'F')
            s[i] = 'L';
        else if (s[i] == 'L')
            s[i] = 'R';
        else if (s[i] == 'R') {
            s[i] = 'S';
            cont = true;
            --i;
        }
    }
    if (i < 0)
        return "END";
    else
        return s;
}

// Считывание данных
void get_data() {
    cin >> robot_count;
    cell_start.resize(robot_count);
    dir_start.resize(robot_count);
    cell_finish.resize(robot_count);
    state_count = 1;
    for (int robot = 0; robot < robot_count; ++robot) {
        int xs, ys, xf, yf;
        char ds;
        cin >> xs >> ys >> ds >> xf >> yf;
        cell_start[robot] = xs + ys * width;
        cell_finish[robot] = xf + yf * width;
        dir_start[robot] = dir_to_int(ds);
        state_count *= 4 * height * width;
    }
}

// Вывод входных данных
void print_data() {
    cout << "--------------------\n";
    for (int robot = 0; robot < robot_count; ++robot) {
        cout << "Robot " << robot + 1 << endl;
        cout << "start: " << cell_start[robot] << " " << dir_start[robot] << endl;
        cout << "finish: " << cell_finish[robot] << endl;
        cout << "--------------------\n";
    }
};

// Поиск в ширину по состояниям лабиринта
void bfs() {
    if (debug)
        cout << "bfs started\n";
    used.resize(state_count, false);
    from.resize(state_count, -1);
    actions.resize(state_count);
    vector <pair <int, int>> cur;
    for (int robot = 0; robot < robot_count; ++robot)
        cur.emplace_back(cell_start[robot], dir_start[robot]);
    used[state_to_int(cur)] = true;
    queue <int> q;
    q.push(state_to_int(cur));
    while (!q.empty()) {
        int cur_st = q.front();
        cur = state_to_vector(cur_st);
        q.pop();
        // Проверить, если все роботы на точках финиша
        bool finish = true;
        for (int robot = 0; robot < robot_count; ++robot)
            if (cur[robot].first != cell_finish[robot]) {
                finish = false;
                break;
            }
        if (finish) {
            state_finish = state_to_int(cur);
            break;
        }
        // перебираем все строки действий вида FFF, FFL, FFR, ...
        string s = string(robot_count, 'S');
        while (s != "END") {
            auto next = cur;
            bool ok = true;
            for (int robot = 0; robot < robot_count; ++robot) {
                if (s[robot] == 'S') {
                    if (cur[robot].first == cell_finish[robot]) {
                        int next_dir = next[robot].second;
                        int next_cell = next[robot].first;
                    } else {
                        ok = false;
                        break;
                    }
                } else if (from[cur_st] == -1 || actions[cur_st][robot] != 'S') {
                    if (s[robot] == 'F'){
                        int next_dir = next[robot].second;
                        int next_cell = adj[next[robot].first][next_dir];
                        if (next_cell == -1) {
                            ok = false;
                            break;
                        }
                        next[robot].first = next_cell;
                        next[robot].second = next_dir;
                    } else if (s[robot] == 'L') {
                        int next_dir = (next[robot].second + 3) % 4;
                        int next_cell = adj[next[robot].first][next_dir];
                        if (next_cell == -1) {
                            ok = false;
                            break;
                        }
                        next[robot].first = next_cell;
                        next[robot].second = next_dir;
                    } else if (s[robot] == 'R') {
                        int next_dir = (next[robot].second + 1) % 4;
                        int next_cell = adj[next[robot].first][next_dir];
                        if (next_cell == -1) {
                            ok = false;
                            break;
                        }
                        next[robot].first = next_cell;
                        next[robot].second = next_dir;
                    }
                } else {
                    ok = false;
                    break;
                }
            }
            for (int i = 0; i < robot_count; ++i)
                for (int j = 0; j < robot_count; ++j) {
                    if (i != j && next[i].first == cur[j].first && 
                        next[i].second != next[j].second) {
                        ok = false;
                        break;
                    }
                    if (i != j && next[i].first == next[j].first) {
                        ok = false;
                        break;
                    }
                }
            if (ok && !used[state_to_int(next)]) {
                used[state_to_int(next)] = true;
                int state_int = state_to_int(next);
                // convert string to C-string
                actions[state_int] = new char[robot_count + 1];
                for (int i = 0; i < robot_count; ++i)
                    actions[state_int][i] = s[i];
                actions[state_int][robot_count] = '\n';
                from[state_to_int(next)] = state_to_int(cur);
                q.push(state_to_int(next));
            }
            s = next_combination(s);
        }
    }
    if (debug)
        cout << "bfs finished\n";
}

void print_path() {
    if (debug)
        cout << state_finish << endl;
    if (state_finish == -1) {
        cout << "No solution!\n";
    } else {
        path.resize(robot_count, "");
        int cur_state = state_finish;
        while (from[cur_state] != -1) {
            for (int robot = 0; robot < robot_count; ++robot)
                path[robot].push_back(actions[cur_state][robot]);
            cur_state = from[cur_state];
        }
        for (int robot = 0; robot < robot_count; ++robot) {
            reverse(path[robot].begin(), path[robot].end());
            path[robot] += 'S';
            path[robot] = path[robot].substr(0, path[robot].find('S'));
            cout << path[robot] << endl;
        }
    }
}

int main() {
    get_data();
    if (debug)
        print_data();
    unsigned int start_time = clock();
    bfs();
    print_path();
    if (debug) {
        unsigned int end_time = clock();
        cout << "Execution time: " << (end_time - start_time) / 1000.0 << " s" << endl;
    }
    return 0;
}