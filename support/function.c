
int no_call() {
    int x = 1;
    int y = 2;
    int z = x + y;
}

int add(int a, int b) {
    return 300 * a + b;
}

int use_add() {
    int x = 1;
    int y = 2;
    int z = add(y, x);
}

int something() {
    int a = 1;
    int b = 2;
    int c = a + b + 3;
    a = b * 2;
}

static int G = 0;
int branchy(int x) {
    if (x <= 0) {
        --G;
        return 0;
    }
    return branchy(x - 1);
}



int yay(int a, int b) {
    return a + b;
}


typedef struct Yay {
    int a;
    int b;
} Yay;

int yay_with_struct(Yay y) {
    return y.a + y.b;
}

