#!/bin/bash

# 给定目录路径，如果没有传递参数，则默认为当前目录
directory="${1:-.}"

# 使用 find 命令遍历目录及所有子目录下的 .jpg, .mov, .mp4 文件
find "$directory" -type f \( -iname "*.jpg" -o -iname "*.mov" -o -iname "*.mp4" \) | while read file; do
    # 检查文件名是否符合第一种格式（MYXJ_20191228185255781_fast.jpg, .mov, .mp4）
    if [[ "$file" =~ MYXJ_([0-9]{8})([0-9]{6}) ]]; then
        # 提取日期和时间
        date="${BASH_REMATCH[1]}"
        time="${BASH_REMATCH[2]}"
        # 格式化为 EXIF 日期时间格式 (YYYY:MM:DD HH:MM:SS)
        datetime="${date:0:4}:${date:4:2}:${date:6:2} ${time:0:2}:${time:2:2}:${time:4:2}"
        # 使用 exiftool 更新 EXIF 时间
        exiftool -overwrite_original "-FileModifyDate=2025:01:01 00:00:00" -datetimeoriginal="$datetime" "$file"
        echo "Updated EXIF time for $file to $datetime"
    
    # 检查文件名是否符合第二种格式（mmexport1585052795748.jpg, .mov, .mp4）
    elif [[ "$file" =~ mmexport([0-9]{13}) ]]; then
	# 提取 Unix 毫秒时间戳
        timestamp="${BASH_REMATCH[1]}"
        # 将时间戳转换为秒级时间戳，并确保不会以科学计数法输出
        timestamp_sec=$(echo "$timestamp" | awk '{printf "%.0f", $1/1000}')
        # 使用 date 将秒级时间戳转换为标准日期时间格式
        datetime=$(date -d @$timestamp_sec "+%Y:%m:%d %H:%M:%S")
        exiftool -overwrite_original "-FileModifyDate=2025:01:01 00:00:00" -datetimeoriginal="$datetime" "$file"
        echo "Updated EXIF time for $file to $datetime"
    fi
done

