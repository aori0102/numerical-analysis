from sympy import Symbol, lambdify, sympify

def main():
    f_expr_str = input("Nhập biểu thức f(x) : ")
    f_derivative_expr_str = input("Nhập biểu thức f'(x) : ")
    p0 = float(sympify(input("Nhập giá trị ban đầu p0: ")).evalf())
    tol = float(sympify(input("Nhập độ chính xác (ví dụ: 0.01): ")).evalf())

    x = Symbol('x')
    
    f_expr = sympify(f_expr_str)
    f_func = lambdify(x, f_expr, 'numpy')
    
    f_derivative_expr = sympify(f_derivative_expr_str)
    f_derivative_func = lambdify(x, f_derivative_expr, 'numpy')
    
    print("\nKết quả lặp:")
    results = solve(f_func, f_derivative_func, p0, tol)
    print_table(results)

def solve(f_func, f_derivative_func, p0, tol):
    results = [(p0, 0)]
    while True:
        p = p0 - f_func(p0) / f_derivative_func(p0)
        diff = abs(p - p0)
        results.append((p, diff))
        if diff < tol:
            break
        p0 = p
    return results

def print_table(data):
    # Tiêu đề bảng
    print(f"| {'n':^5} | {'p_n':^12} | {'|p_n - p_{n-1}|':^12} |")
    print("-" * 36)

    for n in range(len(data)):
        p, diff = data[n]
        print(f"| {n:^5} | {p:<12.6f} | {diff:<12.6f} |")

if __name__ == "__main__":
    main()