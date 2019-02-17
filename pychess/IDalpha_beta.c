#include <stdio.h>
#include "board_and_pieces.h"
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

int max_value(Board *b, int depth, int alpha, int beta);
int min_value(Board *b, int depth, int alpha, int beta);
int number_of_moves(Move** moves);
int time_up(void);

struct timeval start, stop;
double secs = 0;
int maxtime = 1;

int player_pieces(Board* b){
    int p = 0;
    int y,x;
    y = 0;
    while(y<8){
        x = 0;
        while(x<8){
            if( get(b,x,y) && get(b,x,y)*b->current_player > 0)
                p+=1;
            x++;
        }
        y++;
    }
    return p;   
}

int other_pieces(Board* b){
    int o = 0;
    int y,x; y=0;
    while(y<8){
        x = 0;
        while(x<8){
            if( get(b,x,y) && get(b,x,y) < 0)
                o+=1;
            x++;
        }
        y++;
    }
    return o;   
}
int value_of(int piece, int o, int p){
    int endgame = 0;
    if(p+o <= 16)
        endgame = 1;
    if(piece<0)
        piece *= -1;
    switch(piece){
        case 2:
            return 1;
        case 3:
            return endgame ? 6: 3; 
        case 4:
            return endgame ? 5: 10; 
        case 5:
            return endgame ? 3: 8; 
        case 8:
            return endgame ? 8: 2; 
        case 1:
            return endgame ? 6: 2; 
        default:
            return 0;
    }
}

int value_of1(int piece, int o){
    if(piece < 0)
        piece*=-1;
    switch(piece){
        case 2:
            if(o<10)
                return 40;
            else
                return 10;
        case 3:
            if(o>10)
                return 10;
            else if(o>5)
                return 30;
            else
                return 40;
        case 4:
            if(o>10)
                return 40;
            else if(o>5)
                return 30;
            else
                return 20;
        case 5:
            if(o>10)
                return 50;
            else if(o>5)
                return 40;
            else
                return 30;
        case 8:
            if(o<5)
                return 80;
            else if(o>=5 && o<10)
                return 50;
            else
                return 10;
        case 1:
            if(o<10)
                return 30;
            else
                return 10;
        default:
            return 0;
    }
}

int is_terminal_fn(Move** move_boards){
    return (*move_boards)->from == -666;
}

int has_loose_cannon(Move** move_boards){
    int prev = (*move_boards)->from;
    int prev_x = (*move_boards)->old_x;
    int prev_y = (*move_boards)->old_y;
    int to, y, x;
    int from = prev;
    move_boards++;
    while((*move_boards)->from != -666){
        from = (*move_boards)->from;
        to = (*move_boards)->to;
        x = (*move_boards)->old_x;
        y = (*move_boards)->old_y;
        if(from == prev && x == prev_x && y == prev_y && from*to<0)
            move_boards++;    
        else
            return 0;
    }
    return from;
}

int eval_fn(Board*b, int no_moves, int depth, int loose_cannon, int length){
    if(no_moves){
        if(b->current_player == 1)
            return 100000 + depth;
        
        else
            return -100000 - depth;
    }
    int o = other_pieces(b);
    int p = player_pieces(b);
    int pawn_bonus;
    int king_bonus;
    int values[9];
    if(o>=16){
        pawn_bonus = 5;
        king_bonus = 10;
//        int values[9] = {0, 20, 20, 30, 80, 70, 0, 0, 20};
        values[1]=30; values[2]=20; values[3] = 30;
        values[4]=80; values[5] = 70; values[8] = 20;
    }else{
        pawn_bonus = 10;
        king_bonus = -10;
//        int values[9] = {0, 40, 30, 50, 20, 20, 0, 0, 80};
        values[1]=50; values[2]=40;values[3]=50;values[4]=20;
        values[5]=30;values[8]=80;
    }
    int his = 0;
    int my = 0;
    int y,x,cell;
    y = 0;
    while(y<8){
        x = 0;
        while(x<8){
            cell = get(b,x,y);
            if(cell && cell > 0)
                my += value_of1(cell,o);
            if(cell && cell < 0)
                his += value_of1(cell,o);            
            if(cell == 2)
                my -= king_bonus;
            else if(cell == -2)
                my += king_bonus;
            if (cell == 1)
                my -= (6-y)*pawn_bonus;
            else if (cell == -1)
                my += (y-1)*pawn_bonus;        
            x++;
        }
        y++;
    }
    if(loose_cannon && length == 1){
        return -p*2-my-value_of1(loose_cannon,o)*5+his+o*2;
        }        
    else
        return -p*2-my-value_of1(loose_cannon,o)*2+his+o*2;
}

