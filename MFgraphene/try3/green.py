import numpy as np
import tomli
import hwave.qlms
import matplotlib.pyplot as plt

# 定义基态能量，U/t的值, charge gap, 带隙
onsiteU = []
FM = []
AFM = []

# 大循环， 更改变量U从0到10，t一直为1
for i in range(100):

# 这一部分修改coulombintra.dat相互作用项，即onsiteU部分，修改格式遵从coulombintra.dat定义格式, 
# 每次运行前一定要进入coulombintra.dat修改初值为0.100000000000
# 读取文本文件并修改两个数值
  with open('coulombintra.def', 'r') as file:
    lines = file.readlines()

  # 修改两个数值为新值, 注意不要把虚部一起修改了
  new_lines = []
  oldvalue = 0.1*(i+1)
  newvalue= 0.1*(i+2)
  # 新的onsiteU的值
  onsiteU.append(newvalue)
  for line in lines:
    if "{:.15f}".format(oldvalue) in line:
        line = line.replace("{:.15f}".format(oldvalue), "{:.15f}".format(newvalue))
    new_lines.append(line)

  # 将更新后的内容写入原本的文件
  with open('coulombintra.def', 'w') as new_file:
    new_file.writelines(new_lines)



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
  FM.append(rho0up - rho0dn)

  # 反铁磁判据
  rhopiup = sum(-value if index % 2 == 1 else value for index, value in enumerate(realgreen[:length//2]))
  rhopidn = sum(-value if index % 2 == 1 else value for index, value in enumerate(realgreen[length//2:]))
  AFM.append(rhopiup - rhopidn)


# 复原
with open('coulombintra.def', 'r') as file:
   lines = file.readlines()

# 修改两个数值为新值, 注意不要把虚部一起修改了
new_lines = []
oldvalue = 0.1*(i+2)
newvalue= 0.1
for line in lines:
  if "{:.15f}".format(oldvalue) in line:
    line = line.replace("{:.15f}".format(oldvalue), "{:.15f}".format(newvalue))
  new_lines.append(line)

# 将更新后的内容写入原本的文件
with open('coulombintra.def', 'w') as new_file:
  new_file.writelines(new_lines)

print(FM)
print(AFM)