# Airgead Banking Investment Calculator

A C++ console application I completed for SNHU's CS-210 course. It calculates investment growth with and without monthly deposits and displays yearly balances and interest earned.

This project helped me practice organizing code into classes, working with user input, and checking financial calculations.

## What it does

- Takes an initial investment, monthly deposit, annual interest rate, and number of years.
- Calculates interest monthly.
- Prints two yearly reports so the results can be compared.

## Build and run

You need Git and a C++ compiler, such as g++ or clang++.

From a terminal:

```bash
git clone https://github.com/jcoppola86/Airgead-Banking-Investment-Calculator.git
cd Airgead-Banking-Investment-Calculator
g++ -std=c++11 -Wall -Wextra -pedantic src/main.cpp src/InvestmentCalculator.cpp -o investment_calculator
./investment_calculator
```

On macOS, you can substitute `clang++` for `g++`. On Windows with MinGW, the executable is typically `investment_calculator.exe`.

Enter the four requested values, using `6` for a 6% annual interest rate. Press Enter at the continuation prompt to display the reports.

## Example

Inputs:

- Initial investment: $1,000
- Monthly deposit: $100
- Annual interest rate: 6%
- Years: 2

Results from the current program:

| Year | Balance without deposits | Interest that year | Balance with deposits | Interest that year |
| --- | ---: | ---: | ---: | ---: |
| 1 | $1,061.68 | $61.68 | $2,295.23 | $95.23 |
| 2 | $1,127.16 | $65.48 | $3,670.36 | $175.12 |

The program calculates interest on the existing balance before adding each monthly deposit. New deposits begin earning interest the following month.

## Files

- `src/main.cpp`: user input and report headings.
- `src/InvestmentCalculator.h`: calculator class declaration.
- `src/InvestmentCalculator.cpp`: calculations and yearly report output.
- `Pseudocode.txt`: planning notes.
- `CS210_Project2.zip`: archived project copy. The instructions above use the source files in `src`.

## Checks performed

The source compiled with C++11 and the warning flags shown above without compiler warnings. These manual checks were run against the current code:

| Check | Inputs | Observed result |
| --- | --- | --- |
| Monthly growth | $1,000 initial, $100 monthly, 6%, 2 years | Results match the example above |
| Zero interest | $1,000 initial, $100 monthly, 0%, 1 year | $1,000 without deposits; $2,200 with deposits; $0 interest |
| Zero monthly deposit | $1,000 initial, $0 monthly, 6%, 1 year | Both reports show $1,061.68 and $61.68 interest |

After adding input validation, 36 checks passed covering the original example, zero interest/deposits/starting balance, invalid numeric entries, negative values, fractional or out-of-range years, retries, surrounding whitespace, and end of input. These checks do not cover every possible case. Very large finite values or year counts are not capped and can produce overflow or excessive output.

## Current limitations

The program validates complete input lines, rejects nonnumeric or nonfinite values and negative amounts or rates, and requires a positive whole number of years. Invalid entries display a message and prompt again. If input ends, the program exits without calculating. It uses `double` for calculations and displays amounts to two decimal places. It is an academic demonstration, not a production banking application.

## Original course reflection

CS-210 Portfolio Project Reflection

Summarize the project and what problem it was solving.
I chose the Airgead Banking project for my portfolio. The program calculates investment growth over time based on user input for the initial amount, monthly deposit, annual interest rate, and number of years. It solves the problem of helping users understand how their investments grow, both with and without monthly contributions.

What did you do particularly well?
I did a good job keeping the code organized and the output clear. The formatting of the financial report looks professional, and the logic flows smoothly from input to calculation to display. Everything runs consistently without errors.

Where could you enhance your code? How would these improvements make your code more efficient, secure, and so on?
I could strengthen the program by adding more input validation to prevent invalid data from being entered. I’d also refine a few loops to make the program run more efficiently. These changes would make the code more reliable and secure in real-world use.

Which pieces of the code did you find most challenging to write, and how did you overcome this? What tools or resources are you adding to your support network?
The most challenging part was getting the compound interest formulas right and ensuring the results matched what users would expect. I tested the math repeatedly and used class notes and online resources to confirm my calculations. Debugging each step helped me understand how small errors affected the output.

What skills from this project will be particularly transferable to other projects or course work?
This project helped me strengthen my debugging and problem-solving skills, as well as my ability to organize code logically. It also improved my comfort with GitHub and version control, which are essential for any software engineering work.

How did you make this program maintainable, readable, and adaptable?
I kept the code clean and easy to read with consistent indentation, descriptive variable names, and clear comments. Each part of the program is separated into logical sections, so it can be updated easily if new features or calculations are added later.
