#include <cmath>
#include <iostream>
#include <sstream>
#include <string>
#include "InvestmentCalculator.h"

// Read one complete line so invalid entries do not affect the next prompt.
template <typename T>
bool readNumber(const std::string& prompt, const std::string& error,
                T& value, bool positiveOnly) {
    std::string line;
    while (true) {
        std::cout << prompt;
        if (!std::getline(std::cin, line)) {
            return false;
        }

        std::istringstream input(line);
        T candidate{};
        char extra;
        if ((input >> candidate) && !(input >> extra) &&
            std::isfinite(static_cast<double>(candidate)) &&
            (positiveOnly ? candidate > 0 : candidate >= 0)) {
            value = candidate;
            return true;
        }
        std::cout << error << std::endl;
    }
}

int main() {
    double initialInvestment{};
    double monthlyDeposit{};
    double interestRate{};
    int numberOfYears{};

    std::cout << "**********************************" << std::endl;
    std::cout << "********** Data Input ************" << std::endl;

    if (!readNumber("Initial Investment Amount: ",
                    "Enter a nonnegative number for the initial investment.",
                    initialInvestment, false) ||
        !readNumber("Monthly Deposit: ",
                    "Enter a nonnegative number for the monthly deposit.",
                    monthlyDeposit, false) ||
        !readNumber("Annual Interest: ",
                    "Enter a nonnegative annual interest rate (6 means 6%).",
                    interestRate, false) ||
        !readNumber("Number of years: ",
                    "Enter a positive whole number of years.",
                    numberOfYears, true)) {
        std::cout << "\nInput ended. No calculation was performed." << std::endl;
        return 0;
    }

    std::cout << "**********************************" << std::endl;
    std::cout << "Press Enter to continue..." << std::endl;
    std::string continuation;
    if (!std::getline(std::cin, continuation)) {
        std::cout << "\nInput ended. No calculation was performed." << std::endl;
        return 0;
    }

    InvestmentCalculator calculator(initialInvestment, monthlyDeposit,
                                    interestRate, numberOfYears);

    std::cout << "\nBalance and Interest Without Additional Monthly Deposits" << std::endl;
    std::cout << "Year\t\tYear End Balance\t\tYear End Earned Interest" << std::endl;
    calculator.calculateWithoutMonthlyDeposit();

    std::cout << "\nBalance and Interest With Additional Monthly Deposits" << std::endl;
    std::cout << "Year\t\tYear End Balance\t\tYear End Earned Interest" << std::endl;
    calculator.calculateWithMonthlyDeposit();

    return 0;
}
