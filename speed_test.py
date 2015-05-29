import matrix as mat
import random
import time


def random_matrix(N):
    random.seed(0)
    return [[random.randint(0, 100) for _ in xrange(N)] for _ in xrange(N)]


def timed(f, *args):
    start = time.time()
    res = f(*args)
    end = time.time()
    return end - start


def mean(xs):
    return 1.0*sum(xs)/len(xs)


def main(ntrials=5):
    X = random_matrix(300)
    
    b1 = mean([timed(mat.multiply, X, X) for _ in xrange(ntrials)])
    b2 = mean([timed(mat.inv, X) for _ in xrange(ntrials)])
    print "matrix multiplication time = %0.2f" %  b1
    print "matrix inversion time = %0.2f" % b2


if __name__ == "__main__":
    main()

    

