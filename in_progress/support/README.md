### Week 7 - Programming Languages Implementation

What's involved in implementing a programming language? Topics: compilers, interpreters, lexing,
parsing, optimization, JIT, etc.

Instructor: [Heewa Barfchin](http://twitter.com/Heewa), [Chartbeat](http://chartbeat.com/)


## Lectures

1. [Lecture 1](https://github.com/generalassembly-studio/cs-for-hackers/blob/master/week-07/lecture01-compilers.markdown): Compilers 
1. [Lecture 2](https://github.com/generalassembly-studio/cs-for-hackers/blob/master/week-07/lecture02-interpreters.markdown): Interpreters

## Hacking Challenge: WORM

Assignment: Implement a virtual machine (like python) that can run worm bytecode. I've provided an assembler (wiggle.py) and separately a reference file (wormassembly.py) that explains the register layout and instructions you need to support. There's also a sample file (language.txt) of some assembly code (that you can convert to bytecode with wiggle.py).


### Sample Programs

The programs directory contains some worm-assembly programs I've tried out on my own Worm VM. Most of them use input, but some don't, so you can try those before implementing READ, WRITE, and the E register.


### Assembly into Bytecode

Given some assembly program in a file (maybe with the extention .worma), you can use the wiggle.py program to assemble it into bytecode, in either hex ascii or binary. Run wiggle with --help to see how.

* binary (default): the file contains only instructions, no extra bytes.
* hex: the file contains one instruction in hex per line (so, 1 newline per instruction)

If you choose to implement the Worm VM in a low level language, like C/C++/Obj-C/Lisp/etc, then it'll probably be easier to use the binary format. If you use a pleasant dynamic language with tons of string manipulation support, like Python/Ruby/etc, then probably the hex format will be easier to deal with.


### Instruction Format

Each instruction is 4 bytes long. The makeup of those bytes is dependent on the instruction. However, the highest 4 bits are always the instruction code. The rest depends on how many arguments, and what kind of argument the instruction takes.

* **no arguments**: the rest of the instruction is to be ignored. For ex, NOOP's code is 0x0, so a NOOP instruction might look like 0x00000000. Or WRITE's code is 0x6, so a WRITE instruction might look like: 0x60000000.
* **two register arguments**: the next 4 bits are a register identifier (encoded as a binary positive integer), and the following 4 bits are the other register identifier. For ex, MOVE (code 0x2) takes a dest register and a src register, so MOVE %B, %C (B is register 1, and C is register 2) would look like 0x21200000.
* **one long value argument**: the rest of the instruction is 1 binary encoded positive integer. For ex, JMP takes 1 argument (the instruction # to jump to), and its code is 0xB, so an instruction to jump to instruction #16 would look like: 0xB0000010.
* **one register argument & one short value**: the next 4 bits are a register identifier (encoded as a binary positive integer), and the following bits are the value. For ex, SET (code 0x1) takes a dest register and a value to set it to, so SET %S, $18 (S is register 5) would look like 0x15000012.


### Registers

This virtual machine has 4 scratch registers (0-3, identified in assembly as A-D), one magic EOF register (4, identified in assembly as E), and one stack register (5, identified in assembly as S). The stack register isn't special, it can be used however you like, it's just that way for convention.

**IMPORTANT**: The E register needs to contain a 1 when there are definitely no more numbers to read from stdin, and 0 otherwise. However, you don't strictly *have* to keep it up to date at all times, it only needs to be correct when the program tries to use that register, like a MOVE or STORE instruction that refers to it.


### Instructions

#### NOOP
* code: 0x0
* arguments: None
* effect: nothing

#### SET
* code: 0x1
* arguments: dst register ID (4 bits), 1 short value (24 bits)
* effect: the dst register is set to the given value
* Ex: SET %A, $20  ==>  0x10000014

#### MOVE
* code: 0x2
* arguments: dst register ID (4 bits), src register ID (4 bits)
* effect: the dst register is set to the value of the src register
* Ex: MOVE %D, %B  ==>  0x23100000

#### LOAD
* code: 0x3
* arguments: dst register ID (4 bits), stack pointer register ID (4 bits)
* effect: the dst register is set to the value of the memory location 
  identified by the value of the stack pointer register
* Ex: LOAD %C, @A  ==>  0x32000000. If register A contains the number
  8, and the 7th stack (memory) location (0-indexed) contains a 43, then after
  this instruction, register C should contain a 43.

#### STORE
* code: 0x4
* arguments: stack pointer register ID (4 bits), src register ID (4 bits)
* effect: the memory location identified by the value of the stack pointer
  register is set to the value of the src register
* Ex: STORE @B, %E  ==>  0x41400000. If register B contains the number
  0, and register E contains the number 1, then after this instruction executes
  the 1st stack (memory) location (0-indexed) should contain a 1.

#### READ
* code: 0x5
* arguments: None
* effect: a number from standard input is stored in register A
* Ex: READ  ==>  0x50000000. If the next number of standard input is 74,
  then after this instruction runs, register A should contain 74. The
  behavior is not defined for the case where there are no more numbers to
  read from standard input. But unless you've hit EOF (or an input error
  occurs), then you *HAVE* to do whatever necessary to put a number into
  this register, including waiting for more input.

#### WRITE
* code: 0x6
* arguments: None
* effect: the contents of register A are written to stdout
* Ex: WRITE  ==>  0x60000000. If register A contains 39, then after this
  instruction executes, "39\n" should be written to stdout.

#### ADD
* code: 0x7
* arguments: dst register ID (4 bits), src register ID (4 bits)
* effect: the dst register is set to the sum of itself and the src register
* Ex: ADD  %D, %B  ==>  0x73100000. If register D contains 39, and register
  B contains -19, then after this instruction executes, register D should
  contain 20.

#### SUB
* code: 0x8
* arguments: dst register ID (4 bits), src register ID (4 bits)
* effect: the dst register is set to the difference of itself and the src register
* Ex: SUB  %D, %B  ==>  0x73100000. If register D contains 20, and register
  B contains 19, then after this instruction executes, register D should
  contain 39.

#### MUL
* code: 0x9
* arguments: dst register ID (4 bits), src register ID (4 bits)
* effect: the dst register is set to the product of itself and the src register
* Ex: MUL  %D, %B  ==>  0x73100000. If register D contains 3, and register
  B contains 13, then after this instruction executes, register D should
  contain 39.

#### DIV
* code: 0xA
* arguments: dst register ID (4 bits), src register ID (4 bits)
* effect: the dst register is set to the quotient (result of division...yes, I
  had to ask 3 people that, one of which had to google it for us to find out...
  and one of them used to work at Bloomberg...sigh) of itself and the src
  register
* Ex: DIV  %D, %B  ==>  0x73100000. If register D contains 3, and register
  B contains 2, then after this instruction executes, register D should
  contain 1.

#### JMP
* code: 0xB
* arguments: instruction location (28 bits, 0-indexed) to execute next
* effect: the next instruction to execute shall be value'th instruction in
  the program
* Ex: JMP $1  ==>  0xB0000001. The next instruction to execute shall be
  the 2nd instruction of the program, and normally after that (so, unless
  that instruction is a jmp itself, then the following instruction should
  be the 3rd one (index 2).

#### JMP_Z
* code: 0xC
* arguments: instruction location (28 bits, 0-indexed) to execute next
* effect: if register A contains a 0, the next instruction to execute shall
  be value'th instruction in the program, otherwise nothing shall happen
* Ex: JMP\_Z $1  ==>  0xC0000001. If register A contains a 0, then the next
  instruction to execute shall be the 2nd instruction of the program, otherwise
  the instruction following this one should be executed next.

#### JMP_NZ
* code: 0xD
* arguments: instruction location (28 bits, 0-indexed) to execute next
* effect: if register A doesn't contain a 0, the next instruction to execute shall
  be value'th instruction in the program, otherwise nothing shall happen
* Ex: JMP\_Z $1  ==>  0xD0000001. If register A contains anything besides a 0,
  then the next instruction to execute shall be the 2nd instruction of the
  program, otherwise the instruction following this one should be executed next.

#### JMP_GT
* code: 0xE
* arguments: instruction location (28 bits, 0-indexed) to execute next
* effect: if register A contains a number bigger than 0, the next instruction
  to execute shall be value'th instruction in the program, otherwise nothing
  shall happen
* Ex: JMP\_GT $1  ==>  0xE0000001. If register A contains a 1 or greater,
  then the next instruction to execute shall be the 2nd instruction of the
  program, otherwise the instruction following this one should be executed next.

#### JMP_LT
* code: 0xF
* arguments: instruction location (28 bits, 0-indexed) to execute next
* effect: if register A contains a number smaller than 0, the next instruction
  to execute shall be value'th instruction in the program, otherwise nothing
  shall happen
* Ex: JMP\_LT $1  ==>  0xF0000001. If register A contains a -1 or greater,
  then the next instruction to execute shall be the 2nd instruction of the
  program, otherwise the instruction following this one should be executed next.


![](https://github.com/generalassembly-studio/cs-for-hackers/raw/master/week-07/worm.png)


# SPOILER WARNING!!!


### General Tips

* Have a "verbose" mode, where you print the state of registers and ram after every instruction executes.
* Have a "debug" mode where the VM pauses after every instruction waiting for you to press a key to continue.
* It's perfectly ok to fake things to put them off for later. Like input - you can start by "read"ing a random number, and putting a random 0 or 1 into the E register at every cycle.


### Process

1. read bytecode file - turn into a list of instructions, print how many
1. start decoding instructions - print the name of each instruction
1. decode rest of instructions - print arguments
1. implement one easy instruction - set, for example; then "run" the program
   by ignoring any instructions you haven't yet implemented
1. keep implementing the next easiest instruction untill you're done
* Ease of implementation for instructions:
    1. register based ones: set, move, math
    1. output: write
    1. fake input (not really from stdin, make up numbers): read
    1. ram: load, store
    1. jumps
    1. real input


### SUPER SPOILERS!!! OUTRIGHT INSTRUCTIONS!!!

* [How to read instructions](SPOILER_reading.md)
* [How to deal with instructions](SPOILER_instructions.md)
* [How to implement registers](SPOILER_registers.md)
* [How to implement ram](SPOILER_ram.md)
* [How to implement_jumps](SPOILER_jumps.md)
* [How_to_implement_input](SPOILER_input.md)
