# Project Plan: A Compiler for a Programming Language Based on Lower Kenyang

Course: Compiler Construction, Fall 2026
Group size: Four members
Purpose of this document: to let every member understand the whole project, their own part, and why each part matters

---

## 1. What We Are Building

We are building a **compiler**. A compiler is a program that reads instructions written by a person and turns them into instructions that a computer processor can run directly.

Our compiler will read programs written in a new programming language. The special feature of this language is that its keywords come from **Lower Kenyang**, the language of the Bayangi people. Where a language like C uses the word `if`, our language will use the Kenyang word for "if". Where C uses `while`, ours will use the Kenyang word for "while".

The result, from the user's side, looks like this:

1. A person writes a program using Kenyang keywords and saves it in a file.
2. The person runs our compiler on the file.
3. The compiler produces a program that the computer can run.

### 1.1 What This Project Is Not

This project does not teach the computer to understand ordinary Kenyang sentences. That would be a different and much harder field called natural language processing. Our language has fixed, simple rules, like every other programming language. Only the keywords are Kenyang. This keeps the project possible within one semester.

---

## 2. Why This Is Less Difficult Than It Looks

Many people hear "a programming language in a native tongue" and think the work is enormous. It is not, for three reasons.

1. **The Kenyang part is small.** It is a list of words: one Kenyang word for each keyword such as "if", "while", and "return". Once the list exists, the rest of the compiler does not care what language the words come from. A compiler for Kenyang keywords is built in the same way as a compiler for English keywords.
2. **The compiler is built in small stages.** Each stage does one simple job and passes its result to the next stage. No one has to understand the whole machine at once. Each member owns one or two stages.
3. **The method is already known.** Compilers have been built the same way for decades. Our textbook describes each stage. We are following a proven recipe, not inventing one.

---

## 3. The Journey of One Small Program

To make the plan concrete, here is what happens to one line of code as it moves through the compiler. The Kenyang keywords are written as placeholders in square brackets until the team chooses the real words.

**The program the user writes:**

```
[INTEGER] x = 2 + 3 * 4;
[WRITE](x);
```

**Stage 1. Reading the characters (Lexer).** The compiler cuts the text into pieces called tokens. Each token is one meaningful unit: a keyword, a name, a number, or a symbol.

```
[INTEGER]  x  =  2  +  3  *  4  ;  [WRITE]  (  x  )  ;
```

**Stage 2. Checking the structure (Parser).** The compiler checks that the tokens follow the grammar rules, and it builds a tree showing how they fit together. The tree records that `3 * 4` is done before `+ 2`.

```
        =
       / \
      x   +
         / \
        2   *
           / \
          3   4
```

**Stage 3. Checking the meaning (Semantic Analyser).** The compiler checks that the program makes sense. It confirms that `x` was declared, and that adding and multiplying whole numbers is allowed. If someone wrote `x + "hello"`, this stage would report an error.

**Stage 4. Writing a simple middle form (Intermediate Code).** The tree is turned into a flat list of very small steps.

```
t1 = 3 * 4
t2 = 2 + t1
x  = t2
write x
```

**Stage 5. Making it better (Optimiser).** The compiler notices that `3 * 4` is always 12, so it works it out in advance instead of making the computer do it each time.

```
x = 14
write x
```

**Stage 6. Producing the processor instructions (Code Generator).** The simple steps become assembly language, which is a readable form of the instructions the processor understands.

```
mov  qword ptr [x], 14
mov  rdi, [x]
call print_integer
```

**Stage 7. Final conversion (Assembler and Linker).** Existing tools convert the assembly into a real executable file. The user runs it and sees `14`.

That is the entire compiler. Everything in this plan is one of those seven stages, or the work needed to build and test them.

---

## 4. The Steps, and What Each One Means

Each step below is described in the same way:

- **What it is:** the work, in plain words.
- **Why it matters:** the reason it must be done.
- **When it is finished:** what we have once it works.
- **If it is not finished:** what goes wrong for the rest of the project.

### Step 1. Design the Language

