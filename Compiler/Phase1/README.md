# Phase 1 - Lexical Analyzer


This project is a **Lexical Analyzer** developed for the **Compiler course** at **K. N. Toosi University of Technology**, designed by **Professor Morteza Damanafshan**. It serves as a fundamental project for Bachelor-level students to explore the construction of a lexical analyzer for a specific grammar \( G \).

---

## Project Overview

The main goal of this project is to build a lexical analyzer for the grammar \( G \), provided as part of the project description. This lexical analyzer identifies tokens in the input source code and writes them to an output file in a structured format. Additionally, it manages a **symbol table** for identifiers and constants.

### Grammar \( G \)

The lexical analyzer supports the following grammar \( G \):

```
start → program id ; decList funcList block

decList → decs | decList decs
decs → type varList ; | ϵ
type → integer | real | boolean
varList → id | varList , id

funcList → funcList funcDec | ϵ
funcDec → function id parameters : type decList block
parameters → (decList)

block → begin stmtList end
stmtList → stmt | stmtList stmt
stmt → id := expr ;
     | if expr then stmt
     | if expr then stmt else stmt
     | while expr do stmt
     | for id:=expr to expr do stmt
     | return expr ;
     | block

expr → expr and expr | expr or expr
     | expr ∗ expr | expr / expr
     | expr + expr | expr − expr
     | expr relop expr
     | (expr)
     | integerNumber | realNumber
     | true | false
     | id(actualparamlist)
     | id

actualparamlist → expr | actualparamlist, expr | id | ϵ
relop → < | <= | = | <> | >= | >
```

### Token Categories

The analyzer recognizes the following token categories:
1. **Reserved Keywords**: Includes `program`, `if`, `else`, `while`, `return`, `integer`, `real`, and more.
2. **Identifiers**: Variable and function names.
3. **Operators**: Arithmetic (`+`, `-`, `*`, `/`), relational (`<`, `>`, `=`), and logical (`and`, `or`).
4. **Numbers**:
   - **Integer Numbers**: Non-negative integers without leading zeroes.
   - **Real Numbers**: Floating-point numbers, including exponential notation (e.g., `2.3E+16`).
5. **Punctuation**: Includes `;`, `:`, `,`, `(`, `)`.

### Invalid Tokens
The lexical analyzer detects and handles invalid tokens (e.g., integers with leading zeroes such as `05`). These are classified as `Illegal_Lexeme` and are logged in the output file.

---

## System Requirements

- **Python 3.8 or higher**
- **PLY (Python Lex-Yacc)** library  
  Install via pip:
  ```bash
  pip install ply
  ```

---

## Project Structure

- **`lexer.py`**: Implements the lexical analyzer using the PLY library.
- **`main.py`**: Main script to tokenize the input file and write the results to the output file.
- **`input.txt`**: Input file containing the source code to analyze.
- **`output.txt`**: Output file containing the list of tokens.

---

## Usage

1. **Prepare the Input File**:
   - Write the source code you want to analyze in a file named `input.txt` in the root directory of the project.

2. **Run the Program**:
   - Execute the main script:
     ```bash
     python main.py
     ```

3. **Check the Output**:
   - The program processes `input.txt` and writes the results to `output.txt`.

---

## Output Format

The output file includes:
1. **Header**: Contains author information and student ID.
2. **Tokens**: Each line lists a token in the following formats:
   - For identifiers, integers, and real numbers:
     ```
     token_value              <TOKEN_TYPE, SYMBOL_TABLE_INDEX>
     ```
   - For other token types:
     ```
     token_value              <TOKEN_TYPE, ->
     ```

### Example 1

**Input** (`input1.txt`):
```plaintext
program test;
integer x := 10;
real y := 3.14;
if x > 5 then y := y + x;
```

