import fitz
from PIL import Image
import numpy as np
import os
import re


def analyze_pdf(local_pdf_path):
    # 处理文件的双引号
    if re.match(r'^".*"$', local_pdf_path):
        local_pdf_path = local_pdf_path[1:-1]  # 去除第一个和最后一个字符，即双引号

    # 检查文件是否存在
    if not os.path.isfile(local_pdf_path):
        print("File not found at the specified path.")
        return

    # 初始化变量
    colored_page_count = 0
    black_count = 0
    total_count = 0

    # 打开PDF文件
    with fitz.open(local_pdf_path) as doc:
        # 遍历PDF中的每个页面
        for page_number, page in enumerate(doc, start=1):
            # 渲染页面到图像
            pix = page.get_pixmap(alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # 将图像转换为NumPy数组
            arr = np.array(img)
            arr_mean = np.mean(arr, axis=(0, 1))

            # 判断页面是彩色还是黑白
            if np.all(arr_mean[0] == arr_mean[1] == arr_mean[2]):
                black_count += 1
                total_count += 1
            else:
                colored_page_count += 1
                total_count += 1

    # 打印彩色页面和黑白页面的数量
    print(f"页数总计：{total_count}")
    print(f"彩色页数: {colored_page_count}")
    print(f"黑白页数: {black_count}")


# 主程序入口
if __name__ == "__main__":
    # 用户输入本地PDF文件路径
    while True:
        local_pdf_path = input("请输入一个文件地址，使用exit以退出：\n ")
        if local_pdf_path.lower() == 'exit':
            break
        else:
            # 调用analyze_pdf函数处理用户输入的文件路径
            analyze_pdf(local_pdf_path)
        
