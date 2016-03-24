'''def lcs(a,b):
	return lcsH(a,b,{},0,0)

def lcsH(a,b,d,i, j):
	if (a,b) in d:
		return d[(a,b)]
	if i == len(a) or j == len(b):
		d[(a,b)] = 0
		return 0
	if a[i] == b[j]:
		ans = 1 + lcsH(a,b,d,i+1,j+1)
		d[(a,b)] = ans
		return ans
	ans = max((lcsH(a,b,d,i+1,j),lcsH(a,b,d,i,j+1)))
	d[(a,b)] = ans
	return ans
'''
def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = 0
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = 1 + result
            x -= 1
            y -= 1
    return result