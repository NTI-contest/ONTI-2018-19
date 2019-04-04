

// Параметры робота
var pi = 3.141592653589793;
var d = 5.6 // Диаметр колеса, см
var l = 17.5 // База, см
var x = 0 // Начальные координаты робота
var y = 0
var a = 0

// Моторы
var mLeft = brick.motor(M4).setPower;
var mRight = brick.motor(M3).setPower;
var cpr = 360 // Показания энкодера за оборот

// Энкодеры
var eLeft = brick.encoder(E4);
var eRight = brick.encoder(E3);

// Длина клетки
var cellLength = 40 * cpr / (pi * d);

// Датчики расстояния
var svFront = brick.sensor(D1).read;
var svLeft = brick.sensor(A1).read;
var svRigth = brick.sensor(A2).read;

var readGyro = brick.gyroscope().read

function readYaw() {
  return -readGyro()[6];
}

var direction = 0; // absolute angle of direction movement
var directionOld = 0;
var azimut = 0; // we should go on azimut or turn to it
print("-------------------------------------------");

eLeft.reset();
eRight.reset();

var el = eLeft.readRawData();
var er = eRight.readRawData();
mLeft(0);
mRight(0);

//инициализация и калибровка гироскопа
brick.gyroscope().calibrate(12000);
script.wait(13000);
print("gyro inited");
brick.display().addLabel(30, 10, "Start!");
brick.display().redraw();
script.wait(1000);

var v = 50; // velocity

var ex = 0;
var ey = 0;
var encLeftOld = 0;
var encRightOld = 0;
var encLeft = 0;
var encRight = 0;
var n = 0;

// вычисление абсолютного угла относительно начального положения
function angle() {
  var sgn = 0;
  var _direction = readYaw(); // mgrad
  var dtDirection = _direction - directionOld;

  sgn = directionOld == 0 ? 0 : directionOld / Math.abs(directionOld);
  n += sgn * Math.floor(Math.abs(dtDirection / 320000));
  direction = _direction + n * 360000;
  directionOld = _direction;
}

// делаем прерывание основной программы с частотой 200Гц, 
// чтобы посчитать абсолютный угол с гироскопа
var mtimer = script.timer(50);
mtimer.timeout.connect(angle);

//поворот на угол по гироскопу _angle - относительный угол на который необходимо повернуться
function turnDirection(_angle, _v) {
  _angle = azimut + _angle;
  azimut = _angle;
  _angle = _angle * 1000; //toMGrad

  eLeft.reset();
  eRight.reset();

  var _vel = _v == undefined & 40: _v; // скорость по умолчанию
  var angleOfRotate = _angle - direction;
  var sgn = angleOfRotate == 0 ? 0 : angleOfRotate / Math.abs(angleOfRotate);
  mLeft(-_vel * sgn);
  mRight(_vel * sgn);
  eLeftOld = eLeft.read();
  eRightOld = eRight.read();
  target = 211;

  while (Math.abs(eRight.read() - eLeft.read()) / 2 < target) {
    if ((eLeft.read() - eLeftOld) == 0) && (eRight.read() - eRightOld == 0) {
      _vel += 5;
      mLeft(-_vel * sgn);
      mRight(_vel * sgn);
    }
    eLeftOld = eLeft.read();
    eRightOld = eRight.read();
    script.wait(20);
  }

  brick.motor(M3).powerOff(500);
  brick.motor(M4).powerOff(500);
  script.wait(500);
}

// проезд в перед на количество ячеек _kceel со скоростью _v 
// выравниваясь по гироскопу на угол azimut
function forward(_v, _kcell) {
  print("azimut = " + azimut);
  _alpha = azimut;
  var _vel = _v == undefined ? 40 : _v; // скорость по умолчанию
  var u = 0;
  eLeft.reset();
  eRight.reset();
  var el = Math.abs(eLeft.readRawData());
  while (Math.abs(eLeft.readRawData()) < (el + (_kcell * cellLength))) {
    u = 1.5 * (_alpha - direction / 1000);
    mLeft(_vel - u);
    mRight(_vel + u);
    script.wait(5);
  }
  brick.motor(M3).powerOff();
  brick.motor(M4).powerOff();
  script.wait(300);
}

