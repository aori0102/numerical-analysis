from sympy import Symbol, lambdify, sympify

def main():
    f_expr_str = input("Enter f(x) = 0 (e.g., x**3 - x - 1): ")
    n = int(input("Enter number of iterations n (up to p_n): "))
    p0_expr_str = input("Enter p0: ")
    p1_expr_str = input("Enter p1: ")
    p0 = float(sympify(p0_expr_str).evalf())
    p1 = float(sympify(p1_expr_str).evalf())

    x = Symbol('x')
    f_expr = sympify(f_expr_str)
    f_func = lambdify(x, f_expr, 'numpy')

    print("\nIteration Results:")
    results = solve(f_func, p0, p1, n)
    print_table(results)
        
def calculate(f_func, p0, p1):
    return p1 - (f_func(p1) * (p1 - p0)) / (f_func(p1) - f_func(p0))

def solve(f_func, p0, p1, n):
    results = [p0, p1]
    if(n < 2):
        return results
    
    for i in range(2, n + 1):
        res = calculate(f_func, results[i - 2], results[i - 1])
        results.append(res)
    return results

def print_table(data):
    print(f"| {'n':^5} | {'p_{n-1}':^12} | {'p_n':^12} | {'p_{n+1}':^12} | {'|p_{n+1} - p_n|':^12} |")
    print("-" * 60)

    # p0 ~ p{n-1}
    # p1 ~ p{n}
    # p2 ~ p(n+1)
    for n in range (1, len(data) - 1):
        p0, p1, p2 = data[n - 1], data[n], data[n + 1]
        diff = abs(p2 - p1)
        print(f"| {n:^5} | {p0:<12.6f} | {p1:<12.6f} | {p2:<12.6f} | {diff:<12.6f} |")

if __name__ == "__main__":
    main()