**What it is.** We decide what the language can do and write it down. This includes the list of Kenyang keywords, the kinds of data (whole numbers, decimal numbers, true/false, text), and the statements (declare a variable, assign a value, choose with "if", repeat with "while", define a function, read input, print output). We also write the grammar, which is the set of rules for how a correct program is built.

**Why it matters.** Every other step depends on these decisions. The lexer needs the keyword list. The parser needs the grammar. The code generator needs to know what each statement means. If the language is not decided, no one can start their own work with confidence.

**When it is finished.** We have a short written specification that every member can read. Any question such as "is this allowed?" has a written answer.

**If it is not finished.** Members guess differently and build parts that do not fit together. Changes late in the semester force others to redo finished work.

### Step 2. Choose the Kenyang Vocabulary

**What it is.** We make a table with one row per keyword: the idea (for example "repeat while true"), the Kenyang word, how to type it, and the name of the person who confirmed it is correct.

**Why it matters.** This is the part that makes the project "Kenyang" and not just another small language. It is also the part that examiners will look at first. Words must be correct and agreed by a real speaker, so the language is respectful and accurate.

**When it is finished.** The table is complete and verified. The lexer can be given the table directly.

**If it is not finished.** The compiler still works with temporary words, but the project loses its purpose and the group has no authentic result to present.

**Decision needed:** Kenyang uses letters that are not on an ordinary keyboard. We must decide whether programs are typed with the real Kenyang letters, with a plain English-letter spelling, or with both allowed. Allowing both is recommended, because it is easy to type and still respects the real spelling. We do not mark tone in programs, so we must not choose two keywords that differ only by tone.

### Step 3. Build the Lexer

**What it is.** The lexer reads the program file character by character and cuts it into tokens (see Stage 1 in Section 3). It skips spaces and comments, and it reports any character that does not belong.

**Why it matters.** The rest of the compiler cannot work with raw text. It needs clean, labelled pieces. The lexer is also where the Kenyang keyword table is actually used.

**When it is finished.** Give it a program file and it prints the list of tokens. Give it an illegal character and it reports the line and column.

**If it is not finished.** The parser has nothing to read. The whole compiler stops at the first stage.

### Step 4. Build the Parser

**What it is.** The parser takes the tokens, checks them against the grammar, and builds the tree (Stage 2). If the program breaks a rule, such as a missing bracket, it reports a clear error and keeps going so that several mistakes can be shown at once.

**Why it matters.** This is the stage that understands the shape of the program. Later stages cannot work on a flat list of tokens, because they need to know which parts belong together.

**When it is finished.** A correct program gives a tree that can be printed and inspected. A wrong program gives a helpful message with a line number.

**If it is not finished.** No later stage receives any input. Semantic checking, code generation, and testing all wait.

### Step 5. Build the Semantic Analyser

**What it is.** This stage walks the tree and checks the program's meaning. It keeps a **symbol table**, which is a list of every name in the program and its type. It uses the table to catch mistakes such as using a name that was never declared, adding a number to text, or calling a function with the wrong number of arguments.

**Why it matters.** A program can have perfect grammar and still be nonsense. Without this stage, the compiler would produce broken programs, or crash, and give the user no explanation.

**When it is finished.** Meaningless programs are rejected with a clear message. Valid programs pass through with every part labelled with its type.

**If it is not finished.** The code generator receives wrong or incomplete information. The output programs fail in ways that are hard to trace back to the cause.

### Step 6. Build the Intermediate Code Generator

**What it is.** It converts the tree into a flat list of small steps called three-address code (Stage 4). Each step does one thing, such as one addition or one comparison.

**Why it matters.** This is the bridge between the front half of the compiler (which understands the Kenyang language) and the back half (which understands the processor). Because of this bridge, the two halves can be built and tested separately by different people. It is also the form the optimiser works on.

**When it is finished.** Every valid program can print its list of small steps, and a person can check by hand that the steps match the program.

**If it is not finished.** The code generator has no clean input and must work directly from the tree, which is much harder and breaks the division of work.

### Step 7. Build the Code Generator and Runtime