min = function(a, b) {
  return a < b ? a : b;
}
max = function(a, b) {
  return a > b ? a : b;
}

//==============================================================================
// массив для изображения
var pic = [];

var marker_size = 5;
var total_width = 320 / 2;
var total_height = 240 / 2;
var prob = 25 * 5 * 5;

function getColor(pic, x, y) {
  return pic[y * total_width + x];
}

function squareAverage(pic, x, y, diam) {
  var sum = 0;
  var start_row = y * total_width;
  var end_row = start_row + diam * total_width;

  for (var index = start_row + x; index < end_row; index += total_width)
    for (var j = 0; j < diam; j += 1)
      sum += pic[index + j];

  return sum;
}

// lu - left-up corner. Coordinates: (x, y)
// ld - left-down corner
// ru - right-up corner
// rd - right-down corner
function getCenterColor(pic, lu, ld, ru, rd, diam) {
  var x = (lu[0] + ld[0] + ru[0] + rd[0]) >> 2;
  var y = (lu[1] + ld[1] + ru[1] + rd[1]) >> 2;
  var color = squareAverage(pic, x - diam, y - diam, diam << 1);
  return color;
}

function findGridCorners(corners, marker_size) {
  var grid_corners = [];

  var vertical_lines = [];
  var upper_line_x1 = corners[0][0];
  var upper_line_y1 = corners[0][1];
  var upper_line_x2 = corners[2][0];
  var upper_line_y2 = corners[2][1];
  var down_line_x1 = corners[1][0];
  var down_line_y1 = corners[1][1];
  var down_line_x2 = corners[3][0];
  var down_line_y2 = corners[3][1];

  var mks = 1.0 / marker_size;
  var k_ux = (upper_line_x2 - upper_line_x1) * mks;
  var k_uy = (upper_line_y2 - upper_line_y1) * mks;
  var k_dx = (down_line_x2 - down_line_x1) * mks;
  var k_dy = (down_line_y2 - down_line_y1) * mks;

  for (var i = 0; i < marker_size + 1; i += 1) {

    var up_x = upper_line_x1 + k_ux * i;
    var up_y = upper_line_y1 + k_uy * i;

    var down_x = down_line_x1 + k_dx * i;
    var down_y = down_line_y1 + k_dy * i;

    var k_x = (down_x - up_x) * mks;
    var k_y = (down_y - up_y) * mks;

    for (j = 0; j <= marker_size; j += 1) {

      var point_x = up_x + k_x * j;
      var point_y = up_y + k_y * j;

      grid_corners.push([Math.floor(point_x), Math.floor(point_y)]);
    }
  }
  return grid_corners;
}

function detectCode(pic, grid_corners, diam) {
  var calculated_colors = []
  var markerSizePlusOne = marker_size + 1;
  var shiftedDiam = diam << 8;

  for (var i = 0; i < marker_size; i += 1) {
    for (var j = 0; j < marker_size; j += 1) {
      lu_index = i * (markerSizePlusOne) + j;
      ld_index = i * (markerSizePlusOne) + j + 1;
      ru_index = (i + 1) * (markerSizePlusOne) + j;
      rd_index = (i + 1) * (markerSizePlusOne) + j + 1;

      var lu = grid_corners[lu_index];
      var ld = grid_corners[ld_index];
      var ru = grid_corners[ru_index];
      var rd = grid_corners[rd_index];

      grid_color = getCenterColor(pic, lu, ld, ru, rd, diam);
      if (grid_color < shiftedDiam) {
        calculated_colors.push(0);
      } else {
        calculated_colors.push(1);
      }
    }
  }
  return calculated_colors;
}

