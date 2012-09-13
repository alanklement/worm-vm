
typedef struct Car {
    int nwheels;
} Car;

void Car_init(Car* c, int num_wheels) {
    c->nwheels = num_wheels;
}

void Car_free(Car* c) {
    c->nwheels = 0;
}

void Car_add_wheel(Car* c) {
    ++c->nwheels;
}

void local() {
    Car c;
    Car_init(&c, 4);

    Car_add_wheel(&c);

    Car_free(&c);
}

void dynamic() {
    Car* c = malloc(sizeof(Car));
    Car_init(c, 4);

    Car_add_wheel(c);

    Car_free(c);
    free(c);
}

