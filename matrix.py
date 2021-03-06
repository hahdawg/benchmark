from __future__ import division
import random


def shape(X):
    return len(X), len(X[0])


def zeros(N):
    return [[0.0 for _ in xrange(N)] for _ in xrange(N)]


def eye(N):
    return [[0.0 if i != j else 1.0 for i in xrange(N)] for j in xrange(N)]


def concat(X, Y):
    """Concat X and Y by column"""
    return [xi + yi for xi, yi in zip(X, Y)]


def swap(X, i, j):
    """Swap rows i and j in X"""
    X = X[:]
    X[i], X[j] = X[j], X[i]
    return X


def scalar_mult(X, i, c):
    """Multiplies row i of X by c"""
    X = X[:]
    X[i] = [c*x for x in X[i]]
    return X


def add(X, i, j, c=1.0):
    """Adds a multiple c of row i to row j"""
    X = X[:]
    X[j] = [c*xik + xjk for xik, xjk in zip(X[i], X[j])]
    return X


def range_except(n, i):
    return [j for j in xrange(n) if j != i]


def isclose(x, y, tol=1e-6):
    return abs(x - y) < tol


def is_zero(x):
    return isclose(x, 0.0)


def is_one(x):
    return isclose(x, 1.0)


def first_nonzero(X, i):
    """Find index of first nonzero element of X[i:][i]"""
    j = i
    while is_zero(X[j][j]):
        j += 1
    return j


def inv(X):
    N, _ = shape(X)
    A = concat(X[:], eye(N))
    for j in xrange(N):
        k = first_nonzero(A, j)
        if k == N:
            raise ValueError("X is not invertible")
        else:
            A = swap(A, j, k)

        A = scalar_mult(A, j, 1/(A[j][j]))
        for i in range_except(N, j):
            A = add(A, j, i, -A[i][j])

    return [ai[N:] for ai in A]


def transpose(X):
    return map(list, zip(*X))


def dot(xi, yi):
    """dot product"""
    return sum(xij*yij for xij, yij in zip(xi, yi))


def multiply(X, Y):
    return [[dot(xi, yi) for yi in transpose(Y)] for xi in X]


def print_matrix(X):
    for xi in X:
        print xi


def is_eye(X):
    N, _ = shape(X)
    diag = all(is_one(X[i][i]) for i in xrange(N))
    off_diag = all(is_zero(X[i][j]) for i in xrange(N) for j in xrange(N) if i != j)
    return diag and off_diag


def tests():
    assert zeros(2) == [[0, 0], [0, 0]]
    assert eye(2) == [[1, 0], [0, 1]]
    assert concat(eye(2), eye(2)) == [[1, 0, 1, 0], [0, 1, 0, 1]]
    assert swap(eye(2), 0, 1) == [[0, 1], [1, 0]]
    assert scalar_mult(eye(2), 0, 3) == [[3, 0], [0, 1]]
    assert add(eye(2), 0, 1) == [[1, 0], [1, 1]]
    assert add(eye(2), 0, 1, 3) == [[1, 0], [3, 1]]
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    assert dot([1, 2, 3], [4, 5, 6]) == 1*4 + 2*5 + 3*6

    X = [[5, 2, 1], [3, 4, 2], [2, 11, 3]]
    Y = [[1, 2, 3], [4, 6, 1], [9, 1, 2]]
    Z = [[0, 1, 2], [4, 2, 1], [12, 9, 11]]
    assert transpose(Y) == [[1, 4, 9], [2, 6, 1], [3, 1, 2]]
    assert dot(X[0], transpose(Y)[0]) == 5*1 + 4*2 + 1*9
    assert multiply(X, Y) == [[22, 23, 19], [37, 32, 17], [73, 73, 23]]
    assert is_zero(0)
    assert is_one(1)
    assert is_eye([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert not is_eye(Y)
    assert is_eye(inv(eye(5)))
    assert is_eye(multiply(X, inv(X)))
    assert is_eye(multiply(Y, inv(Y)))
    assert is_eye(multiply(Z, inv(Z)))

    random.seed(0)
    N = 100
    W = [[random.randint(0, 100) for _ in xrange(N)] for _ in xrange(N)]
    assert is_eye(multiply(W, inv(W)))

    print "tests passed"


if __name__ == "__main__":
    tests()
