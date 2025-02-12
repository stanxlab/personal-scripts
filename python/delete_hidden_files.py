import os
import argparse

def delete_small_hidden_files(root_dir):
    # 遍历目录及其所有子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # 构造文件的完整路径
            file_path = os.path.join(dirpath, filename)
            
            # 检查文件是否是以 . 开头且文件大小小于 10KB
            if filename.startswith('.'):
                size = os.path.getsize(file_path)
                if size > 10 * 1024:
                    print(f"隐藏文件，过大，不删除: {file_path}")
                    pass
                  
                try:
                    # 删除文件
                    os.remove(file_path)
                    print(f"Deleted: {file_path}, size: {size / 1024}k")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    # 使用 argparse 处理命令行参数
    parser = argparse.ArgumentParser(description="Delete hidden files smaller than 10KB")
    parser.add_argument("directory", help="The root directory to start the search")
    
    args = parser.parse_args()

    # 获取传入的目录路径并调用函数
    root_directory = args.directory
    if os.path.isdir(root_directory):
        delete_small_hidden_files(root_directory)
    else:
        print(f"The directory '{root_directory}' is not valid.")


