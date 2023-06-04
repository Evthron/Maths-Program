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
    return(resultant_matrix)


matrixA = [[1, 1, 0],
          [0, 1, 0],
          [0, 0, 1]]
matrixB = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]]

print(MatrixMultiplication(matrixA, matrixB))