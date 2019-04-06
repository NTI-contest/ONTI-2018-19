#include <string.h>
#include <unistd.h>
#include <fcntl.h>
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
int main(int argn, char *argv[])
{
    // FILE* tmpfile;
    int mode;
    mode = 1;
    unsigned long code_block = 0;
    long i, j, length;
    char *block;
    unsigned char *file_content;
    unsigned char *new_file_content;
    long file_len;
    long block_len;
    char srch_block[255];
    FILE *in;
    FILE *out;
    in = fopen(argv[1], "rb");
    out = fopen(argv[2], "wb");
    file_content = calloc(MAX_FILE_SIZE + 1, sizeof(char));
    if (!file_content)
    {
        fprintf(stderr, "no memory\n");
        exit(1);
    }
    new_file_content = calloc(MAX_FILE_SIZE + 1, sizeof(char));
    if (!new_file_content)
    {
        fprintf(stderr, "no memory\n");
        exit(1);
    }
    block = calloc(100000, /*DATA_BLOCK_LEN*2,*/ sizeof(char));
    if (!block)
    {
        fprintf(stderr, "no memory\n");
        exit(1);
    }
    length = fread(file_content, sizeof(char), MAX_FILE_SIZE + 1, in);
    if (length > MAX_FILE_SIZE)
    {
        fprintf(stderr, "file too long to process\n");
        exit(1);
    }
    long actual_len;
    header_code_type header_block;
    footer_code_type footer_block;
    file_len = 0;
    // for(i=0;i<length;)
    for (i = 0; i < length; i++)
    {
        memcpy((void *)(&header_block), (void *)(file_content + i), 
            HEADER_BLOCK_LEN);
        memcpy(&footer_block, file_content + i + HEADER_BLOCK_LEN + 
            DATA_BLOCK_LEN, FOOTER_BLOCK _LEN);
        if (memcmp((void *)(header_block.head), HEADER_MARK, HEADER_MARK_LEN) == 0 &&
            memcmp((void *)(footer_block.foot), FOOTER_MARK, FOOTER_MARK_LEN) == 0 &&
            footer_block.code_block == header_block.code_block &&
            i + HEADER_BLOCK_LEN + DATA_BLOCK_LEN + FOOTER_BLOCK_LEN < length)
        {
            memcpy((void *)(block), file_content + i + HEADER_BLOCK_LEN, DATA_BLOCK_LEN);
            memcpy(new_file_content + header_block.code_block * 
                DATA_BLOCK_LEN, block, DATA_BLOCK_ LEN);
            block[DATA_BLOCK_LEN] = 0;
            i += HEADER_BLOCK_LEN;
            i += DATA_BLOCK_LEN;
            i += FOOTER_BLOCK_LEN;
            i--;
            file_len += DATA_BLOCK_LEN;
            continue;
        }
    }
    fprintf(stderr, "flen:%ld\n", file_len);
    char *tmp1;
    long new_len = 20000000;
    for (i = file_len; i >= 0; i--)
        if (new_file_content[i] != 0)
            break;
    // fwrite(new_file_content,sizeof(char),file_len,out);
    fwrite(new_file_content, sizeof(char), i + 1, out);
    fflush(out);
}
