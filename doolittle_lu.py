import sympy as sp

def doolittle_lu_symbolic(A):
    """
    Decomposes matrix A into L * U using Doolittle's method 
    returning fractional/symbolic expressions (SymPy).
    """
    n = A.rows
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
                raise ValueError("Pivot element is zero, row exchange is required.")
            s = sum(L[j, k] * U[k, i] for k in range(i))
            L[j, i] = (A[j, i] - s) / U[i, i]
            
    return L, U

def main():
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
    
    print("\nMatrix A you entered:")
    sp.pprint(A)
    
    try:
        L, U = doolittle_lu_symbolic(A)
        
        print("\n" + "="*30)
        print("L-U DECOMPOSITION RESULTS (EXACT FRACTIONS)")
        print("="*30)
        
        print("\nMatrix L:")
        sp.pprint(L)
        
        print("\nMatrix U:")
        sp.pprint(U)
        
    except ValueError as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()