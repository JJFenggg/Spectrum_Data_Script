from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                              QFileDialog, QMessageBox, QFrame)
from PySide6.QtCore import Qt
from main import FileProcessor

class FileProcessorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件处理工具")
        self.resize(800, 600)
        self.setMinimumSize(800, 600)

        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 文件选择区域
        file_frame = QFrame()
        file_frame.setFrameStyle(QFrame.StyledPanel)
        file_layout = QVBoxLayout(file_frame)
        
        # 源文件夹选择
        source_layout = QHBoxLayout()
        source_label = QLabel("源文件夹:")
        source_label.setStyleSheet("font-size: 24px;")
        self.data_dir = QLineEdit("./data")
        self.data_dir.setStyleSheet("font-size: 24px; padding: 8px;")
        browse_source = QPushButton("浏览")
        browse_source.setStyleSheet("font-size: 24px; padding: 10px 20px;")
        browse_source.clicked.connect(self.browse_data_dir)
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.data_dir)
        source_layout.addWidget(browse_source)
        file_layout.addLayout(source_layout)
        
        # 目标文件夹选择
        target_layout = QHBoxLayout()
        target_label = QLabel("备份文件夹:")
        target_label.setStyleSheet("font-size: 24px;")
        self.copy_dir = QLineEdit("./data_copy")
        self.copy_dir.setStyleSheet("font-size: 24px; padding: 8px;")
        browse_target = QPushButton("浏览")
        browse_target.setStyleSheet("font-size: 24px; padding: 10px 20px;")
        browse_target.clicked.connect(self.browse_copy_dir)
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.copy_dir)
        target_layout.addWidget(browse_target)
        file_layout.addLayout(target_layout)
        
        main_layout.addWidget(file_frame)

        # 设置区域
        settings_frame = QFrame()
        settings_frame.setFrameStyle(QFrame.StyledPanel)
        settings_layout = QHBoxLayout(settings_frame)
        
        # 文件名结尾设置
        endwith_layout = QHBoxLayout()
        endwith_label = QLabel("文件名结尾:")
        endwith_label.setStyleSheet("font-size: 24px;")
        self.endwith = QLineEdit("_i")
        self.endwith.setStyleSheet("font-size: 24px; padding: 8px;")
        self.endwith.setFixedWidth(100)
        endwith_layout.addWidget(endwith_label)
        endwith_layout.addWidget(self.endwith)
        endwith_layout.addStretch()
        
        # 删除行数设置
        line_num_layout = QHBoxLayout()
        line_num_label = QLabel("删除行数:")
        line_num_label.setStyleSheet("font-size: 24px;")
        self.line_num = QLineEdit("29")
        self.line_num.setStyleSheet("font-size: 24px; padding: 8px;")
        self.line_num.setFixedWidth(100)
        line_num_layout.addWidget(line_num_label)
        line_num_layout.addWidget(self.line_num)
        line_num_layout.addStretch()
        
        settings_layout.addLayout(endwith_layout)
        settings_layout.addLayout(line_num_layout)
        main_layout.addWidget(settings_frame)

        # 功能按钮区域
        buttons_frame = QFrame()
        buttons_frame.setFrameStyle(QFrame.StyledPanel)
        buttons_layout = QVBoxLayout(buttons_frame)
        
        # 普通功能按钮
        normal_buttons = QHBoxLayout()
        self.copy_btn = QPushButton("备份文件")
        self.delete_btn = QPushButton("删除文件")
        self.delete_lines_btn = QPushButton("删除行")
        self.process_btn = QPushButton("处理数据")
        
        for btn in [self.copy_btn, self.delete_btn, self.delete_lines_btn, self.process_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    padding: 15px 30px;
                    background-color: #f0f0f0;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            normal_buttons.addWidget(btn)
        
        buttons_layout.addLayout(normal_buttons)
        
        # 一键处理按钮
        self.process_all_btn = QPushButton("一键处理")
        self.process_all_btn.setStyleSheet("""
            QPushButton {
                font-size: 32px;
                font-weight: bold;
                padding: 20px;
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        buttons_layout.addWidget(self.process_all_btn)
        
        main_layout.addWidget(buttons_frame)
        
        # 连接信号
        self.copy_btn.clicked.connect(self.copy_files)
        self.delete_btn.clicked.connect(self.delete_files)
        self.delete_lines_btn.clicked.connect(self.delete_lines)
        self.process_btn.clicked.connect(self.process_data)
        self.process_all_btn.clicked.connect(self.process_all)

    def browse_data_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "选择源文件夹")
        if directory:
            self.data_dir.setText(directory)
            
    def browse_copy_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "选择备份文件夹")
        if directory:
            self.copy_dir.setText(directory)
            
    def get_processor(self):
        return FileProcessor(self.data_dir.text(), self.copy_dir.text())
    
    def copy_files(self):
        try:
            processor = self.get_processor()
            processor.copy_files()
            QMessageBox.information(self, "成功", "文件复制完成")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
            
    def delete_files(self):
        try:
            processor = self.get_processor()
            processor.delete_files(self.endwith.text())
            QMessageBox.information(self, "成功", "文件删除完成")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
            
    def delete_lines(self):
        try:
            processor = self.get_processor()
            processor.delete_lines(int(self.line_num.text()))
            QMessageBox.information(self, "成功", "行删除完成")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
            
    def process_data(self):
        try:
            processor = self.get_processor()
            processor.process_date()
            QMessageBox.information(self, "成功", "数据处理完成")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def process_all(self):
        try:
            self.copy_files()
            self.delete_files()
            self.delete_lines()
            self.process_data()
            
            QMessageBox.information(self, "成功", "所有操作已完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

if __name__ == '__main__':
    app = QApplication([])
    window = FileProcessorGUI()
    window.show()
    app.exec() 