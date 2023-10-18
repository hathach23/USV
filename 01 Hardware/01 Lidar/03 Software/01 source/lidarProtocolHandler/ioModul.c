#include "ioModul.h"

static uint8_t buffer[BUFFER_MAX_LENGTH] = {0};
static uint16_t stringPtr = 0;

static inline int32_t min(int32_t a, int32_t b)
{
    return (a<b)?a:b;
}

static inline int32_t max(int32_t a, int32_t b)
{
    return (a>b)?a:b;
}

static inline uint8_t char2hexNum(uint8_t input)
{
    uint8_t result = 0;
    if((input>=65)&&(input<=70))
    {
        result = input - 55;
    }
    else if((input>=48)&&(input <= 57))
    {
        result = input - 48;
    }
    return result;
}

void readFile(char* path)
{
    FILE *input = fopen(path,"r");
    char character;
    uint8_t shift = 0;
    if(input!=NULL)
    {
        while((character = fgetc(input)) != EOF)
        {
            if(character!='\n')
            {
                character = char2hexNum(character);
                buffer[stringPtr] |= character << ((!shift)*4);
                shift = (shift + 1) %2;
                if(!shift)
                {
                    //printf("a[%d] = 0x%02X \n",stringPtr,buffer[stringPtr]);
                    stringPtr++;
                }
                character = 0;
            }
        }
    }
    else
    {
        printf("File not exist\n");
    }

    if(fclose(input))
    {
        printf("Closing Error");
    }
}

void getData(uint8_t* data, uint16_t* dataLen)
{
    if((*dataLen) > stringPtr)
    {
        for(int i = 0; i< stringPtr; i++)
        {
            data[i] = buffer[i];
            //printf("data[%d] = 0x%02X \n",i,data[i]);
        }
        *dataLen = stringPtr;
        stringPtr = 0;
    }
}

void writeFileInt32(uint8_t* name, uint16_t len, uint8_t format, int32_t* value, uint16_t valLen)
{
    //TODO Fehlertrennung
    FILE *input;
    char path[BUFFER_MAX_LENGTH] = {0};
    uint16_t pathLen = 0;
    memcpy(path,name,len-1);
    pathLen = len-1;
    //TODO Fehlertrennung
    switch(format)
    {
    case TEXT_FORM:
        memcpy(&path[pathLen],".txt",sizeof(".txt"));
        pathLen += sizeof(".txt");
        break;
    case CSV_FORM:
        memcpy(&path[pathLen],".csv",sizeof(".txt"));
        pathLen += sizeof(".txt");
        break;
    default:
        break;
    }
    input = fopen(path,"w+");
    if(input!=NULL)
    {
        for(int i = 0; i<valLen ; i++)
        {
            fprintf(input,"%d\n",value[i]);
        }
    }
    else
    {
        printf("Fehler beim Schreiben von Daten\n");
    }
    if(fclose(input))
    {
        printf("Fehler beim Schliessen von Daten\n");
    }
}

void writeFileInt64(uint8_t* name, uint16_t len, uint8_t format, int64_t* value, uint16_t valLen)
{
    //TODO Fehlertrennung
    FILE *input;
    char path[BUFFER_MAX_LENGTH] = {0};
    uint16_t pathLen = 0;
    memcpy(path,name,len-1);
    pathLen = len-1;
    //TODO Fehlertrennung
    switch(format)
    {
    case TEXT_FORM:
        memcpy(&path[pathLen],".txt",sizeof(".txt"));
        pathLen += sizeof(".txt");
        break;
    case CSV_FORM:
        memcpy(&path[pathLen],".csv",sizeof(".txt"));
        pathLen += sizeof(".txt");
        break;
    default:
        break;
    }
    input = fopen(path,"w+");
    if(input!=NULL)
    {
        for(int i = 0; i<valLen ; i++)
        {
            fprintf(input,"%I64d\n",value[i]);
        }
    }
    else
    {
        printf("Fehler beim Schreiben von Daten\n");
    }
    if(fclose(input))
    {
        printf("Fehler beim Schliessen von Daten\n");
    }
}


