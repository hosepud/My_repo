#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void print_piece(int n){
    char red[6] = "\033[31m";
    char blue[6] = "\033[34m";
    char end[5] = "\033[0m";
    switch(n){
        case 1:
            printf(" %sp%s ", red, end);
            break;
        case -1:
            printf(" %sp%s ", blue, end);
            break;
        case 2:
            printf(" %sK%s ", red, end);
            break;
        case -2:
            printf(" %sK%s ", blue, end);
            break;       
        case 3:
            printf(" %sN%s ", red, end);
            break;
        case -3:
            printf(" %sN%s ", blue, end);
            break;    
        case -4:
            printf(" %sB%s ", blue, end);
            break;
        case 4:
            printf(" %sB%s ", red, end);
            break;
        case 5:
            printf(" %sR%s ", red, end);
            break;
        case -5:
            printf(" %sR%s ", blue, end);
            break;
        case 8:
            printf(" %sQ%s ", red, end);
            break;
        case -8:
            printf(" %sQ%s ", blue, end);
            break;
        default:
            printf(" %d ", n);
    }
}

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

int* empty_board_array(void){
    int* a = malloc(sizeof(int)*64); 
    int i = 0;
    while(i<64){
        *(a+i) = 0;
         i++;
    }  
    return a;
}


Board* make_board(int* b, int current_player){
    Board* a = malloc(sizeof(Board));
    a->b = b;
    a->current_player = current_player;
    a->is_terminal = 0;
    return a;
}

int get(Board* b, int x, int y){
    if(x<0 || x>7 || y<0 || y>7)
        return -666;
    else
        return b->b[y*8+x];
}

void set(Board* b, int x, int y, int n){
    if(x<0 || x>7 || y<0 || y>7)
        return;
    b->b[y*8+x] = n;
    return;
}

Board* make_initial_board(void){
    Board* b = make_board(empty_board_array(), 1);
    for(int column = 0;column<8;column++){
        set(b, column, 1, -1);
        set(b, column, 6, 1);
    }
    set(b, 0, 0,-5); set(b, 1, 0, -3); set(b, 2, 0, -4); set(b, 3, 0, -8); set(b, 4, 0, -2); set(b, 5, 0, -4); set(b, 6, 0, -3); set(b, 7, 0, -5);
    set(b, 0, 7, 5); set(b, 1, 7, 3); set(b, 2, 7, 4); set(b, 3, 7, 8); set(b, 4, 7, 2); set(b, 5, 7, 4);set(b, 6, 7, 3);set(b, 7, 7, 5); 
    return b;
}

void send_memo(void){
    FILE* memo = fopen("listen.txt", "w");
    fprintf(memo, "1");
    fclose(memo);
    sleep(1);
    memo = fopen("listen.txt", "w");
    fprintf(memo, "0");
    fclose(memo);
    return;
}

Board* load_from_file(int online){
    if(!online)
        send_memo();
    char line[6];
    Board* b = make_board(empty_board_array(), 1);
    FILE* fp = fopen("current_board.txt", "r");
    while(fgets(line, 6, fp) != NULL){
        if(line[2] == '-')
            set(b, line[0]-'0', line[1]-'0', -(line[3]-'0'));
        else
            set(b, line[0]-'0', line[1]-'0', line[2]-'0');
    }
    fclose(fp);
    return b;
}

Board* load_from_argv(char* fp, char* lastmove){
    char line[6];
    int ctr = 0;
    int i = 0;
    Board* b = make_board(empty_board_array(), 1);
    while(ctr<64){
        line[0] = fp[i];line[1] = fp[i+1];line[2] = fp[i+2];line[3] = fp[i+3];
        if(line[2] == '-'){
            set(b, line[0]-'0', line[1]-'0', -(line[3]-'0'));
            i+=5;
        }
        else{
            set(b, line[0]-'0', line[1]-'0', line[2]-'0');
            i+=4;
        }
        ctr++;
    }
    if(lastmove[0]-'0'){
        b->p = -(lastmove[0] - '0');
        b->new_x = lastmove[1]-'0';
        b->new_y = lastmove[2]-'0';
        b->old_y = lastmove[3]-'0';
    }else{
        b->p = -2;
        b->new_x = 2;
        b->new_y = 2;
        b->old_y = 3;
    }
    return b;
}

