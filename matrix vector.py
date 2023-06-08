import copy


class Matrix(list):
    """
    attribute: is_augmented
    """

    def __init__(self):
        self.is_augmented = False
        self.augmented_column_number = 0

    def __str__(self):
        a = copy.deepcopy(self)
        for i in range(len(a)):
            for j in range(len(a[0])):
                a[i][j] = str(a[i][j])

        result = "-------\n"
        for row in a:
            variable_row = row[0:len(row) - self.augmented_column_number]
            answer_row = row[-self.augmented_column_number:]
            result += " ".join(variable_row)
            if self.is_augmented:
                result += " | " + " ".join(answer_row)
            result += "\n"
        result += "-------"
        return result

    def add_row(self, *args):
        for row in args:
            if self == Matrix():
                self.append(row)
            elif len(row) == len(self[0]):
                self.append(row)
            else:
                raise Exception("matrix column number should be ", len(self[0]), "now get", len(row))

    def transpose(self):
        transposed_matrix = Matrix()
        for i in range(len(self[0])):
            row = list()
            for j in range(len(self)):
                row.append(self[j][i])
            transposed_matrix.add_row(row)
        return transposed_matrix

    def identity(self):
        """
        return the identity matrix with the same size as the matrix

        """
        identity_matrix = Matrix()
        matrix_size = len(self)
        for i in range(matrix_size):
            identity_row = list()
            for j in range(matrix_size):
                if i == j:
                    identity_row.append(1.0)
                else:
                    identity_row.append(0.0)
            identity_matrix.add_row(identity_row)
        return identity_matrix


    def inverse(self):
        matrix = copy.deepcopy(self)
        number_of_row = len(matrix)
        number_of_column = len(matrix[0])
        if number_of_row != number_of_column:
            print("not square matrix, not invertible")
            return
        matrix_size = number_of_row

        identity_matrix = matrix.identity()
        matrix = matrix.augment_matrix(identity_matrix)

        matrix = matrix.gaussian_elimination(is_finding_inverse=True)

        verify_matrix = Matrix()
        for i in range(matrix_size):
            verify_matrix.add_row(matrix[i][0:matrix_size])

        if identity_matrix != verify_matrix:
            print("can't return to identity matrix, not invertible")
            return

        inverted_matrix = Matrix()
        for i in range(matrix_size):
            inverted_matrix.add_row(matrix[i][matrix_size:])

        return inverted_matrix

    def projection(self):
        """
        finds the projection matrix

        :return: projection matrix A * (AtA)^-1 * At
        """
        matrixAt = self.transpose()
        AtA = matrixAt.multiply_matrix(self)
        inverse_AtA = AtA.inverse()
        projection_matrix = self.multiply_matrix(inverse_AtA, matrixAt)
        return projection_matrix

    def multiply_vector(self, vector):
        answer = list()
        for i in range(len(self)):
            sum = 0
            for j in range(len(vector)):
                sum += vector[j] * self[i][j]
            answer.append(sum)
        return answer

    def augment_vector(self, vector):
        matrixA_augmented = copy.deepcopy(self)
        for i in range(len(vector)):
            matrixA_augmented[i].append(vector[i])
        matrixA_augmented.is_augmented = True
        matrixA_augmented.augmented_column_number = 1
        return matrixA_augmented

    def augment_matrix(self, matrix2):
        resultant_matrix = copy.deepcopy(self)
        matrix2_transpose = matrix2.transpose()
        for vector in matrix2_transpose:
            resultant_matrix = resultant_matrix.augment_vector(vector)
        resultant_matrix.is_augmented = True
        resultant_matrix.augmented_column_number = len(matrix2_transpose)
        return resultant_matrix

    def standardise(self):
        matrix = copy.deepcopy(self)
        for row in matrix:
            divisor = 0
            for i in range(len(row)):
                if abs(row[i]) > 1e-10:
                    divisor = row[i]
                    break
            if divisor != 0:
                for i in range(len(row)):
                    row[i] = row[i] / divisor
        return matrix

    def gaussian_elimination(self, is_fiding_solution = False, is_finding_inverse = False):
        "找到該行一個非零的數，與其他所有行相減，使他們全部變爲0,下一列，找到一個除了上面用過那行以外的非零數，和其他所有行相減,直到行或列結束就停止記錄用過的行"
        matrix = copy.deepcopy(self)
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

        matrix = matrix.standardise()

        # swapping rows
        for column in range(number_of_max_square):
            if matrix[column][column] == 0:
                for row in range(number_of_row):
                    if matrix[row][column] != 0:
                        matrix[column],matrix[row] = matrix[row], matrix[column]

        return matrix

    def multiply_matrix(self, *args):
        current_matrix_product = self
        for matrix in args:
            transposed_matrix = matrix.transpose()
            new_matrix_product = Matrix()
            for vector in transposed_matrix:
                row = current_matrix_product.multiply_vector(vector)
                new_matrix_product.append(row)
            current_matrix_product = new_matrix_product.transpose()
        return current_matrix_product

    def value_reset(self):
        row_number = int(input("Enter row_number: "))
        column_number = int(input("Enter column number: "))
        self = Matrix()
        for i in range(row_number):
            row = input("Enter row: ").split()
            for i in range(len(row)):
                row[i] = float(row[i])
            RowFillZero(row, column_number)
            self.add_row(row)


def RowFillZero(row, column):
    for i in range(column - len(row)):
        row.append(0.0)


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


def square_root_linear_approximate():
    vector = list()
    matrixA = Matrix()

    precision = 10
    for i in range(0, 10 * precision + 1):
        matrixA.add_row([i/precision, 1.0])
        vector.append((i/precision) ** 2)

    projected_vector = matrixA.projection().multiply_vector(vector)
    augmented_matrixA = matrixA.augment_vector(projected_vector)
    end_matrix = augmented_matrixA.gaussian_elimination(is_fiding_solution=True)
    m = end_matrix[0][-1]
    c = end_matrix[1][-1]
    y = int(input())
    print((y - c)/m)