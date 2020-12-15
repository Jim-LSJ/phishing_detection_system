from selenium import webdriver
from selenium import common
import pandas as pd
import time, os

def create_driver():
    # geckodriver
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    driver = webdriver.Firefox(executable_path = os.path.join(".", "geckodriver", "geckodriver"), firefox_options=fireFoxOptions)
    driver.set_page_load_timeout(30)
    return driver

def close_driver(driver):
    driver.close()
    return

def browse(url, driver=None):
    # geckodriver
    if driver is None:    
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        driver = webdriver.Firefox(executable_path = os.path.join(".", "geckodriver", "geckodriver"), firefox_options=fireFoxOptions)
        driver.set_page_load_timeout(30)
    
    df = pd.DataFrame()

    print("\nCrawl {}".format(url))

    try:
        driver.get(url)
        
        time.sleep(3)
        driver.save_screenshot(os.path.join("screenshot", "test.png"))

        html = driver.page_source
        # file = open(os.path.join("html", "test.html"), "w")
        # file.write(html)
        # file.close()

        cookies = driver.get_cookies()
        protection = ["httpOnly", "secure", "expiry"]
        httponly = secure = session = h_s = 0
        for cookie in cookies:
            if cookie.get(protection[0]):
                httponly += 1
            if cookie.get(protection[1]):
                secure += 1
            if not cookie.get(protection[2]):
                session += 1
            if cookie.get(protection[1]) and not cookie.get(protection[2]):
                h_s += 1

        js_global_var = driver.execute_script("return Object.keys( window );")

        df.loc[0, "Cookies"] = len(cookies)
        df.loc[0, "httponly"] = httponly
        df.loc[0, "secure"] = secure
        df.loc[0, "session"] = session
        df.loc[0, "session & httponly"] = h_s
        df.loc[0, "JSGlobalVar"] = len(js_global_var)
        
    except common.exceptions.TimeoutException:
        print('\t{} Timeout'.format(url))
        return df, None
    except common.exceptions.NoSuchElementException:
        print('\t{} cannot find code'.format(url))
        return df, None

    except:
        print("\t{} unknown error".format(url))
        return df, None

    print("Finish collecting data")
    return df, html

if __name__ == "__main__":
    driver = create_driver()