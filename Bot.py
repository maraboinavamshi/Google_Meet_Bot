import logging
import time,json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.INFO)

class GoogleMeetBot():
    def __init__(self, meet_url):
        # create chrome instance
        opt = Options()
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--start-maximized')
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })
        self.web_driver = 'chromedriver.exe'
        logging.info("Running Chrome Web Driver")
        self.driver = webdriver.Chrome(self.web_driver,options=opt)
        
        self.google_login_url = "https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ"
        self.email_input_by_id = "identifierId"
        self.pass_input_xpath = '//*[@id="password"]/div[1]/div/div[1]/input'
        self.next_button_email = "identifierNext"
        self.next_button_pswd = "passwordNext"
        self.meet_url = meet_url
        self.join_now_xpath = "//span[text()='Join now']"
        self.ask_to_join_xpath = "//span[text()='Ask to join']"
        self.turn_off_mic_css_selector = 'div[data-tooltip="Turn off microphone (ctrl + d)"]'
        self.turn_off_cam_css_selector = 'div[data-tooltip="Turn off camera (ctrl + e)"]'
        
        self.dismiss_btn_xpath = "//*[@id='yDmH0d']/div[3]/div/div[2]/div[3]/div/span/span"

    def google_login(self, email_id, password):
        # Login Page
        self.driver.get(self.google_login_url)

        # input Gmail
        logging.info("Gmail Login...")
        logging.info("Entering Gmail Address")
        self.driver.find_element(By.ID, self.email_input_by_id).send_keys(email_id)
        time.sleep(2)
        self.driver.find_element(By.ID, self.next_button_email).click()
        time.sleep(2)
        self.driver.implicitly_wait(300)

        # input Password
        logging.info("Entering Password...")
        self.driver.find_element(By.XPATH,self.pass_input_xpath).send_keys(password)
        time.sleep(2)
        self.driver.implicitly_wait(300)
        self.driver.find_element(By.ID, self.next_button_pswd).click()
        logging.info("Logging in to Google...")
        time.sleep(2)
        self.driver.implicitly_wait(300)

        # go to google home page
        self.driver.get('https://google.com/')
        logging.info("Google Login Successful..!!!")
        time.sleep(3)
        self.driver.implicitly_wait(300)
      

    def join_meeting(self,cam=True,mic=True):
        # Join meet
        print('joining in meeting...')
        self.driver.get(self.meet_url)
        logging.info("Opening Google Meet Link...")
        time.sleep(3)
        self.driver.implicitly_wait(200)
        #--------------------------
        if not mic:
            time.sleep(5)
            print('turning off mic...')
            self.driver.find_element(By.CSS_SELECTOR,self.turn_off_mic_css_selector).click()
        if not cam:
            # turn off camera
            time.sleep(2)
            print('turning off camera...')
            self.driver.find_element(By.CSS_SELECTOR,self.turn_off_cam_css_selector).click()
            
        #--------------------------
        self.driver.implicitly_wait(60)
        try:
            self.driver.find_element_by_xpath(self.ask_to_join_xpath).click()
        except:
            self.driver.find_element_by_xpath(self.join_now_xpath).click()
        #self.driver.find_element(by=By.XPATH, value=self.join_now_xpath).click()
        logging.info("Joined the meeting...")
          


    def ask_to_join(self):
        print('joining in meeting...')
        self.driver.get(self.meet_url)
        # Ask to Join meet
        time.sleep(3)
        self.driver.implicitly_wait(200)
        self.driver.find_element(by=By.XPATH, value=self.ask_to_join_xpath).click()
        logging.info("Joined the meeting...")


    def leave_meeting(self):
        self.driver.refresh()
        time.sleep(15)
        self.driver.close()
