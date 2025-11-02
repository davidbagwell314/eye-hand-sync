#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    float x;
    float y;
} Pos;

typedef struct
{
    float time;
    Pos target;
    Pos hand;
    Pos eye;
} Data;

void print_data(Data data)
{
    printf("{%f, (%f, %f), (%f, %f), (%f, %f)}\n", data.time, data.target.x, data.target.y, data.hand.x, data.hand.y, data.eye.x, data.eye.y);
}

int main()
{
    // Initialise variables
    FILE *file = fopen("data/r1/tracking_r1_prt_1.csv", "r");
    char line[256];

    char **raw_data = malloc(sizeof(char *));

    size_t num_lines = 0;

    while (fgets(line, sizeof(line), file) != NULL)
    {
        num_lines++;
        raw_data = realloc(raw_data, num_lines * sizeof(char *));
        raw_data[num_lines - 1] = malloc(strlen(line) + 1);
        strcpy(raw_data[num_lines - 1], line);
    }

    Data *data = malloc(sizeof(Data) * num_lines);

    for (int i = 0; i < num_lines; i++)
    {
        int value_start = 0;

        float values[7];
        int num_values = 0;

        for (int j = 0; j < strlen(raw_data[i]); j++)
        {
            char org = raw_data[i][j];
            if (raw_data[i][j] == ',' || raw_data[i][j] == '\n')
            {
                raw_data[i][j] = 0;

                float value = strtof(&(raw_data[i][value_start]), NULL);
                values[num_values++] = value;

                raw_data[i][j] = org;
                value_start = j + 1;
            }
        }

        data[i].time = values[0];
        data[i].target.x = values[1];
        data[i].target.y = values[2];
        data[i].hand.x = values[3];
        data[i].hand.y = values[4];
        data[i].eye.x = values[5];
        data[i].eye.y = values[6];
    }

    for (int i = 0; i < num_lines; i++)
    {
        print_data(data[i]);
    }

    // Free allocated data

    for (int i = 0; i < num_lines; i++)
        free(raw_data[i]);

    free(raw_data);
    free(data);
}