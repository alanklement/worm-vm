
class Car {

    int nwheels;

public:
    Car(int num_wheels) {
        this.nwheels = num_wheels;
    }

    ~Car() {
        this.nwheels = 0;
    }

    void add_wheel() {
        ++this.nwheels;
    }
};

void local() {
    Car c(4);

    c.add_wheel();
}

void dynamic() {
    Car* c = new Car(4);

    c->add_wheel();

    delete(c);
}

