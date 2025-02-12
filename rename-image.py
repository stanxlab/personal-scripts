import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_photo_date_taken(image_path):
    """
    获取照片的拍摄日期（从EXIF信息中提取）
    如果照片没有EXIF信息，则返回None
    """
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':  # 查找拍摄日期
                    return value
    except Exception as e:
        print(f"无法获取 {image_path} 的EXIF数据: {e}")
    return None

def rename_photos_in_directory(directory):
    """
    批量修改目录中的照片文件名为拍摄日期
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # 仅处理图片文件
        if os.path.isfile(file_path) and filename.lower().endswith(('jpg', 'jpeg', 'png', 'heic')):
            date_taken = get_photo_date_taken(file_path)

            if date_taken:
                try:
                    # 将日期格式化为 YYYY-MM-DD_HH-MM-SS 格式
                    date_taken = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
                    new_filename = date_taken.strftime('%Y-%m-%d_%H-%M-%S') + os.path.splitext(filename)[1]

                    new_file_path = os.path.join(directory, new_filename)

                    # 避免重命名为已经存在的文件
                    if not os.path.exists(new_file_path):
                        os.rename(file_path, new_file_path)
                        print(f"文件 {filename} 已重命名为 {new_filename}")
                    else:
                        print(f"文件 {new_filename} 已存在，跳过重命名")
                except Exception as e:
                    print(f"处理 {filename} 时出错: {e}")
            else:
                print(f"无法获取 {filename} 的拍摄日期，跳过此文件")
        else:
            print(f"{filename} 不是有效的图片文件，跳过")

# 设置你想要批量处理的目录路径
directory_path = '/root/tmp'
rename_photos_in_directory(directory_path)

