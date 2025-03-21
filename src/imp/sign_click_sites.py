from selenium.webdriver.common.by import By
from cloud import add_cookies, find_base_url
from config import do_sleep


def do_sign_site(browser, cookie_data, click_site):
    print("do_sign_site begin")
    url = click_site.get("url", "")
    if not url:
        return
    try:
        browser.get(find_base_url(url))
        add_cookies(browser, cookie_data, url)
        browser.get(url)
        do_sleep(2)
        btn_id = click_site.get("btn_id", "")
        if btn_id:
            btn = browser.find_element(By.ID, btn_id)
            if btn:
                try:
                    btn.click()
                except:
                    browser.execute_script("arguments[0].click();", btn)
        do_sleep(2)
        btn_path = click_site.get("btn_xpath")
        if btn_path:
            btn = browser.find_element(By.XPATH, btn_path)
            if btn:
                try:
                    btn.click()
                except:
                    browser.execute_script("arguments[0].click();", btn)
    except:
        print(url, "do_sign_sites error")
    print("do_sign_sites end")
