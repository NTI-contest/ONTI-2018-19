#ifndef _GEARS_
#define _GEARS_
struct Gears
{ //для формы шестерни
    int kd;
    char *kod;
};
class GearsSignal
{
  private:
    char *namefile;
    int *kd;                 //Длина кодовой последовательности
    char **kod;              //Форма кодовой последовательности
    double tau1, tau2, tau3; //Длины фронтов модельного импульса
    double dt;               //Расстояние между отсчетами
    int ngear;
    int I;           //Кол-во отсчетов в измеренной сигнале
    double **A;      //Измеренный сигнал (0-я колонка - время)
    double *TP;      //Период сигнала для каждой шестерни
    int *I0;         //Кол-во отсчетов в модельном импульсе
    double **A0;     //Форма модельного сигнала
    char *direction; //Направление вращения
    double *DT;      //Сдвиг по времени
    double *Amp;     //Амплитуда кор-функции
    double *Err;     //Невязка между измерениями и моделью
    void InitArray();
    int ReadFile(char *_namefile); //Чтение данных из файла
    void CalcPeriod();             //Определяем период сигнала для каждой шестерни
    void sort(double *A, int n);
    void SignalModel();                                                                                                                //Модель сигнала - один период
    void IzlImpAdd(int kd, double dt, double Tadd, double tau1, double tau2, 
        double tau3, double T, double *&A0, int &J0); //Модель сигнала
    void IzlImpAdd2(int kd, char *kod, double dt, double Tadd, double tau1, 
        double tau2, double tau3, double T, double *&A0, int &J0); //Модель сигнала
    void CorAnaliz2(char rw);                                                                                                          //Корреляционный анализ с моделью сигнала
    double *CorAnaliz(double *&A1, int I1, double *&A2, int I2, double &DT,
                      double &AmpAkf, char rw);
    void PrintArray();
    void EnergyError();

  public:
    void calc_signal();
    void control_period();
    GearsSignal();
    GearsSignal(char *nameconfig);
    void GearsAnaliz();
};
#endif