**Output** (`output1.txt`):
```
Mohammad Taha Karbalaee Esmaeili - 40121803          محمد طاها کربلای اسمعیلی - ۴۰۱۲۱۸۰۳
program                       <PROGRAM_KW, ->
test                          <IDENTIFIER, 0>
;                             <SEMICOLON, ->
integer                       <INTEGER_KW, ->
x                             <IDENTIFIER, 1>
:=                            <ASSIGN_OP, ->
10                            <INTEGER_NUMBER, 2>
;                             <SEMICOLON, ->
real                          <REAL_KW, ->
y                             <IDENTIFIER, 3>
:=                            <ASSIGN_OP, ->
3.14                          <REAL_NUMBER, 4>
;                             <SEMICOLON, ->
if                            <IF_KW, ->
x                             <IDENTIFIER, 1>
>                             <GT_OP, ->
5                             <INTEGER_NUMBER, 5>
then                          <THEN_KW, ->
y                             <IDENTIFIER, 3>
:=                            <ASSIGN_OP, ->
y                             <IDENTIFIER, 3>
+                             <ADD_OP, ->
x                             <IDENTIFIER, 1>
;                             <SEMICOLON, ->
```

### Example 2

**Input** (`input2.txt‍‍`):
```plaintext
program prg1;
integer num, divisor, quotient;
begin
    num:=61;
    divisor:=2;
    quotient:=0;
    if num=1 then
        return false;
    else if num=2 then
        return true;
    while divisor<=(num/2) do
    begin
        quotient:=num/divisor;
        if divisor * quotient=num then
            return false;
        divisor:=divisor+1;
    end
    return true;
end
```

**Output** (`output2.txt`):
```
Mohammad Taha Karbalaee Esmaeili - 40121803          محمد طاها کربلای اسمعیلی - ۴۰۱۲۱۸۰۳
program                       <PROGRAM_KW, ->
prg1                          <IDENTIFIER, 0>
;                             <SEMICOLON, ->
integer                       <INTEGER_KW, ->
num                           <IDENTIFIER, 1>
,                             <COMMA, ->
divisor                       <IDENTIFIER, 2>
,                             <COMMA, ->
quotient                      <IDENTIFIER, 3>
;                             <SEMICOLON, ->
begin                         <BEGIN_KW, ->
num                           <IDENTIFIER, 1>
:=                            <ASSIGN_OP, ->
61                            <INTEGER_NUMBER, 4>
;                             <SEMICOLON, ->
divisor                       <IDENTIFIER, 2>
:=                            <ASSIGN_OP, ->
2                             <INTEGER_NUMBER, 5>
;                             <SEMICOLON, ->
quotient                      <IDENTIFIER, 3>
:=                            <ASSIGN_OP, ->
0                             <INTEGER_NUMBER, 6>
;                             <SEMICOLON, ->
if                            <IF_KW, ->
num                           <IDENTIFIER, 1>
=                             <EQ_OP, ->
1                             <INTEGER_NUMBER, 7>
then                          <THEN_KW, ->
return                        <RETURN_KW, ->
false                         <FALSE_KW, ->
;                             <SEMICOLON, ->
else                          <ELSE_KW, ->
if                            <IF_KW, ->
num                           <IDENTIFIER, 1>
=                             <EQ_OP, ->
2                             <INTEGER_NUMBER, 5>
then                          <THEN_KW, ->
return                        <RETURN_KW, ->
true                          <TRUE_KW, ->
;                             <SEMICOLON, ->
while                         <WHILE_KW, ->
divisor                       <IDENTIFIER, 2>
<=                            <LE_OP, ->
(                             <LEFT_PA, ->
num                           <IDENTIFIER, 1>
/                             <DIV_OP, ->
2                             <INTEGER_NUMBER, 5>
)                             <RIGHT_PA, ->
do                            <DO_KW, ->
begin                         <BEGIN_KW, ->
quotient                      <IDENTIFIER, 3>
:=                            <ASSIGN_OP, ->
num                           <IDENTIFIER, 1>
/                             <DIV_OP, ->
divisor                       <IDENTIFIER, 2>
;                             <SEMICOLON, ->
if                            <IF_KW, ->
divisor                       <IDENTIFIER, 2>
*                             <MUL_OP, ->
quotient                      <IDENTIFIER, 3>
=                             <EQ_OP, ->
num                           <IDENTIFIER, 1>
then                          <THEN_KW, ->
return                        <RETURN_KW, ->
false                         <FALSE_KW, ->
;                             <SEMICOLON, ->
divisor                       <IDENTIFIER, 2>
:=                            <ASSIGN_OP, ->
divisor                       <IDENTIFIER, 2>
+                             <ADD_OP, ->
1                             <INTEGER_NUMBER, 7>
;                             <SEMICOLON, ->
end                           <END_KW, ->
return                        <RETURN_KW, ->
true                          <TRUE_KW, ->
;                             <SEMICOLON, ->
end                           <END_KW, ->
```