Board* flipped(Board* b){
    Board* new_b = make_board(empty_board_array(), 1);
    int x,y;
    int from = 0;
    for(x=0;x<8;x++){
        for(y=0;y<8;y++){
            from = get(b, x, y);
            set(new_b, 7-x,7-y, -from);
        }
    }
    return new_b;
}

void print_board(Board* b){
    int y,x;
    y = 0;
    printf("\n  ");
    for(x=0;x<8;x++)
        printf(" %d ", x);
    printf("\n");
    while(y<8){
        x = 0;
        printf("%d ", y);
        while(x<8){
            print_piece(get(b, x, y));
            x++;   
        }
        y++;
        printf("\n");
    }
}

int current_player(Board* b){
    return b->current_player;
}
int other_player(Board* b){
    return b->current_player*(-1);
}

Board* copy_board(Board* b){
    int* new_board_ptr = malloc(sizeof(int)*64);
    int i =0;
    while(i<64){
        *(new_board_ptr+i) = *(i+(b->b));
        i++;
    }
    Board* new_board = malloc(sizeof(Board));
    new_board->b = new_board_ptr;
    new_board->current_player = b->current_player;
    new_board->forced = b->forced;
    new_board->is_terminal = b->is_terminal;
    return new_board;
}

/////////////////////////////////////////////////////////

int is_enemy(int self, int other){
    return (self>0 && other<0) || (self<0 && other>0);
}

int* get_squares_king(int x,int y, Board* b,int name){
        int ctr = 0;
        int adj[16] = {x-1, y, x+1, y, x, y+1, x+1, y+1, x-1, y+1, x, y-1, x+1, y-1, x-1, y-1};
        int* buf = malloc(sizeof(int)*17);
        for(int i=0;i<15;i+=2){
            x = adj[i];
            y = adj[i+1];
            if(!((x >= 8 || y >= 8) || (x <= -1 || y <= -1))){
                if(!get(b, x, y) || is_enemy(name, get(b, x, y))){
                    buf[ctr] = x;
                    buf[ctr+1] = y;
                    ctr+=2;
                }
            }
        }
        buf[ctr] = -666;
        return buf;  
}

////////////////////////////////////////////////////////

int* get_squares_knight(int x, int y, Board* b, int name){
    int ctr = 0;
    int adj[16] = {x+1, y-2, x+1, y+2, x+2, y-1, x+2, y+1, x-1, y-2, x-1, y+2, x-2, y-1, x-2, y+1};
    int* buf = malloc(sizeof(int)*17);
    for(int i=0;i<15;i+=2){
        x = adj[i];
        y = adj[i+1];
        if(!((x >= 8 || y >= 8) || (x <= -1 || y <= -1))){
            if(!get(b, x, y) || is_enemy(name, get(b, x, y))){
                
                buf[ctr] = x;
                buf[ctr+1] = y;
                ctr+=2;
            }
        }
    }
    buf[ctr] = -666;
    return buf;  
}
//////////////////////////////////////////////////////////
int* get_diags(int x, int y, Board* b, int name){
        int* buf = malloc(sizeof(int)*33);
        int i = x;
        int j = y;
        int ctr = 0;
        for(int quadrant=1;quadrant<5; quadrant++){
            x = i;
            y = j;
            while(1){
                if(x!=i || y!=j){
                    if(x > 7 || y > 7 || x < 0 || y < 0)
                        break;
                    if(get(b, x,y) && is_enemy(name, get(b, x ,y))){
                        buf[ctr] = x;
                        buf[ctr+1] = y;
                        ctr+=2;
                        break;
                    }else if(get(b,x,y)){
                        break;
                    }else{
                        buf[ctr] = x;
                        buf[ctr+1] = y;
                        ctr+=2;
                    }
                }
                if(quadrant == 1){
                    x-=1;
                    y-=1;
                }else if(quadrant == 2){
                    x+=1;
                    y-=1;
                }else if(quadrant == 3){
                    x+=1;
                    y+=1;
                }else if(quadrant == 4){
                    x-=1;
                    y+=1;
                }
            }
        }
        buf[ctr] = -666;
        return buf;    
}

