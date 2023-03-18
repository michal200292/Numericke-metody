import numpy as np


def random_matrix_size_n(n):
    return [[np.float32(np.random.uniform(0, 1)) for _ in range(n)] for _ in range(n)]


def random_vector_size_n(n):
    return [np.float32(np.random.uniform(0, 1)) for _ in range(n)]


def euclid_dist(v1, v2):
    return np.sqrt(sum([pow(v1[i] - v2[i], 2) for i in range(len(v1))]))


def gauss_jordan(A, B):
    n = len(A)
    for i in range(n):
        for j in range(n):
            if i != j:
                multiplier = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= multiplier*A[i][k]
                B[j] -= multiplier*B[i]

    for i in range(n):
        B[i] /= A[i][i]
    return B


def gauss_jordan_partial_pivoting(A, B):
    n = len(A)
    perm = [i for i in range(n)]
    for i in range(n):
        pivot = i
        for j in range(i + 1, n):
            if abs(A[perm[pivot]][i]) < abs(A[perm[j]][i]):
                pivot = j

        perm[pivot], perm[i] = perm[i], perm[pivot]
        for j in range(n):
            if i != j:
                multiplier = A[perm[j]][i] / A[perm[i]][i]
                for k in range(i, n):
                    A[perm[j]][k] -= multiplier*A[perm[i]][k]
                B[perm[j]] -= multiplier*B[perm[i]]

    for i in range(n):
        B[perm[i]] /= A[perm[i]][i]

    ans = [0 for _ in range(n)]
    for i in range(n):
        ans[i] = B[perm[i]]
    return ans


def gauss_jordan_complete_pivoting(A, B):
    n = len(A)
    perm_r = [i for i in range(n)]
    perm_c = perm_r[:]
    for i in range(n):
        pivot_r = i
        pivot_c = i
        for j in range(i, n):
            for k in range(i, n):
                if abs(A[perm_r[pivot_r]][perm_c[pivot_c]]) < abs(A[perm_r[j]][perm_c[k]]):
                    pivot_r = j
                    pivot_c = k

        perm_r[pivot_r], perm_r[i] = perm_r[i], perm_r[pivot_r]
        perm_c[pivot_c], perm_c[i] = perm_c[i], perm_c[pivot_c]
        for j in range(n):
            if i != j:
                multiplier = A[perm_r[j]][perm_c[i]] / A[perm_r[i]][perm_c[i]]
                for k in range(i, n):
                    A[perm_r[j]][perm_c[k]] -= multiplier*A[perm_r[i]][perm_c[k]]
                B[perm_r[j]] -= multiplier*B[perm_r[i]]

    for i in range(n):
        B[perm_r[i]] /= A[perm_r[i]][perm_c[i]]

    ans = [0 for _ in range(n)]
    for i in range(n):
        ans[perm_c[i]] = B[perm_r[i]]
    return ans


def lu_decomposition_in_situ(A):
    n = len(A)
    for i in range(n - 1):
        for j in range(i + 1, n):
            multiplier = A[j][i] / A[i][i]
            A[j][i] = multiplier
            for k in range(i + 1, n):
                A[j][k] -= multiplier*A[i][k]
    return A


def compute_lu_distance(A, LU):
    C = np.zeros((len(A), len(A)))
    n = len(A)
    norm = 0
    for i in range(n):
        for j in range(n):
            entry = 0
            if i == j:
                for k in range(i):
                    entry += LU[i][k] * LU[k][i]
                entry += LU[i][i]
            elif i < j:
                for k in range(i):
                    entry += LU[i][k]*LU[k][j]
                entry += LU[i][j]
            else:
                for k in range(j + 1):
                    entry += LU[i][k]*LU[k][j]
            C[i][j] = entry
            norm += pow(A[i][j] - entry, 2)
    return np.sqrt(norm)

