import numpy as np
from sklearn.cluster import KMeans


def calLaplacianMatrix(adjacentMatrix):
    # compute the Degree Matrix: D=sum(A)
    degreeMatrix = np.sum(adjacentMatrix, axis=1)

    # compute the Laplacian Matrix: L=D-A
    laplacianMatrix = np.diag(degreeMatrix) - adjacentMatrix

    # normailze to D^(-1/2) L D^(-1/2)
    sqrtDegreeMatrix = np.diag(1.0 / (degreeMatrix ** (0.5)))
    return np.dot(np.dot(sqrtDegreeMatrix, laplacianMatrix), sqrtDegreeMatrix)


def run(SimilarityMatrix, clusters):
    Laplacian = calLaplacianMatrix(SimilarityMatrix)
    x, V = np.linalg.eig(Laplacian)
    x = zip(x, range(len(x)))
    x = sorted(x, key=lambda x: x[0])
    H = np.vstack([V[:, i] for (v, i) in x[:len(SimilarityMatrix)]]).T
    result = KMeans(n_clusters=clusters).fit(H)
    return result.labels_
