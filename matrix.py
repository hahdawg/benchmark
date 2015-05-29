from __future__ import division
import random


def shape(X):
    return len(X), len(X[0])


def zeros(N):
    return [[0 for _ in xrange(N)] for _ in xrange(N)]


def eye(N):
    res = zeros(N)
    for i in xrange(N):
        res[i][i] = 1
    return res


def concat(X, Y):
    return [xi + yi for xi, yi in zip(X, Y)]


def swap(X, i, j):
    X = X[:]
    X[i], X[j] = X[j], X[i]
    return X


def scalar_mult(X, i, c):
    X = X[:]
    X[i] = [c*x for x in X[i]]
    return X


def add(X, i, j, c=1):
    """Adds a multiple of row i to row j"""
    X = X[:]
    X[j] = [c*xik + xjk for xik, xjk in zip(X[i], X[j])]
    return X


def excl_range(n, i):
    xs = range(n)
    xs.remove(i)
    return xs


def isclose(x, y, tol=1e-6):
    return abs(x - y) < tol


def is_zero(x):
    return isclose(x, 0.0)


def is_one(x):
    return isclose(x, 1.0)


def inv(X):
    N, _ = shape(X)
    A = concat(X, eye(N))
    for j in xrange(N):
        k = j
        while is_zero(A[k][k]):
            k += 1

        if k == N:
            raise ValueError("X is not invertible")
        else:
            A = swap(A, j, k)

        A = scalar_mult(A, j, 1/(A[j][j]))
        for i in excl_range(N, j):
            A = add(A, j, i, -A[i][j])
    return [ai[N:] for ai in A]


def transpose(X):
    return map(list, zip(*X))


def dot(xi, yi):
    return sum(xij*yij for xij, yij in zip(xi, yi))


def multiply(X, Y):
    return [[dot(xi, yi) for yi in transpose(Y)] for xi in X]


def print_matrix(X):
    for xi in X:
        print xi


def is_eye(X):
    N = len(X)
    for i in xrange(N):
        for j in xrange(N):
            if i == j:
                if not is_one(X[i][j]):
                    return False
            else:
                if not is_zero(X[i][j]):
                    return False
    return True


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
    invX = inv(X)
    invY = inv(Y)
    invZ = inv(Z)
    assert is_eye(multiply(X, invX))
    assert is_eye(multiply(Y, invY))
    assert is_eye(multiply(Z, invZ))

    random.seed(0)
    N = 100
    W = [[random.randint(0, 100) for _ in xrange(N)] for _ in xrange(N)]
    assert is_eye(multiply(W, inv(W)))
    

    print "tests passed"


if __name__ == "__main__":
    tests()
