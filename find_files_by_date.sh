
#!/bin/bash

# 给定目录路径，如果没有传递参数，则默认为当前目录
directory="${1:-.}"

# 使用 find 命令遍历目录及所有子目录下的 .jpg, .mov, .mp4 文件
find "$directory" -type f \( -iname "*.jpg" -o -iname "*.mov" -o -iname "*.mp4" \) | while read file; do
    # 使用 exiftool 获取 FileModifyDate 信息
    file_modify_date=$(exiftool -q -FileModifyDate -d "%Y:%m:%d" "$file" | awk -F': ' '{print $2}')
    
    # 检查文件是否缺少 DateTimeOriginal 时间
    datetime_original=$(exiftool -q -DateTimeOriginal "$file" | awk -F': ' '{print $2}')

    # 判断条件：FileModifyDate 为 2025:02:11 且没有 DateTimeOriginal
    if [[ "$file_modify_date" == "2025:02:10" && -z "$datetime_original" ]]; then
        # 输出文件名
        realpath "$file"
    fi
done