### Example 3


**Input** (`input3.txt`):
```plaintext
program prg2;

function avg(integer m; integer n;):real
integer sum, num;
real average;
begin
    sum:=0;
    average:=0;
    for num:=m to n do
        sum:=sum+num;
    average:=sum/(n-m+1);
    return average;
end

begin
    a:=avg(1,20);
end
```

**Output** (`output3.txt`):
```
Mohammad Taha Karbalaee Esmaeili - 40121803          محمد طاها کربلای اسمعیلی - ۴۰۱۲۱۸۰۳
program                       <PROGRAM_KW, ->
prg2                          <IDENTIFIER, 0>
;                             <SEMICOLON, ->
function                      <FUNCTION_KW, ->
avg                           <IDENTIFIER, 1>
(                             <LEFT_PA, ->
integer                       <INTEGER_KW, ->
m                             <IDENTIFIER, 2>
;                             <SEMICOLON, ->
integer                       <INTEGER_KW, ->
n                             <IDENTIFIER, 3>
;                             <SEMICOLON, ->
)                             <RIGHT_PA, ->
:                             <COLON, ->
real                          <REAL_KW, ->
integer                       <INTEGER_KW, ->
sum                           <IDENTIFIER, 4>
,                             <COMMA, ->
num                           <IDENTIFIER, 5>
;                             <SEMICOLON, ->
real                          <REAL_KW, ->
average                       <IDENTIFIER, 6>
;                             <SEMICOLON, ->
begin                         <BEGIN_KW, ->
sum                           <IDENTIFIER, 4>
:=                            <ASSIGN_OP, ->
0                             <INTEGER_NUMBER, 7>
;                             <SEMICOLON, ->
average                       <IDENTIFIER, 6>
:=                            <ASSIGN_OP, ->
0                             <INTEGER_NUMBER, 7>
;                             <SEMICOLON, ->
for                           <FOR_KW, ->
num                           <IDENTIFIER, 5>
:=                            <ASSIGN_OP, ->
m                             <IDENTIFIER, 2>
to                            <TO_KW, ->
n                             <IDENTIFIER, 3>
do                            <DO_KW, ->
sum                           <IDENTIFIER, 4>
:=                            <ASSIGN_OP, ->
sum                           <IDENTIFIER, 4>
+                             <ADD_OP, ->
num                           <IDENTIFIER, 5>
;                             <SEMICOLON, ->
average                       <IDENTIFIER, 6>
:=                            <ASSIGN_OP, ->
sum                           <IDENTIFIER, 4>
/                             <DIV_OP, ->
(                             <LEFT_PA, ->
n                             <IDENTIFIER, 3>
-                             <SUB_OP, ->
m                             <IDENTIFIER, 2>
+                             <ADD_OP, ->
1                             <INTEGER_NUMBER, 8>
)                             <RIGHT_PA, ->
;                             <SEMICOLON, ->
return                        <RETURN_KW, ->
average                       <IDENTIFIER, 6>
;                             <SEMICOLON, ->
end                           <END_KW, ->
begin                         <BEGIN_KW, ->
a                             <IDENTIFIER, 9>
:=                            <ASSIGN_OP, ->
avg                           <IDENTIFIER, 1>
(                             <LEFT_PA, ->
1                             <INTEGER_NUMBER, 8>
,                             <COMMA, ->
20                            <INTEGER_NUMBER, 10>
)                             <RIGHT_PA, ->
;                             <SEMICOLON, ->
end                           <END_KW, ->
```

---

## Notes

- The lexical analyzer adheres strictly to the provided grammar \( G \).
- Error handling for illegal lexemes is limited to classification and logging.


---

## Author Information

- **Author**: Mohammad Taha Karbalaee Esmaeili
- **Student ID**: 40121803
- **Acknowledgment**: Designed by **Professor Morteza Damanafshan** for the Compiler course at **K. N. Toosi University of Technology**.