int* get_squares_bishop(int x, int y, Board* b, int name){
    return get_diags(x, y, b, name);
}
    
/////////////////////////////////////////////////////// 
int* get_lines(int x, int y, Board* b, int name){
        int* buf = malloc(sizeof(int)*65);
        int i = x; int j = y;
        int ctr = 0;
        for(int quadrant=1;quadrant<5;quadrant++){
            x = i; y = j;
            while(1){
                if(x!=i || y!=j){
                    if(x > 7 || y > 7 || x < 0 || y < 0)
                        break;
                    if(get(b, x,y) && is_enemy(name, get(b, x ,y))){
                        buf[ctr] = x;
                        buf[ctr+1] = y;
                        ctr+=2;
                        break;
                    }else if(get(b,x,y)){
                        break;
                    }else{
                        buf[ctr] = x;
                        buf[ctr+1] = y;
                        ctr+=2;
                    }
                }
                if(quadrant == 1){
                    y-=1;
                }else if(quadrant == 2){
                    y+=1;
                }else if(quadrant == 3){
                    x-=1;
                }else if(quadrant == 4){
                    x+=1;
                }
            }
        }
        buf[ctr] = -666;
        return buf;    
}

int* get_squares_rook(int x, int y, Board* b, int name){
    return get_lines(x, y, b, name);
}

int* get_squares_queen(int x, int y, Board* b, int name){
    int ctr = 0;
    int* buf = malloc(sizeof(int)*(64+33));
    int *diags = get_diags(x, y, b, name);
    int *lines = get_lines(x, y, b, name);
    int* temp = diags;
    while(*diags != -666){
        buf[ctr] = *diags;
        ctr+=1;
        diags++;
    }
    free(temp);
    temp = lines;
    while(*lines != -666){
        buf[ctr] = *lines;
        ctr+=1;
        lines++;
    }
    free(temp);
    buf[ctr] = -666;
    return buf;
}

int en_passant_white(Board* b, int x, int y){
    int truth = (b->p == -1) && (b->new_y - b->old_y==2) && (b->new_x == x-1 || b->new_x == x+1) && y == b->new_y;
    if(truth){
        if(b->new_x == x+1)
            return x+1;
        else if(b->new_x == x-1)
            return x-1;
    }
    return -1;
}

int en_passant_black(Board* b, int x, int y){
    int truth = (b->p == 1) && (b->old_y - b->new_y==2) && (b->new_x == x-1 || b->new_x == x+1) && y == b->new_y;
    if(truth){
        if(b->new_x == x+1)
            return x+1;
        else if(b->new_x == x-1)
            return x-1;
    }
    return -1;
}
      
int* get_squares_pawn_white(int x, int y, Board* b, int name){
        int* adj = malloc(sizeof(int)*15);
        int ctr = 0;
        if(y == 6)
            if(!get(b, x, y-1) && !get(b,x, y-2)){
                adj[ctr] = x;
                adj[ctr+1] = y-2;
                ctr+=2;
            }
        if(!get(b, x, y-1)){
            adj[ctr] = x;
            adj[ctr+1] = y-1;
            ctr+=2;
        }    
        if(x>0 && get(b, x-1, y-1) && is_enemy(name, get(b, x-1, y-1))){
            adj[ctr] = x-1; 
            adj[ctr+1] = y-1;
            ctr+=2;
        }
        if(x<7 && get(b, x+1, y-1) && is_enemy(name, get(b, x+1, y-1))){
            adj[ctr] = x+1; 
            adj[ctr+1] = y-1;
            ctr+=2;
        }
        if(en_passant_white(b, x, y) != -1){
            adj[ctr] = en_passant_white(b,x,y);
            adj[ctr+1] = y-1;
            ctr += 2;
        }
        adj[ctr] = -666;
/*        int i = 0;
        while(adj[i]!=-666){
            printf("%d %d\n", adj[i], adj[i+1]);
            i+=2;
        }
        printf("done\n");
*/
        return adj;
}

