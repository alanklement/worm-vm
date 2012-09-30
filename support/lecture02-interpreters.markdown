# Compilers & Interpreters

---
# Interpreters

* Compiling "Interpreter"
* AST Interpreter
* Bytecode Interpreter
* Hybrids

---
# Interpreters

## AST interpreter
* run the tree itself
* store data in tree or outside

---
# Interpreters

## bytecode
* serialize AST to virtual-machine instructions
* can keep complex machine state -> simpler machine language
    * eg, Lua's table operations
* control tables
    * eg, used to lookup bytecode ops
* stack based
    * smaller instructions
    * simpler instructions - easier decoding
    * simpler VM
* register based
    * fewer instructions needed
    * easier to translate to native
    * easier to reorder instructions
    * more efficient

---
# Interpreters

## LUA case study
    # register machine
    local a,t,i          1: LOADNIL 0 2 0
    a=a+i                2: ADD 0 0 2
    a=a+1                3: ADD 0 0 250 ; 1
    a=t[i]               4: GETTABLE 0 1 2
    
    # stack machine
    local a,t,i          1: PUSHNIL 3
    a=a+i                2: GETLOCAL 0 ; a
                         3: GETLOCAL 2 ; i
                         4: ADD
                         5: SETLOCAL 0 ; a
    a=a+1                6: GETLOCAL 0 ; a
                         7: ADDI 1
                         8: SETLOCAL 0 ; a
    a=t[i]               9: GETLOCAL 1 ; t
                        10: GETINDEXED 2 ; i
                        11: SETLOCAL 0 ; a

---
# Interpreters

## JIT
* compile last minute from bytecode to native
* initially slow, eventually fast
* use runtime info to optimize
* can be very architecture specific (eg, SIMD instructions)

---
# Interpreters

## hybrid - bytecode + JIT
1. compile to bytecode
1. run interpreted at first
1. determine critical sections & compile them
1. optionally throw away cached compiled code

---
# language constructs

## c constructs
* function calling
    * passing arguments via register & stack
    * return value in register

---
# language constructs

## c++ oop
* classes vs structs
* function table
* polymorphism
* virtual function table
* manual oop in c  (code samples)

