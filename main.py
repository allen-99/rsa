# 1.	Необходимо реализовать алгоритм RSA.
# 2.	Два простых числа могут генерироваться как сами, так и введены пользователем.
# 3.	На вход подается строка из латинских букв разного регистра, цифр, знаков препинания и пробела.
# 4.	Пользователь на выбор может как зашифровать, так и расшифровать входные данные.
# 5.	Позволяется использование любого языка программирования.

def input_check_q_r(q, r):
    check_q_r_are_prime = eratosthenes(q + r)
    return not check_q_r_are_prime[q] or not check_q_r_are_prime[r] or q == 1 or r == 1


def eratosthenes(n):
    bool_result = [True] * (n + 1)

    for i in range(2, n + 1):
        if bool_result[i]:
            for j in range(2 * i, n + 1, i):
                bool_result[j] = False
    return bool_result


def sort_prime_for_e(boolean_prime):
    result_with_one = []
    for i in range(5, len(boolean_prime)):
        if boolean_prime[i]:
            result_with_one.append((i, bin(i).count('1')))
    result_with_one = sorted(result_with_one, key=lambda point: (point[1], -point[0]))
    result = [elem[0] for elem in result_with_one]
    return result


def gcs(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def extended_gsc(a, b):
    if b == 0:
        x = 1
        y = 0
        return x, y

    x1, y1 = extended_gsc(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return x, y


def pfi(q, r):
    return (q - 1)*(r - 1)


def rsa_public_key_generate(q, r):
    n = q * r
    pfi_ = pfi(q, r)

    prime_numbers = sort_prime_for_e(eratosthenes(pfi_))
    e = 3
    for i in range(len(prime_numbers)):
        if gcs(n, prime_numbers[i] == 1):
            e = prime_numbers[i]
            break

    return e


def rsa_private_key_generate(q, r, e):
    pfi_ = pfi(q, r)

    a, b = extended_gsc(e, pfi_)
    if a < 0:
        a += pfi_
    d = a
    if d == e:
        d += pfi_
    return d


def multiply(a, b, n):
    res = 1
    while b != 0:
        if b % 2 == 0:
            b = b / 2
            a = (a * a) % n
        elif b % 2 != 0:
            b = b - 1
            res = (res * a) % n
    return res


def encode(public_key, m):
    e = public_key[0]
    n = public_key[1]

    c = multiply(m, e, n)
    return c


def decode(private_key, c):
    d = private_key[0]
    n = private_key[1]

    m = multiply(c, d, n)
    return m


def main():

    question = input('encode - 1, decode - 0, else - exit: ')

    q = int(input('input q (prime and more then 10): '))
    r = int(input('input r (prime and more then 10): '))
    m = (input('input initial message: '))

    if input_check_q_r(q, r):
        print('q or q is not prime number!')
        return

    n = q * r
    public_key = (rsa_public_key_generate(q, r), n)
    private_key = (rsa_private_key_generate(q, r, public_key[0]), n)

    print('initial message: ', m)

    if question == '1':
        encode_m = []
        for char in m:
            c = encode(public_key, ord(char))
            encode_m.append(c)

        encode_m = ''.join([chr(a) for a in encode_m])
        print('encode message: ', encode_m)
    elif question == '0':
        encode_m = [ord(a) for a in m]
        decode_m = []
        for ascii_char in encode_m:
            m_decode = decode(private_key, ascii_char)
            decode_m.append(chr(m_decode))

        decode_m = ''.join(decode_m)
        print('m decode: ', decode_m)



if __name__ == "__main__":
    main()

