import fitz
from PIL import Image
import numpy as np
import os
import re
import sys


def analyze_pdf(local_pdf_path, threshold_num=3):
    threshold_num = int(threshold_num)
    if not 0 <= threshold_num <= 5:
        print("敏感度参数应为0-5，请重新输入")
        return

    # 处理文件的双引号
    if re.match(r'^".*"$', local_pdf_path):
        local_pdf_path = local_pdf_path[1:-1]  # 去除第一个和最后一个字符，即双引号

    # 检查文件是否存在
    if not os.path.isfile(local_pdf_path):
        print("文件路径有误，请检查")
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
            # 只比较RGB的整数值
            if np.all(round(arr_mean[0], threshold_num) == round(arr_mean[1], threshold_num) == round(arr_mean[2], threshold_num)):
                black_count += 1
                total_count += 1
            else:
                colored_page_count += 1
                total_count += 1

                # 调试代码
                # print(
                #     f"第{total_count}页，RGB值为{round(arr_mean[0], threshold_num)},{round(arr_mean[1], threshold_num)},{round(arr_mean[2],threshold_num)}")

    # 打印彩色页面和黑白页面的数量
    print(f"页数总计：{total_count}")
    print(f"彩色页数: {colored_page_count}")
    print(f"黑白页数: {black_count}")
    print("--------------------------------")


# 主程序入口
if __name__ == "__main__":
    # 拖拽启动
    if len(sys.argv) > 1:
        local_pdf_path = sys.argv[1]
        analyze_pdf(local_pdf_path)

    # 使用无限循环以重复处理
    while True:
        # 用户输入本地PDF文件路径
        user_input_str = input("请输入文件地址，或拖入一个文件，使用exit以退出：\n")
        user_input_group = []
        if user_input_str.lower() == 'exit':
            break
        # 处理敏感度参数
        if "--t" in user_input_str:
            user_input_group = user_input_str.rsplit(maxsplit=2)
            local_pdf_path = user_input_group[0]
            threshold_num = user_input_group[2]
        else:
            local_pdf_path = user_input_str
        # 调用analyze_pdf函数处理用户输入的文件路径
        if not "--t" in user_input_str:
            analyze_pdf(local_pdf_path)
        else:
            analyze_pdf(local_pdf_path, threshold_num)
