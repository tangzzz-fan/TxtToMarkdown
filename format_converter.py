import re
import os

class FormatConverter:
    def __init__(self):
        self.link_pattern = re.compile(r'\{(.*?)\}\|(.*?)(?:\s|$)')
        self.image_pattern = re.compile(r'!\{(.*?)\}\|(.*?)(?:\s|$)')
    
    def convert_links(self, line):
        """转换链接格式 {text}|{url} 为 [text](url)"""
        return self.link_pattern.sub(r'[\1](\2)', line)
    
    def convert_images(self, line):
        """转换图片格式 !{alt}|{url} 为 ![alt](url)"""
        return self.image_pattern.sub(r'![\1](\2)', line)
    
    def process_line(self, line):
        """处理单行文本"""
        # 移除文件头和分隔线
        if '=' * 16 in line or line.endswith('.txt'):
            return ''
            
        # 处理标题的分隔线
        if line.strip() and all(c == '-' for c in line.strip()):
            return ''
            
        # 转换列表符号
        if line.strip().startswith('•'):
            line = line.replace('•', '*', 1)
            
        # 转换链接和图片
        line = self.convert_links(line)
        line = self.convert_images(line)
        
        # 处理转义字符
        line = line.replace('\\#', '#')
        line = line.replace('\\*', '*')
        line = line.replace('\\\\', '\\')
        
        return line

    def convert_file(self, input_path, output_path=None):
        """转换整个文件"""
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + '.md'
            
        with open(input_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
            
        processed_lines = []
        skip_next_line = False
        
        for i, line in enumerate(lines):
            if skip_next_line:
                skip_next_line = False
                continue
                
            # 处理当前行
            processed_line = self.process_line(line)
            
            # 如果不是空行，添加到结果中
            if processed_line.strip():
                processed_lines.append(processed_line)
            # 保留段落之间的空行
            elif i > 0 and i < len(lines) - 1 and lines[i-1].strip() and lines[i+1].strip():
                processed_lines.append('\n')
                
        # 写入新文件
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(''.join(processed_lines))
            
        return output_path

def main():
    converter = FormatConverter()
    
    # 获取当前目录下所有的 .txt 文件
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    for txt_file in txt_files:
        try:
            output_file = converter.convert_file(txt_file)
            print(f'Successfully converted {txt_file} to {output_file}')
        except Exception as e:
            print(f'Error converting {txt_file}: {str(e)}')

if __name__ == '__main__':
    main() 