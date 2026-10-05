from sympy import Symbol, lambdify, sympify

def main():
    f_expr_str = input("Nhập biểu thức f(x) = 0 (ví dụ: x**3 - x - 1): ")
    a = float(sympify(input("Đầu mút trái a: ")).evalf())
    b = float(sympify(input("Đầu mút phải b: ")).evalf())
    tol = float(sympify(input("Nhập độ chính xác (ví dụ: 0.01): ")).evalf())

    x = Symbol('x')
    f_expr = sympify(f_expr_str)
    f_func = lambdify(x, f_expr, 'numpy')

    print("\nKết quả lặp:")
    results = solve(f_func, a, b, tol)
    print_table(results)
        
def solve(f_func, a, b, tol):
    results = []
    while True:
        c = calculate_c(f_func, a, b)
        res = f_func(c)
        results.append((c, res))
        if abs(res) < tol:
            break
        if f_func(a) * res < 0:
            b = c
        else:
            a = c
    return results

def calculate_c(f_func, a, b):
    return b - (f_func(b) * (b - a)) / (f_func(b) - f_func(a))

def print_table(data):
    # Tiêu đề bảng
    print(f"| {'n':^5} | {'c_n':^12} | {'f(c_n)':^12} |")
    print("-" * 36)

    for n in range(len(data)):
        c, f_c = data[n]
        print(f"| {n + 1:^5} | {c:<12.6f} | {f_c:<12.6f} |")

if __name__ == "__main__":
    main()