int* get_squares_pawn_black(int x, int y, Board* b, int name){
        int* adj = malloc(sizeof(int)*15);
        int ctr = 0;
        if(y == 1){
            if(!get(b, x, y+1) && !get(b, x, y+2)){
                adj[ctr] = x;
                adj[ctr+1] = y+2;
                ctr+=2;
            }
        }
        if(!get(b, x, y+1)){
            adj[ctr] = x;
            adj[ctr+1]=y+1;
            ctr+=2;
        }    
        if(x>0 && get(b, x-1, y+1) && is_enemy(name, get(b, x-1, y+1))){
            adj[ctr] = x-1;
            adj[ctr+1] = y+1;
            ctr+=2;
        }
        if(x<7 && get(b, x+1, y+1) && is_enemy(name, get(b, x+1, y+1))){
            adj[ctr] = x+1;
            adj[ctr+1]=y+1;
            ctr+=2; 
        }
        if(en_passant_black(b, x, y) != -1){
            adj[ctr] = en_passant_black(b,x,y);
            adj[ctr+1] = y+1;
            ctr += 2;
        }
        adj[ctr] = -666;
        return adj;
}

/////////////////////////////////////////   

int extend(int* buf, int* temp_coords, int ctr, int x, int y){
    int i = 0;
    int j = 0;
    while(*(temp_coords+i)!=-666){
        *(buf+j+ctr) = *(temp_coords+i);
        *(buf+j+ctr+1) = *(temp_coords+i+1);
        *(buf+j+ctr+2) = x;
        *(buf+j+ctr+3) = y;
        i+=2;
        j+=4;
    }    
    free(temp_coords);
    return j;
}

int* next_boards(Board* b){
        int* buf = malloc(sizeof(int)*1000);
        int p = b->current_player;
        int y,x, cell,ctr; y=ctr=0;
        while(y<8){
            x = 0;
            while(x<8){
                cell = get(b, x,y);
                if(cell && cell*p > 0){
                    switch(cell){
                        case 1:
                            ctr+=extend(buf, get_squares_pawn_white(x,y,b,2), ctr, x, y);
                            break;
                        case 2:
                            ctr+=extend(buf, get_squares_king(x,y,b,2), ctr,x,y);
                            break;
                        case 3:
                            ctr+=extend(buf, get_squares_knight(x,y,b,3), ctr,x,y);
                            break;   
                        case 4:
                            ctr+=extend(buf, get_squares_bishop(x,y,b,4), ctr,x,y);
                            break; 
                        case 5:
                            ctr+=extend(buf, get_squares_rook(x,y,b,5), ctr,x,y);
                            break;
                        case 8:
                            ctr += extend(buf, get_squares_queen(x,y,b,8), ctr,x,y);
                            break;
                        case -1:
                            ctr+=extend(buf, get_squares_pawn_black(x,y,b,-1), ctr, x, y);
                            break;
                        case -2:
                            ctr+=extend(buf, get_squares_king(x,y,b,-2), ctr,x,y);
                            break;
                        case -3:
                            ctr+=extend(buf, get_squares_knight(x,y,b,-3), ctr,x,y);
                            break;   
                        case -4:
                            ctr+=extend(buf, get_squares_bishop(x,y,b,-4), ctr,x,y);
                            break; 
                        case -5:
                            ctr+=extend(buf, get_squares_rook(x,y,b,-5), ctr,x,y);
                            break;
                        case -8:
                            ctr += extend(buf, get_squares_queen(x,y,b,-8), ctr,x,y);
                            break;
                            
                    }
                
                }   
                x++;
            }
            y++;
        }
        buf[ctr] = -666;
        return buf;
}

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

