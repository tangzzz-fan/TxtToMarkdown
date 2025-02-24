#!/bin/bash

# 将当前目录下所有 .txt 文件重命名为 .md
for file in *.txt; do
    if [ -f "$file" ]; then
        mv "$file" "${file%.txt}.md"
        echo "Renamed: $file -> ${file%.txt}.md"
    fi
done 