function findULCorner(pic, diam) {
  var color = 1;
  for (var i = 0; i < total_height; i += 1) {
    for (var j = 0; j <= i; j += 1) {
      var x = j;
      var y = i - j;
      if (getColor(pic, x, y) == 0) {
        color = squareAverage(pic, x, y, diam);
        if (color < prob) {
          return [x, y];
        }
      }
    }
  }
}

function findDLCorner(pic, diam) {
  var color = 1;
  for (var i = 0; i < total_height; i += 1) {
    for (var j = 0; j <= i; j += 1) {
      var x = j;
      var y = total_height - (i - j);
      if (getColor(pic, x, y) == 0) {
        color = squareAverage(pic, x, y - diam + 1, diam);
        if (color < prob) {
          return [x, y];
        }
      }
    }
  }
}

function findURCorner(pic, diam) {
  for (var i = 0; i < total_height; i += 1) {
    for (var j = 0; j <= i; j += 1) {
      var x = total_width - j;
      var y = i - j;
      if (getColor(pic, x, y) == 0) {
        var color = squareAverage(pic, x - diam + 1, y, diam);
        if (color < prob) {
          return [x, y];
        }
      }
    }
  }
}

function findDRCorner(pic, diam) {
  for (var i = 0; i < total_height; i += 1) {
    for (var j = 0; j <= i; j += 1) {
      var x = total_width - j;
      var y = total_height - (i - j);
      if (getColor(pic, x, y) == 0) {
        var color = squareAverage(pic, x - diam + 1, y - diam + 1, diam);
        if (color < prob) {
          return [x, y];
        }
      }
    }
  }
}

function findCorners(pic, diam) {
  return [findULCorner(pic, diam), findDLCorner(pic, diam), findURCorner(pic,
    diam), findDRCorner(pic, diam)];
}

function threshold2(level, pic, height, width) {
  var length = pic.length;
  for (var i = 0; i < length; i += 1) {
    var color = pic[i];
    if (color < level) {
      pic[i] = 0;
    } else {
      pic[i] = 255;
    }
  }

  return pic;
}

// ---------------------------------------------------------------------------------
var scale = 1;
var histogram = [];
var histSize = 256;

function calculateHistogram() {
  for (var i = 0; i < histSize; i += 1)
    histogram[i] = 0;

  var curPixelLine = 0;
  for (var i = 0; i < total_height; i += 1) {
    curPixelLine = i * total_width;
    for (var j = 0; j < total_width; j += 1)
      histogram[Math.floor(pic[curPixelLine + j])] += 1;
  }
}

// binarization using 2 elems in grayscale
var grayscale = "@#ao|-. ";
var numOfBins = grayscale.length;
var rangeBins = [];
var binCapacity = total_height * total_width / numOfBins;

function getRange() {
  for (var i = 0; i < numOfBins; i += 1)
    rangeBins[i] = 0;

  var curBin = 0;
  var curSum = 0;
  var i = 0;
  var lastIndexBin = numOfBins - 1;

  for (;
    (i < histSize) && (curBin < lastIndexBin); i += 1) {
    var diff = binCapacity - curSum;

    if (Math.abs(diff) < Math.abs(diff - histogram[i])) {
      curBin++;
      curSum = 0;
    }

    curSum += histogram[i];
    rangeBins[curBin] = i;
  }

  for (; curBin <= lastIndexBin; curBin += 1)
    rangeBins[curBin] = histSize;
}

var mapColorToLetter = [];

function initMapColorToLetter() {
  var curBin = 0;
  for (var i = 0; i < histSize; i += 1) {
    if (rangeBins[curBin] <= i) {
      curBin += 1;
    }
    mapColorToLetter[i] = grayscale[curBin];
  }
}

