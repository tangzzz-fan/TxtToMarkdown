#!/bin/bash

# 显示帮助信息的函数
show_help() {
    echo "用法: $0 [目录路径]"
    echo "将指定目录(默认为当前目录)下的所有 .md 文件重命名为 .txt"
    echo ""
    echo "选项:"
    echo "  -h, --help    显示此帮助信息"
}

# 处理命令行参数
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# 设置工作目录
WORK_DIR="${1:-.}"

# 确认是否继续
echo "即将在目录 '$WORK_DIR' 中将所有 .md 文件重命名为 .txt"
read -p "是否继续? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "操作已取消"
    exit 1
fi

# 计数器
converted=0
errors=0

# 递归查找并重命名文件
find "$WORK_DIR" -type f -name "*.md" | while read -r file; do
    new_name="${file%.md}.txt"
    if mv "$file" "$new_name" 2>/dev/null; then
        echo "✓ 已重命名: $file -> $new_name"
        ((converted++))
    else
        echo "✗ 重命名失败: $file"
        ((errors++))
    fi
done

# 输出统计信息
echo ""
echo "完成! 统计信息:"
echo "- 成功转换: $converted 个文件"
echo "- 失败: $errors 个文件"

if [ $errors -gt 0 ]; then
    exit 1
fi 