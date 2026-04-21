import subprocess, os, sys

fonts_dir = r'c:\冬\项目\文本展示\fonts'
common_chars = open(os.path.join(fonts_dir, 'common-chars.txt'), 'r', encoding='utf-8').read().strip()

text_file = os.path.join(fonts_dir, 'subset_text.txt')
with open(text_file, 'w', encoding='utf-8') as f:
    f.write(common_chars)

input_path = os.path.join(fonts_dir, '汇文明朝体.ttf')
out_dir = os.path.join(fonts_dir, 'huiwenmingchao')
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

print('Processing HuiWenMingChao...')
try:
    result = subprocess.run([
        sys.executable, '-m', 'fontTools.subset',
        '--output-file=' + os.path.join(out_dir, 'HuiWenMingChao-subset.woff2'),
        '--flavor=woff2',
        '--text-file=' + text_file,
        input_path
    ], capture_output=True, text=True)
    
    print(f'  Return code: {result.returncode}')
    if result.stderr:
        print(f'  STDERR: {result.stderr[:2000]}')
    if result.returncode == 0:
        size_kb = os.path.getsize(os.path.join(out_dir, 'HuiWenMingChao-subset.woff2')) / 1024
        print(f'  Done: {size_kb:.1f} KB')
except Exception as e:
    print(f'  Error: {e}')