// Возвращает значение ARTag 
function getARTagValue() {
  source_pic = getPhoto();

  // init pic, grayscale mode
  for (var i = 0; i < total_height; i += 1) {
    for (var j = 0; j < total_width; j += 1) {
      var x = (j + i * scale * total_width) * scale;
      var p = source_pic[x];
      p = (((p & 0xff0000) >> 18) + ((p & 0xff00) >> 10) + ((p & 0xff) >> 2));
      pic[j + i * total_width] = p;
    }
  }
  calculateHistogram();
  getRange();
  initMapColorToLetter();

  var thresh = threshold2(rangeBins[1], pic, total_height, total_width);
  var corners = findCorners(thresh, 9);
  var grid_corners = findGridCorners(corners, marker_size)
  var values = detectCode(thresh, grid_corners, 3);

  var ans = 0;
  if (values[1][1] == 0)
    ans = 8 * values[3][2] + 4 * values[2][3] + 2 * values[2][1] + values[1][2];
  else if (values[1][3] == 0)
    ans = 8 * values[2][1] + 4 * values[3][2] + 2 * values[1][2] + values[2][3];
  else if (values[3][3] == 0)
    ans = 8 * values[1][2] + 4 * values[2][1] + 2 * values[2][3] + values[3][2];
  else if (values[3][1] == 0)
    ans = 8 * values[2][3] + 4 * values[2][3] + 2 * values[3][2] + values[2][1];
  else
    print("Error: Incorrect ARTag");
  return ans;
};
//==================================================================

// Местонахождение робота
var positionOfRobot = 0;
var directionOfRobot = 0;

// карта
lab = [
  [-1, 1, 8, -1],
  [-1, 2, -1, 0],
  [-1, 3, 10, 1],
  [-1, 4, -1, 2],
  [-1, 5, -1, 3],
  [-1, -1, 13, 4],
  [-1, -1, -1, -1],
  [-1, -1, 15, -1],
  [0, -1, 16, -1],
  [-1, -1, -1, -1],
  [2, -1, 18, -1],
  [-1, -1, 19, -1],
  [-1, -1, -1, -1],
  [5, 14, 21, -1],
  [-1, 15, -1, 13],
  [7, -1, -1, 14],
  [8, 17, -1, -1],
  [-1, 18, -1, 16],
  [10, -1, 26, 17],
  [11, 20, 27, -1],
  [-1, 21, -1, 19],
  [13, -1, 29, 20],
  [-1, -1, -1, -1],
  [-1, -1, 31, -1],
  [-1, -1, 32, -1],
  [-1, -1, -1, -1],
  [18, -1, 34, -1],
  [19, -1, -1, -1],
  [-1, -1, -1, -1],
  [21, 30, 37, -1],
  [-1, 31, -1, 29],
  [23, -1, 39, 30],
  [24, 33, 40, -1],
  [-1, 34, -1, 32],
  [26, 35, 42, 33],
  [-1, 36, -1, 34],
  [-1, 37, 44, 35],
  [29, -1, 45, 36],
  [-1, -1, -1, -1],
  [31, -1, -1, -1],
  [32, -1, -1, -1],
  [-1, -1, -1, -1],
  [34, -1, 50, -1],
  [-1, -1, -1, -1],
  [36, 45, -1, -1],
  [37, 46, 53, 44],
  [-1, 47, -1, 45],
  [-1, -1, 55, 46],
  [-1, 49, 56, -1],
  [-1, 50, -1, 48],
  [42, 51, 58, 49],
  [-1, -1, 59, 50],
  [-1, -1, -1, -1],
  [45, -1, -1, -1],
  [-1, -1, -1, -1],
  [47, -1, 63, -1],
  [48, -1, -1, -1],
  [-1, -1, -1, -1],
  [50, 59, -1, -1],
  [51, 60, -1, 58],
  [-1, 61, -1, 59],
  [-1, 62, -1, 60],
  [-1, 63, -1, 61],
  [55, -1, -1, 62]
];

