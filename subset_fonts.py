import subprocess, os, sys

fonts_dir = r'c:\冬\项目\文本展示\fonts'
common_chars = open(os.path.join(fonts_dir, 'common-chars.txt'), 'r', encoding='utf-8').read().strip()

seen = set()
unicode_list = []
for ch in common_chars:
    cp = ord(ch)
    if cp not in seen:
        seen.add(cp)
        unicode_list.append(f'U+{cp:04X}')

unicodes_str = ','.join(unicode_list)

text_file = os.path.join(fonts_dir, 'subset_text.txt')
with open(text_file, 'w', encoding='utf-8') as f:
    f.write(common_chars)

configs = [
    ('HYZhengYuan', 'HYZhengYuan-45W.ttf', 'hyzhengyuan'),
    ('JingHuaOldSong', '京華老宋体-LT原版鉛字字形.ttf', 'jinghuaoldsong'),
    ('HuiWenMingChao', '汇文明朝体.ttf', 'huiwenmingchao')
]

for name, input_file, output_dir in configs:
    input_path = os.path.join(fonts_dir, input_file)
    out_dir = os.path.join(fonts_dir, output_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    print(f'Processing {name}...')
    try:
        result = subprocess.run([
            sys.executable, '-m', 'fontTools.subset',
            '--output-file=' + os.path.join(out_dir, f'{name}-subset.woff2'),
            '--flavor=woff2',
            '--text-file=' + text_file,
            '--layout-features=*',
            input_path
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f'  STDERR: {result.stderr[:500]}')
            raise Exception(f'fonttools returned {result.returncode}')
        
        css_content = f"""@font-face {{
    font-family: '{name}';
    src: url('{name}-subset.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}}
"""
        with open(os.path.join(out_dir, 'result.css'), 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        woff2_path = os.path.join(out_dir, f'{name}-subset.woff2')
        size_kb = os.path.getsize(woff2_path) / 1024
        print(f'  Done: {out_dir} ({size_kb:.1f} KB)')
    except Exception as e:
        print(f'  Error: {e}')

print('All fonts processed.')
