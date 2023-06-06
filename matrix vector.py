def PrintMatrix(matrix):
    for row in matrix:
        print(row)
    print()
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



def RowFillZero(row, column):
    for i in range(column - len(row)):
        row.append(0.0)


def RowStandardise(row):
    divisor = 0
    for i in range(len(row)):
        if abs(row[i]) > 1e-10:
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


def GaussianElimination(eqn, is_fiding_solution = False, is_finding_inverse = False):
    "找到該行一個非零的數，與其他所有行相減，使他們全部變爲0,下一列，找到一個除了上面用過那行以外的非零數，和其他所有行相減,直到行或列結束就停止記錄用過的行"
    matrix = eqn[:]
    number_of_row = len(matrix)
    number_of_column = len(matrix[0])
    if is_fiding_solution:
        number_of_column -= 1
    elif is_finding_inverse:
        number_of_column -= number_of_row

    number_of_max_square = min(number_of_row, number_of_column)
    #數值的總和應該叫 sum? total? number? count?
    #計數器應該叫 counter? number?
    # cardinal Ordinal
    subtractor_row = 0
    used_row = list() #把初始化放在回圈外面!!!
    for column in range(number_of_max_square):
        #找非零行，用來減其他行的
        for row in range(number_of_row):
            # row是行編號的意思
            if (row not in used_row) and (matrix[row][column] != 0):
                subtractor_row = row
                break

        for row in range(number_of_row):
            if row != subtractor_row and matrix[row][column] != 0:
                matrix[row] = RowSubtract(matrix[row], matrix[subtractor_row])
        used_row.append(subtractor_row)

    for row in matrix:
        RowStandardise(row)

    # swapping rows
    for column in range(number_of_max_square):
        if matrix[column][column] == 0:
            for row in range(number_of_row):
                if matrix[row][column] != 0:
                    matrix[column],matrix[row] = matrix[row], matrix[column]

    return matrix

def Identity(matrix):
    identity_matrix = list()
    matrix_size = len(matrix)
    for i in range(matrix_size):
        identity_row = list()
        for j in range(matrix_size):
            if i == j:
                identity_row.append(1.0)
            else:
                identity_row.append(0.0)
        identity_matrix.append(identity_row)
    return identity_matrix

def InverseMatrix(mtx):
    matrix = mtx[:]
    number_of_row = len(matrix)
    number_of_column = len(matrix[0])
    if number_of_row != number_of_column:
        print("not square matrix, not invertible")
        return
    matrix_size = number_of_row

    identity_matrix = Identity(matrix)
    matrix = AugmentMatrix(matrix, identity_matrix)

    matrix = GaussianElimination(matrix, is_finding_inverse=True)

    verify_matrix = list()
    for i in range(matrix_size):
        verify_matrix.append(matrix[i][0:matrix_size])

    if identity_matrix != verify_matrix:
        print("can't return to identity matrix, not invertible")
        return

    inverted_matrix = list()
    for i in range(matrix_size):
        inverted_matrix.append(matrix[i][matrix_size:])

    return inverted_matrix


def ProjectionMatrix(matrixA):
    matrixAt = MatrixTranspose(matrixA)
    AtA = MatrixMultiplication(matrixAt, matrixA)
    inverse_AtA = InverseMatrix(AtA)
    projection_matrix = MultipleMatrixMultiplication(matrixA, inverse_AtA, matrixAt)
    return projection_matrix

def AugmentVector(matrix, vector):
    matrixA_augmented = matrix[:]
    for i in range(len(vector)):
        matrixA_augmented[i].append(vector[i])
    return matrixA_augmented

def AugmentMatrix(matrix1, matrix2):
    resultant_matrix = matrix1[:]
    matrix2_transpose = MatrixTranspose(matrix2[:])
    for vector in matrix2_transpose:
        resultant_matrix = AugmentVector(resultant_matrix, vector)
    return resultant_matrix


vector = list()
matrixA = list()

for i in range(0, 101):
    matrixA.append([i/10, 1.0])
    vector.append((i/10) ** 2)

projected_vector = MatrixVectorMultiplication(ProjectionMatrix(matrixA), vector)
augmented_matrixA = AugmentVector(matrixA, projected_vector)
end_matrix = GaussianElimination(augmented_matrixA, is_fiding_solution=True)
m = end_matrix[0][-1]
c = end_matrix[1][-1]
y = int(input())
print((y - c)/m)

def InputMatrix():
    row_number = int(input("Enter row_number: "))
    column_number = int(input("Enter column number: "))
    matrix = list()
    for i in range(row_number):
        row = input("Enter row: ").split()
        for i in range(len(row)):
            row[i] = float(row[i])
        RowFillZero(row, column_number)
        matrix.append(row)
    return matrix