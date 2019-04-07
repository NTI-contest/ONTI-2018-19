#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "Gears.h"
#define PI (3.1415926535897932384626433832795)
//Инициализация массивов
void GearsSignal::InitArray()
{
    TP =
        (double *)calloc(ngear, sizeof(double));     //Период сигнала для каждой шестерни
    direction = (char *)calloc(ngear, sizeof(char)); //Направление вращения
    DT = (double *)calloc(ngear, sizeof(double));    //Сдвиг повремени
    Amp = (double *)calloc(ngear, sizeof(double));   //Амплитуда кор-функции
    Err = (double *)calloc(ngear, sizeof(double));   //Ошибка
}
GearsSignal::GearsSignal()
{
    ngear = 3;
    InitArray();
}
//Чтение конфигурационного файла
GearsSignal::GearsSignal(char *nameconfig)
{
    FILE *conf;
    conf = fopen(nameconfig, "r"); //Работаем с конфигурационным файлом
    fscanf(conf, "%d", &ngear);    //Cтрока №1 - Длина кодовой последовательности
    kd = (int *)calloc(ngear, sizeof(int));
    kod = (char **)calloc(ngear, sizeof(char *));
    InitArray();
    namefile = (char *)calloc(1000, sizeof(char));
    fscanf(conf, "%s", namefile); //Cтрока №2 имя файла с измерениями
    for (int i = 0; i < ngear; i++)
    {
        fscanf(conf, "%d", &kd[i]); //Cтрока №3 - Длина кодовой
                                    //последовательности
        kod[i] = (char *)calloc(kd[i] + 1, sizeof(char));
        fscanf(conf, "%s", kod[i]); //Cтрока №4 - форма кодовой
                                    //последовательности
        printf("kd[%d]=%d\n", i, kd[i]);
        printf("kod[%d]=%s\n", i, kod[i]);
    }
    fscanf(conf, "%lf", &tau1); //Cтрока №5 - длительность переднего фронта
                                //(милисек)
        fscanf(conf, "%lf", &tau2); //Cтрока №6 - длительность смены фазы (милисек)
    fscanf(conf, "%lf", &tau3);     //Cтрока №7 - длительность заднего фронта
                                    //(милисек)
        fscanf(conf, "%lf", &dt); //Cтрока №8 - время между отсчетами (милисек)
    fclose(conf);
}
//Анализ каналов – опредление энергии невязки между модельным и измеренным
//сигналами
void GearsSignal::GearsAnaliz()
{
    if (ReadFile(namefile))
    {
        CalcPeriod();
        SignalModel();
        CorAnaliz2('w');
        PrintArray();
        EnergyError();
    }
    else
        printf("analiz disable!\n");
}
void GearsSignal::EnergyError()
{
    double dE, E, E1, E2;
    for (int k = 0; k < ngear; k++)
    {
        int i = (int)DT[k];   //сдвиг
        int n = direction[k]; //направление вращения
        dE = 0.0;             //интеграл ошибок
        E1 = E2 = E = 0.0;
        for (int j = 0; j < I0[k]; j++) //Интегреируем
            if (i + j >= 0 && i + j < I)
            {
                E1 += A0[n][j] * A0[n][j];
                E2 += A[k + 1][i + j] * A[k + 1][i + j];
                E += A0[n][j] * A[k + 1][i + j];
                dE += (A[k + 1][i + j] - A0[n][j]) * (A[k + 1][i + j] -
                                                      A0[n][j]);
            }
        if (I0[k] > 0)
        {
            Err[k] = 100.0 * dE / E1; //Енергия невязки
        }
        else
            Err[k] = -100.0;
    }
    for (int i = 0; i < ngear; i++)
        printf("Err[%d]=%lf\n", i, Err[i]);
}
void GearsSignal::CorAnaliz2(char rw)
{
    double dtime[2], amp[2];
    double **akf;
    akf = (double **)calloc(ngear, sizeof(double *));
    // for(int i = 0; i<ngear; i++)
    // akf[i] = (double*)calloc(I,sizeof(double));
    for (int i = 0; i < ngear; i++)
    {
        if (I0[i] > 0)
        {
            akf[i] = CorAnaliz(A0[2 * i], I0[i], A[i + 1], I, dtime[0],
                               amp[0], 'r');
            free(akf[i]);
            akf[i] = CorAnaliz(A0[2 * i + 1], I0[i], A[i + 1], I, dtime[1],
                               amp[1], 'r');
            free(akf[i]);
            if (amp[0] > amp[1])
            {
                printf("direction[%d]=forvard!\n", i);
                DT[i] = dtime[0];
                Amp[i] = amp[0];
                direction[i] = 2 * i;
                akf[i] = CorAnaliz(A0[2 * i], I0[i], A[i + 1], I,
                                   dtime[0], amp[0], rw);
            }
            else
            {
                printf("direction[%d]=back!\n", i);
                DT[i] = dtime[1];
                Amp[i] = amp[1];
                direction[i] = 2 * i + 1;
                akf[i] = CorAnaliz(A0[2 * i + 1], I0[i], A[i + 1], I,
                                   dtime[1], amp[1], rw);
            }
        }
    }
    FILE *rez;
    rez = fopen("coranaliz_signal.dat", "w");
    for (int j = 0; j < I; j++)
    {
        fprintf(rez, "%lf ", dt * (double)j);
        for (int i = 0; i < ngear; i++)
        {
            fprintf(rez, "%lf ", akf[i][j]);
        }
        fprintf(rez, "\n");
    }
    fclose(rez);
}
double *GearsSignal::CorAnaliz(double *&A1, int I1, double *&A2, 
    int I2, double &DT, double &AmpAkf, char rw)
{
    FILE *rez;
    if (rw == 'w')
    {
        rez = fopen("coranaliz_test_signal.dat", "w");
        fprintf(rez, "dI E\n");
    }
    int i, imax;
    double E, E1, E2;
    double Emax = 0.0;
    double *akf;
    akf = (double *)calloc(I2, sizeof(double));
    for (i = 0; i < I2; i++)
    { //Сдвиг первого сигнала относительно второго
        E1 = E2 = E = 0.0;
        for (int j = 0; j < I1; j++) //Интегреируем по разверте второго
            //сигнала
        if (i + j >= 0 && i + j < I2)
        {
            double v1 = A1[j];
            double v2 = A2[i + j];
            E1 += v1 * v1;
            E2 += v2 * v2;
            E += v1 * v2;
        }
        akf[i] = E;
        if (rw == 'w')
            fprintf(rez, "%d %lf\n", i, E);
        if (E > Emax)
        {
            Emax = E;
            imax = i;
        }
    }
    if (rw == 'w')
        fclose(rez);
    DT = (double)imax;
    AmpAkf = Emax;
    return akf;
}
void GearsSignal::control_period()
{
    if (ReadFile(namefile))
        CalcPeriod(); //Средний период для всех шестерней
    int k = 1;
    int i = 1, i2 = 0;
    char **shortkod;
    shortkod = (char **)calloc(ngear, sizeof(char *));
    for (int k = 0; k < ngear; k++)
    {
        shortkod[k] = (char *)calloc(kd[k] + 1, sizeof(char));
    }
    for (int k = 0; k < ngear; k++)
    {
        int l = 0;
        shortkod[k][l++] = kod[k][0];
        for (i = 1; i < kd[k]; i++)
        {
            if (kod[k][i] != kod[k][i - 1])
                shortkod[k][l++] = kod[k][i];
        }
        shortkod[k][l] = 0;
    }
    for (k = 1; k <= 3; k++)
    {
        i = 1, i2 = 0;
        while (A[k][i] * A[k][i - 1] > 0.0)
            i++;
        i2 = i;
        i++;
        int n = 0, N = 0;
        double per[1000] = {0.0};
        double Period, cko;
        while (i < I)
        {
            while (A[k][i] * A[k][i - 1] > 0.0 && i < I)
                i++;
            if (i >= I)
                break;
            n++;
            if (n == strlen(shortkod[k - 1]))
            {
                per[N] = (double)(i - i2);
                i2 = i;
                n = 0;
                N++;
            }
            i++;
        }
        Period = 0.0;
        for (int i = 0; i < N; i++)
            Period += per[i];
        Period = Period / ((double)N);
        cko = 0.0;
        for (int i = 0; i < N; i++)
            cko += (per[i] - Period) * (per[i] - Period);
        cko = sqrt(cko / ((double)N));
printf("Kanal=%d Numder period=%d Period=%1.1lf
CKO=%1.1lf\n",k,N,Period,cko);
    }
}
void GearsSignal::SignalModel()
{ //Модель сигнала - один период
    int Jmax = 0;
    double Tadd = 0.0; //Уширение/сужение импульса
    I0 = (int *)calloc(ngear, sizeof(int));
    A0 = (double **)calloc(2 * ngear, sizeof(double *));
    for (int j = 0; j < ngear; j++)
    {
        if (TP[j] > 1.0)
        {
            IzlImpAdd2(kd[j], kod[j], dt, Tadd, tau1, tau2, tau3, TP[j], A0[2 * j], I0[j]);
            A0[2 * j + 1] = (double *)calloc(I0[j], sizeof(double));
            for (int i = 0; i < I0[j]; i++)
                A0[2 * j + 1][i] = A0[2 * j][I0[j] - i - 1];
            if (I0[j] > Jmax)
                Jmax = I0[j];
        }
        else
            I0[j] = 0;
    }
    FILE *rez;
    rez = fopen("model_signal.dat", "w");
    for (int i = 0; i < Jmax; i++)
    {
        fprintf(rez, "%lf ", dt * (float)i);
        for (int j = 0; j < ngear; j++)
        {
            if (i < I0[j])
fprintf(rez,"%lf %lf
",A0[2*j][i],A0[2*j+1][i]);
else
fprintf(rez,"%lf %lf ",0.0,0.0);
        }
        fprintf(rez, "\n");
    }
    fclose(rez);
}
void GearsSignal::IzlImpAdd2(int kd, char *kod, double dt, double Tadd, 
    double tau1, double tau2, double tau3, double T, double *&A0, int &J0)
{
    int i, j, J, K3, k0, j0, jb; //Длительность сигнала в отсчетах
    int Np;                      //Длительность реализации в отсчетах - степень двойки
    int ll, l, m, m1, m2, m3, ml, k;
    int km[2][300];
    double amp, max, freq, t, tau, td, tl, Tl, x, y, ct, cT, T0;
    double Amp, st, sT, tc, E0;
    double *Xt;
    char c;
    ll = 32000;
    Xt = (double *)calloc(ll, sizeof(double));
    k0 = (int)((double)(T) / dt); //Длительность плоской вершины изл. имп.
    T0 = T + 0.0;
    T += Tadd; //
    //-----------------------------------------------------------//
    ll = 0;
    m = 0;
    m1 = 0;
    for (i = 0; i < kd; i++)
    { //Разбераем строку на отдельные чипы
        c = kod[i];
        k = atoi(&c);
        if (k == 0)
            k = -1;
        if ((i > 0) && (m1 != k))
        {
            km[1][ll] = i - m; //Число элементарных элементов в чипе
            km[0][ll] = m1;    //Фаза чипа
            m = i;
            ll++;
        }
        m1 = k;
    }
    if (kd == 1)
    {
        km[0][ll] = 1;
        km[1][ll] = 1;
    }
    else
    {
        km[0][ll] = k;
        km[1][ll] = kd - m;
    }
    //-----------------------------------------------------------//
    if (tau1 <= tau3)
        tau = tau1;
    else
        tau = tau3;
    if (tau > tau2 / 2)
        tau = tau2 / 2; //Ищем самый короткий фронт
    //---------------Формируем излученный импульс----------------//
    td = 0.5;
    if (td > dt)
        td = dt;
    tl = T0 / (double)(kd);             //Длительность чипа в in mks
    tl = (double)((int)(tl / td)) * td; //Длительность чипа Д/Б кратна шагу
    T0 = (double)(kd)*tl;               //Новая длительность импульса
    k = (int)(T0 / td);
    j = 0;
    //----Создаем базу для фазаманипулированного импульса--------//
    //----Т.е. огибающую на основе плоского импульса-------------//
    for (t = 0; t <= T; t += td)
    { //Текущая длительность в mks
        j++;
        //-----------------------------------------------------------//
        if (tau1 + tau3 <= T)
        { //Импульс не фазаманипулированный и длиньше
            //длительности фронтов if (t <= tau1)
            { //Строим передний фронт когда все нормально
                Xt[j] = (1.0 - cos(PI * t / tau1)) / 2.0;
            }
            if ((t > tau1) && (t <= T - tau3))
            {
                Xt[j] = 1.0;
            }
            if (t > T - tau3)
            {
                Xt[j] = (1.0 + cos(PI * (t - (T - tau3)) / tau3)) / 2.0;
            }
        }
        //-----------------------------------------------------------//
        else
        { //Импульс не фазаманипулированный и короче длительности
            //фронтов
            tau = T * tau1 / (tau1 + tau3); //Место встречи фронтов
            if (t <= tau)
            {
                Xt[j] = (1.0 - cos(PI * t / tau1)) / 2.0;
            }
            else
            {
                Xt[j] = (1.0 + cos(PI * (t - (T - tau3)) / tau3)) / 2.0;
            }
        }
        //-----------------------------------------------------------//
    }
    jb = j;
    //-----------------------------------------------------------//
    //----Теперь наполняем импульс фазавой манипуляцией----------//
    if (kd > 1)
    {
        j = 0;
        j = (int)(tau1 / 2 / td);
        for (i = 0; i <= ll; i++)
        { //Цикл по чипам
            Tl = tl * (double)(km[1][i]);
            amp = (double)(km[0][i]);
            //-----------------------------------------------------------//
            for (t = 0; t <= Tl - td + 0.000000001; t += td)
            { //Цикл внутри чипа
                j++;
                if (j <= k)
                {
                    x = Xt[j];
                    //-----------------------------------------------------------//
                    if (Tl >= tau2)
                    { //Если длительность чипа
                        //больше фронта if (t <= tau2 / 2)
                        { //Передний фронт
                            if (i > 0)
                            {
                                Xt[j] *= amp * sin(PI * t / tau2); 
                                //Форма фронта в момент переброса фазы в А-
                                //квадратуре
                            }
                        }
                        if ((t > tau2 / 2) && (t <= Tl - tau2 / 2))
                        {
                            Xt[j] *= amp;
                            //Yt[j]=0;
                        }
                        if (t > Tl - tau2 / 2)
                        { //Задний фронт
                            if (i < ll)
                            {
                                Xt[j] *= amp * sin(PI * (t - (Tl - tau2)) / tau2); 
                                //Форма фронта в момент переброса
                                //фазы в А - квадратуре
                            }
                            if (i == ll)
                            {
                                Xt[j] *= amp;
                            }
                        }
                    }
                    //-----------------------------------------------------------//
                    else
                    {
                        tau = Tl / 2.0; //Место встречи фронтов
                        if (t <= tau)
                        {
                            if (i > 0)
                            {
                                Xt[j] *= amp * sin(PI * t / tau2); 
                                //Форма фронта в момент переброса фазы в А-
                                //квадратуре
                            }
                        }
                        else
                        {
                            if (i < ll)
                            {
                                Xt[j] *= amp * sin(PI * (t - (Tl - tau2)) / tau2); 
                                //Форма фронта в момент переброса
                                //фазы в А - квадратуре
                            }
                            if (i == ll)
                            {
                                Xt[j] *= amp;
                            }
                        }
                    }
                    //-----------------------------------------------------------//
                } //if(j<=k){
                else
                {
                    Xt[j] *= amp;
                }
            } //for(t=0;t<=Tl;t+=td){//Циклвнутричипа
        }     //for(i=0;i<=ll;i++){//Циклпочипам
        //-----------------------------------------------------------//
        for (i = j + 1; i <= jb; i++)
        { //Цикл внутри чипа
            Xt[i] *= amp;
        }
        //-----------------------------------------------------------//
    } //if(kd>1){
    //-----------------------------------------------------------//
    //----Теперь сплайнируем сигнал на отсчеты через dt----------//
    l = 0;
    for (t = 0; t <= T; t += dt)
        l++;
    J0 = l; //Длительность импульса в отсчетах
    A0 = (double *)calloc(J0, sizeof(double));
    l = 0;
    for (t = 0; t <= T; t += dt)
    {
        l++;
        m = (int)(t / td) + 1;
        m1 = m + 1;
        if (m1 <= jb)
        {
            A0[l] = Xt[m] + (Xt[m1] - Xt[m]) * (t / td - (double)(m - 1));
            if (fabs(A0[l]) > 1)
                A0[l] = A0[l] / fabs(A0[l]);
        }
        else
        {
            A0[l] = 0;
        }
    }
    //-----------------------------------------------------------//
    free(Xt);
}
void GearsSignal::CalcPeriod()
{
    int i, k, imax1, imax2;
    double **Emax, **EMAX;
    double E1, E2, E, Emax1, Emax2;
    Emax = (double **)calloc(ngear, sizeof(double *));
    EMAX = (double **)calloc(ngear, sizeof(double *));
    for (k = 0; k < ngear; k++)
    { //Цикл по шестерням
        Emax[k] = (double *)calloc(I, sizeof(double));
        EMAX[k] = (double *)calloc(I / 2, sizeof(double));
    }
    for (k = 1; k <= ngear; k++)
    { //Цикл по шестерням
        for (i = 0; i < I; i++)
        { //Сдвиг
            E1 = E2 = E = 0.0;
            for (int j = 0; j < I; j++) //Интегреируем
                if (i + j >= 0 && i + j < I)
                {
                    E1 += A[k][j] * A[k][j];
                    E2 += A[k][i + j] * A[k][i + j];
                    E += A[k][j] * A[k][i + j];
                }
            Emax[k - 1][i] = E;
        }
        Emax1 = Emax[k - 1][0];
        imax1 = imax2 = 0;
        Emax2 = 0.0;
        for (i = 1; i < I - 1; i++)
            if (Emax[k - 1][i] > Emax[k - 1][i - 1] && 
                Emax[k - 1][i] > Emax[k - 1][i + 1])
            {
                if (Emax2 < Emax[k - 1][i])
                {
                    imax2 = i;
                    Emax2 = Emax[k - 1][i];
                }
            }
        TP[k - 1] = (double)(imax2 - imax1);
    }
    for (int i = 0; i < ngear; i++)
        printf("TP[%d]=%lf\n", i, TP[i]);
    FILE *rez;
    rez = fopen("period_analiz.dat", "w");
    for (int j = 0; j < I; j++)
    {
        fprintf(rez, "%lf ", dt * (double)j);
        for (int i = 0; i < ngear; i++)
        {
            fprintf(rez, "%lf ", Emax[i][j]);
        }
        fprintf(rez, "\n");
    }
    fclose(rez);
}
int GearsSignal::ReadFile(char *_namefile)
{
    FILE *file, *file2;
    int i = 0;
    char str[200], ch;
    file = fopen(_namefile, "r");
    if (!file)
        return 0;
    fgets(str, '/n', file);
    while (!feof(file))
    {
        fgets(str, '/n', file);
        if (strlen(str) < 5)
            break;
        i++;
    }
    fclose(file);
    I = i;
    A = (double **)calloc(ngear + 1, sizeof(double *));
    for (i = 0; i < ngear + 1; i++)
        A[i] = (double *)calloc(I, sizeof(double));
    file2 = fopen("gear_data.dat", "w");
    file = fopen(_namefile, "r");
    fgets(str, '/n', file);
    i = 0;
    while (!feof(file))
    {
        fgets(str, '/n', file);
        if (strlen(str) < 5)
            break;
sscanf(str,"%lf %lf %lf
%lf",&A[0][i],&A[1][i],&A[2][i],&A[3][i]);
for(int j=0; j<=ngear; j++){
            if (j > 0)
                A[j][i] = 1.0 - 2.0 * A[j][i];
}
fprintf(file2,"%lf %lf %lf
%lf\n",A[0][i],A[1][i],A[2][i],A[3][i]);
i++;
    }
    fclose(file);
    fclose(file2);
    return 1;
}
void GearsSignal::PrintArray()
{
    FILE *rez;
    int Jmax = 0, k;
    int *DI;
    DI = (int *)calloc(ngear, sizeof(int));
    for (int i = 0; i < ngear; i++)
        DI[i] = (int)DT[i];
    rez = fopen("new_signal.dat", "w");
    fprintf(rez, "T A\n");
    for (int i = 0; i < I; i++)
    {
        fprintf(rez, "%d ", i);
        for (int j = 0; j < ngear; j++)
        {
            int di = i - DI[j];
            k = direction[j];
            if (di >= 0 && di < I0[j])
                fprintf(rez, "%lf ", A0[k][di]);
            else
                fprintf(rez, "%lf ", 0.0);
        }
        fprintf(rez, "\n");
    }
    free(DI);
    fclose(rez);
}