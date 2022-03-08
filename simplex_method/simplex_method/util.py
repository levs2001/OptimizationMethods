import itertools

import numpy as np


def submatrix_by_indexes(AMN: np.array, M: np.array, Nk: np.array) -> np.array:
    '''
    :param AMN: matrix A[M, N]
    :param M: vector of indices
    :param Nk: second vector of indices
    :return: A[M, Nk]
    '''

    res = np.empty((0, np.size(Nk)), float)
    for i in M:
        try:
            t = np.array([[AMN[i, j] for j in Nk]])
            res = np.concatenate((res, t), axis=0)
        except IndexError as err:
            print(f'invalid Nk: {Nk}')
            raise IndexError(err)
    return res


def subvector_by_indexes(x: np.array, nk: np.array) -> np.array:
    return np.array([x[i] for i in nk])


# return Lk[ind] instead of just ind cuz indices in x
# are {0 .. |Lk| - 1} and not {Lk[0], Lk[1] ..}
def find_first_neg_ind(x: np.array, Lk: np.array):
    for ind, val in np.ndenumerate(subvector_by_indexes(x, Lk)):
        if val < 0:
            return Lk[ind]


def find_subsets(s, n):
    '''
    :param s: set
    :param n: size of subset
    :return: generator of all subsets of s of size n
    '''
    return itertools.combinations(s, n)


def positive_elements_indexes(xk: np.array) -> np.array:
    '''
    :param xk: vector
    :return: Nk+ - indicis of positive elements of xk
    '''
    return np.array([i for i in range(np.size(xk)) if xk[i] > 0]).astype(int)