int max_value(Board* board, int depth, int alpha, int beta){
    if(time_up())
        return -666;
    Move** moves = next_moves_boards(board);
    int no_moves = 0;
    int loose_cannon = 0;
    int length = number_of_moves(moves);
    if(is_terminal_fn(moves))
        no_moves = 1;
    if(!no_moves && has_loose_cannon(moves))
        loose_cannon = has_loose_cannon(moves);
    int v = -1000000;
    int candidate;
    int return_alpha = 0;
    Move** temp = moves;
    while((*moves)->from != -666){
        
        if(!return_alpha && !(depth <= 0 || no_moves)){
            candidate = min_value((*moves)->b, depth-1, alpha, beta);
            if(candidate>v)
                v = candidate;
            if(v>alpha)
                alpha = v;
            if(alpha >= beta)
                return_alpha = 1;
        }
        moves++;
    }
    //free moves
    free_moves(temp);
    if(no_moves)
        return eval_fn(board, 1, depth, loose_cannon, length);
    if(depth == 0)
        return eval_fn(board, 0, depth, loose_cannon, length);
    if(return_alpha)
        return alpha;
    return v;
}
int min_value(Board* board, int depth, int alpha, int beta){
    if(time_up())
        return -666;
    Move** moves = next_moves_boards(board);
    int no_moves = 0;
    int loose_cannon = 0;
    if(is_terminal_fn(moves))
        no_moves = 1;
    if(!no_moves && has_loose_cannon(moves))
        loose_cannon = has_loose_cannon(moves);
    int v = 1000000;
    int candidate;
    int return_beta = 0;
    int length = number_of_moves(moves);
    Move** temp = moves;
    while((*moves)->from != -666){
        if(!return_beta && !(depth <= 0 || no_moves)){
            candidate = max_value((*moves)->b, depth-1, alpha, beta);
            if(candidate < v)
                v = candidate;
            if(v<beta)
                beta = v;
            if(alpha >= beta)
                return_beta = 1;
        }
        moves++;
    }
    free_moves(temp);
    if(no_moves)
        return eval_fn(board, 1, depth, loose_cannon, length);
    if(depth == 0)
        return eval_fn(board, 0, depth, loose_cannon, length);
    if(return_beta)
        return beta;
    return v;
}

void print_move(Move* best){
    char* horiz = "ABCDEFGH";
    printf("(%c %d)=>(%c %d)\n", horiz[best->old_x], 8-best->old_y, horiz[best->new_x], 8-best->new_y);
    if(best->from != best->to && best->from*best->to>0){
        print_piece(best->from); 
        printf("     ");
        print_piece(best->to);
        printf("\n");
    }
    return;
}

void send_move(Move* best){
    if(best->en_passant)
        printf("%d,%d,%d,%d,7", best->old_x, best->old_y, best->new_x, best->new_y);    
    else if (best->from != best->to && best->from*best->to > 0)
        printf("%d,%d,%d,%d,%d", best->old_x, best->old_y, best->new_x, best->new_y, best->to);
    else
        printf("%d,%d,%d,%d",best->old_x, best->old_y, best->new_x, best->new_y);
    return;   
}
int determine_depth(Board* board, int loose_cannon){
    int p = player_pieces(board);   
    int o = other_pieces(board);
    if(p+o > 25){
//        if(loose_cannon)
//            return 10;
        return 6;
    }
    else if(p+o > 10){
//        if(loose_cannon)
//            return 10;
        return 6;
    }
    else {
//        if(loose_cannon)
//            return 10;
        return 9;
    }
}

