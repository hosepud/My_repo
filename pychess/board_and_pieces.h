#ifndef __BOARD_H__
#define __BOARD_H__

typedef struct Board{
    int* b;
    int forced;
    int current_player;
    int is_terminal;
    int new_x;
    int new_y;
    int old_y;
    int p;
}Board;

typedef struct Move{
    int from;
    int to;
    int new_x;
    int new_y;
    int old_x;
    int old_y;
    int en_passant;
    Board* b;
}Move;

void print_piece(int n);
int get(Board* b, int x, int y);
Move** next_moves_boards(Board* b);
Board* load_from_file(int online);
Board* load_from_argv(char* fp, char* lastmove);
void print_board(Board* b);
Board* flipped(Board* b);
void free_moves(Move** moves);
#endif
