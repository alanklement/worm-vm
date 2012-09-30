# Compilers and Interpreters

## why?

* need for translation from human to machine
* computers understand 1 language: their instruction set
* human problems are abstract

---
# Compilers and Interpreters

## why?

* humans used to manage this gap
    * convert from problem into abstract idea a solution
    * convert solution into a design of a formal system that can solve it
    * convert the formal system design into instructions that make a machine run it
    * convert those instructions into opcodes
    * run that resulting program

---
# Compilers and Interpreters

## what?

* language as translation from human to computer languages
* languages are used to represent the abstract idea of a system

---
# Compilers and Interpreters

## how?

* two main approaches to crossing that gap: compilers & interpreters


---
# compilers

## compilers / translators

* convert from more human-friendly language to difficult-to-manage machine language
* automates part of the previously human task of converting from abstract to concrete

---
# compilers

* hides architecture-specific details:
    * opcodes
    * specific instructions
    * registers
    * managing the call stack

---
# compilers

* adds features:
    * named variables
    * functions
    * types
    * scope
    * branching constructs (ifs, loops, switch)

---
# compilers

* first compiler written by Grace Hopper in 1952: A-0

---
# interpreters

## interpreters / virtual machines

* convert a difficult-to-manage machine into a more human-friendly machine
* next lecture

---
# language concepts

## base language concepts
* pre-processing / meta-programming
    * macros
    * conditionals
    * include in C vs import in python
    * C++ templates

---
# language concepts

* variables
* types
    * static / dynamic
    * polymorphism
    * casting

---
# language concepts

* functions / subroutines
    * passing arguments
    * return values
* scope
* flow (branching, looping, iterators, switch statements, recursion)

---
# language concepts

* object oriented programming
    * class - code & data
    * help with abstractions: composition, inheritance, first-class functions
    * help with specifics: operators, constructors/destructors, garbage collection

---
# compiler architecture

## compiler architecture
* front end: language to internal representation
    * lexical processing (tokens)
    * preprocessing / meta-programming
    * tokens -> AST
    * semantic processing: AST -> internal representation (often still a tree)

---
# compiler architecture

* middle end: optimizations

---
# compiler architecture

* back end: translate to machine-specfic code
    * serializing to instructions
    * instruction reordering - instruction dependency
        * control (branching)
        * data (variables)
        * aliases
    * register allocation
        * graph coloring
