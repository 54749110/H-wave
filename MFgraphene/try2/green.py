import numpy as np
import tomli
import hwave.qlms
import matplotlib.pyplot as plt

# 定义基态能量，U/t的值, charge gap, 带隙
Nsite = 32
fillingcircle = 16
onsiteU = []
FM = [[0 for _ in range(fillingcircle-1)] for _ in range(100)]
AFM =[[0 for _ in range(fillingcircle-1)] for _ in range(100)]

# 大循环， 更改变量U从0到20，t一直为1
for i in range(20):
  # 小循环，更改filling
  for j in range(fillingcircle-1) :
  

  # 读取文本内容
    with open('input.toml', 'r') as file:
      content = file.read()

  # 找到Ncond = 后面的数字
    ncond_index = content.find('Ncond = ')
    if ncond_index != -1:
      ncond_value_start = ncond_index + len('Ncond = ')
      ncond_value_end = content.find('\n', ncond_value_start)
      ncond_value = int(content[ncond_value_start:ncond_value_end])

    # 修改filling
    updated_content_plus_one = content.replace(f'Ncond = {ncond_value}', f'Ncond = {2*(j+1)*Nsite//fillingcircle}', 1)
    with open('input.toml', 'w') as file_plus_one:
      file_plus_one.write(updated_content_plus_one)
        
    # 运行
    with open("input.toml", "rb") as fp:
      toml_dict = tomli.load(fp)
    hwave.qlms.run(input_dict=toml_dict)

    # 读取green.dat文件,提取第五列数据,这就是green的实部
    data_file = 'output/green.dat'
    realgreen = []

    with open(data_file, 'r') as file:
      for line in file:
        # 以空格分割每行数据，并获取第五列数据
        columns = line.split()
        if len(columns) >= 5:
            realgreen.append(float(columns[4])) 

    length=len(realgreen)

    # 铁磁判据
    rho0up = sum(realgreen[:length//2])
    rho0dn = sum(realgreen[length//2:])
    FM[i][j]=(rho0up - rho0dn)

    # 反铁磁判据
    rhopiup = sum(-value if index % 2 == 1 else value for index, value in enumerate(realgreen[:length//2]))
    rhopidn = sum(-value if index % 2 == 1 else value for index, value in enumerate(realgreen[length//2:]))
    AFM[i][j] = (rhopiup - rhopidn)

# 小循环结束



# 这一部分修改coulombintra.dat相互作用项，即onsiteU部分，修改格式遵从coulombintra.dat定义格式, 
# 每次运行前一定要进入coulombintra.dat修改初值为0.100000000000
# 读取文本文件并修改两个数值
  with open('coulombintra.def', 'r') as file:
    lines = file.readlines()

    # 修改两个数值为新值, 注意不要把虚部一起修改了
  new_lines = []
  oldvalue = 0.1+1*i
  newvalue= 0.1+1*(i+1)
  # 新的onsiteU的值
  onsiteU.append(newvalue)
  for line in lines:
    if "{:.15f}".format(oldvalue) in line:
      line = line.replace("{:.15f}".format(oldvalue), "{:.15f}".format(newvalue))
    new_lines.append(line)

  # 将更新后的内容写入原本的文件
  with open('coulombintra.def', 'w') as new_file:
    new_file.writelines(new_lines)


# 大循环结束

print(FM)
print(AFM)

# 复原 U
with open('coulombintra.def', 'r') as file:
   lines = file.readlines()

# 修改两个数值为新值, 注意不要把虚部一起修改了
new_lines = []
oldvalue = 0.1+1*(i+1)
newvalue= 0.1
for line in lines:
  if "{:.15f}".format(oldvalue) in line:
    line = line.replace("{:.15f}".format(oldvalue), "{:.15f}".format(newvalue))
  new_lines.append(line)

# 将更新后的内容写入原本的文件
with open('coulombintra.def', 'w') as new_file:
  new_file.writelines(new_lines)

# 复原 ncond
with open('input.toml', 'r') as file:
  content = file.read()
# 找到Ncond = 后面的数字
  ncond_index = content.find('Ncond = ')
  if ncond_index != -1:
    ncond_value_start = ncond_index + len('Ncond = ')
    ncond_value_end = content.find('\n', ncond_value_start)
    ncond_value = int(content[ncond_value_start:ncond_value_end])

# 修改filling
  updated_content_plus_one = content.replace(f'Ncond = {ncond_value}', f'Ncond = {Nsite}', 1)
with open('input.toml', 'w') as file_plus_one:
  file_plus_one.write(updated_content_plus_one)



# 画图
# 创建空列表来存储需要标记的点
points_red = []
points_orange = []
points_blue = []

# 找出AFM中绝对值大于0.1的点
for i in range(len(AFM)):
    for j in range(len(AFM[0])):
        if abs(AFM[i][j]) > 0.1:
            points_red.append((j, i))  # 注意这里(j, i)是为了将坐标转换为(x, y)

# 找出FM中绝对值大于0.1的点
for i in range(len(FM)):
    for j in range(len(FM[0])):
        if abs(FM[i][j]) > 0.1:
            points_orange.append((j, i))  # 注意这里(j, i)是为了将坐标转换为(x, y)
        else:
            points_blue.append((j, i))  # 注意这里(j, i)是为了将坐标转换为(x, y)

# 创建图表并绘制点
plt.figure(figsize=(8, 10))
#for point in points_red:
#    plt.scatter(point[0], point[1], color='red')
for point in points_orange:
    plt.scatter(point[0], point[1], color='orange')
for point in points_blue:
    plt.scatter(point[0], point[1], color='blue')

plt.xlabel('Column Index')
plt.ylabel('Row Index')
plt.title('Elements Visualization')

plt.gca().invert_yaxis()  # 因为坐标原点在左上角，所以需要反转y轴
plt.savefig("phasediagram.png")
plt.show()






print(FM)
print(AFM)