int number_of_moves(Move** moves){
    int ctr = 0;
    while((*moves)->from != -666){
        ctr += 1;
        moves ++;
    }
    return ctr;
}

Move* best_move(Board* board, int depth){
    Move** moves = next_moves_boards(board);
    int loose_cannon = 0;
    if(!is_terminal_fn(moves) && has_loose_cannon(moves))
        loose_cannon = has_loose_cannon(moves);
//    printf("LOOSE? : %d\n", loose_cannon);
    int v = -1000000;
    int candidate = 0;
    Move* best = malloc(sizeof(Move));
    best->from = -666;
    Move** temp = moves;
//    int depth = determine_depth(board, loose_cannon);
//    printf("%d: depth\n", depth);
    int length = number_of_moves(moves);
    while((*moves)->from != -666){
//        printf("FROM:%d\n",(*moves)->from);
        if (length != 1){
            candidate = min_value((*moves)->b, depth-1, -1000000, 1000000);   
            if(candidate == -666){
                free_moves(temp);
                return NULL;
            }
        }
        else
            candidate = eval_fn(board, 0, depth, loose_cannon, length);
//        printf("cand:%d, v:%d\n", candidate, v);
        if(candidate >= v){
            v = candidate;
            best->from = (*moves)->from;
            best->to = (*moves)->to;
            best->new_x = (*moves)->new_x;
            best->old_x = (*moves)->old_x;
            best->old_y = (*moves)->old_y;
            best->new_y = (*moves)->new_y;
            best->en_passant = (*moves)->en_passant;
            best->b = NULL;
        }
        moves++;
    }
    free_moves(temp);
//    if(best->from != -666)
//        send_move(best);
//    printf("value: %d\n", v);
//    print_move(best);
    return best;
}

char* make_command(char *str1, char* str2, char *str3){
    char* new = malloc(sizeof(char)*100);
    int ctr = 0;
    while(*str1){
        *(new + ctr) = *str1;
        str1++;
        ctr +=1;
    }while(*str2){
        *(new + ctr) = *str2;
         str2++;
        ctr += 1;
    }
    new[ctr] = ' ';
    ctr +=1;
    new[ctr] = *str3;
    ctr += 1;
    new[ctr] = '\0';
    return new;
}

Move* IDS(Board* board, int depth){
    Move *m = NULL;
    Move *tmp = NULL;
    for(int i=0;i<depth;i++){
        tmp = best_move(board, i);
        if(tmp){
            if(m)
                free(m);
            m = tmp;
        }else{
            printf("%d,",i);
            return m;       
        }
    }       
    printf("%d,",depth);
    return m;
}
int time_up(void){
    gettimeofday(&stop, NULL);
    secs = (double)(stop.tv_usec - start.tv_usec) / 1000000 + (double)(stop.tv_sec - start.tv_sec);
    return secs > maxtime;
}



int main(int argc, char *argv[]){  
    Board* board = NULL;
    Move *m = NULL;
    board = load_from_argv(argv[1], argv[3]);
/*
    printf("NEW STATE\n");
    print_board(board);    

    printf("p:%d, new_x:%d, new_y:%d, old_y:%d\n",board->p, board->new_x, board->new_y, board->old_y);
    Move** moves = next_moves_boards(board);

    while((*moves)->from != -666){
        print_board((*moves)->b);
        print_move(*moves);
        printf("p:%d, new_x:%d, new_y:%d, old_y:%d, FROM:%d , TO:%d\n",(*moves)->b->p, (*moves)->b->new_x, (*moves)->b->new_y, (*moves)->b->old_y, (*moves)->from, (*moves)->to);
        moves++;
    }
*/    
    maxtime = (double)(atoi(argv[2]));
    int depth = 100;
    gettimeofday(&start, NULL);
    m = IDS(board, depth);
    send_move(m);
    if(board){
        free(board->b);
        free(board);
        free(m); 
    }
    return 0;
}

