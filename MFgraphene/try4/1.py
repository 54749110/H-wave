# 创建一个4x4的正方形，标记每个点
square = [[(i * 4) + j + 1 for j in range(4)] for i in range(4)]

# 初始化一个空列表来存储连线
connections = []

# 遍历每个点，找到其最近邻点
for i in range(4):
    for j in range(4):
        # 当前点的序号
        current = square[i][j]
        
        # 检查右边的点（水平连线）
        if j < 3:
            right = square[i][j + 1]
            connections.append((current, right))
        
        # 检查下面的点（垂直连线）
        if i < 3:
            bottom = square[i + 1][j]
            connections.append((current, bottom))

# 将连线转换为2列的矩阵
connection_matrix = [[a, b] for (a, b) in connections]

# 输出结果
print("连线矩阵：")
for row in connection_matrix:
    print(row)