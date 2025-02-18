import os
import pandas as pd


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
          "文件已经保存到本目录下的 'result.csv。\n"
          "按 'Enter' 退出。\n"
          "#################################\n")


def main():
    input("#################################\n"
          "请把所有的 CSV 文件放到 data 文件夹下\n"
          "并把背景以 'bg.csv' 命名。\n"
          "然后按 'Enter' 继续。\n"
          "#################################\n")
    try:
        modify_csv_files()

    except Exception as e:
        print(f"Error: {e}")
        input("按 'Enter' 退出。\n")


if __name__ == "__main__":
    main()
