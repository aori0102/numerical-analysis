import argparse
import re
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_EVEN, Context

def parse_arguments():
    parser = argparse.ArgumentParser(description="Solve linear systems using the Gauss-Jordan method.")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--partialpivot', action='store_true', help='Use partial pivoting strategy')
    group.add_argument('--scaledpivot', action='store_true', help='Use scaled partial pivoting strategy')
    
    parser.add_argument('--indecimal', nargs='?', const=6, type=int, 
                        help='Display results as decimals rounded to n decimal places (default: 6)')
    parser.add_argument('--roundtomeaningful', type=int,
                        help='Round to n significant digits after every atomic operation using round-half-even')
    
    return parser.parse_args()

def round_significant(val, sig_digits):
    d = Decimal(str(val))
    if d.is_zero():
        return Decimal('0')
    c = Context(prec=sig_digits, rounding=ROUND_HALF_EVEN)
    return c.create_decimal(d)

def compute_op(val_str, sig_digits, decimal_places):
    if sig_digits is not None:
        return round_significant(Decimal(val_str), sig_digits)
    elif decimal_places is not None:
        return Decimal(val_str)
    else:
        return Fraction(val_str)

def beautify_print(op_str, M, n, row_labels):
    # Tạo từ điển ánh xạ từ nhãn hiện tại sang nhãn hiển thị thứ tự (1, 2, ..., n)
    mapping = {str(row_labels[i]): str(i + 1) for i in range(n)}
    
    # Thay thế các nhãn E_x trong chuỗi thao tác dựa vào từ điển
    def repl(match):
        lbl = match.group(1)
        return f"E_{mapping.get(lbl, lbl)}"
    
    beautified_op = re.sub(r'E_(\d+)', repl, op_str)
    if beautified_op.strip():
        print(beautified_op)
    
    # In ma trận theo thứ tự hiển thị từ trên xuống dưới ứng với E_1, E_2, ... E_n
    for i in range(n):
        row_str = "  ".join(f"{str(val):>12}" for val in M[i])
        print(f"  E_{i+1}: [ {row_str} ]")
    print()

def format_final_number(val, decimal_places, sig_digits):
    if sig_digits is not None:
        return str(round_significant(val, sig_digits))
    elif decimal_places is not None:
        d = Decimal(str(val))
        format_str = '0.' + '0' * decimal_places if decimal_places > 0 else '0'
        rounded = d.quantize(Decimal(format_str), rounding=ROUND_HALF_EVEN)
        return str(rounded)
    else:
        return str(val)

def main():
    args = parse_arguments()
    sig_digits = args.roundtomeaningful
    decimal_places = args.indecimal if sig_digits is None else None

    print("=== GAUSS-JORDAN METHOD PROGRAM ===")
    
    try:
        n = int(input("Enter the number of variables/equations (n): "))
        if n <= 0:
            print("Error: n must be greater than 0.")
            return
    except ValueError:
        print("Error: Please enter a valid integer for n.")
        return

    print(f"\nEnter elements for matrix A ({n}x{n}):")
    A = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            while True:
                try:
                    val_str = input(f"  A[{i+1}][{j+1}] = ")
                    A[i][j] = compute_op(val_str, sig_digits, decimal_places)
                    break
                except ValueError:
                    print("  Invalid input. Please enter a valid number.")

    print(f"\nEnter elements for vector b ({n} elements):")
    b = [None for _ in range(n)]
    for i in range(n):
        while True:
            try:
                val_str = input(f"  b[{i+1}] = ")
                b[i] = compute_op(val_str, sig_digits, decimal_places)
                break
            except ValueError:
                print("  Invalid input. Please enter a valid number.")

    # Khởi tạo ma trận M
    zero_val = Decimal('0') if (sig_digits is not None or decimal_places is not None) else Fraction(0)
    M = [[compute_op(str(A[i][j]), sig_digits, decimal_places) for j in range(n)] + [compute_op(str(b[i]), sig_digits, decimal_places)] for i in range(n)]
    
    row_labels = list(range(1, n + 1))

    print("\n--- INITIAL AUGMENTED MATRIX [A | b] ---")
    beautify_print("", M, n, row_labels)

    s_list = []
    if args.scaledpivot:
        for i in range(n):
            max_val = max(abs(val) for val in M[i][:n])
            if max_val == 0:
                print(f"Error: Row E_{row_labels[i]} has all coefficients equal to 0; unique solution does not exist.")
                return
            s_list.append(compute_op(str(max_val), sig_digits, decimal_places))

    for i in range(n):
        print(f"----------------------------------------")
        print(f"STEP {i+1}:")

        p = i
        if args.partialpivot:
            max_val = abs(M[i][i])
            for k in range(i + 1, n):
                val = abs(M[k][i])
                if val > max_val:
                    max_val = val
                    p = k
        elif args.scaledpivot:
            max_ratio = compute_op(str(abs(M[i][i]) / s_list[i]), sig_digits, decimal_places)
            for k in range(i + 1, n):
                ratio = compute_op(str(abs(M[k][i]) / s_list[k]), sig_digits, decimal_places)
                if ratio > max_ratio:
                    max_ratio = ratio
                    p = k
        else:
            while p < n and M[p][i] == 0:
                p += 1

        if p >= n or M[p][i] == 0:
            print("Error: No unique solution exists (pivot element is zero).")
            return

        if p != i:
            op_swap = f"  Row swap: (E_{row_labels[i]}) <-> (E_{row_labels[p]})"
            M[i], M[p] = M[p], M[i]
            row_labels[i], row_labels[p] = row_labels[p], row_labels[i]
            if args.scaledpivot:
                s_list[i], s_list[p] = s_list[p], s_list[i]
            beautify_print(op_swap, M, n, row_labels)

        pivot_element = M[i][i]

        if pivot_element != 1:
            op_norm = f"  Normalize pivot: (1 / {pivot_element}) * E_{row_labels[i]} -> E_{row_labels[i]}"
            for j in range(i, n + 1):
                res = M[i][j] / pivot_element
                M[i][j] = compute_op(str(res), sig_digits, decimal_places)
            beautify_print(op_norm, M, n, row_labels)

        for j in range(n):
            if j != i:
                factor = M[j][i]
                if factor != 0:
                    op_elim = f"  Eliminate row: (E_{row_labels[j]} - ({factor}) * E_{row_labels[i]}) -> E_{row_labels[j]}"
                    for k in range(i, n + 1):
                        prod = compute_op(str(factor * M[i][k]), sig_digits, decimal_places)
                        diff = M[j][k] - prod
                        M[j][k] = compute_op(str(diff), sig_digits, decimal_places)
                    beautify_print(op_elim, M, n, row_labels)

    print("----------------------------------------")
    print("PROCESS COMPLETED. Matrix in [I | x] form:")
    beautify_print("", M, n, row_labels)

    solutions = [None] * n
    for i in range(n):
        for j in range(n):
            if M[i][j] == 1:
                solutions[j] = M[i][n]

    print("System Solution:")
    for i in range(n):
        val = solutions[i] if solutions[i] is not None else zero_val
        formatted_val = format_final_number(val, decimal_places, sig_digits)
        print(f"  x_{i+1} = {formatted_val}")

if __name__ == "__main__":
    main()