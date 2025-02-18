from pathlib import Path
import pandas as pd


class FileProcessor:
    """文件处理类,用于复制、删除和处理文件"""
    
    def __init__(self, data_dir='./data', copy_dir='./data_copy'):
        """
        初始化FileProcessor类
        
        参数:
            data_dir: 源数据文件夹路径,默认为'/data'
            copy_dir: 文件复制的目标文件夹路径,默认为'/data_copy'
        """
        self.data_dir = Path(data_dir)
        self.copy_dir = Path(copy_dir)
    
    def copy_files(self):
        """将data文件夹下所有文件复制到copy_dir文件夹"""
        # 如果目标文件夹不存在则创建
        if not self.copy_dir.exists():
            self.copy_dir.mkdir(parents=True)
            
        # 遍历源文件夹中的所有文件
        for file in self.data_dir.glob('*'):
            if file.is_file():
                # 构建目标文件路径
                dst_file = self.copy_dir / file.name
                # 复制文件
                dst_file.write_bytes(file.read_bytes())
    
    def delete_files(self, endwith='_i'):
        """
        删除指定文件夹下所有文件名(不含后缀)不以endwith结尾的文件
        
        参数:
            endwith: 文件名结尾字符串,默认为'_i'
        """
        # 遍历文件夹中的所有文件
        for file in self.data_dir.glob('*'):
            # 只处理文件,不处理文件夹
            if file.is_file() and (file.suffix.lower() == '.dat' or file.suffix.lower() == '.csv'):
                # 获取不带后缀的文件名
                filename = file.name.split('.')[0]
                # 如果文件名不以endwith结尾
                if not filename.endswith(endwith):
                    # 删除文件
                    file.unlink()
    
    def delete_lines(self, line_num=29):
        """
        删除指定文件夹下所有文件的前line_num行
        
        参数:
            line_num: 要删除的行数,默认为29
        """
        # 遍历文件夹中的所有文件
        for file in self.data_dir.glob('*'):
            # 只处理文件,不处理文件夹
            if file.is_file() and file.suffix.lower() == '.csv':
                # 读取文件所有行
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # 只保留从line_num行之后的内容
                with open(file, 'w', encoding='utf-8') as f:
                    f.writelines(lines[line_num:])


    def process_date(self):
        """
        处理指定文件夹下的光谱数据，自动除背景
        """
        result = pd.DataFrame()
        background_data = pd.DataFrame()
        # 遍历文件夹中的所有文件
        for file in self.data_dir.glob('*'):
            # 只处理文件,不处理文件夹
            if file.is_file() and file.suffix.lower() == '.csv':
                filename_lower = file.name.split('.')[0].lower()
                if 'bg' in filename_lower or 'background' in filename_lower:
                    # 读取文件所有行,并写入变量background中
                    background_data = pd.read_csv(file, header=None, names=['wavelength', 'background_intensity'])
                else:
                    # 读取文件所有行
                    df = pd.read_csv(file, header=None, names=['wavelength', file.name.split('.')[0]])
                    # 获取光谱数据列
                    spectrum_data = df.iloc[:, 1]
                    # 把光谱数据列添加到result中
                    result = pd.concat([result, spectrum_data], axis=1)
        # 把所有的列按照列名排序
        result = result.sort_index(axis=1)
        # 把result和background合并，background在最左边
        result = pd.concat([background_data, result], axis=1)
        # 从第三列开始的所有列，除以第二列（background）
        for i in range(2, result.shape[1]):
            result.iloc[:, i] = result.iloc[:, i] / result.iloc[:, 1]
        # 把result保存为csv文件
        result.to_csv('result.csv', index=False)


if __name__ == '__main__':
    # 创建FileProcessor对象
    file_processor = FileProcessor()
    # 复制文件
    file_processor.copy_files()
    # 删除文件
    file_processor.delete_files()
    # 删除行
    file_processor.delete_lines()
    # 处理数据
    file_processor.process_date()
