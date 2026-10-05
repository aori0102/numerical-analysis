# numerical-analysis
A set of Python program to assist in Numerical Analysis course.

## How to use

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