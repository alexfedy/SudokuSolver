#include "sudoku.h"

int checkRows(Square ***sudoku, Box **boxes)
{
    int i, j, k;
    int sum[9];
    int place[9];
    for (i = 0; i < SIZE_ROWS; i++)
    {
        // initialize
        for (j = 0; j < SIZE_COLUMNS; j++)
        {
            place[j] = 0;
            sum[j] = 0;
        }
        for (j = 0; j < SIZE_COLUMNS; j++)
        {
            if (sudoku[i][j]->number != 0)
            {
                continue;
            }
            for (k = 0; k < SIZE_COLUMNS; k++)
            {
                if (sudoku[i][j]->possible[k] == 0)
                {
                    sum[k]++;
                    place[k] = j;
                }
            }
        }
        for (k = 0; k < SIZE_COLUMNS; k++)
        {
            if (sum[k] == 1)
            {
                sudoku[i][place[k]]->number = k + 1;
                sudoku[i][place[k]]->solvable = 0;
                UNSOLVED--;
                updateSudoku(sudoku, i, place[k]);
                updateBoxes(sudoku, i, place[k]);
                return 1;
            }
        }
    }
    return 0;
}