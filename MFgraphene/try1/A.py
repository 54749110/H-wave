with open('input.toml', 'r') as file:
    content = file.read()

# 找到Ncond = 后面的数字
ncond_index = content.find('Ncond = ')
if ncond_index != -1:
    ncond_value_start = ncond_index + len('Ncond = ')
    ncond_value_end = content.find('\n', ncond_value_start)
    ncond_value = int(content[ncond_value_start:ncond_value_end])

    # 创建加一的新文件
    updated_content_plus_one = content.replace(f'Ncond = {ncond_value}', f'Ncond = {ncond_value + 2}', 2)
    with open('your_file_plus_one.txt', 'w') as file_plus_one:
        file_plus_one.write(updated_content_plus_one)

    # 创建减一的新文件
    updated_content_minus_one = content.replace(f'Ncond = {ncond_value}', f'Ncond = {ncond_value - 2}', 2)
    with open('your_file_minus_one.txt', 'w') as file_minus_one:
        file_minus_one.write(updated_content_minus_one)