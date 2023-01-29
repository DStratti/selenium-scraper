from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
#from fake_useragent import UserAgent
import undetected_chromedriver as uc

def numeric_mapper(num='0'):
    '''
    Map the numeric string values provided into the correct numeric amount
    '''
    num = str(num)
    
    if num == 'unknown':
        return 0

    if 'k' in num.lower():
        return float(num.lower().replace('k', '')) * 1_000
    elif 'm' in num.lower():
        return float(num.lower().replace('m', '')) * 1_000_000
    elif '%' in num.lower():
        return float(num.lower().replace('%', '')) / 100

    return float(num)
    

def safe_css_select_text(element, css_selector='*'):
    '''
    Safely extract data from element using css selectors
    '''
    try:
        term = element.find_element(By.CSS_SELECTOR, css_selector)
        term = term.text
    except Exception as e:
        print(e)
        term = 'unknown'
    return term


def safe_css_select_attribute(element, css_selector='*', attribute='href'):
    '''
    Safely extract data from the attributes of element using css selectors
    '''
    try:
        attributes = [term.get_attribute(attribute) for term in element.find_elements(By.CSS_SELECTOR, css_selector)]
    except Exception as e:
        print(e)
        attributes = ['unknown']
    return attributes

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    #uc.install(executable_path='./chromedriver')
    uc.TARGET_VERSION = 90 
    chrome_options = uc.ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    # # chrome_prefs = {}
    # chrome_options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def grab_bio(driver):
    ''' Grab the bio and links '''
    bio = safe_css_select_text(driver, 'h2.share-desc')
    links = safe_css_select_attribute(driver, 'div.share-links a')

    # check if verified
    verified = False
    try:
        handle = driver.find_element(By.CSS_SELECTOR, 'h2.share-title.verified')
        verified = True
    except NoSuchElementException as nsee:
        pass
    except Exception as e:
        print(e)

    return {'bio': bio, 'links': links, 'verified': verified}


def grab_insights(driver):
    ''' Grab the follows, followers and likes'''
    try:
        following = safe_css_select_text(driver, 'strong[data-e2e="following-count"]')
        followers = safe_css_select_text(driver, 'strong[data-e2e="followers-count"]')
        likes = safe_css_select_text(driver, 'strong[data-e2e="likes-count"]')
        
        insight_scrape = {
            "follows_count": numeric_mapper(following),
            "followers_count": numeric_mapper(followers),
            "likes_count": numeric_mapper(following),
        }
    except Exception as e:
        print(e)
        insight_scrape = {'unknown': e}

    return insight_scrape


def grab_media(driver):
    ''' Grab the first 15 video links'''

    # grab all video links
    # mouse over each and grab the video
    videos = safe_css_select_attribute(driver, 'a.video-feed-item-wrapper div.image-card video', 'src')

    return {'videos': videos}


if __name__ == "__main__":
    chrome_options = set_chrome_options()
    driver = uc.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')


    # test
    url = "https://www.tiktok.com/@therock?"
    driver.get(url)

    timeout = 20
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.count-infos div.number strong:first-child')))
    except TimeoutException:
        print("Timed out waiting for page to load")


    insights = grab_insights(driver)
    
    videos = get_media_links(browser)
    
    processed_videos = []
    # Calc engagements
    for video in videos:
        # get likes and comments
        processed_videos.append(get_media_engagements(browser, video))
    #media = grab_media(driver)

    print({**bio, **insights})

    # Do stuff with your driver
    driver.close()