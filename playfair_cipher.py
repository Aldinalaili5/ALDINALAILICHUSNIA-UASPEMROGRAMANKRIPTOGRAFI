from flask import Flask, render_template, request

app = Flask(__name__)

def prepare_key(key):
    # Fungsi untuk menyusun kunci dalam bentuk matriks 5x5
    # Implementasi sederhana, bisa dimodifikasi sesuai kebutuhan
    key = key.upper().replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key_matrix = [[0] * 5 for _ in range(5)]
    key_set = set()

    i, j = 0, 0
    for char in key + alphabet:
        if char not in key_set:
            key_matrix[i][j] = char
            key_set.add(char)
            j += 1
            if j == 5:
                i += 1
                j = 0

    return key_matrix

def find_coordinates(matrix, char):
    # Fungsi untuk mencari koordinat suatu karakter dalam matriks
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == char:
                return i, j

def playfair_encrypt(plaintext, key_matrix):
    # Fungsi untuk mengenkripsi menggunakan Playfair Cipher
    plaintext = plaintext.upper().replace('J', 'I')
    pairs = [plaintext[i:i+2] for i in range(0, len(plaintext), 2)]

    ciphertext = ""
    for pair in pairs:
        if len(pair) == 2:
            a, b = pair
            a_i, a_j = find_coordinates(key_matrix, a)
            b_i, b_j = find_coordinates(key_matrix, b)

            if a_i == b_i:
                ciphertext += key_matrix[a_i][(a_j + 1) % 5] + key_matrix[b_i][(b_j + 1) % 5]
            elif a_j == b_j:
                ciphertext += key_matrix[(a_i + 1) % 5][a_j] + key_matrix[(b_i + 1) % 5][b_j]
            else:
                ciphertext += key_matrix[a_i][b_j] + key_matrix[b_i][a_j]
        else:
            ciphertext += pair[0] + 'X'

    return ciphertext

def playfair_decrypt(ciphertext, key_matrix):
    # Fungsi untuk mendekripsi menggunakan Playfair Cipher
    ciphertext = ciphertext.upper()
    pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]

    plaintext = ""
    for pair in pairs:
        a, b = pair
        a_i, a_j = find_coordinates(key_matrix, a)
        b_i, b_j = find_coordinates(key_matrix, b)

        if a_i == b_i:
            plaintext += key_matrix[a_i][(a_j - 1) % 5] + key_matrix[b_i][(b_j - 1) % 5]
        elif a_j == b_j:
            plaintext += key_matrix[(a_i - 1) % 5][a_j] + key_matrix[(b_i - 1) % 5][b_j]
        else:
            plaintext += key_matrix[a_i][b_j] + key_matrix[b_i][a_j]

    return plaintext

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key = request.form['key']
        plaintext = request.form['plaintext']

        key_matrix = prepare_key(key)
        ciphertext = playfair_encrypt(plaintext, key_matrix)
        decrypted_text = playfair_decrypt(ciphertext, key_matrix)

        return render_template('index.html', result=True, key=key, plaintext=plaintext,
                               ciphertext=ciphertext, decrypted_text=decrypted_text)

    return render_template('index.html', result=False)

if __name__ == '__main__':
    app.run(debug=True)
