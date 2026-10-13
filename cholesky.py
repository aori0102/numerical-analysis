import sys
import sympy as sp

def parse_arguments():
    """
    Parses command-line arguments:
    --nosolve: Skips solving step and vector b input.
    --indecimal [n]: Formats output as decimal numbers rounded to n decimal places (default n=6).
    """
    nosolve = "--nosolve" in sys.argv
    
    inrealnum = False
    decimals = 6  # default
    
    if "--indecimal" in sys.argv:
        inrealnum = True
        idx = sys.argv.index("--indecimal")
        # Check if a number follows --indecimal
        if idx + 1 < len(sys.argv):
            try:
                decimals = int(sys.argv[idx + 1])
            except ValueError:
                pass  # Use default 6 if not a valid integer
    elif len(sys.argv) == 1:
        # Default behavior if no arguments are provided (can be customized, 
        # here we keep sympy fractions by default unless requested)
        pass
        
    return nosolve, inrealnum, decimals

def format_output(item, inrealnum, decimals):
    """
    Formats a SymPy matrix, vector, or number into either 
    exact fractional form or rounded decimal form.
    """
    if inrealnum:
        if isinstance(item, sp.Matrix):
            # Apply evalf and round to each element
            return item.applyfunc(lambda val: round(float(val.evalf()), decimals))
        else:
            return round(float(item.evalf()), decimals)
    else:
        return item

def cholesky_decomposition_program():
    nosolve, inrealnum, decimals = parse_arguments()
    
    print("--- CHOLESKY DECOMPOSITION & SOLVER PROGRAM ---")
    if nosolve:
        print("[Mode: --nosolve enabled -> Decomposition only]")
    if inrealnum:
        print(f"[Mode: --indecimal enabled -> Decimal output rounded to {decimals} places]")

    n = int(input("\nEnter matrix size n (e.g., 3): "))
    
    print(f"Enter the elements of matrix A ({n}x{n}):")
    matrix_data = []
    for i in range(n):
        row = []
        for j in range(n):
            val = input(f"A[{i+1}][{j+1}] = ")
            row.append(sp.Rational(val))
        matrix_data.append(row)
    A = sp.Matrix(matrix_data)
    
    print("\nMatrix A entered:")
    sp.pprint(A)
    
    try:
        # --- STEP 1: Check Symmetry ---
        print("\n[Step 1] Checking Symmetry:")
        A_T = A.T
        print("Matrix A^T (Transpose of A):")
        sp.pprint(A_T)
        
        if A != A_T:
            raise ValueError("Matrix A is NOT symmetric (A != A^T). Cholesky method cannot be applied.")
        print("-> Result: Matrix A is symmetric (A = A^T). Passed!")

        # --- STEP 2: Check Positive-Definiteness (Leading Principal Minors) ---
        print("\n[Step 2] Checking Positive-Definiteness via Leading Principal Minors:")
        for k in range(1, n + 1):
            sub_matrix = A[:k, :k]
            det_val = sub_matrix.det()
            print(f"Delta_{k} = {det_val}")
            
            if not (det_val.is_positive or (det_val.is_number and float(det_val.evalf()) > 0)):
                raise ValueError(f"Matrix A is NOT positive-definite because Delta_{k} = {det_val} <= 0.")
                
        print("-> Result: All leading principal minors are strictly positive. Matrix A is positive-definite. Passed!")

        # --- STEP 3: Compute Matrix B and B^T ---
        print("\n[Step 3] Computing Cholesky Factor B (A = B * B^T):")
        B = sp.zeros(n, n)
        
        for i in range(n):
            for j in range(i + 1):
                if i == j:
                    sum_sq = sum(B[i, k]**2 for k in range(j))
                    val = sp.sqrt(A[i, i] - sum_sq)
                    B[i, j] = val
                else:
                    sum_prod = sum(B[i, k] * B[j, k] for k in range(j))
                    val = (A[i, j] - sum_prod) / B[j, j]
                    B[i, j] = val
                    
        B_T = B.T
        
        # Format outputs according to flags
        formatted_B = format_output(B, inrealnum, decimals)
        formatted_B_T = format_output(B_T, inrealnum, decimals)
        
        print("\nMatrix B (Lower triangular):")
        sp.pprint(formatted_B)
        print("Matrix B^T (Upper triangular):")
        sp.pprint(formatted_B_T)

        # --- STEP 4: Solve Equations (Skipped if --nosolve is active) ---
        if nosolve:
            print("\n" + "="*40)
            print("DECOMPOSITION COMPLETED (--nosolve active)")
            print("="*40)
            return

        print(f"\nEnter the elements of vector b ({n}x1):")
        vector_b_data = []
        for i in range(n):
            val = input(f"b[{i+1}] = ")
            vector_b_data.append([sp.Rational(val)])
        b = sp.Matrix(vector_b_data)
        print("Vector b entered:")
        sp.pprint(b)

        print("\n[Step 4] Solving equations By = b and B^T x = y:")
        
        # 4.1: Solve By = b (Forward Substitution)
        y = sp.zeros(n, 1)
        for i in range(n):
            sum_term = sum(B[i, k] * y[k, 0] for k in range(i))
            y[i, 0] = (b[i, 0] - sum_term) / B[i, i]
            
        formatted_y = format_output(y, inrealnum, decimals)
        print("Vector y (from By = b):")
        sp.pprint(formatted_y)
        
        # 4.2: Solve B^T x = y (Back Substitution)
        x = sp.zeros(n, 1)
        for i in range(n - 1, -1, -1):
            sum_term = sum(B_T[i, k] * x[k, 0] for k in range(i + 1, n))
            x[i, 0] = (y[i, 0] - sum_term) / B_T[i, i]
            
        formatted_x = format_output(x, inrealnum, decimals)
        print("Vector x (Solution of Ax = b):")
        sp.pprint(formatted_x)
        
        print("\n" + "="*40)
        print("COMPUTATION COMPLETED SUCCESSFULLY")
        print("="*40)
        
    except ValueError as e:
        print("\n" + "="*40)
        print("ERROR / STOPPED:")
        print("="*40)
        print(f"-> {e}")

if __name__ == "__main__":
    cholesky_decomposition_program()