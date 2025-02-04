import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(998990)
def cTs(s):
    ss = ""
    while (s):
        ss = ss + chr((s%32) + ord('0'))
        s = s // 10

    return ss


def GIDS(ss, ln1):
    s = 0

    for i in range(ln1):
        s = s + ord(ss[i]) - ord('0')
    return cTs(s)

def GDR(ss):

    if (len(ss) == 1):
        return ord(ss[0])-ord('0')

    ss = GIDS(ss,len(ss))

    return GDR(ss)

if __name__ == '__main__':
    ss = input("Enter 01022025:")

    print(GDR(ss))

     
