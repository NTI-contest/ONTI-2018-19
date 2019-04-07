#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
unsigned char mask[] = {128, 64, 32, 16, 8, 4, 2, 1};
void read_file(const char name[], char *&buff, long &size);
void write_file(const char name[], char *&buff, long &size);
class Hamming
{
  private:
    int order(int a);
    void CharToBinaryArray(char &c, char
        arr[]); //Разложение битов кода символа в массив
    char EncodedPartArray(char arr[], int
        begin); //Кодирование части битов символа (сейчас это 4 бита)
    char BinaryArrayToChar(char arr[]); //Массив битов преобразуем в символ
    char DecoderChar(char &e); //Декодируем отдельный символ
    char UnionChar(char e[]); //Объединение двух отдельных символов при
    //декодировании(так используется расширенный код Хэмминга)
    void Encoder(char &c, char e[]); //Кодирование расширенным кодом Хэмминга
    //(4, 8) из одного символа получаем 2 
    char Decoder(char e[]); //Декодирование пары символов и объединение в один
  public:
    unsigned int lencod; //Длина в битах закодированного сообщения
    unsigned int lenbit; //Длина в битах полезного сообщения
    unsigned int lenctr; //Кол-во контролльных бит
    Hamming();
    Hamming(unsigned int _lencod);
    void ENCODER(char *&buff, const long size, char *&buff_encod, long &size_encod);
    void DECODER(char *&buff, long &size, char *&buff_encod, const long size_encod);
};
void read_file(const char name[], char *&buff, long &size)
{
    FILE *inp;
    inp = fopen(name, "rb");
    if (!inp)
    {
        printf("File %s not open!\n", name);
        return;
    }
    else
    {
        fseek(inp, 0, SEEK_END); //переместить внутренний указатель в конец файла
            size = ftell(inp);
        rewind(inp); //Устанавливаем указатель в конец файла
        buff = (char *)calloc(size, sizeof(char));
        if (buff == NULL)
        {
            printf("Error of memory\n");
            return;
        }
        printf("size = %ld\n", size);
        long result = fread(buff, 1, size, inp);
        printf("result = %d\n", result);
        if (result != size)
        {
            printf("Error of read\n");
            return;
        }
        fclose(inp);
    }
}
void write_file(const char name[], char *&buff, long &size)
{
    FILE *out;
    out = fopen(name, "wb");
    if (!out)
    {
        printf("File %s not open!\n", name);
        return;
    }
    else
    {
        long result = fwrite(buff, 1, size, out);
        if (result != size)
        {
            printf("Error of write!\n");
            return;
        }
        fclose(out);
    }
}
class CodFile
{
  private:
    int num; // кол-во байт в блоке
    char *buff, *buff_encod;
    long size, size_encod;
    Hamming hamming;
    void ReadFile(const char name[], 
        char *&_buff, long &_size); 
        //Чтение данных из файла и сброс содержимого в буфер buff
    void WriteFile(char name[], char *&_buff, long &_size);      
        //Запись содержимого buff вфайл
  public:
    CodFile() {}
    CodFile(const char *filename); //Заполнение буфера данными из файла
    void ENCODER(char *name_inp_file, char *name_out_file);
    void DECODER(char *name_inp_file, char *name_out_file);
    void ADDNOISE(char *name_inp_file, char *name_out_file);
    void WriteFile(char simbol, const char *name); //Запись содержимого buff в файл
    ~CodFile();
};
void main(int argc, char *argv[])
{
    if (argc < 4)
    {
        printf("Run file.exe E/D/N inpfile outfile\n");
        return;
    }
    CodFile codfile;
    if (argv[1][0] == 'E' || argv[1][0] == 'e')
    {
        codfile.ENCODER(argv[2], argv[3]);
    }
    else if (argv[1][0] == 'D' || argv[1][0] == 'd')
    {
        codfile.DECODER(argv[2], argv[3]);
    }
    else if (argv[1][0] == 'N' || argv[1][0] == 'n')
    {
        codfile.ADDNOISE(argv[2], argv[3]);
    }
    else
    {
        printf("Second param error (E|D)\n");
    }
}
CodFile::CodFile(const char *namefile)
{
    read_file(namefile, buff, size);
    puts(buff);
    printf("n=%d size = %d\n", strlen(buff), size);
}
void CodFile::DECODER(char *name_inp_file, char *name_out_file)
{
    read_file(name_inp_file, buff_encod, size_encod);
    hamming.DECODER(buff, size, buff_encod, size_encod);
    write_file(name_out_file, buff, size);
}
void CodFile::ENCODER(char *name_inp_file, char *name_out_file)
{
    read_file(name_inp_file, buff, size);
    hamming.ENCODER(buff, size, buff_encod, size_encod);
    write_file(name_out_file, buff_encod, size_encod);
}
void CodFile::ADDNOISE(char *name_inp_file, char *name_out_file)
{
    read_file(name_inp_file, buff_encod, size_encod);
    long i;
    for (i = 0; i < size_encod; i++)
        buff_encod[i] = buff_encod[i] ^ mask[rand() % 8];
    write_file(name_out_file, buff_encod, size_encod);
}
void CodFile::WriteFile(char simbol, const char *name)
{
    FILE *out;
    if (simbol == 'D' || simbol == 'd')
    {
        write_file(name, buff, size);
    }
    else if (simbol == 'E' || simbol == 'e')
    {
        write_file(name, buff_encod, size_encod);
    }
    else
    {
        printf("Parametr for write: D|d|E|e\n");
        return;
    }
}
CodFile::~CodFile()
{
    delete[] buff;
    delete[] buff_encod;
}
Hamming::Hamming()
{
    lencod = 7; //Общая длина
    lenbit = 4; //Полезная информация
}
void Hamming::DECODER(char *&buff, long &size, char *&buff_encod, const long size_encod)
{
    long i = 0, j = 0;
    char e[2];
    size = size_encod / 2;
    buff = new char[size];
    while (size_encod > i)
    {
        e[0] = buff_encod[i++];
        e[1] = buff_encod[i++];
        buff[j++] = Decoder(e);
    }
}
void Hamming::ENCODER(char *&buff, const long size, char *&buff_encod, long &size_encod)
{
    long i = 0, j = 0;
    char e[2];
    size_encod = 2 * size;
    buff_encod = new char[size_encod];
    for (i = 0; i < size; i++)
    {
        Encoder(buff[i], e);
        buff_encod[j++] = e[0];
        buff_encod[j++] = e[1];
    }
}
char Hamming::Decoder(char e[])
{
    char D, d[2];
    d[0] = DecoderChar(e[0]); //Декодируем
    d[1] = DecoderChar(e[1]); //Декодируем
    D = UnionChar(d);         //Объединяем
    return D;
}
void Hamming::Encoder(char &c, char e[])
{
    char arr[8];
    CharToBinaryArray(c, arr);
    e[0] = EncodedPartArray(arr, 0); //Кодируем Хэмингом(4,7)
    e[1] = EncodedPartArray(arr, 4); //Кодируем Хэмингом(4,7)
}
char Hamming::UnionChar(char d[])
{
    char Data[8] = {0};
    char data[2][8] = {0};
    CharToBinaryArray(d[0], data[0]);
    CharToBinaryArray(d[1], data[1]);
    Data[0] = data[0][0];
    Data[1] = data[0][1];
    Data[2] = data[0][2];
    Data[3] = data[0][4];
    Data[4] = data[1][0];
    Data[5] = data[1][1];
    Data[6] = data[1][2];
    Data[7] = data[1][4];
    return BinaryArrayToChar(Data);
}
char Hamming::DecoderChar(char &e)
{
    char c, c1, c2, c3;
    char data[8] = {0};
    CharToBinaryArray(e, data);
    c1 = data[6] ^ data[4] ^ data[2] ^ data[0];
    c2 = data[5] ^ data[4] ^ data[1] ^ data[0];
    c3 = data[3] ^ data[2] ^ data[1] ^ data[0];
    c = c3 * 4 + c2 * 2 + c1;
    if (c)
        if (data[7 - c] == '0')
            data[7 - c] = '1';
        else
            data[7 - c] = '0';
    return BinaryArrayToChar(data);
}
char Hamming::EncodedPartArray(char arr[], int begin)
{
    char data[8] = {0};
    data[0] = arr[0 + begin];
    data[1] = arr[1 + begin];
    data[2] = arr[2 + begin];
    data[4] = arr[3 + begin];
    data[6] = data[0] ^ data[2] ^ data[4];
    data[5] = data[0] ^ data[1] ^ data[4];
    data[3] = data[0] ^ data[1] ^ data[2];
    char c = BinaryArrayToChar(data);
    return c;
}
void Hamming::CharToBinaryArray(char &c, char arr[])
{
    for (int i = 0; i < 8; i++)
        arr[i] = c & mask[i] ? '1' : '0';
}
char Hamming::BinaryArrayToChar(char arr[])
{
    char c = 0;
    for (int i = 0; i < 8; i++)
        c |= (arr[i] - '0') ? mask[i] : 0;
    return c;
}