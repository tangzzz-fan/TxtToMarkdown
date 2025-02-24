import re
import os

class CustomFormatConverter:
    def __init__(self):
        self.rules = {
            # 标题转换
            r'@h1:\s*(.+)': r'# \1',
            r'@h2:\s*(.+)': r'## \1',
            r'@h3:\s*(.+)': r'### \1',
            r'@h4:\s*(.+)': r'#### \1',
            
            # 列表转换
            r'^==>\s*(.+)': r'* \1',
            
            # 文本样式转换
            r'<<(.+?)>>': r'**\1**',
            r'/(.+?)/' : r'*\1*',
            r'~(.+?)~': r'~~\1~~',
            
            # 链接和图片转换
            r'\[\[(.+?)>>(.+?)\]\]': r'[\1](\2)',
            r'\{\{(.+?)>>(.+?)\}\}': r'![\1](\2)',
            
            # 引用转换
            r'>>>\s*(.+)': r'> \1',
            
            # 代码块转换
            r'%code\s+(.+?)%([\s\S]+?)%end%': r'```\1\n\2\n```',
            
            # 表格转换
            r'\$table([\s\S]+?)\$end': lambda m: self._convert_table(m.group(1)),
        }
    
    def _convert_table(self, table_content):
        rows = re.findall(r'\$row\s+(.+)', table_content)
        if not rows:
            return ''
        
        markdown_table = []
        # 添加表头
        markdown_table.append(rows[0])
        # 添加分隔行
        separator = '|'.join(['---' for _ in rows[0].split('|')])
        markdown_table.append(separator)
        # 添加数据行
        markdown_table.extend(rows[1:])
        
        return '\n'.join(markdown_table)
    
    def convert(self, text):
        # 移除文件头
        text = re.sub(r'^.+\n=+\n', '', text)
        
        # 应用所有转换规则
        for pattern, replacement in self.rules.items():
            if callable(replacement):
                text = re.sub(pattern, replacement, text)
            else:
                text = re.sub(pattern, replacement, text)
        
        return text

def main():
    converter = CustomFormatConverter()
    
    # 获取当前目录下所有的 .txt 文件
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as infile:
                text = infile.read()
            
            converted_text = converter.convert(text)
            
            output_file = os.path.splitext(txt_file)[0] + '.md'
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(converted_text)
            
            print(f'Successfully converted {txt_file} to {output_file}')
        except Exception as e:
            print(f'Error converting {txt_file}: {str(e)}')

if __name__ == '__main__':
    main() 