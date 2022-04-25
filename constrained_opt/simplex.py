import numpy as np
import numpy.linalg
import itertools

ZERO = 1e-4


def simplex_solve(A, b, c, xk=None):
    max_iterations = 20
    if xk is None:
        xk = starting_vector(A, b, c)
    Nk = None
    solution_found = False
    for i in range(max_iterations):
        if np.any(xk < 0):
            raise ValueError("negative xk[j] found")

        xk, Nk, solution_found, yk = step(A, b, c, xk)
        if solution_found:
            # print(f'solution: {xk}')
            # print(f'target function: {np.round(c.dot(xk), decimals=10)}')
            break

    return xk, yk


def calc_BNkM(AMNk: np.ndarray) -> np.ndarray:
    '''
        :param AMNk: square matrix
        :return: inverse of AMNk
    '''
    return np.linalg.inv(AMNk)


def set_dif(N: np.array, Nk: np.array) -> np.array:
    '''
        :param N: vector of indices from 0 to n-1 inclusively
        :param Nk: vector of basis indices
        :return: their difference
    '''
    mask = np.array([not x for x in np.isin(N, Nk)])
    return N[mask]


def transform_uk(uk: np.array, N: np.array, Nk: np.array, jk: int) -> np.array:
    uk_new = np.zeros(np.size(N))
    for i in range(np.size(Nk)):
        uk_new[Nk[i]] = uk[i]
    uk_new[jk] = -1
    return uk_new


def get_all_possible_Nk(AMN: np.array, M: np.array, N: np.array, Nk_plus: np.array) -> np.array:
    '''
    :param AMN: initial matrix A[M,N]
    :param M: number of rows
    :param N: number of columns
    :param Nk_plus: indices of positive elements of xk
    :return: basis indices Nk such that A[M, Nk]'s determinant is not zero
    '''
    # need to choose |M| basis vectors, |Nk+| are already chosen
    # we iterate over all possible combinations of indices from N \ Nk+
    # Nk is chosen basis vectors indices
    # print(f'N \ Nk+: {set_dif(N, Nk_plus)}')
    # print(f"N:{N}")


    for Nk_0 in itertools.combinations(set_dif(N, Nk_plus), np.size(M) - np.size(Nk_plus)):
        Nk_0 = np.array(Nk_0)
        Nk = np.sort(np.append(Nk_0, Nk_plus)).astype(int)
        # print(f'Nk_0:{Nk_0}; next Nk:{Nk}')
        AMNk = submatrix_by_indexes(AMN, M, Nk)
        try:
            if abs(np.linalg.det(AMNk)) > ZERO:
                yield Nk.astype(int)
        except numpy.linalg.LinAlgError as err:
            print(f"cant calculate det of matrix w/ shape {AMNk.shape}")
            raise numpy.linalg.LinAlgError(err)


def step(A: np.array, b: np.array, c: np.array, xk: np.array, Nk_prev_iter=None) -> (np.array, np.array, bool):
    M = np.arange(np.shape(A)[0])
    N = np.arange(np.shape(A)[1])
    Nk_plus = positive_elements_indexes(xk)
    # print(f'Nk_plus:{Nk_plus}')
    list_Nk = list(get_all_possible_Nk(A, M, N, Nk_plus))
    if Nk_prev_iter is not None:
        list_Nk.insert(0, Nk_prev_iter.astype(int))
    for Nk in list_Nk:
        Lk = set_dif(N, Nk).astype(int)
        BkM = np.linalg.inv(submatrix_by_indexes(A, M, Nk))
        ck = subvector_by_indexes(c, Nk)
        yk = ck @ BkM
        # print(f'yk: {yk}')
        # print(f'yk * bk = {yk.dot(b)}')
        dk = c - yk @ A
        if np.all(subvector_by_indexes(dk, Lk) >= -ZERO):
            return xk, Nk, True, yk

        jk = find_first_neg_ind(dk, Lk)
        uk_Nk = BkM @ A[:, jk]
        # print(f"uk_Nk:{uk_Nk}")
        if np.all(uk_Nk <= 0):
            raise ValueError("c^T x is unbounded")

        uk_N = transform_uk(uk_Nk, N, Nk, jk)
        # print(f"uk_N:{uk_N}")
        if np.array_equal(Nk, Nk_plus) or np.all(uk_N[set_dif(Nk, Nk_plus)] <= 0):
            Nk_uk_plus = np.array([i for i in Nk if uk_N[i] > 0])
            thetas_indexed = [(i, xk[i] / uk_N[i]) for i in Nk_uk_plus]
            ik, theta_k = sorted(thetas_indexed, key=lambda tupl: tupl[1])[0]
            x_new = xk - theta_k * uk_N
            N_new = np.sort(np.append(set_dif(Nk, np.array([ik])), jk)).astype(int)
            return x_new, N_new, False, yk

    raise Exception("can't build basis")


def starting_vector(A: np.array, b: np.array, c: np.array) -> np.array:
    N = np.array(list(range(A.shape[1])))
    M = np.array(list(range(A.shape[0])))
    for Nk in itertools.combinations(N, np.size(M)):
        AMNk = submatrix_by_indexes(A, M, Nk)
        if abs(np.linalg.det(AMNk)) > ZERO:
            B = np.linalg.inv(AMNk)
            xNk = B @ b
            # print(f'xnk dim: {xNk.shape}, b dim: {b.shape}, B dim: {B.shape},')
            if np.min(xNk) < 0:
                # print(f'skipped starting vector xnk: {xNk}')
                continue  # we need only vectors with all positive components
            xN = np.zeros(np.size(N))
            for i in range(len(Nk)):
                xN[Nk[i]] = xNk[i]
            # print(f'starting vector xnk: {xNk}')
            # print(f'starting vector xn: {xN}')
            return xN

    raise Exception("error, initial vector not found!")

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
