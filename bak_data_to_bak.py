import shutil

src_dir = 'data'  # 源文件夹路径
dst_dir = 'bak'   # 目标文件夹路径

try:
    shutil.copytree(src_dir, dst_dir)
    print(f'备份成功：{src_dir} -> {dst_dir}')
except FileExistsError:
    shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)
    print(f'覆盖备份成功：{src_dir} -> {dst_dir}')