// double cycle for traveling in maze
cycle = [0, 2, 4, 13, 15, 21, 19, 29, 31, 37, 45, 46, 55, 62, 60, 50, 48, 34,
  32, 18, 16, 0, 2, 4, 13, 15, 21, 19, 29, 31, 37, 45, 46, 55, 62, 60, 50, 48,
  34, 32, 18, 16
];

var foundedDestroyedSectors = 0;
var destroyedSectors = 0;

// получаем маршрут перемещения до необходимой точки из текущей
// в нотации F, L, R
function getPath(finishSector) {
  from = [];
  for (var i = 0; i < 64; i++) {
    from[i] = [];
    for (var j = 0; j < 4; j++)
      from[i][j] = "N";

  }

  var queue = [];
  queue.push([positionOfRobot, directionOfRobot]);
  var finishDir = 0;
  while (queue.length > 0) {
    temp = queue.shift();
    currentSector = temp[0], currentDir = temp[1];
    if (currentSector == finishSector) {
      finishDir = currentDir;
      break;
    }
    // Вперед
    if (lab[currentSector][currentDir] > -1) {
      adjSector = lab[currentSector][currentDir];
      adjDir = currentDir;
      if (from[adjSector][adjDir] == "N") {
        from[adjSector][adjDir] = "F";
        queue.push([adjSector, adjDir]);
      }
    }
    // Направо
    if (from[currentSector][(currentDir + 1) % 4] == "N") {
      adjSector = currentSector;
      adjDir = (currentDir + 1) % 4;
      from[adjSector][adjDir] = "R";
      queue.push([adjSector, adjDir]);
    }
    // Налево
    if (from[currentSector][(currentDir + 3) % 4] == "N") {
      adjSector = currentSector;
      adjDir = (currentDir + 3) % 4;
      from[adjSector][adjDir] = "L";
      queue.push([adjSector, adjDir]);
    }
  }

  path = "";
  // Восстанавливаем путь
  if (from[finishSector][finishDir] == "N")
    print("No way");
  else {
    currentSector = finishSector;
    currentDir = finishDir;
    while (currentSector != positionOfRobot || currentDir != directionOfRobot) {
      action = from[currentSector][currentDir];
      if (action == "F") {
        path = "F" + path;
        currentSector = lab[currentSector][(currentDir + 2) % 4];
      } else if (action == "R") {
        path = "R" + path;
        currentDir = (currentDir + 3) % 4;
      } else if (action == "L") {
        path = "L" + path;
        currentDir = (currentDir + 1) % 4;
      }
    }
  }
  return path;
}

// Внести информацию о недоступности сектора
function isolateSector(sector) {
  foundedDestroyedSectors++;
  for (dir = 0; dir < 4; dir++)
    if (lab[sector][dir] > -1) {
      lab[lab[sector][dir]][(dir + 2) % 4] = -2;
      lab[sector][dir] = -2;
    }
  calcAvailable();
  print("countUnavailable=", countUnavailable);
}

// Проверка окружающих секторов
function checkAdjacentSectors() {
  if (!(svFront() > 25) && 
        lab[positionOfRobot][directionOfRobot] > -1)
    isolateSector(lab[positionOfRobot][directionOfRobot]);
  if (!(svLeft() > 25) && 
        lab[positionOfRobot][(directionOfRobot + 3) % 4] > -1)
    isolateSector(lab[positionOfRobot][(directionOfRobot + 3) % 4]);
  if (!(svRigth() > 25) && 
        lab[positionOfRobot][(directionOfRobot + 1) % 4] > - 1)
    isolateSector(lab[positionOfRobot][(directionOfRobot + 1) % 4]);
}

