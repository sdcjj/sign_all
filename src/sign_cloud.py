from cloud import load_clound
from config import do_sleep, initBrowser, load_config, quitBrowser
from imp.sign_click_sites import do_sign_site


def do_sign_cloud(debug, config):
    cookie_cloud_config = config.get("cookie_cloud")
    cookid_data = load_clound(cookie_cloud_config)

    cloud_config = load_config("cloud_config.json")
    pt_sites = cloud_config.get("pt_sites", None)
    if pt_sites:
        print("do_sign_pt_sites begin")
        for pt_site in pt_sites:
            site_model = {"url": pt_site}
            try:
                with initBrowser(debug, config) as browser:
                    do_sign_site(browser, cookid_data, site_model)
                    quitBrowser(browser)
            except Exception as e:
                print("do_sign_pt_site 异常", pt_site, e)
        print("do_sign_pt_sites end")

    do_sleep(3)

    click_sites = cloud_config.get("click_sites", None)
    if click_sites:
        print("do_sign_click_sites begin")
        for click_site in click_sites:
            try:
                with initBrowser(debug, config) as browser:
                    do_sign_site(browser, cookid_data, click_site)
                    quitBrowser(browser)
            except Exception as e:
                print("do_sign_click_site 异常", click_site, e)
        print("do_sign_click_sites end")
