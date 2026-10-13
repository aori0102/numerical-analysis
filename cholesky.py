import sympy as sp

def cholesky_decomposition(A):
    """
    Performs Cholesky decomposition A = B * B^T for a symmetric positive-definite matrix A.
    """
    n = A.rows
    
    # --- STEP 1: Check Symmetry ---
    print("\n[Step 1] Checking Symmetry:")
    A_T = A.T
    print("Matrix A^T (Transpose of A):")
    sp.pprint(A_T)
    
    if A != A_T:
        raise ValueError("Matrix A is NOT symmetric ($A \neq A^T$). Cholesky method cannot be applied.")
    print("-> Result: Matrix A is symmetric (A = A^T). Passed!")

    # --- STEP 2: Check Positive-Definiteness (Leading Principal Minors) ---
    print("\n[Step 2] Checking Positive-Definiteness via Leading Principal Minors:")
    for k in range(1, n + 1):
        # Extract the k-th leading principal submatrix (top-left k x k submatrix)
        sub_matrix = A[:k, :k]
        det_val = sub_matrix.det()
        print(f"Delta_{k} = {det_val}")
        
        # Check if the determinant is strictly positive (> 0)
        # Using .is_positive or evaluating numerically for safety
        if not (det_val.is_positive or (det_val.is_number and float(det_val.evalf()) > 0)):
            raise ValueError(f"Matrix A is NOT positive-definite because Delta_{k} = {det_val} <= 0.")
            
    print("-> Result: All leading principal minors are strictly positive. Matrix A is positive-definite. Passed!")

    # --- STEP 3: Compute Matrix B and B^T ---
    print("\n[Step 3] Computing Cholesky Factor B (A = B * B^T):")
    B = sp.zeros(n, n)
    
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                # Diagonal elements
                sum_sq = sum(B[i, k]**2 for k in range(j))
                val = sp.sqrt(A[i, i] - sum_sq)
                B[i, j] = val
            else:
                # Off-diagonal elements
                sum_prod = sum(B[i, k] * B[j, k] for k in range(j))
                val = (A[i, j] - sum_prod) / B[j, j]
                B[i, j] = val
                
    B_T = B.T
    return B, B_T

def main():
    print("--- CHOLESKY DECOMPOSITION PROGRAM ---")
    n = int(input("Enter matrix size n (e.g., 3): "))
    
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
        B, B_T = cholesky_decomposition(A)
        
        # --- STEP 4 & Final Output ---
        print("\n" + "="*40)
        print("CHOLESKY RESULTS SUCCESSFUL")
        print("="*40)
        
        print("\nMatrix B (Lower triangular matrix):")
        sp.pprint(B)
        
        print("\nMatrix B^T (Transpose of B, Upper triangular matrix):")
        sp.pprint(B_T)
        
    except ValueError as e:
        print("\n" + "="*40)
        print("ERROR / STOPPED:")
        print("="*40)
        print(f"-> {e}")

if __name__ == "__main__":
    main()