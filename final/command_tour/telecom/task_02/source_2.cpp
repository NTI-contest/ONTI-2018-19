#ifndef __CODE_DECODE_H__
#define __CODE_DECODE_H__
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define DATA_BLOCK_LEN 400
#define CODE_BLOCK_LEN (sizeof(unsigned long))
#define FULL_BLOCK_LEN (DATA_BLOCK_LEN + CODE_BLOCK_LEN)
#define MAX_FILE_SIZE 20000000
#define HEADER_MARK "ABCDEFG"
#define FOOTER_MARK "HIJKLMN"
#define HEADER_MARK_LEN 7
#define FOOTER_MARK_LEN 7
typedef struct
{
    char head[HEADER_MARK_LEN + 1];
    unsigned int code_block;
    long block_len;
} header_code_type;
typedef struct
{
    char foot[FOOTER_MARK_LEN + 1];
    unsigned int code_block;
    // long block_len;
} footer_code_type;
#define HEADER_BLOCK_LEN (sizeof(header_code_type))
#define FOOTER_BLOCK_LEN (sizeof(footer_code_type))
#endif
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
void init_header_code(header_code_type *header_code, footer_code_type *
                                                         footer_code)
{
    sprintf(header_code->head, HEADER_MARK);
    sprintf(footer_code->foot, FOOTER_MARK);
    header_code->code_block = 0;
    header_code->block_len = 0;
}
int main(int argn, char *argv[])
{
    char *tmp_file1;
    char *tmp_file2;
    long compr_len;
    unsigned long code_block = 0;
    header_code_type header_code;
    footer_code_type footer_code;
    long i, j;
    char *block;
    int mode;
    if (argn > 1)
        mode = atol(argv[1]);
    else
        mode = 1;
    FILE *in;
    FILE *out;
    tmp_file1 = calloc(sizeof(char), 40000000);
    tmp_file2 = calloc(sizeof(char), 40000000);
    long file_len, block_len;
    block = calloc(DATA_BLOCK_LEN * 2, sizeof(char));
    code_block = 0;
    file_len = 0;
    in = fopen(argv[1], "rb");
    out = fopen(argv[2], "wb");
    for (i = 0; !feof(in);)
    {
        block_len = fread(block, sizeof(char), DATA_BLOCK_LEN, in);
        memcpy(tmp_file1 + i, block, block_len);
        i += block_len;
    }
    compr_len = 20000000;
    memcpy(tmp_file2, tmp_file1, i);
    compr_len = i;
    file_len = 0;
    init_header_code(&header_code, &footer_code);
    for (j = 0; j < compr_len; j += DATA_BLOCK_LEN)
    {
        block_len = DATA_BLOCK_LEN;
        if (j + DATA_BLOCK_LEN <= compr_len)
            memcpy(block, tmp_file2 + j, DATA_BLOCK_LEN);
        else
        {
            block_len = compr_len - j;
            memcpy(block, tmp_file2 + j, block_len);
        }
        file_len += block_len;
        for (i = block_len; i < DATA_BLOCK_LEN; i++)
            block[i] = 0;
        header_code.block_len = DATA_BLOCK_LEN;
        header_code.code_block = code_block;
        footer_code.code_block = code_block;
        code_block++;
        fwrite(&(header_code), sizeof(char), sizeof(header_code), out);
        fwrite(block, sizeof(char), DATA_BLOCK_LEN, out);
        fwrite(&(footer_code), sizeof(char), sizeof(footer_code), out);
        for (i = 0; i < DATA_BLOCK_LEN; i++)
            block[i] = 0;
    }
    code_block = -1;
    fprintf(stderr, "file len: %ld\n", file_len);
    memcpy(block, &file_len, sizeof(long));
    fwrite(block, sizeof(char), DATA_BLOCK_LEN, out);
    fwrite(&code_block, sizeof(char), CODE_BLOCK_LEN, out);
    fflush(out);
    fclose(out);
    //copy result twice to compensate dead regions of satellite
    long len = 0;
    out = fopen(argv[2], "rb");
    len = fread(tmp_file1, sizeof(char), 40000000, out);
    fclose(out);
    out = fopen(argv[2], "wb");
    fwrite(tmp_file1, sizeof(char), len, out);
    fwrite(tmp_file1, sizeof(char), len, out);
    fclose(out);
}
