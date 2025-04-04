import numpy as np
import tomli
import hwave.qlms
import matplotlib.pyplot as plt

# 定义基态能量，U/t的值, charge gap, 带隙
eigenenergy = []
totalenergy = []
onsiteU = []
chargegap = []
diracgap = []

# 大循环， 更改变量U从0到10，t一直为1
for i in range(100):

# 这一部分修改coulombintra.dat相互作用项，即onsiteU部分，修改格式遵从coulombintra.dat定义格式, 
# 每次运行前一定要进入coulombintra.dat修改初值为0.100000000000
# 读取文本文件并修改两个数值
  with open('coulombintra.dat', 'r') as file:
    lines = file.readlines()

# 修改两个数值为新值, 注意不要把虚部一起修改了
  new_lines = []
  oldvalue = 0.1*(i+1)
  newvalue= 0.1*(i+2)
  # 新的onsiteU的值
  onsiteU.append(newvalue)
  for line in lines:
    if "{:.12f}".format(oldvalue) in line:
        line = line.replace("{:.12f}".format(oldvalue), "{:.12f}".format(newvalue))
    new_lines.append(line)

# 将更新后的内容写入原本的文件
  with open('coulombintra.dat', 'w') as new_file:
    new_file.writelines(new_lines)



# 提取输入并运行
  # 读取文本内容
  with open('input.toml', 'r') as file:
    content = file.read()

# 计算charge gap  为n+1传导电子基态能量加上n-1传导电子基态能量与两倍n传导电子基态能量之差，half-filling ,修改input.toml传导电子数
# 找到Ncond = 后面的数字
  ncond_index = content.find('Ncond = ')
  if ncond_index != -1:
    ncond_value_start = ncond_index + len('Ncond = ')
    ncond_value_end = content.find('\n', ncond_value_start)
    ncond_value = int(content[ncond_value_start:ncond_value_end])

  # 传导电子加一
  updated_content_plus_one = content.replace(f'Ncond = {ncond_value}', f'Ncond = {ncond_value + 2}', 1)
  with open('input.toml', 'w') as file_plus_one:
    file_plus_one.write(updated_content_plus_one)
        
  # 运行
  with open("input.toml", "rb") as fp:
    toml_dict = tomli.load(fp)
  hwave.qlms.run(input_dict=toml_dict)
      
  # 读取基态能量文本文件，所有eigenvalue最小值
  data = np.load("output/eigen.npz") 
  eigenvalue = data["eigenvalue"]
  eigenenergyadd1 = ((min([min(eigenvalue[:,0]),min(eigenvalue[:,1]),min(eigenvalue[:,2]),min(eigenvalue[:,3])])))

  # 传导电子减一
  updated_content_minus_one = content.replace(f'Ncond = {ncond_value}', f'Ncond = {ncond_value - 2}', 1)
  with open('input.toml', 'w') as file_minus_one:
    file_minus_one.write(updated_content_minus_one)

  # 运行
  with open("input.toml", "rb") as fp:
    toml_dict = tomli.load(fp)
  hwave.qlms.run(input_dict=toml_dict)

  # 读取基态能量文本文件，所有eigenvalue最小值
  data = np.load("output/eigen.npz") 
  eigenvalue = data["eigenvalue"]
  eigenenergyminus1 = ((min([min(eigenvalue[:,0]),min(eigenvalue[:,1]),min(eigenvalue[:,2]),min(eigenvalue[:,3])])))

  # 还原原始文件内容
  with open('input.toml', 'w') as file:
    file.write(content)

  # 运行
  with open("input.toml", "rb") as fp:
    toml_dict = tomli.load(fp)
  hwave.qlms.run(input_dict=toml_dict)
      


# 运行部分结束


# 读取总能量文本文件并提取第一行中的数字
  with open('output/energy.dat', 'r') as file:
    first_line = file.readline().strip()  # 读取第一行并去除换行符和空格
    # 使用split函数分割字符串，获取等号右侧的数字部分
    number_str = first_line.split('=')[-1].strip()  
    # 将字符串转换为浮点数
    number = float(number_str)


  totalenergy.append(number)

# 读取基态能量文本文件，所有eigenvalue最小值
  data = np.load("output/eigen.npz") 
  eigenvalue = data["eigenvalue"]
  wavevec_index   = data["wavevector_index"]
  wavevec_unit    = data["wavevector_unit"]
  eigenenergynochange = (min([min(eigenvalue[:,0]),min(eigenvalue[:,1]),min(eigenvalue[:,2]),min(eigenvalue[:,3])]))
  eigenenergy.append(eigenenergynochange)


# 计算charge gap  为n+1传导电子基态能量加上n-1传导电子基态能量与两倍n传导电子基态能量之差，half-filling
  chargegap.append(eigenenergyadd1 + eigenenergyminus1 -2*eigenenergynochange)

# 是否打开了狄拉克锥 ？
  diracgap.append(min(eigenvalue[:,1])- max(eigenvalue[:,2]))



# 复原onsiteU
with open('coulombintra.dat', 'r') as file:
  lines = file.readlines()

# 修改两个数值为新值, 注意不要把虚部一起修改了
new_lines = []
oldvalue = 0.1*(i+2)
newvalue= 0.1
for line in lines:
  if "{:.12f}".format(oldvalue) in line:
      line = line.replace("{:.12f}".format(oldvalue), "{:.12f}".format(newvalue))
  new_lines.append(line)

# 将更新后的内容写入原本的文件
with open('coulombintra.dat', 'w') as new_file:
  new_file.writelines(new_lines)



# 绘图
plt.scatter(onsiteU, eigenenergy)
plt.legend()
plt.xlabel("U/t")
plt.ylabel("GS Energy")
plt.savefig("gsenergy.png")
plt.clf()

plt.scatter(onsiteU, chargegap)
plt.legend()
plt.xlabel("U/t")
plt.ylabel("Gap")
plt.savefig("chargegap.png")
plt.clf()

plt.scatter(onsiteU, diracgap)
plt.legend()
plt.xlabel("U/t")
plt.ylabel("diracGap")
plt.savefig("diracgap.png")
plt.clf()
#plt.show()