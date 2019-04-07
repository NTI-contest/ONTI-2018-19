#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
unsigned int maskf[] = {0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x100, 0x200, 0x400, 
    0x800, 0x1000, 0x2000, 0x4000, 0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 0x100000, 
    0x200000, 0x400000, 0x800000, 0x1000000};
void CharToBinaryArray(int &a, int l, char arr[]);
void AddControlBit(char arr[], int l, char arrc[], int lc);
int order(int a); //кол-во разрядов в двоичном представлении
void matrpreobr(char **preobr, int lrow, int lcol);
void decoder_hamming(char **preobr, int lrow, int lcol, char earr[], char darr[]);
void cutcontrolbit(int lcol, char darr[], int l, char arr[]);
void HammingDecoderArr(char *esignal, int l_esignal, char *&signal, int &l_signal);
void main(int argc, char *argv[])
{
    //---------------Decoder-------------------------------------//
    int l_esignal = strlen(argv[1]); //Длина входной последовательности
    int l_signal;
    char *esignal;
    char *signal = NULL;
    esignal = (char *)calloc(l_esignal + 1, sizeof(char));
    strcpy(esignal, argv[1]);
    printf("esignal = %s length = %d\n", esignal, l_esignal);
    HammingDecoderArr(esignal, l_esignal, signal, l_signal);
    printf(" signal = %s length = %d\n", signal, l_signal);
    //---------------------------------------------------------//
}
void HammingDecoderArr(char *esignal, int l_esignal, char *&signal, int &l_signal)
{
    int lrow = order(l_esignal);
    l_signal = l_esignal - lrow;
    signal = (char *)calloc(l_signal, sizeof(char));
    char *darr = new char[l_esignal];
    char **preobr = new char *[lrow];
    for (int i = 0; i < lrow; i++)
        preobr[i] = new char[l_esignal];
    matrpreobr(preobr, lrow, l_esignal); //Формируем матрицу преобразования
    decoder_hamming(preobr, lrow, l_esignal, esignal,
                    darr); //Декодированный сигнал (исправленыошибки)
    cutcontrolbit(l_esignal, darr, l_signal, signal);
    delete[] darr;
    for (int i = 0; i < lrow; i++)
        delete[] preobr[i];
    delete[] preobr;
}
void decoder_hamming(char **preobr, int lrow, int lcol, char earr[], char darr[])
{
    int k = 0;
    strcpy(darr, earr);
    for (int i = 0; i < lrow; i++)
    {
        int sum = 0;
        for (int j = 0; j < lcol; j++)
            sum += (preobr[i][j] - '0') * (earr[j] - '0');
        sum = sum % 2;
        k += sum * (1 << i);
    }
    darr[k - 1] = (darr[k - 1] == '0') ? '1' : '0';
    printf("k=%d\n", k);
}
void matrpreobr(char **preobr, int lrow, int lcol)
{
    int i2 = 0, v;
    char arr[100];
    for (int i = 1; i <= lcol; i++)
    { //цикл по столбцам
        if ((i & (i - 1)) == 0)
        { //степени двойки
            i2++;
            v = 1 << (i2 - 1);
            CharToBinaryArray(v, lrow, arr);
            for (int j = 0; j < lrow; j++) //цикл по строкам
                preobr[j][i - 1] = arr[j];
        }
        else
        { //номера информационных битов
            CharToBinaryArray(i, lrow, arr);
            for (int j = 0; j < lrow; j++) //цикл по строкам
                preobr[j][i - 1] = arr[j];
        }
    }
    for (int j = 0; j < lrow; j++)
        preobr[j][lcol] = 0;
}
void cutcontrolbit(int lcol, char darr[], int l, char arr[])
{
    int j = 0, i = 1;
    while (i <= lcol)
    {
        if (i & (i - 1))
            arr[j++] = darr[i - 1];
        i++;
    }
    arr[j] = 0;
}
void AddControlBit(char arr[], int l, char arrc[], int lc)
{
    int j = 0, i = 1;
    while (j < l)
    {
        if ((i & (i - 1)) == 0)
            arrc[i - 1] = '0';
        else
            arrc[i - 1] = arr[j++];
        i++;
    }
    arrc[i - 1] = 0;
}
int order(int a)
{
    double x = (double)a;
    x = log(x) / log(2.0);
    return (int)x + 1;
}
void CharToBinaryArray(int &a, int l, char *arr)
{
    for (int i = 0; i < l; i++)
        arr[i] = a & maskf[i] ? '1' : '0';
    arr[l] = 0;
}