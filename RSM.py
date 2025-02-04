def cTs(s):
    ss1 = ""
    while s:
        ss1 = ss1 + chr((s % 10) + ord('0'))
        s = s // 10
    return ss1

def GIDS(ssl, ln1):
    s = 0
    for i in range(ln1):
        if ssl[i].isdigit():  # Ensure the character is a digit
            s += int(ssl[i])
        else:
            raise ValueError("Input must contain only digits.")
    return cTs(s)

def GDR(ssl):
    if len(ssl) == 1:
        return ord(ssl[0]) - ord('0')

    ssl = GIDS(ssl, len(ssl))
    return GDR(ssl)

if __name__ == '__main__':
    ssl = input("Enter:")  # No need for str() as input() already returns a string
    try:
        print(GDR(ssl))
    except ValueError as e:
        print(e)
