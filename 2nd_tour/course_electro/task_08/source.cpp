#include <stdio.h> 

int readADC(float v) 
{ 
    return 1023.0*v/5; 
} 

int puzirok(int *mas, int size)//and delete 
{ 
    for(int i = 0; i < size; i++) 
    { 
        for(int j = i+1; j < size; j++) 
        { 
            if(mas[j] < mas[i]) 
            { 
                int temp = mas[i]; 
                mas[i] = mas[j]; 
                mas[j] = temp; 
            } 
            if(mas[j] == mas[i])//delete element 
            { 
                size--; 
                mas[j] = mas[size]; 
                j = i; 
            } 
        }   
    }    
return size; 
} 

int main() { 
    // put your code here 
    int R1; 
    int R2; 
    int mas[128] = {0}; 
    int size = 0; 
    scanf("%d", &R1); 
    scanf("%d", &R2); 
    //1 - вариант когда out out 
    mas[size++] = 0;// 0 0 //0 + 
    mas[size++] = R1*1023/((R1+R2));// 0 1 + //272 + 
    mas[size++] = R2*1023/((R1+R2));// 1 0 + //750 + 
    mas[size++] = 1023;// 1 1 ?(0) //1023 + 
    //out in тоже самое 
    //in in 0(1023) 
    mas[size++] = R1*1023/((R1 + R2 + 10));//inpullpull out(0) //223 +- 
    mas[size++] = R2*1023/((R1 + R2 + 10)); //613 +- 

    float valR1 = (R1*10)/1.0/((R1 + 10)); 
    mas[size++] = R2*1023/((R2 + valR1)); //877 +— 
    float valR2 = (R2*10)/1.0/((R2 + 10)); 
    mas[size++] = R1*1023/((R1 + valR2)); //623 +— 

    mas[size++] = R2*1023/((R2 + 10)); //785 +- 
    mas[size++] = R1*1023/((R1 + 10)); //558 +- 

    float valR = (R1*R2)*1.0/((R1 + R2)); 
    mas[size++] = valR*1023/((valR + 10)); //478 

    valR2 = ((R2 + 10)*10)/1.0/((R2 + 10 + 10)*1.0); 
    mas[size++] = R1*1023/((R1 + valR2)); //610 
    valR1 = ((R1 + 10)*10)/1.0/((R1 + 10 + 10)*1.0); 
    mas[size++] = R2*1023/((R2 + valR1)); //846 
    //+ 

    size = puzirok(mas, size); 
    printf("%d\n", size); 

    for(int i = 0;i < size; i++) 
        printf("%d ", mas[i]); 

    return 0; 
}