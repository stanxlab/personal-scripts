#!/bin/bash

# 配置参数
volume_size="2G"                # 分卷大小（如100m、1g）
password=`cat ~/zip_password.txt`          # 加密密码（替换为实际密码）

log_file="/var/log/zip_backup.log"             # 日志文件


# 记录开始时间
echo "===== Backup Started: $(date) =====" >> "$log_file"

# 定义子方法：压缩以数字开头的子目录
compress_dir() {
    dir="$1"
    backup_dir="$2"
    echo "process: $dir ======= $backup_dir"
    echo ""

    # 检查是否存在匹配的目录
    if [ ! -d "$dir" ]; then
        echo "No directories starting with a number found." >> "$log_file"
        return
    fi

    # 去掉目录名末尾的斜杠
    dir_name=$(basename "$dir")

    # 设置备份文件名
    backup_file="${backup_dir}/${dir_name}.7z"

    # 执行7z加密分卷压缩
    echo "Compressing directory: $dir_name" >> "$log_file"
    7z a -v${volume_size} -mhe=on -p"${password}" "${backup_file}" "${dir}" >> "$log_file" 2>&1

    # 检查执行状态
    if [ $? -eq 0 ]; then
        echo "Success: $dir_name compressed at $(date)" >> "$log_file"
    else
        echo "Error: Failed to compress $dir_name at $(date)" >> "$log_file"
    fi
}

# 遍历以数字开头的子目录
for dir in /vol2/1000/Photos/[0-9]*/; do
    # 调用子方法
    compress_dir "$dir" "/vol2/1000/Read2BaiduPan"
done

# 遍历手机备份的子目录
for dir in /vol2/1000/Photos/Stan_iphone/[0-9]*/; do
    # 调用子方法
    compress_dir "$dir" "/vol2/1000/Read2BaiduPan/Stan_iphone"
done

for dir in /vol2/1000/Photos/Echo_iphone/[0-9]*/; do
    # 调用子方法
    compress_dir "$dir" "/vol2/1000/Read2BaiduPan/Echo_iphone"
done

# 记录结束时间
echo "===== Backup Completed: $(date) =====" >> "$log_file"
