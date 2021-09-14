ans = 0

def dfs(graph1, graph2, vis, x, y):
    global ans
    if x == 1:
        for i in range(len(graph1[y])):
            v = graph1[y][i]
            if vis[v] == 0: ans += 1
            vis[v] = 1
            dfs(graph1, graph2, vis, x, v)
    if x == 0:
        for i in range(len(graph2[y])):
            v = graph2[y][i]
            if vis[v] == 1: ans -= 1
            vis[v] = 0
            dfs(graph1, graph2, vis, x, v)

if __name__ == '__main__':
    n, q = [int(item) for item in str(input()).strip().split(' ')]
    graph1 = [[] for _ in range(n + 1)]
    graph2 = [[] for _ in range(n + 1)]
    vis = [0] * (n + 5)
    for i in range(n):
        yl = str(input()).strip().split(' ')
        num = int(yl[0])
        for j in range(1, num + 1):
            graph1[i + 1].append(int(yl[j]))
            graph2[int(yl[j])].append(i + 1)
    for i in range(q):
        xy = str(input()).strip().split(' ')
        x, y = int(xy[0]), int(xy[1])
        if x == 1 and vis[y] == 0:
            ans += 1
            vis[y] = 1
        if x == 0 and vis[y] == 1:
            ans -= 1
            vis[y] = 0
        dfs(graph1, graph2, vis, x, y)
        print(ans)

"""
3 2
1 2
1 3
0
1 1
0 2
"""

