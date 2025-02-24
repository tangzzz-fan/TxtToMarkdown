import re
import os

class MarkdownToTxtConverter:
    def __init__(self):
        self.link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
        self.image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

    def convert_links(self, line):
        """转换 Markdown 链接 [text](url) 为 {text}|{url}"""
        return self.link_pattern.sub(r'{\1}|\2', line)

    def convert_images(self, line):
        """转换 Markdown 图片 ![alt](url) 为 !{alt}|{url}"""
        return self.image_pattern.sub(r'!{\1}|\2', line)

    def add_section_separator(self, title_level):
        """根据标题级别添加分隔线"""
        return '-' * (10 + title_level)

    def process_line(self, line):
        """处理单行文本"""
        line = line.rstrip()
        
        # 转换链接和图片
        line = self.convert_links(line)
        line = self.convert_images(line)

        # 处理标题
        if line.startswith('#'):
            title_level = len(re.match(r'^#+', line).group())
            return f"\n{line}\n{self.add_section_separator(title_level)}\n"

        # 处理列表项
        if line.strip().startswith('*'):
            # 计算缩进级别
            indent = len(line) - len(line.lstrip())
            # 将 * 转换为 •
            line = ' ' * indent + '•' + line.lstrip()[1:]

        # 处理引用块
        if line.startswith('>'):
            return line

        # 处理需要转义的字符
        line = line.replace('#', '\\#')
        line = line.replace('*', '\\*')
        line = line.replace('\\', '\\\\')

        return line

    def convert_file(self, input_path, output_path=None):
        """转换整个文件"""
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + '.txt'

        # 获取文件名用于头部
        filename = os.path.basename(output_path)
        
        with open(input_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        processed_lines = [
            f"{filename}\n",
            "=" * 16 + "\n"
        ]

        for line in lines:
            processed_line = self.process_line(line)
            if processed_line:
                processed_lines.append(processed_line + '\n')

        # 写入新文件
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(processed_lines)

        return output_path

def main():
    converter = MarkdownToTxtConverter()
    
    # 获取当前目录下所有的 .md 文件
    md_files = [f for f in os.listdir('.') if f.endswith('.md')]
    
    for md_file in md_files:
        try:
            output_file = converter.convert_file(md_file)
            print(f'Successfully converted {md_file} to {output_file}')
        except Exception as e:
            print(f'Error converting {md_file}: {str(e)}')

if __name__ == '__main__':
    main() 