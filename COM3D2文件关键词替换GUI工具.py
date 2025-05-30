import os
import sys
import json
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import re
from pathlib import Path


class FileKeywordReplacer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("文件关键词替换工具")
        self.geometry("900x700")
        
        # 设置变量
        self.folder_path = tk.StringVar()
        self.meido_path = tk.StringVar()
        self.search_keyword = tk.StringVar()
        self.replace_keyword = tk.StringVar()
        self.file_pattern = tk.StringVar(value="*.*")
        self.file_search_keyword = tk.StringVar()
        self.file_replace_keyword = tk.StringVar()
        self.recursive_var = tk.BooleanVar(value=True)
        self.file_types = tk.StringVar()
        self.delete_json_var = tk.BooleanVar(value=True)
        
        # 初始化界面
        self._init_ui()
        
    def _init_ui(self):
        """初始化用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建选项卡
        tab_control = ttk.Notebook(main_frame)
        
        # 文件内容替换选项卡
        content_tab = ttk.Frame(tab_control)
        tab_control.add(content_tab, text="文件内容替换")
        
        # 文件名替换选项卡
        filename_tab = ttk.Frame(tab_control)
        tab_control.add(filename_tab, text="文件名替换")
        
        tab_control.pack(expand=True, fill=tk.BOTH)
        
        # 设置文件内容替换选项卡
        self._setup_content_tab(content_tab)
        
        # 设置文件名替换选项卡
        self._setup_filename_tab(filename_tab)
        
    def _setup_content_tab(self, parent):
        """设置文件内容替换选项卡"""
        # 文件夹选择部分
        folder_frame = ttk.LabelFrame(parent, text="文件夹设置", padding="10")
        folder_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(folder_frame, text="选择文件夹:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(folder_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(folder_frame, text="浏览...", command=self._browse_folder).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(folder_frame, text="MeidoSerialization路径:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(folder_frame, textvariable=self.meido_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(folder_frame, text="浏览...", command=self._browse_meido).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(folder_frame, text="文件类型 (逗号分隔):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(folder_frame, textvariable=self.file_types, width=50).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(folder_frame, text="例如: menu,mate,tex").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        
        ttk.Checkbutton(folder_frame, text="包含子文件夹", variable=self.recursive_var).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(folder_frame, text="处理完成后删除 JSON 文件", variable=self.delete_json_var).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 关键词替换部分
        keyword_frame = ttk.LabelFrame(parent, text="关键词替换", padding="10")
        keyword_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(keyword_frame, text="查找关键词:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(keyword_frame, textvariable=self.search_keyword, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(keyword_frame, text="替换为:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(keyword_frame, textvariable=self.replace_keyword, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # 操作按钮
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(button_frame, text="开始替换", command=self._start_content_replacement).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="预览文件", command=self._preview_files).pack(side=tk.RIGHT, padx=5)
        
        # 日志输出
        log_frame = ttk.LabelFrame(parent, text="处理日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=80, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def _setup_filename_tab(self, parent):
        """设置文件名替换选项卡"""
        # 文件夹选择部分
        folder_frame = ttk.LabelFrame(parent, text="文件夹设置", padding="10")
        folder_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(folder_frame, text="选择文件夹:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(folder_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(folder_frame, text="浏览...", command=self._browse_folder).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(folder_frame, text="文件名模式:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(folder_frame, textvariable=self.file_pattern, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(folder_frame, text="例如: *.txt, *.menu").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        ttk.Checkbutton(folder_frame, text="包含子文件夹", variable=self.recursive_var).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        
        # 关键词替换部分
        keyword_frame = ttk.LabelFrame(parent, text="文件名关键词替换", padding="10")
        keyword_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(keyword_frame, text="查找关键词:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(keyword_frame, textvariable=self.file_search_keyword, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(keyword_frame, text="替换为:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(keyword_frame, textvariable=self.file_replace_keyword, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # 操作按钮
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(button_frame, text="开始替换文件名", command=self._start_filename_replacement).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="预览匹配文件", command=self._preview_filename_matches).pack(side=tk.RIGHT, padx=5)
        
        # 日志输出
        log_frame = ttk.LabelFrame(parent, text="处理日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.filename_log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=80, height=15)
        self.filename_log_text.pack(fill=tk.BOTH, expand=True)
    
    def _browse_folder(self):
        """浏览并选择文件夹"""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
    
    def _browse_meido(self):
        """浏览并选择MeidoSerialization程序"""
        file_path = filedialog.askopenfilename(filetypes=[("可执行文件", "*.exe")])
        if file_path:
            self.meido_path.set(file_path)
    
    def _log(self, message, log_widget=None):
        """添加日志信息"""
        if log_widget is None:
            log_widget = self.log_text
            
        log_widget.insert(tk.END, message + "\n")
        log_widget.see(tk.END)
        log_widget.update()
    
    def _find_files(self, directory, recursive=True, file_types=None):
        """查找匹配的文件"""
        files = []
        if file_types:
            type_list = [t.strip() for t in file_types.split(",")]
        else:
            type_list = []
            
        # 遍历指定的目录
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                # 跳过JSON文件
                if filename.endswith('.json'):
                    continue
                
                # 如果指定了文件类型，则筛选
                if type_list:
                    file_ext = os.path.splitext(filename)[1].lstrip('.')
                    if file_ext not in type_list:
                        continue
                        
                files.append(os.path.join(root, filename))
                
            # 如果不递归，则跳出循环
            if not recursive:
                break
                
        return files
    
    def _find_files_by_pattern(self, directory, pattern="*.*", recursive=True):
        """使用模式查找匹配的文件"""
        files = []
        # 遍历指定的目录
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                # 使用fnmatch来匹配模式
                if self._match_pattern(filename, pattern):
                    files.append(os.path.join(root, filename))
                
            # 如果不递归，则跳出循环
            if not recursive:
                break
                
        return files
    
    def _match_pattern(self, filename, pattern):
        """匹配文件名模式，支持*, ?等通配符"""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def _preview_files(self):
        """预览匹配的文件"""
        folder = self.folder_path.get().strip()
        if not folder:
            messagebox.showerror("错误", "请选择文件夹")
            return
            
        file_types = self.file_types.get().strip()
        recursive = self.recursive_var.get()
        
        self.log_text.delete(1.0, tk.END)
        self._log("正在查找匹配的文件...")
        
        files = self._find_files(folder, recursive, file_types)
        
        self._log(f"找到 {len(files)} 个匹配的文件:")
        for file in files:
            self._log(f"- {file}")
    
    def _preview_filename_matches(self):
        """预览匹配文件名的文件"""
        folder = self.folder_path.get().strip()
        if not folder:
            messagebox.showerror("错误", "请选择文件夹")
            return
            
        pattern = self.file_pattern.get().strip()
        recursive = self.recursive_var.get()
        
        self.filename_log_text.delete(1.0, tk.END)
        self._log("正在查找匹配的文件...", self.filename_log_text)
        
        files = self._find_files_by_pattern(folder, pattern, recursive)
        
        self._log(f"找到 {len(files)} 个匹配的文件:", self.filename_log_text)
        for file in files:
            self._log(f"- {file}", self.filename_log_text)
            
        search_keyword = self.file_search_keyword.get().strip()
        if search_keyword:
            self._log("\n包含关键词的文件:", self.filename_log_text)
            matching_files = [f for f in files if search_keyword in os.path.basename(f)]
            self._log(f"找到 {len(matching_files)} 个包含关键词 '{search_keyword}' 的文件:", self.filename_log_text)
            for file in matching_files:
                self._log(f"- {file}", self.filename_log_text)
                new_name = os.path.basename(file).replace(search_keyword, self.file_replace_keyword.get().strip())
                self._log(f"  将重命名为: {new_name}", self.filename_log_text)
    
    def _convert_to_json(self, file_path, meido_path):
        """使用MeidoSerialization将文件转换为JSON"""
        try:
            # 构建命令
            cmd = [meido_path, "convert2json", file_path]
            
            # 执行命令
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self._log(f"转换失败: {stderr.decode('utf-8', errors='ignore')}")
                return None
                
            # 返回JSON文件路径
            return f"{file_path}.json"
        except Exception as e:
            self._log(f"转换过程发生错误: {str(e)}")
            return None
    
    def _convert_to_mod(self, json_file_path, meido_path):
        """使用MeidoSerialization将JSON转回原格式"""
        try:
            # 构建命令
            cmd = [meido_path, "convert2mod", json_file_path]
            
            # 执行命令
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self._log(f"转换回原格式失败: {stderr.decode('utf-8', errors='ignore')}")
                return False
                
            return True
        except Exception as e:
            self._log(f"转换回原格式过程发生错误: {str(e)}")
            return False
    
    def _replace_keywords_in_json(self, json_file_path, search_keyword, replace_keyword):
        """在JSON文件中替换关键词"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 替换关键词
            modified_content = content.replace(search_keyword, replace_keyword)
            
            # 检查是否有变化
            if content == modified_content:
                return False
                
            # 写入修改后的内容
            with open(json_file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            return True
        except Exception as e:
            self._log(f"替换关键词时发生错误: {str(e)}")
            return False
    
    def _start_content_replacement(self):
        """开始替换文件内容关键词的处理"""
        folder = self.folder_path.get().strip()
        meido_path = self.meido_path.get().strip()
        search_keyword = self.search_keyword.get().strip()
        replace_keyword = self.replace_keyword.get().strip()
        file_types = self.file_types.get().strip()
        recursive = self.recursive_var.get()
        delete_json = self.delete_json_var.get()
        
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("错误", "请选择有效的文件夹")
            return
            
        if not meido_path or not os.path.isfile(meido_path):
            messagebox.showerror("错误", "请选择有效的MeidoSerialization程序")
            return
            
        if not search_keyword:
            messagebox.showerror("错误", "请输入要查找的关键词")
            return
            
        # 清空日志
        self.log_text.delete(1.0, tk.END)
            
        # 在后台线程中运行，避免界面冻结
        threading.Thread(target=self._process_files_replacement, 
                         args=(folder, meido_path, search_keyword, replace_keyword, 
                              file_types, recursive, delete_json),
                         daemon=True).start()
    
    def _process_files_replacement(self, folder, meido_path, search_keyword, replace_keyword, 
                                 file_types, recursive, delete_json):
        """处理文件替换的主要逻辑"""
        self._log("开始处理文件...")
        
        # 查找匹配的文件
        files = self._find_files(folder, recursive, file_types)
        self._log(f"找到 {len(files)} 个匹配的文件")
        
        modified_count = 0
        error_count = 0
        
        for file_path in files:
            try:
                self._log(f"处理文件: {file_path}")
                
                # 转换为JSON
                json_file = self._convert_to_json(file_path, meido_path)
                if not json_file:
                    self._log(f"无法转换文件: {file_path}")
                    error_count += 1
                    continue
                    
                self._log(f"已转换为JSON: {json_file}")
                
                # 在JSON中替换关键词
                if self._replace_keywords_in_json(json_file, search_keyword, replace_keyword):
                    self._log(f"已在JSON中替换关键词")
                    
                    # 将修改后的JSON转回原格式
                    if self._convert_to_mod(json_file, meido_path):
                        self._log(f"已将修改后的JSON转回原格式")
                        modified_count += 1
                    else:
                        self._log(f"转回原格式失败")
                        error_count += 1
                else:
                    self._log(f"文件中未找到关键词")
                
                # 删除JSON文件
                if delete_json and os.path.exists(json_file):
                    os.remove(json_file)
                    self._log(f"已删除临时JSON文件")
                    
            except Exception as e:
                self._log(f"处理文件时发生错误: {str(e)}")
                error_count += 1
                
        self._log(f"\n处理完成: 共处理 {len(files)} 个文件, 修改了 {modified_count} 个文件, 发生 {error_count} 个错误")
    
    def _start_filename_replacement(self):
        """开始替换文件名的处理"""
        folder = self.folder_path.get().strip()
        pattern = self.file_pattern.get().strip()
        search_keyword = self.file_search_keyword.get().strip()
        replace_keyword = self.file_replace_keyword.get().strip()
        recursive = self.recursive_var.get()
        
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("错误", "请选择有效的文件夹")
            return
            
        if not search_keyword:
            messagebox.showerror("错误", "请输入要查找的关键词")
            return
            
        # 清空日志
        self.filename_log_text.delete(1.0, tk.END)
            
        # 在后台线程中运行，避免界面冻结
        threading.Thread(target=self._process_filename_replacement, 
                         args=(folder, pattern, search_keyword, replace_keyword, recursive),
                         daemon=True).start()
    
    def _process_filename_replacement(self, folder, pattern, search_keyword, replace_keyword, recursive):
        """处理文件名替换的主要逻辑"""
        self._log("开始处理文件名...", self.filename_log_text)
        
        # 查找匹配的文件
        files = self._find_files_by_pattern(folder, pattern, recursive)
        self._log(f"找到 {len(files)} 个匹配的文件", self.filename_log_text)
        
        renamed_count = 0
        error_count = 0
        
        for file_path in files:
            try:
                base_name = os.path.basename(file_path)
                if search_keyword in base_name:
                    new_name = base_name.replace(search_keyword, replace_keyword)
                    new_path = os.path.join(os.path.dirname(file_path), new_name)
                    
                    self._log(f"重命名文件: {file_path} -> {new_path}", self.filename_log_text)
                    
                    # 重命名文件
                    os.rename(file_path, new_path)
                    renamed_count += 1
                
            except Exception as e:
                self._log(f"重命名文件时发生错误: {str(e)}", self.filename_log_text)
                error_count += 1
                
        self._log(f"\n处理完成: 共检查 {len(files)} 个文件, 重命名了 {renamed_count} 个文件, 发生 {error_count} 个错误", self.filename_log_text)


if __name__ == "__main__":
    # 设置高DPI缩放
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
        
    app = FileKeywordReplacer()
    app.mainloop()
