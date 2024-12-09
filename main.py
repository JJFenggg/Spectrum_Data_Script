import os
import pandas as pd


def create_folders():
    try:
        os.mkdir('data')
        os.mkdir('copy')
    except FileExistsError:
        pass

    input("#################################\n"
          "data文件夹与copy文件夹已创建。\n"
          "#################################\n")


def copy_files():
    for root, dirs, files in os.walk('./'):
        for file in files:
            if file.endswith('.csv') or file.endswith('.CSV'):
                file_path = os.path.join(root, file)
                with (open(file_path, 'r', encoding='utf-8') as old_file,
                      open('./copy/' + file, mode='a+', encoding='utf-8') as new_file):
                    lines = old_file.readlines()
                    for line in lines:
                        new_file.write(line)

    input("#################################\n"
          "所有的文件已备份到 copy 文件夹下\n"
          "#################################\n")


def delete_useless_files():
    for root, dirs, files in os.walk('./'):
        for file in files:
            # 检查文件是否满足删除条件
            if (
                (file.endswith('.csv') or file.endswith('.CSV'))  # 是 CSV 文件
                and root == './'                                  # 限制只读取当前目录下的 CSV 文件
                and 'i' not in file                              # 文件名中不包含 'i'
            ):
                file_path = os.path.join(root, file)  # 构建文件路径
                try:
                    os.remove(file_path)  # 删除文件
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

    input("#################################\n"
          "所有的无用文件已删除。\n"
          "#################################\n")


def delete_useless_lines(lines_number=28):
    for root, dirs, files in os.walk('./'):
        for file in files:
            if file.endswith('.csv') or file.endswith('.CSV'):
                file_path = os.path.join(root, file)
                with (open(file_path, 'r', encoding='utf-8') as old_file,
                      open('./data/' + file, mode='a+', encoding='utf-8') as new_file):
                    lines = old_file.readlines()
                    for index, line in enumerate(lines):
                        if index > lines_number:
                            new_file.write(line)

    input("#################################\n"
          "文件的前30行已删除，并保存在data文件夹下\n"
          "#################################\n")


def modify_csv_files():
    result = pd.DataFrame()

    for root, dirs, files in os.walk('./data'):
        for file in files:
            if (file.endswith('.csv') or file.endswith('.CSV')) and (root == './data'):  # 限制只读取当前目录下的 CSV 文件
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(file_path, encoding='utf-8', header=None, names=['wavelength', f'{file}'])
                    # 读取 CSV 文件
                    if "bg" not in file:
                        result = pd.concat([result, df[f'{file}']], axis=1)
                    else:
                        result = pd.concat([result, df], axis=1)
                    # 将读取的数据合并到 result 中

                except UnicodeDecodeError:
                    print(f"UnicodeDecodeError: Cannot read file {file_path} with 'utf-8' encoding.")
                    continue

    # 将 'wavelength' 和 'bg' 列移动到最前面
    for col in result.columns:
        if "bg" in col:
            bg = result.pop(col)
            result.insert(0, col, bg)
        else:
            pass
    for col in result.columns:
        if "wavelength" in col:
            wl = result.pop(col)
            result.insert(0, col, wl)
        else:
            pass

    # 对除了 'wavelength' 和 'bg' 以外的列进行操作
    bg_column_name = result.columns[1]
    for col in result.columns:
        if col != 'wavelength' and col != bg_column_name:
            result[col] = result[col] / result[bg_column_name]

    result.to_csv('result.csv', index=False, encoding='utf-8')  # 将合并后的数据保存到 result.csv 文件中

    input("#################################\n"
          "文件已经保存到本目录下的 'result。\n"
          "按 'Enter' 退出。\n"
          "#################################\n")


def main():
    input("#################################\n"
          "请把背景以 'bg' 命名。\n"
          "然后按 'Enter' 继续。\n"
          "#################################\n")
    create_folders()
    copy_files()
    delete_useless_files()
    delete_useless_lines()
    modify_csv_files()


if __name__ == "__main__":
    main()
