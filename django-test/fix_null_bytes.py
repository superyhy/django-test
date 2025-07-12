import os

def remove_null_bytes_from_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    if b'\x00' in content:
        print(f"[!] Null byte found and cleaned in: {file_path}")
        content = content.replace(b'\x00', b'')
        with open(file_path, 'wb') as f:
            f.write(content)

def scan_and_fix_null_bytes(base_dir):
    print(f"🔍 Scanning Python files under: {base_dir}\n")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                remove_null_bytes_from_file(file_path)

if __name__ == '__main__':
    # 当前脚本所在目录作为根目录开始扫描
    base_directory = os.path.dirname(os.path.abspath(__file__))
    scan_and_fix_null_bytes(base_directory)
    print("\n✅ Done. You may now re-run your Django project.")
