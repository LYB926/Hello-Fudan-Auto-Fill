# > nul 2>&1 || @echo off && cls && cd "%~dp0" && python "%~0" && goto :eof
# > nul 2>&1 || echo 完成,请关闭本窗口 && exit

from selenium import webdriver
import time
import sys
import os
import os.path

url = r"https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Fzlapp.fudan.edu.cn%2Fa_fudanzlapp%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fzlapp.fudan.edu.cn%252Fsite%252Fncov%252FfudanDaily%253Ffrom%253Dhistory%26from%3Dwap"


def kill():
    print("-5 s后关闭浏览器", end="")
    time.sleep(5)
    for i in range(5):
        print("\r", str(5-i), end="", flush=True)
        time.sleep(0.98)
    print("\r"+" "*16, end="", flush=True)
    print()
    driver.close()
    sys.exit(1)


# 默认使用Edge
edge_driver = os.getcwd() + "/msedgedriver.exe"
driver = webdriver.Edge(edge_driver)
driver.get(url)
time.sleep(1)


title = driver.title
print("目前页面为：", title)
if title != "复旦大学统一身份认证":
    print("错误：目前页面不是复旦大学统一身份认证，请尝试重新运行")
    kill()


if os.path.exists("account.txt"):
    with open("account.txt", "r", encoding="utf-8") as fi:
        account = fi.readlines()
        uid = account[0].strip()
        if len(uid) != 11:
            print("错误：学号应为11位数字")
            kill()
        psw = account[1].strip()
else:
    print("首次运行，将创建新UIS凭据。")
    with open("account.txt", "x", encoding="utf-8") as fi:
        account = input("请输入您的UIS学号：")
        fi.write(account)
        fi.write("\n")
        psw = input("请输入您的UIS密码：")
        fi.write(psw)
        fi.write("\n----------\n此文件用于储存您的UIS凭据。")
        fi.close()
    with open("account.txt", "r", encoding="utf-8") as fi:
        account = fi.readlines()
        uid = account[0].strip()
        if len(uid) != 11:
            print("错误：学号应为11位数字")
            kill()
        psw = account[1].strip()

username = driver.find_element_by_xpath('//*[@id="username"]')
username.clear()
username.send_keys(uid)
password = driver.find_element_by_xpath('//*[@id="password"]')
password.clear()
password.send_keys(psw)
try:
    print("正在登录...")
    driver.find_element_by_xpath('//*[@id="idcheckloginbtn"]').click()
    time.sleep(2)
except:
    print("已登录")
    time.sleep(3)

# check
title = driver.find_element_by_xpath(
    "/html/body/div[1]/div/div[1]/section/header/a[1]/em").text
print("目前页面为：", title)

if title != "Daily updates":
    print("重试中")
    time.sleep(3)
    title = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[1]/section/header/a[1]/em").text
    print("目前页面", title)
    if title != "Daily updates":
        print("错误：未进入每日上报页面，请检查account.txt中的登录凭据是否正确。")
        kill()
    else:
        print("已进入上报页面")

tmp = driver.find_element_by_xpath(
    "/html/body/div[1]/div/div[1]/section/div[5]/div/a").get_attribute("class")
if tmp == "wapcf-btn-qx":
    print("\n\n今日已完成填报。")
    kill()

# 弹框-知晓
try:
    driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div").click()
    print("知晓")
except:
    try:
        driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[2]/div").click()
        print("知晓")
    except:
        print("已知晓")
time.sleep(1)

# 定位
try:
    driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[1]/section/div[4]/ul/li[6]/div/span").click()
    print("定位中")
except:
    print("错误：定位失败")
    kill()

time.sleep(5)

# end
try:
    driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[1]/section/div[5]/div/a").click()
except:
    print("错误：上报数据失败。")
    kill()

time.sleep(2)
try:
    driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div[2]").click()
    print("确定")
    print("上报成功。")

except:
    print("错误：上报数据失败。")
    kill()

kill()