// Перемещение по кратчайшему пути до finishSector
function follow_path(finishSector) {
  path = getPath(finishSector);
  while (positionOfRobot != finishSector && path != "") {
    if (foundedDestroyedSectors < destroyedSectors)
      checkAdjacentSectors();
    for (var i = 0; i < path.length; i++) {
      if (path[i] == "R") {
        turnDirection(-90, v);
        directionOfRobot = (directionOfRobot + 1) % 4;
      } else if (path[i] == "L") {
        turnDirection(90, v);
        directionOfRobot = (directionOfRobot + 3) % 4;
      } else if (path[i] == "F") {
        if (lab[positionOfRobot][directionOfRobot] < 0) {
          print("The path is blocked. No way!");
          break;
        }
        forward(v, 1);
        positionOfRobot = lab[positionOfRobot][directionOfRobot];
      }
      if (foundedDestroyedSectors < destroyedSectors)
        checkAdjacentSectors();
      else if (foundedDestroyedSectors == destroyedSectors)
        break;
    }
    if (foundedDestroyedSectors == destroyedSectors) {
      foundedDestroyedSectors++;
      break;
    }
    path = getPath(finishSector);
  }
}

// Поворот робота на заданное направление
function turnTo(targetDir) {
  var dDir = (targetDir - directionOfRobot + 4) % 4;
  if (dDir == 1) {
    turnDirection(-90, v);
  } else if (dDir == 3) {
    turnDirection(90, v);
  } else if (dDir == 2) {
    turnDirection(-180, v);
  }
  directionOfRobot = targetDir;
}

// Проход по лабиринту
function travelThroughoutMaze() {
  var firstSector = 0;
  for (firstSector = 0; firstSector < cycle.length / 2; ++firstSector) {
    if (positionOfRobot == cycle[firstSector] || lab[positionOfRobot][0] ==
      cycle[firstSector] || lab[positionOfRobot][1] == cycle[firstSector] ||
      lab[positionOfRobot][2] == cycle[firstSector] || 
      lab[positionOfRobot][3] == cycle[firstSector])
      break;
  }
  for (i = firstSector; i < firstSector + cycle.length / 2; i++) {
    follow_path(cycle[i]);
    if (foundedDestroyedSectors >= destroyedSectors) {
      break;
    }
  }
}

function dfs(sector) {
  used[sector] = true;
  countAvailable++;
  for (var dir = 0; dir < 4; ++dir) {
    nextSector = lab[sector][dir];
    if (nextSector > -1 && !used[nextSector])
      dfs(nextSector);
  }
}

// Вычисление доступных/недоступных секторов
function calcAvailable() {
  used = [];
  for (var i = 0; i < 64; i++)
    used = [];
  // Сколько доступных секторов
  countAvailable = 0;
  dfs(positionOfRobot);
  // Сколько недоступных секторов
  countUnavailable = 64 - countAvailable - 12;
}

var value1, value2;
// Считывание двух ARTag маркеров
function readARTag(dist) {
  forward(-v, dist);
  value1 = getARTagValue();

  forward(v, dist);
  value2 = getARTagValue();
  print(value1 + " " + value2);
}

//=================================================================================
//=================================M A I N ========================================
var main = function() {

  var xStart = 7;
  var yStart = 1;
  directionOfRobot = 3;
  var xARTag = 5;
  var yARTag = 6;
  // С какой стороны от сектора распредления решений располагается ARTag
  var directionOfARTag = 3;
  
  // Количество обрушенных секций
  destroyedSectors = 2; 
  positionOfRobot = xStart + yStart * 8;

  travelThroughoutMaze();
  follow_path(xARTag + yARTag * 8);
  turnTo((directionOfARTag + 3) % 4);

  //detecting ARTag markers until it isn't successful
  value1 = 0;
  value2 = 0;
  dist = 0.3;
  while (value1 < 8 && value2 < 8 || value1 > 7 && value2 > 7) {
    readARTag(dist);
    dist += 0.05;
  }

  // Координаты финиша
  xFinish = 0;
  yFinish = 0;
  if (value1 < 8) {
    xFinish = value1;
    yFinish = value2 - 8;
  } else {
    xFinish = value2;
    yFinish = value1 - 8;
  }

  print(xFinish + " " + yFinish);
  finishSector = xFinish + yFinish * 8;
  follow_path(finishSector);
  print(countUnavailable);
  return;
}