void fill_move(Board* b, int from, int new_x, int new_y, int old_y){
    b->p = from;
    b->new_x = new_x;
    b->new_y = new_y;
    b->old_y = old_y;
    return;
}

Move* move_board(int old_x, int old_y, int new_x, int new_y, Board* b){
    Move* m = malloc(sizeof(Move));
    if(old_x != -666){
        int from = get(b, old_x, old_y);
        int to = get(b, new_x, new_y);
        m->from = from; m->to = to; m->new_x = new_x; m->new_y = new_y;
        m->old_x = old_x; m->old_y = old_y; m->b = copy_board(b);
        set(m->b, old_x, old_y, 0);
        set(m->b, new_x, new_y, from);
        m->b->current_player*=(-1);
        fill_move(m->b, from, new_x, new_y, old_y);  
    }else{
        int from = -666;
        int to = -666;
        m->from = from; m->to = to; m->new_x = new_x; m->new_y = new_y;
        m->old_x = old_x; m->old_y = old_y; m->b = copy_board(b);
        m->b->current_player*=(-1);
        fill_move(m->b, from, new_x, new_y, old_y);
    }
    m->en_passant = 0;
    return m;
}

int is_promotion(int new_x, int new_y, int old_x, int old_y, Board* b){
    int piece = get(b, old_x, old_y);
    return (piece == 1 && new_y == 0) || (piece == -1 && new_y == 7);
}

Move** promotion_boards(int old_x, int old_y, int new_x, int new_y, Board* b){
    int promoteds[5] = {2,3,4,5,8};
    int ctr, piece;
    ctr = 0;
    Move** promotion_boards = malloc((sizeof(int)*64 + sizeof(Board) + sizeof(Move))*10);
    Move* m = NULL;
    int from = get(b, old_x, old_y);
    for(int i = 0;i<5;i++){
        piece = promoteds[i];
        m = malloc(sizeof(Move));
        m->from = from;
        m->to = piece*b->current_player;
        m->old_x = old_x; m->old_y = old_y; m->new_x = new_x; m->new_y = new_y;
        m->b = copy_board(b);
        m->b->current_player *= (-1);
        set(m->b, new_x, new_y, m->to);
        set(m->b, old_x, old_y, 0);
        m->en_passant = 0;
        promotion_boards[ctr] = m;
        fill_move(m->b, m->from, new_x, new_y, old_y);
        ctr += 1;
        }
    promotion_boards[ctr] = move_board(-666, -666, -666, -666, b);
    return promotion_boards;
}

void free_moves(Move** moves){
    Move** temp = moves;
    while((*moves)->from != -666){
        free((*moves)->b->b);
        free((*moves)->b);
        free((*moves));
        moves++;
    }
    free((*moves)->b->b);
    free((*moves)->b);
    free((*moves));
    free(temp);
    return;
}

Move** get_forced(Move** ans, Board* b){ 
    Move** temp = NULL;   
    Move** forced = malloc((sizeof(int)*64 + sizeof(Board) + sizeof(Move))*100);
    temp = ans;
    int ctr = 0;
    int cell;
    while((*temp)->from != -666){
 //       print_board((*temp)->b);
        cell = get(b, (*temp)->new_x, (*temp)->new_y);
        if(((*temp)->to != 0 && (*temp)->from*cell < 0) || (*temp)->en_passant){
            forced[ctr] = *temp;
            ctr += 1;
        }
        
        temp++;
    }
    forced[ctr] = move_board(-666, -666, -666, -666, b);
    if((*forced)->from == -666){
        free((*forced)->b->b);
        free((*forced)->b);
        free((*forced));
        free(forced);
        return ans;
    }else{
        temp = ans;
        while((*temp)->from != -666){
            cell = get(b, (*temp)->new_x, (*temp)->new_y);
            if(!(((*temp)->to != 0 && (*temp)->from*cell < 0) || (*temp)->en_passant)){
                free((*temp)->b->b);
                free((*temp)->b);
                free((*temp));
            }
            temp++;
        }
        free((*temp)->b->b);
        free((*temp)->b);
        free((*temp));
        free(ans);
        return forced;
    }
    
}

