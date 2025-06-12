import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from config import do_sleep


def do_reply(browser, config):
    domin = config.get("domin")
    if not domin or not domin.startswith("http"):
        return
    fid = config.get("fid", "2")
    browser.get(domin + f"/forum.php?mod=forumdisplay&fid={fid}")
    do_sleep(5)
    eles = browser.find_elements(
        By.XPATH,
        f'//table[@summary="forum_{fid}"]/tbody[contains(@id, "normalthread_")]//th/a[@class="s xst" and not(@style)]',
    )
    hrefs = []
    for i in range(len(eles)):
        if i <= 5:
            continue
        hrefs.append(eles[i].get_attribute("href"))
    count = 3
    num = 0
    replyList = config.get("replyList")

    for href in hrefs:
        if num >= count:
            break
        random_number = random.randint(0, len(replyList) - 1)
        do_reply_message(browser, href, replyList[random_number])
        do_sleep(30)
        num = num + 1
    print("回帖完毕：" + str(num))


def do_reply_message(browser, href, message):
    browser.get(href)
    do_sleep(2)
    ip_message = browser.find_element(By.ID, "fastpostmessage")
    ip_message.clear()
    ip_message.send_keys(message)
    do_sleep(1)
    browser.find_element(By.ID, "fastpostsubmit").click()
    print("回帖：" + message)


def calc_answer(ptext):
    text = ptext.replace("换一个\n", "")
    text = text.replace(" ", "")
    text = text.split("=")[0]

    result = 0
    if text.find("+") > 0:
        nums = text.split("+")
        result = int(nums[0]) + int(nums[1])
    elif text.find("-") > 0:
        nums = text.split("-")
        result = int(nums[0]) - int(nums[1])
    print("计算结果：" + str(result))
    return str(result)


def do_login(browser, config):
    uid = config.get("account").get("uid")
    pwd = config.get("account").get("pwd")
    qid = config.get("account").get("qid")
    answer = config.get("account").get("answer")

    domin = config.get("domin")
    if not domin or not domin.startswith("http"):
        return
    browser.get(domin)
    do_sleep(5)
    browser.find_element(By.CLASS_NAME, "enter-btn").click()
    do_sleep(1)

    browser.find_element(By.ID, "ls_username").send_keys(uid)
    do_sleep(1)
    browser.find_element(By.ID, "ls_password").send_keys(pwd)
    do_sleep(1)
    browser.find_element(By.XPATH, '//*[@id="lsform"]//button').click()
    do_sleep(5)
    questionid = browser.find_element(By.NAME, "questionid")
    # 设置下拉框的值
    select = Select(questionid)

    # 通过可见文本设置下拉框的值
    select.select_by_value(qid)
    do_sleep(1)
    browser.find_element(By.NAME, "answer").send_keys(answer)

    browser.find_element(By.XPATH, '//*[@name="login"]//button').click()
    do_sleep(5)


def do_sign(browser, config):
    domin = config.get("domin")
    if not domin or not domin.startswith("http"):
        return
    do_sleep(10)
    browser.get(domin + "/plugin.php?id=dd_sign")
    do_sleep(5)
    browser.find_element(By.CLASS_NAME, "ddpc_sign_btn_red").click()

    do_sleep(15)
    pro = browser.find_element(By.XPATH, '//div[@class="rfm"]/table/tbody/tr/td')
    answer = calc_answer(pro.text)

    do_sleep(5)
    ip_answer = browser.find_element(By.NAME, "secanswer")
    ip_answer.clear()
    ip_answer.send_keys(answer)
    do_sleep(1)
    browser.find_element(By.NAME, "signsubmit").click()
    do_sleep(5)
