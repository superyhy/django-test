import os

def clean_null_bytes(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'rb') as f:
                    content = f.read()
                    if b'\x00' in content:
                        print(f"[!] Cleaning null byte from: {path}")
                        new_content = content.replace(b'\x00', b'')
                        with open(path, 'wb') as f2:
                            f2.write(new_content)

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    clean_null_bytes(base)
    print("✅ Cleaned all files containing null bytes.")