int is_en_passant(int new_x, int new_y, int old_x, int old_y, Board* b){
    if(b->current_player == 1) 
        return (en_passant_white(b, old_x, old_y) != -1) && (new_x-old_x == 1 || old_x-new_x == 1) && (get(b, old_x, old_y) == 1);
    else        
        return (en_passant_black(b, old_x, old_y) != -1) && (new_x-old_x == 1 || old_x-new_x == 1) && (get(b, old_x, old_y) == -1);
}

Move* en_passant_board(int new_x, int new_y, int old_x, int old_y, Board* b){
//    printf("ANPASSANING\n");
    Move* m = malloc(sizeof(Move));
    int to;
    int from;
    if(old_x != -666){
        m->b = copy_board(b);
        m->en_passant = 1;
        if(b->current_player == 1){
            to = get(b, new_x, new_y+1);
        }else{
            to = get(b, new_x, new_y-1);            
        }
        from = get(b, old_x, old_y);
        m->from = from; m->to = to; m->new_x = new_x; m->new_y = new_y;
        m->old_x = old_x; m->old_y = old_y;
        set(m->b, new_x, new_y, from);
        set(m->b, b->new_x, b->new_y, 0);
        set(m->b, old_x, old_y, 0);
        m->b->current_player*=(-1);
        fill_move(m->b, from, new_x, new_y, old_y);      
    }
//    print_board(m->b);
    return m;
}

Move** next_moves_boards(Board* b){
    int* buf = next_boards(b);
    int* temp = buf;
    Move** ans = malloc((sizeof(int)*64 + sizeof(Board) + sizeof(Move))*100); 
    Move** promotions = NULL;
    Move** temp2 = NULL;
    int new_x, new_y, old_x, old_y, ctr;
    ctr = 0;
    while(*buf != -666){
        new_x = *buf;
        new_y = *(buf+1);
        old_x = *(buf+2);
        old_y = *(buf+3);
        buf+=4;
//        printf("new_x:%d, new_y:%d, old_x:%d, old_y:%d HERE\n", new_x, new_y, old_x, old_y);
        if(is_promotion(new_x, new_y, old_x, old_y, b)){
            promotions = promotion_boards(old_x, old_y, new_x, new_y, b);
            temp2 = promotions;
            while((*promotions)->from != -666){
                ans[ctr] = (*promotions);
                ctr+=1;
                promotions++;    
            }
            free((*promotions)->b->b);
            free((*promotions)->b);
            free((*promotions));
            free(temp2);                
        }else if(is_en_passant(new_x, new_y, old_x, old_y, b)){
       //     printf("new_x:%d, new_y%d, old_x:%d, old_y:%dHERE\n", new_x, new_y, old_x, old_y);
            ans[ctr] = en_passant_board(new_x, new_y, old_x, old_y, b);
//            print_board(ans[ctr]->b);
            ctr+=1;        
        }else{
            ans[ctr]=move_board(old_x, old_y, new_x, new_y, b);
            ctr += 1;
        }
    }
    ans[ctr] = move_board(-666, -666, -666, -666, b);
    free(temp);
    return get_forced(ans, b);
}


/*
int main(void){  
    Board* board = load_from_file(0); 
//    set(board, 2, 4, 1);
    set(board, 1,4,-1);
    set(board,2,5,1);
    board->new_x = 2;
    board->new_y = 4;
    board->old_y = 5;
    board->p = 1;
    board->current_player *= -1;
    print_board(board);
    int* xys = get_squares_pawn_black(1, 4, board, 1);
    int i;
    while(xys[i] != -666){
        printf("(%d %d)\n", xys[i], xys[i+1]);
        i+=2;
    }

    Move** moves = next_moves_boards(board);
    while((*moves)->from != -666){
            print_board((*moves)->b);
            printf("from:%d, to:%d", (*moves)->from, (*moves)->to);   
        
        moves++;
    }
    printf("\n");
    return 0;
}

*/
