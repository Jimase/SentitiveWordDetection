ans = 0

def dfs(graph, vis, x, y, n):
    global ans
    for i in range(1, n + 1):
        if x == 1:
            if graph[y][i] == 1:
                # print(i)
                if vis[i] == 0: ans += 1
                vis[i] = 1
                dfs(graph, vis, x, i, n)
        elif x == 0:
            if graph[i][y] == 1:
                if vis[i] == 1: ans -= 1
                vis[i] = 0
                dfs(graph, vis, x, i, n)

if __name__ == '__main__':
    n, q = [int(item) for item in str(input()).strip().split(' ')]
    graph = [[0] * (n + 5) for _ in range(n + 5)]
    vis = [0] * (n + 5)
    for i in range(n):
        yl = str(input()).strip().split(' ')
        num = int(yl[0])
        for j in range(1, num + 1):
            graph[i + 1][int(yl[j])] = 1
    for i in range(q):
        xy = str(input()).strip().split(' ')
        x, y = int(xy[0]), int(xy[1])
        if x == 1 and vis[y] == 0:
            ans += 1
            vis[y] = 1
        if x == 0 and vis[y] == 1:
            ans -= 1
            vis[y] = 0
        dfs(graph, vis, x, y, n)
        print(ans)

"""
3 2
1 2
1 3
0
1 1
0 2
"""

