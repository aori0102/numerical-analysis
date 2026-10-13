import sys
import sympy as sp

def parse_arguments():
    """
    Parses command-line arguments:
    --nosolve: Skips vector b input and solving steps (decomposition only).
    --indecimal [n]: Formats the final output as decimal numbers rounded to n decimal places (default n=6).
    """
    nosolve = "--nosolve" in sys.argv
    
    indecimal = False
    decimals = 6  # default
    
    if "--indecimal" in sys.argv:
        indecimal = True
        idx = sys.argv.index("--indecimal")
        if idx + 1 < len(sys.argv):
            try:
                decimals = int(sys.argv[idx + 1])
            except ValueError:
                pass  # Use default 6 if not a valid integer
                
    return nosolve, indecimal, decimals

def format_output(item, indecimal, decimals):
    """
    Formats a SymPy matrix or value into rounded decimal form only if indecimal is True.
    Otherwise, keeps exact symbolic/fractional form.
    """
    if indecimal:
        if isinstance(item, sp.Matrix):
            return item.applyfunc(lambda val: round(float(val.evalf()), decimals))
        else:
            return round(float(item.evalf()), decimals)
    else:
        return item

def doolittle_lu_program():
    nosolve, indecimal, decimals = parse_arguments()
    
    print("--- DOOLITTLE LU DECOMPOSITION & SOLVER PROGRAM ---")
    if nosolve:
        print("[Mode: --nosolve enabled -> Decomposition only, b input skipped]")
    if indecimal:
        print(f"[Mode: --indecimal enabled -> Final output rounded to {decimals} decimal places]")

    # --- 1. INPUT PHASE (Matrix A and Vector b upfront) ---
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
    
    b = None
    if not nosolve:
        print(f"\nEnter the elements of vector b ({n}x1):")
        vector_b_data = []
        for i in range(n):
            val = input(f"b[{i+1}] = ")
            vector_b_data.append([sp.Rational(val)])
        b = sp.Matrix(vector_b_data)
    
    print("\nMatrix A entered:")
    sp.pprint(A)
    if not nosolve:
        print("Vector b entered:")
        sp.pprint(b)
    
    try:
        # --- 2. DECOMPOSITION PHASE ---
        print("\n[Step 1] Performing Doolittle LU Decomposition (A = L * U):")
        L = sp.zeros(n, n)
        U = sp.zeros(n, n)
        
        for i in range(n):
            L[i, i] = 1
            
            # Compute row i of U
            for j in range(i, n):
                s = sum(L[i, k] * U[k, j] for k in range(i))
                U[i, j] = A[i, j] - s
                
            # Compute column i of L
            for j in range(i + 1, n):
                if U[i, i] == 0:
                    raise ValueError(f"Pivot element U[{i+1},{i+1}] is zero. Row exchange is required (PA = LU needed).")
                s = sum(L[j, k] * U[k, i] for k in range(i))
                L[j, i] = (A[j, i] - s) / U[i, i]
                
        # Format decomposition outputs for display
        display_L = format_output(L, indecimal, decimals)
        display_U = format_output(U, indecimal, decimals)
        
        print("\nMatrix L (Lower triangular, diagonal = 1):")
        sp.pprint(display_L)
        print("\nMatrix U (Upper triangular):")
        sp.pprint(display_U)

        # --- 3. SOLVING PHASE (Skipped if --nosolve is active) ---
        if nosolve:
            print("\n" + "="*40)
            print("DECOMPOSITION COMPLETED (--nosolve active)")
            print("="*40)
            return

        print("\n[Step 2] Solving equations Ly = b and Ux = y (using exact arithmetic):")
        
        # 2.1: Solve Ly = b (Forward Substitution) - calculated purely in symbolic fractions
        y = sp.zeros(n, 1)
        for i in range(n):
            sum_term = sum(L[i, k] * y[k, 0] for k in range(i))
            y[i, 0] = (b[i, 0] - sum_term) / L[i, i]
            
        display_y = format_output(y, indecimal, decimals)
        print("Vector y (from Ly = b):")
        sp.pprint(display_y)
        
        # 2.2: Solve Ux = y (Back Substitution) - calculated purely in symbolic fractions
        x = sp.zeros(n, 1)
        for i in range(n - 1, -1, -1):
            sum_term = sum(U[i, k] * x[k, 0] for k in range(i + 1, n))
            if U[i, i] == 0:
                raise ValueError(f"Cannot perform back substitution: U[{i+1},{i+1}] = 0.")
            x[i, 0] = (y[i, 0] - sum_term) / U[i, i]
            
        display_x = format_output(x, indecimal, decimals)
        print("Vector x (Solution of Ax = b):")
        sp.pprint(display_x)
        
        print("\n" + "="*40)
        print("COMPUTATION COMPLETED SUCCESSFULLY")
        print("="*40)
        
    except ValueError as e:
        print("\n" + "="*40)
        print("ERROR / STOPPED:")
        print("="*40)
        print(f"-> {e}")

if __name__ == "__main__":
    doolittle_lu_program()