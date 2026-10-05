from sympy import Symbol, lambdify, sympify

def main():
    f_expr_str = input("Nhập biểu thức f(x) = 0 (ví dụ: x**3 - x - 1): ")
    a = float(sympify(input("Đầu mút trái a (p0): ")).evalf())
    b = float(sympify(input("Đầu mút phải b (p1): ")).evalf())
    n = int(input("Nhập số lần lặp n (đến p bao nhiêu): "))

    x = Symbol('x')
    f_expr = sympify(f_expr_str)
    f_func = lambdify(x, f_expr, 'numpy')

    print("\nKết quả lặp:")
    results = solve(f_func, a, b, n)
    print_table(results)

def solve(f_func, a, b, n):
    results = [
        (a, f_func(a)),
        (b, f_func(b))
    ]
    for _ in range(n - 1):
        c = calculate_c(f_func, a, b)
        res = f_func(c)
        results.append((c, res))
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
        print(f"| {n:^5} | {c:<12.6f} | {f_c:<12.6f} |")

if __name__ == "__main__":
    main()