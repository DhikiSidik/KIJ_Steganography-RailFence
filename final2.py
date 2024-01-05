from PIL import Image

def genData(data):
    return [format(ord(i), '08b') for i in data]

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
        for j in range(8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                pix[j] = pix[j] + 1 if pix[j] != 0 else pix[j] - 1

        if i == lendata - 1:
            pix[-1] = pix[-1] - 1 if pix[-1] % 2 == 0 and pix[-1] != 0 else pix[-1] + 1
        else:
            pix[-1] = pix[-1] - 1 if pix[-1] % 2 != 0 else pix[-1]

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x, y = 0, y + 1
        else:
            x += 1

def encode_rail_fence(message, key):
    result = ""
    matrix = [["" for _ in range(len(message))] for _ in range(key)]
    increment = 1
    row, col = 0, 0

    for c in message:
        if row + increment < 0 or row + increment >= len(matrix):
            increment = increment * -1

        matrix[row][col] = c
        row += increment
        col += 1

    for i in range(key):
        for j in range(len(matrix[0])):
            if matrix[i][j] != "":
                result += matrix[i][j]

    return result

def decode_rail_fence(encoded_message, key):
    message_length = len(encoded_message)
    matrix = [["" for _ in range(message_length)] for _ in range(key)]

    idx = 0
    increment = 1

    for selectedRow in range(0, len(matrix)):
        row = 0

        for col in range(0, len(matrix[row])):
            if row + increment < 0 or row + increment >= len(matrix):
                increment = increment * -1

            if row == selectedRow:
                matrix[row][col] = encoded_message[idx]
                idx += 1

            row += increment

    matrix = transpose(matrix)
    result = ""

    for lst in matrix:
        result += "".join(lst)

    return result.strip()

def decode_steganography(image):
    imgdata = iter(image.getdata())
    data = ''

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        binstr = ''.join('0' if i % 2 == 0 else '1' for i in pixels[:8])
        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data

def encode():
    img = input("Masukkan Gambar Beserta Extensi: ")
    image = Image.open(img, 'r')

    data = input("Masukkan Pesan: ")
    if not data:
        raise ValueError('Pesan Tidak Boleh Kosong')

    key = 3
    encoded_message = encode_rail_fence(data, key)

    newimg = image.copy()
    encode_enc(newimg, encoded_message)

    new_img_name = input("Nama Baru Untuk Gambar Beserta Extensi: ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def decode():
    img = input("Masukkan Gambar Beserta Extensi: ")
    image = Image.open(img, 'r')

    key = 3
    encoded_message = decode_steganography(image)
    decoded_message = decode_rail_fence(encoded_message, key)

    print("Decoded Message: {0}".format(decoded_message))

def transpose(m):
    result = [[0 for _ in range(len(m))] for _ in range(len(m[0]))]

    for i in range(len(m)):
        for j in range(len(m[0])):
            result[j][i] = m[i][j]

    return result

def main():
    try:
        choice = input("1. Encode\n2. Decode\n")
        if choice == '1':
            encode()
        elif choice == '2':
            decode()
        else:
            raise Exception("Input tidak sesuai")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
