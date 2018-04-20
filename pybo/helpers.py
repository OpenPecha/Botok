def open_file(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, mode='r', encoding='utf-16-le') as f:
            return f.read()
