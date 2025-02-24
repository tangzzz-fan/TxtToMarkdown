#!/bin/bash

# 将当前目录下所有 .md 文件重命名为 .txt
for file in *.md; do
    if [ -f "$file" ]; then
        mv "$file" "${file%.md}.txt"
        echo "Renamed: $file -> ${file%.md}.txt"
    fi
done 