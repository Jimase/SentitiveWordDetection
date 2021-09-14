import collections

ans = set()

def sol(tiles, deepth, current):
    if deepth == len(tiles):
        global ans
        if len(current) > 0:
            ans.add(current)
        return
    for i in range(0, len(tiles) + 1):
        if i == len(tiles):
            sol(tiles, deepth + 1, current)
        else:
            cc = collections.Counter(current)
            bb = collections.Counter(tiles)
            if cc[tiles[i]] + 1 <= bb[tiles[i]]:
                sol(tiles, deepth + 1, current + tiles[i])

if __name__ == '__main__':
    tiles = str(input()).strip()
    sol(tiles, 0, "")
    print(len(ans))
    # print(ans)