**What it is.** The code generator turns each small step into processor instructions, written as assembly text (Stage 6). It decides where each variable is stored, how functions receive their inputs and return their results, and how decisions and loops become jumps. The **runtime** is a tiny helper library, written once, that handles things every program needs, such as printing a number to the screen and reading a number typed by the user. Existing tools then assemble and link the result into an executable file.

**Why it matters.** This is the step that delivers what the assignment asks for: machine code. Without it, we have a program checker, not a compiler.

**When it is finished.** A Kenyang program is compiled, the executable runs, and it prints the right answer.

**If it is not finished.** The project has no executable output and cannot meet the main requirement of the course. For this reason it is started early, and a simpler fallback exists (see Section 8).

### Step 8. Optimise

**What it is.** The optimiser improves the small steps before code generation without changing what the program does. The first two improvements are working out constant calculations in advance (Stage 5) and removing steps whose results are never used.

**Why it matters.** It shows we understand how real compilers make programs faster, and it is a normal part of the course. It is also the safest step to shorten if time is short, because the compiler works without it.

**When it is finished.** Compiled programs give the same answers but use fewer instructions. We can show a before-and-after comparison in the report.

**If it is not finished.** The compiler still works correctly. We lose some marks for completeness and lose a good demonstration, but nothing else is blocked. This is the one step that may be reduced if time runs out.

### Step 9. Test Everything

**What it is.** We write many small programs and check the compiler against them. Some programs are correct and must produce known output. Others contain deliberate mistakes and must produce the expected error message.

**Why it matters.** A compiler that works on one example may fail on the next. Tests tell us immediately when a change breaks something, so that we can fix it while the change is still fresh.

**When it is finished.** One command runs all tests and shows which pass and which fail. The suggested test programs are: simple arithmetic, factorial, Fibonacci, greatest common divisor, prime check, and printing text.

**If it is not finished.** We cannot trust any result. Bugs surface at the demonstration, in front of the lecturer.

### Step 10. Write the Documentation and Report

**What it is.** We write the language reference (the keyword table and grammar, so someone else can write programs in our language), and the project report (what we built, why, how it works, test results, and what we did not finish).

**Why it matters.** This is what the lecturer reads and grades. The work is only valuable if it can be understood by someone who was not in the group.

**When it is finished.** A stranger can read it, write a small Kenyang program, compile it, and run it.

**If it is not finished.** Good work is graded as incomplete work.

---

## 5. Who Does What

Each member owns one area and hands the result to the next person. The hand-over format for each stage (the token list, the tree, the small steps) is agreed in the first two weeks, so that everyone can work at the same time and not wait.

| Member | Owns | Receives | Hands over | Why this part is important |
|---|---|---|---|---|
| 1 | Language design, Kenyang vocabulary, Lexer (Steps 1, 2, 3) | The assignment and the group's decisions | Token list | Defines what the language is. Everyone else depends on these decisions. |
| 2 | Grammar, Parser (Step 4) | Token list | Syntax tree | Gives the program its structure. Nothing after it can run without the tree. |
| 3 | Symbol table, Semantic Analyser, Optimiser (Steps 5, 8) | Syntax tree | Checked tree, then improved small steps | Makes sure only meaningful programs continue and makes the output efficient. |
| 4 | Intermediate Code, Code Generator, Runtime, Build tools (Steps 6, 7) | Checked tree | Executable file | Produces the machine code, which is the main requirement of the course. |

**Shared by everyone:** Step 9 (testing) and Step 10 (documentation). Each member writes the tests and the report section for their own stage. Each member also reviews one other member's stage, so that everyone can explain the whole compiler during the oral defence.

The roles are a starting suggestion. The group can change them at the first meeting to suit each person's strengths.

---

## 6. Order and Timing

The weeks below are counted from the day work begins. When the lecturer's deadline is confirmed, the weeks should be stretched or squeezed to fit.

