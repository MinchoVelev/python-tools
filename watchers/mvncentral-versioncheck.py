from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def removeWeirdChars(str):
    toRemove = []
    tmp = str
    for c in tmp:
        if ord(c) < 33 or ord(c) > 126:
            toRemove.append(c)
    
    for c in toRemove:
        tmp = tmp.replace(c, '')
    
    return tmp

def getLatestVersion(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument("--mute-audio")

    # https://sites.google.com/a/chromium.org/chromedriver/downloads
    browser = webdriver.Chrome(options=options)

    browser.get(url)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'latest-version')))


    latestDiv = browser.find_element(by=By.CLASS_NAME, value='latest-version')

    latestLink = latestDiv.find_element(by=By.TAG_NAME, value='a')

    version = latestLink.get_attribute("innerHTML")
    browser.quit()

    return removeWeirdChars(version);

def hasNewer(lastKnownVersion, url):
    latest = getLatestVersion(url).strip()

    if latest != lastKnownVersion:
        notify("Version Watcher", "New version available! Latest is " + latest)
    else:
        notify("Version Watcher", "No new version available. Latest is " + latest)


if __name__ == "__main__":
    hasNewer("2.13.2", "https://search.maven.org/artifact/com.fasterxml.jackson.core/jackson-databind")









