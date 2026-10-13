# numerical-analysis
A set of Python program to assist in Numerical Analysis course.

## Calculation Methods

### Packages

Includes these methods:

* [Newton with n iterations](./newton_n.py)

* [Newton with tolerance](./newton_tol.py)

* [False position with n iterations](./false_position_n.py)

* [False position with tolerance](./false_position_tol.py)

* [Secant method with n iterations](./secant_n.py)

* [Secant method with tolerance](./secant_tol.py)

### How to use

* Run `python` with the desired method. `_n` is calculating with n steps, whilst `_tol` is calculating with tolerance.

* Things to know when typing expressions:


  * The variable used in all programs is `x`.
  * When typing multiplication, make sure to use `*`. The program won't recognize `2x`, it must be `2*x`.
  * For power, use `**` instead of `^`. i.e. $2^x$ is `2**x`.
  * Functions like $sin(x)$, $cos(x)$, $tan(x)$,... requires parenthesis. i.e. `sin(x)`, `cos(x)`, `tan(x)`...
  * For exponential function, it should be `exp(x)`.
  * For logarithm:
    * $ln(x)$ is equivalent to `log(x)`or `ln(x)`.
    * $log_a(x)$ is equivalent to `log(x, a)`.
    * $log_{10}(x)$ is equivalent to `log(x, 10)` or `log10(x)`.
    * $log_{2}(x)$ is equivalent to `log(x, 2)` or `log2(x)`.

  * $arcsin(x)$, $arccos(x)$, $arctan(x)$ are equivalent to `asin(x)`, `acos(x)`, `atan(x)` respectively.
  * $\pi$ is equivalent to `pi`. i.e. $\pi/2$ is `pi/2`.

## Sovling system of equations

### Packages

* [Doolittle LU decomposition method](./doolittle_lu.py)

* [Cholesky decomposition method](./cholesky.py)

### How to use

* Run the desired program. It will ask for matrix inputs.

* By default, the program's result will be displayed in simplified expressions (i.e. $1/3$ instead of $0.3333333...$)

* There are some arguments to pass into the program to alter the result to your need:

  * `--nosolve` : This argument tells the program to stop at decomposition without solving the actual system.

  * `--indecimal n` : This argument tells the program to display the result in decimals instead of expression, round to the `n`th digits after the decimal point. If you only pass `--indecimal`, the program will round the results to the 6th digits after the decimal point.

* For Gauss-Jordan method:

  * There is no arguments for `--nosolve`.

  * Use `partialpivot` for switching to partial pivot selection (max value of the first element each row)

  * Use `scaledpivot` for switching to scaled pivot selection (max scalar value of each row)

  * Use `roundtomeaningful n` to make the program round the result to n significant digits after each calculation.