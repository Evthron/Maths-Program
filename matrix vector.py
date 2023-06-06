def MatrixTranspose(matrix):
    transposed_matrix = list()
    for i in range(len(matrix[0])):
        row = list()
        for j in range(len(matrix)):
            row.append(matrix[j][i])
        transposed_matrix.append(row)
    return transposed_matrix

def MatrixVectorMultiplication(matrix, vector):
    answer = list()
    for i in range(len(matrix)):
        sum = 0
        for j in range(len(vector)):
            sum += vector[j] * matrix[i][j]
        answer.append(sum)
    return answer

def MatrixMultiplication(matrix1, matrix2):
    transposed_matrix = MatrixTranspose(matrix2)
    resultant_matrix = list()
    for vector in transposed_matrix:
        row = MatrixVectorMultiplication(matrix1, vector)
        resultant_matrix.append(row)
    resultant_matrix = MatrixTranspose(resultant_matrix)
    return(resultant_matrix)

def MultipleMatrixMultiplication(*args):
    resultant_matrix = list()
    for matrix in args:
        if resultant_matrix == list():
            resultant_matrix = matrix
        else:
            resultant_matrix = MatrixMultiplication(resultant_matrix, matrix)
    return resultant_matrix

def AugmentedIdetity(mtx):
    matrix = mtx[:]
    matrix_size = len(matrix)
    for row in matrix:
        for j in range(matrix_size):
            row.append(0.0)
    for i in range(matrix_size):
        matrix[i][i+matrix_size] = 1.0
    return matrix


def RowFillZero(row, column):
    for i in range(column - len(row)):
        row.append(0.0)


def RowStandardise(row):
    divisor = 0
    for i in range(len(row)):
        if row[i] != 0:
            divisor = row[i]
            break
    if divisor != 0:
        for i in range(len(row)):
            row[i] = row[i] / divisor


def RowSubtract(row1, row2):
    row1_factor = 1
    row2_factor = 1
    answer_row = list()
    row1_copy = row1[:]
    row2_copy = row2[:]
    for i in range(len(row1_copy)):
        if row1_copy[i] != 0 and row2_copy[i] != 0:
            row1_factor = row1_copy[i]
            row2_factor = row2_copy[i]
            break

    for i in range(len(row1_copy)):
        row1_copy[i] = row1_copy[i] * row2_factor
        row2_copy[i] = row2_copy[i] * row1_factor
        answer_row.append(row1_copy[i] - row2_copy[i])
    return answer_row


def GaussianElimination(eqn):
    equation = eqn[:]
    number_of_row = len(equation)
    number_of_column = len(equation[0])
    RowStandardise(equation[0])
    for i in range(number_of_column - 1):
        for j in range(i + 1, number_of_row):
            if equation[j][i] != 0:
                equation[j] = RowSubtract(equation[i], equation[j])

    for i in reversed(range(1, number_of_row)):
        for j in range(1, number_of_column - 1):
            if equation[i][j] != 0:
                for k in range(i-1, -1, -1):
                    if equation[k][j] != 0:
                        equation[k] = RowSubtract(equation[i], equation[k])
                break

    for row in equation:
        RowStandardise(row)

    return equation


def InverseMatrix(eqn):
    equation = eqn[:]
    equation = AugmentedIdetity(equation)
    number_of_row = len(equation)
    number_of_column = len(equation[0])
    equation = GaussianElimination(equation)
    for i in range(number_of_row):
        check = list()
        for j in range(number_of_row):
            check.append(0.0)
        check[i] = 1.0
        if equation[i][0:number_of_row] != check:
            print("not invertible")

    inverted_matrix = list()
    for i in range(number_of_row):
        inverted_matrix.append(equation[i][number_of_row:number_of_column])

    return inverted_matrix


vector = [6, 0, 0]

matrixA = [[0, 1],
           [1, 1],
           [2, 1]]
"""vector = list()
matrixA = list()
for i in range(1001):
    matrixA.append([i/100, 1.0])
    vector.append((i/100) ** 2)"""

def VectorMatrixProjection(vector, matrixA):
    matrixAt = MatrixTranspose(matrixA)
    AtA = MatrixMultiplication(matrixAt, matrixA)
    inverse_AtA = InverseMatrix(AtA)
    final_matrix = MultipleMatrixMultiplication(matrixA, inverse_AtA, matrixAt)
    vector_projection = MatrixVectorMultiplication(final_matrix, vector)
    return vector_projection


def AugmentVector(matrix, vector):
    matrixA_augmented = matrix[:]
    for i in range(len(vector)):
        matrixA_augmented[i].append(vector[i])
    return matrixA_augmented

# y = 10x - 16.65