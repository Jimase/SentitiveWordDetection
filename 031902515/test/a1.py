import queue
import cProfile

def sol(vis):
    Q = queue.Queue()
    # 当前值，能用的k，花费的步数
    Q.put((0, 1, 0))
    vis[0] = 0
    while Q.empty() == False:
        val, k, num = Q.get()
        nval = val + k
        if nval < 200 and nval >= 0:
            Q.put((nval, k + 1, num + 1))
        if nval >= 0 and vis[nval] == -1:
            vis[nval] = num + 1
        nval = val - k
        if nval < 0 and nval > -200:
            Q.put((nval, k + 1, num + 1))
        if nval < 0 and vis[-nval] == -1:
            vis[-nval] = num + 1

if __name__ == '__main__':
    vis = [-1] * 2000
    sol(vis)
    # print(vis[0: 101])
    t = int(input())
    for _ in range(t):
        a, b = str(input()).strip().split(' ')
        a, b = int(a), int(b)
        ab = abs(a - b)
        print(vis[ab])
