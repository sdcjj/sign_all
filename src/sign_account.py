from imp.sign98 import do_login, do_reply, do_sign
from config import do_sleep, do_sleep_random, initBrowser, load_config, quitBrowser
from imp.sign_account_site import do_sign_account_site
from message import send_message


def do_sign_account(debug, config):
    account_config = load_config("account_config.json")

    do_sign_98(debug, config, account_config.get("98"))

    print("common 执行开始")
    common_configs = account_config.get("common", None)
    if not common_configs:
        return
    success_count = 0
    fail_count = 0
    for common_config in common_configs:
        url = common_config.get("url", "未配置")
        print("do_sign_account_site 执行开始", url)
        browser = initBrowser(debug, config)
        try:
            do_sign_account_site(browser, common_config)
            success_count += 1
            print(url, "do_sign_account_site 执行结束")
        except Exception as e:
            print(url, "do_sign_account_site 异常 等待重试", e)
            fail_count += 1
        finally:
            quitBrowser(browser)
    send_message(
        config.get("qiye_wx", None),
        f"common执行完毕,成功{success_count},失败{fail_count}",
    )
    print("common 执行结束")


def do_sign_98(debug, config, config98):
    do_sleep_random("98签到随机延迟", config98.get("sleepRandomSeconds", 3600))
    browser = initBrowser(debug, config)
    try:
        print("98 开始登录")
        do_login(browser, config98)
        print("98 登录完毕")
        do_sleep(5)

        print("98 开始回复")
        do_reply(browser, config98)
        print("98 回复完毕")
        do_sleep(5)

        print("98 开始签到")
        sign_success=False
        for i in range(0, 3):
            try:
                do_sign(browser, config98)
                print("98 签到完毕")
                send_message(config.get("qiye_wx", None), "98签到完毕")
                sign_success=True
                break
            except Exception as e:
                print("98 签到异常 准备重试",i, e)
                do_sleep((i+1)*15)
        if not sign_success:
            send_message(config.get("qiye_wx", None), "98签到重试3次都失败,请手动签到")
            print("98 签到重试3次都失败,请手动签到")
        do_sleep(5)
    except Exception as e:
        print("do_sign_98 异常 等待重试", e)
    finally:
        quitBrowser(browser)
