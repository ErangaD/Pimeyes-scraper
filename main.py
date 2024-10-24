from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


use_proxy = False  # Set to True to use proxy, False to use your host IP

if use_proxy:
    from seleniumwire import webdriver
    import getProxy
else:
    from selenium import webdriver

url = "https://pimeyes.com/en"

def upload(url, path, use_proxy):
    driver = None

    if use_proxy:
        prox = getProxy.fetchsocks5()  # FORMAT = USERNAME:PASS@IP:PORT
        options = {
            'proxy': {
                'http': prox,
                'https': prox,
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        driver = webdriver.Chrome(seleniumwire_options=options)
    else:
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Uncomment to run Chrome in headless mode (no GUI)
        driver = webdriver.Chrome(options=chrome_options)
    
    results = None
    currenturl = None 

    try:
        driver.get(url)
        upload_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="hero-section"]/div/div[1]/div/div/div[1]/button[2]'))
        )

        time.sleep(2)

        driver.execute_script("""
            var element = document.getElementById('CybotCookiebotDialog');
            if (element) {
                element.parentNode.removeChild(element);
            }
        """)

        upload_button.click()
        
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=file]'))
        )

        file_input.send_keys(path)
        time.sleep(7)

        # agreement1_xpath = '#app > div.wrapper.mobile-fullscreen-mode.mobile-full-height > div > div > div > div > div > div > div.permissions > div:nth-child(1) > label > input[type=checkbox]'
        # agreement2_xpath = '#app > div.wrapper.mobile-fullscreen-mode.mobile-full-height > div > div > div > div > div > div > div.permissions > div:nth-child(2) > label > input[type=checkbox]'
        # agreement3_xpath = '#app > div.wrapper.mobile-fullscreen-mode.mobile-full-height > div > div > div > div > div > div > div.permissions > div:nth-child(3) > label > input[type=checkbox]'
        
        agreement1_xpath = '.form-group:nth-child(1) input'
        agreement2_xpath = '.form-group:nth-child(2) > .checkbox > input'
        agreement3_xpath = '.form-group:nth-child(3) > .checkbox > input'
        submit_xpath = 'button:nth-child(5)'

        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, agreement1_xpath))).click()
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, agreement2_xpath))).click()
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, agreement3_xpath))).click()
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_xpath))).click()

        time.sleep(5)
        currenturl = driver.current_url
        resultsXPATH = '//*[@id="results"]/div/div[2]/div[1]/div/div/div[1]/div/div[1]/button/div/span/span'
        results = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, resultsXPATH))
        ).text

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        print("Results: ", results)
        print("URL: ", currenturl)
        if driver:
            driver.quit()

def main():
    path = input("Enter path to the image: ")
    upload(url, path, use_proxy)

if __name__ == "__main__":
    main()
