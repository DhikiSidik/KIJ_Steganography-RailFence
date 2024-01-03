def main():
    choice = input("Enter '1' for encryption or '2' for decryption: ").upper()

    if choice == '1':
        clearText = input("Enter the text to be encrypted: ")
        key = 3
        cipherText = cipher(clearText, key)
        print("Ciphered Text: {0}".format(cipherText))

    elif choice == '2':
        cipherText = input("Enter the text to be decrypted: ")
        key = 3
        decipherText = decipher(cipherText, key)
        print("Deciphered Text: {0}".format(decipherText))

    else:
        print("Invalid choice. Please enter 'E' for encryption or 'D' for decryption.")

    return


def cipher(clearText, key):
    result = ""

    matrix = [["" for x in range(len(clearText))] for y in range(key)]

    increment = 1
    row = 0
    col = 0

    for c in clearText:
        if row + increment < 0 or row + increment >= len(matrix):
            increment = increment * -1

        matrix[row][col] = c

        row += increment
        col += 1

    for lst in matrix:
        result += "".join(lst)

    return result


def decipher(cipherText, key):
    result = ""

    matrix = [["" for x in range(len(cipherText))] for y in range(key)]

    idx = 0
    increment = 1

    for selectedRow in range(0, len(matrix)):
        row = 0

        for col in range(0, len(matrix[row])):
            if row + increment < 0 or row + increment >= len(matrix):
                increment = increment * -1

            if row == selectedRow:
                matrix[row][col] += cipherText[idx]
                idx += 1

            row += increment

    matrix = transpose(matrix)
    for lst in matrix:
        result += "".join(lst)

    return result


def transpose(m):
    result = [[0 for y in range(len(m))] for x in range(len(m[0]))]

    for i in range(len(m)):
        for j in range(len(m[0])):
            result[j][i] = m[i][j]

    return result


main()
