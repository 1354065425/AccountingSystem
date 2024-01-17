#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AccountingSystem 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：搬不完的砖
@Date    ：2024/1/16 11:43 
"""
import datetime
import tkinter as tk
from tkinter.messagebox import *
from loguru import logger

logger.add(f"./log/{datetime.datetime.now().year}_{datetime.datetime.now().month}_{datetime.datetime.now().day}.log")

outbound_list = []
inventory_list = []
out_price_list_total = []
inv_price_list_total = []

WALLETTOTAL = 0


# 总账
def all_money():
    all_money_count = sum(out_price_list_total) + sum(inv_price_list_total) + WALLETTOTAL
    info_text.insert("end", f"总账为：{all_money_count} 元\n")
    logger.info(f"总账为：{all_money_count} 元")


# 打印信息
def info_print(list_name, status):
    for i in list_name:
        logger.info(f"{i['name']} 单价 {i['price']} {i['number']}支 总价 {i['total_price']}")
        info_text.insert("end",
                         str(f"{status}\n{i['name']} 单价 {i['price']} {i['number']} 支 总价 {i['total_price']}\n"))


# 出库总金额
def out_count_total_price():
    global out_price_list_total
    for price in outbound_list:
        total_price = price["total_price"]
        out_price_list_total.append(total_price)
    info_text.insert("end", f"出库总金额：{sum(out_price_list_total)}\n")
    logger.info(f"出库总金额{sum(out_price_list_total)}")


# 库存总金额
def inv_count_total_price():
    global inv_price_list_total
    for price in inventory_list:
        total_price = price["total_price"]
        inv_price_list_total.append(total_price)
    info_text.insert("end", f"库存总金额：{sum(inv_price_list_total)}\n")
    logger.info(f"库存总金额：{sum(inv_price_list_total)}")


# 出库单一品种计算总价，并保存到列表中
def submit_out_total_price():
    info_dict = {}
    if price_entry.get() and count_entry.get() is not None:
        name = category_entry.get()
        price = int(price_entry.get())
        number = int(count_entry.get())
        total_price = price * number

        info_dict["name"] = name
        info_dict["price"] = price
        info_dict["number"] = number
        info_dict["total_price"] = total_price

        outbound_list.append(info_dict)
        print(outbound_list)
        total_price_entry.delete(0, "end")
        total_price_entry.insert(0, str(total_price))
        logger.info(
            f"{info_dict['name']} 单价 {info_dict['price']} {info_dict['number']}支 总价 {info_dict['total_price']}")
    else:
        print(showwarning(title="错误", message=f"请输入单价与数量"))


# 库存单一品种计算总价，并保存到列表中
def submit_inv_total_price():
    info_dict = {}
    if inventory_price_entry.get() and inventory_count_entry.get() is not None:
        name = inventory_category_entry.get()
        price = int(inventory_price_entry.get())
        number = int(inventory_count_entry.get())
        total_price = price * number

        info_dict["name"] = name
        info_dict["price"] = price
        info_dict["number"] = number
        info_dict["total_price"] = total_price

        inventory_list.append(info_dict)
        print(inventory_list)
        inventory_total_price_entry.delete(0, "end")
        inventory_total_price_entry.insert(0, str(total_price))
        logger.info(
            f"{info_dict['name']} 单价 {info_dict['price']} {info_dict['number']}支 总价 {info_dict['total_price']}")
    else:
        print(showwarning(title="错误", message=f"请输入单价与数量"))


# 钱包总金额
def wallet_total():
    global WALLETTOTAL
    if alipay_entry.get() and alipay_remain_entry.get() and wechat_entry.get() and wechat_remain_entry.get() is not None:
        WALLETTOTAL = int(alipay_entry.get()) + int(alipay_remain_entry.get()) + int(wechat_entry.get()) + int(
            wechat_remain_entry.get())
        info_text.insert("end", f"钱包总金额为：{WALLETTOTAL} 元\n")
        logger.info(f"钱包总金额为：{WALLETTOTAL} 元")
    else:
        print(showwarning(title="错误", message=f"请输入各个余额，没有就填 0"))


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()  # 获取显示屏宽度
    screenheight = root.winfo_screenheight()  # 获取显示屏高度
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)  # 设置窗口居中参数
    return size


main_window = tk.Tk()

main_window.title("AccountingSystem")
main_window.geometry(center_window(main_window, 900, 800))  # 让窗口居中显示

# 出库计算
outbound_calc_lable = tk.Label(main_window, text="今日出库计算")
category_lable = tk.Label(main_window, text="品类")
price_lable = tk.Label(main_window, text="单价(元)")
count_lable = tk.Label(main_window, text="数量(支)")
total_price_lable = tk.Label(main_window, text="总价(元)")
calc_total_price_lable = tk.Label(main_window, text="计算")
operate_lable = tk.Label(main_window, text="操作")

outbound_calc_lable.grid(row=1, column=3)
category_lable.grid(row=2, column=1)
price_lable.grid(row=2, column=2)
count_lable.grid(row=2, column=3)
total_price_lable.grid(row=2, column=4)
operate_lable.grid(row=2, column=5, columnspan=2)
calc_total_price_lable.grid(row=2, column=7)

category_entry = tk.Entry(main_window, width=20)
price_entry = tk.Entry(main_window, width=20)
count_entry = tk.Entry(main_window, width=20)
total_price_entry = tk.Entry(main_window, width=20)

submit_btn = tk.Button(main_window, width=10, text="提交", command=lambda: submit_out_total_price())
operate_btn = tk.Button(main_window, width=10, text="打印", command=lambda: info_print(outbound_list, "出库"))
calc_total_price_btn = tk.Button(main_window, width=10, text="计算总价",
                                 command=lambda: out_count_total_price())

category_entry.grid(row=3, column=1, pady=5, padx=5)
price_entry.grid(row=3, column=2, pady=5, padx=5)
count_entry.grid(row=3, column=3, pady=5, padx=5)
total_price_entry.grid(row=3, column=4, pady=5, padx=5)

submit_btn.grid(row=3, column=5, pady=6, padx=5)
operate_btn.grid(row=3, column=6, pady=5, padx=5)
calc_total_price_btn.grid(row=3, column=7, pady=5, padx=5)

# 库存计算
inventory_calc_lable = tk.Label(main_window, text="今日库存计算")
inventory_category_lable = tk.Label(main_window, text="品类")
inventory_price_lable = tk.Label(main_window, text="单价(元)")
inventory_count_lable = tk.Label(main_window, text="数量(支)")
inventory_total_price_lable = tk.Label(main_window, text="总价(元)")
inventory_calc_total_price_lable = tk.Label(main_window, text="计算")
inventory_operate_lable = tk.Label(main_window, text="操作")

inventory_calc_lable.grid(row=4, column=3, pady=20)
inventory_category_lable.grid(row=5, column=1)
inventory_price_lable.grid(row=5, column=2)
inventory_count_lable.grid(row=5, column=3)
inventory_total_price_lable.grid(row=5, column=4)
inventory_operate_lable.grid(row=5, column=5, columnspan=2)
inventory_calc_total_price_lable.grid(row=5, column=7)

inventory_category_entry = tk.Entry(main_window, width=20)
inventory_price_entry = tk.Entry(main_window, width=20)
inventory_count_entry = tk.Entry(main_window, width=20)
inventory_total_price_entry = tk.Entry(main_window, width=20)

inventory_submit_btn = tk.Button(main_window, width=10, text="提交", command=lambda: submit_inv_total_price())
inventory_calc_total_price_btn = tk.Button(main_window, width=10, text="计算总价",
                                           command=lambda: inv_count_total_price())
inventory_operate_btn = tk.Button(main_window, width=10, text="打印",
                                  command=lambda: info_print(inventory_list, "库存"))

inventory_category_entry.grid(row=6, column=1, pady=5, padx=5)
inventory_price_entry.grid(row=6, column=2, pady=5, padx=5)
inventory_count_entry.grid(row=6, column=3, pady=5, padx=5)
inventory_total_price_entry.grid(row=6, column=4, pady=5, padx=5)
inventory_submit_btn.grid(row=6, column=5)
inventory_operate_btn.grid(row=6, column=6, pady=5, padx=5)
inventory_calc_total_price_btn.grid(row=6, column=7, pady=5, padx=5)

# 钱包金额
wallet_calc_lable = tk.Label(main_window, text="钱包金额计算")
alipay_lable = tk.Label(main_window, text="支付宝余额(元)")
alipay_remain_lable = tk.Label(main_window, text="余额宝(元)")
wechat_count_lable = tk.Label(main_window, text="微信余额(元)")
wechat_remain_lable = tk.Label(main_window, text="微信零钱通(元)")
wallet_lable = tk.Label(main_window, text="计算")

wallet_calc_lable.grid(row=7, column=3, pady=20)
alipay_lable.grid(row=8, column=1)
alipay_remain_lable.grid(row=8, column=2)
wechat_count_lable.grid(row=8, column=3)
wechat_remain_lable.grid(row=8, column=4)
wallet_lable.grid(row=8, column=5, columnspan=2)

alipay_entry = tk.Entry(main_window, width=20)
alipay_remain_entry = tk.Entry(main_window, width=20)
wechat_entry = tk.Entry(main_window, width=20)
wechat_remain_entry = tk.Entry(main_window, width=20)

wallet_total_btn = tk.Button(main_window, width=10, text="钱包总金额",
                             command=lambda: wallet_total())
all_money_btn = tk.Button(main_window, width=10, text="总账", command=lambda: all_money())

alipay_entry.grid(row=9, column=1, pady=5, padx=5)
alipay_remain_entry.grid(row=9, column=2, pady=5, padx=5)
wechat_entry.grid(row=9, column=3, pady=5, padx=5)
wechat_remain_entry.grid(row=9, column=4, pady=5, padx=5)
wallet_total_btn.grid(row=9, column=5, pady=5, padx=5)
all_money_btn.grid(row=9, column=6, pady=5, padx=5)

# 信息打印
info_lable = tk.Label(main_window, text="信息打印")
info_lable.grid(row=10, column=3)
info_text = tk.Text(main_window, height=30, width=120)
info_text.grid(row=11, column=1, columnspan=7)
delete_info_btn = tk.Button(main_window, width=10, text="清除打印信息", command=lambda: info_text.delete("1.0", "end"))
delete_info_btn.grid(row=12, column=7, pady=5, padx=5)

main_window.mainloop()