| Weeks | Work | What we have at the end |
|---|---|---|
| 1 | Set up shared folder, choose tools, assign roles | Everyone can run the same project on their own computer |
| 1 to 2 | Steps 1 and 2: language design and vocabulary | Written specification and keyword table |
| 3 to 4 | Steps 3 and 4: lexer and parser | A program file turns into a printed tree |
| 5 to 6 | Step 5: semantic analysis | Bad programs are rejected with clear messages |
| 6 to 7 | Step 6: intermediate code | Every program prints its small steps |
| 7 to 9 | Step 7: code generation and runtime | The first program compiles and runs |
| 9 to 10 | Step 8: optimisation | Before-and-after comparison |
| 10 to 11 | Step 9: full testing and bug fixing | All tests pass |
| 11 to 12 | Step 10: report and demonstration | Submission |

Testing and documentation are written while each step is built. They are not left to the last two weeks.

---

## 7. How We Will Know the Project Is Complete

The project is complete when all five statements below are true.

1. A program written in the Kenyang-based language can be compiled from the command line.
2. The result is an executable file that runs without any extra interpreter.
3. Its output is correct for all of our test programs.
4. Programs with mistakes produce clear error messages that name the line.
5. A person outside the group can follow our documentation to write and run a program.

---

## 8. What Could Go Wrong, and What We Do About It

| Problem | What we do |
|---|---|
| The group cannot agree on a Kenyang word | One named speaker decides, and the choice is written in the table. Changing a word later is cheap, because it only changes one line of the table. |
| Special Kenyang letters appear broken on someone's computer | All files use one standard text format (UTF-8), and the plain English-letter spelling is always accepted too. |
| One stage runs late and the others wait | Each person tests their stage with sample input files written by hand, so that nobody needs to wait for the stage before. |
| The machine code stage proves too hard | We start it early, in week 7 at the latest. If it fails, we fall back to a simpler target: a small virtual machine that runs the small steps directly. The front half of the compiler is the same either way. |
| The project grows too large | We finish the core features first. Extras, such as arrays, are added only after all core tests pass. |
| Differences between computers | We agree on one working environment in week 1. Because the target is the common Linux style of machine code, the group will use Windows Subsystem for Linux. |

---

## 9. Decisions We Must Make in Week 1

1. **Which programming language do we write the compiler in?** It must be one that all four of us can read. Python is recommended because it is quick to write and easy to test. If the course requires a specific language, that decides it.
2. **How are Kenyang letters typed in programs?** Real letters, plain letters, or both. Both is recommended.
3. **What is the deadline, and are there checkpoints before it?** Ask the lecturer.
4. **May we use tools that generate a lexer and parser automatically?** Ask the lecturer. We recommend writing them by hand, because it is not much harder and everyone then understands them fully.
5. **Which extra features, if any, do we attempt after the core is done?**

---

## 10. Glossary

| Term | Meaning |
|---|---|
| Compiler | A program that translates one language into another. Ours translates Kenyang-based programs into machine code. |
| Machine code | The instructions a computer processor runs directly. |
| Assembly | A readable text form of machine code. |
| Token | One meaningful piece of a program: a keyword, a name, a number, or a symbol. |
| Lexer | The stage that cuts program text into tokens. |
| Grammar | The written rules for what a correct program looks like. |
| Parser | The stage that checks the grammar and builds the tree. |
| Syntax tree | A diagram of how the parts of a program fit together. |
| Symbol table | A list of every name in the program and what type it has. |
| Semantic analysis | Checking that a program makes sense, beyond its grammar. |
| Intermediate code | A flat list of very small steps between the tree and the machine code. |
| Optimiser | The stage that improves the small steps without changing the result. |
| Runtime | A small helper library that programs use for printing and reading. |
| Executable | The final file the user can run. |

---

## References

Aho, A. V., Lam, M. S., Sethi, R., and Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.

Cooper, K. D., and Torczon, L. (2011). *Engineering a Compiler* (2nd ed.). Morgan Kaufmann.

Eberhard, D. M., Simons, G. F., and Fennig, C. D. (eds.). *Ethnologue: Languages of the World*. SIL International. Entry for Kenyang (ISO 639-3: ken).

Nystrom, R. (2021). *Crafting Interpreters*. Genever Benning.
