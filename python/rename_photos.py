import os
import re
import sys
import datetime
import piexif
import subprocess
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

# 注册 HEIC 格式支持
register_heif_opener()

# 允许处理的文件扩展名（小写）
ALLOWED_EXTENSIONS = {
    '.heic', '.heif', '.jpg', '.jpeg', '.png',
    '.mov', '.mp4', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp'
}

def get_photo_datetime(file_path, directory):
    """获取文件的拍摄时间，优先读取元数据，若失败则使用文件创建时间"""
    file_ext = file_path.suffix.lower()
    
    # 处理图片的 EXIF 信息
    if file_ext in {'.heic', '.heif', '.jpg', '.jpeg', '.png'}:
        try:
            img = Image.open(file_path)
            exif_dict = piexif.load(img.info["exif"])
            date_str = exif_dict["0th"][piexif.ImageIFD.DateTime].decode("utf-8")
            if date_str.startswith('0000'):
                print(f"⚠️ 无法获取拍摄时间-0000，跳过: {file_path.relative_to(directory)}")
                return None
            return datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
        except Exception:
            pass  # EXIF 读取失败，继续尝试其他方法
    
    # 处理视频的元数据（使用 exiftool）
    elif file_ext in {'.mov', '.mp4', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp'}:
        try:
            # 尝试读取 CreateDate
            result = subprocess.run(
                ['exiftool', '-CreateDate', '-d', '%Y:%m:%d %H:%M:%S', '-s3', str(file_path)],
                capture_output=True, text=True, check=True
            )
            if date_str := result.stdout.strip():
                if date_str.startswith('0000'):
                    print(f"⚠️ 无法获取拍摄时间-0000，跳过: {file_path.relative_to(directory)}")
                    return None
                return datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            
            # 尝试读取 MediaCreateDate
            result = subprocess.run(
                ['exiftool', '-MediaCreateDate', '-d', '%Y:%m:%d %H:%M:%S', '-s3', str(file_path)],
                capture_output=True, text=True, check=True
            )
            if date_str := result.stdout.strip():
                if date_str.startswith('0000'):
                    print(f"⚠️ 无法获取拍摄时间-0000，跳过: {file_path.relative_to(directory)}")
                    return None
                return datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass  # exiftool 调用失败或未安装，回退到文件时间
    
    # 使用文件创建时间作为回退方案
    #try:
    #    file_stat = file_path.stat()
    #    return datetime.datetime.fromtimestamp(file_stat.st_ctime)
    #except Exception:
    print(f"⚠️ 未获取到拍摄时间，跳过: {file_path.relative_to(directory)}")
    return None

def rename_files(directory):
    """递归查找并重命名所有符合规则的文件"""
    directory_path = Path(directory)
    if not directory_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        return

    no_time_index = 0
    for file_path in directory_path.rglob('*'):
        if not file_path.is_file():
            continue

        # 检查文件扩展名是否允许
        file_ext = file_path.suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            continue

        # 匹配文件名模式（IMG_四位数字开头）
        stem = file_path.stem
        match = re.match(r"^IMG_(\d{4})$", stem, re.IGNORECASE)
        if not match:
            continue
        num_part = match.group(1)

        # 获取拍摄时间
        photo_datetime = get_photo_datetime(file_path, directory)
        if not photo_datetime:
            print(f"⚠️ 无法获取拍摄时间，跳过: {file_path.relative_to(directory)}")
            no_time_index += 1
            new_name = f"IMG_{num_part}.{no_time_index}{file_ext}"
            new_path = file_path.parent / new_name
        else:
            # 构造新文件名
            new_name = f"{photo_datetime.strftime('%Y%m%d_%H%M%S')}_{num_part}{file_ext}"
            new_path = file_path.parent / new_name

        # 处理文件名冲突
        counter = 1
        while new_path.exists():
            base, ext = os.path.splitext(new_name)
            new_name = f"{base}_{counter}{ext}"
            new_path = file_path.parent / new_name
            counter += 1

        # 执行重命名
        try:
            file_path.rename(new_path)
            print(f"✅ 已重命名: {file_path.relative_to(directory)} -> {new_path.name}")
        except Exception as e:
            print(f"❌ 重命名失败 {file_path.relative_to(directory)}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ 请输入要处理的目录路径！\n示例：python rename_heic.py /path/to/directory")
        sys.exit(1)
    rename_files(sys.argv[1])
