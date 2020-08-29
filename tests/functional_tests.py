from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

admin_username = 'Jay'
admin_password = 'Pois0nwr4th'

class NewVisitorTest(unittest.TestCase): 

    # Function to login as admin that can be used before other testing other functionality
    def login_as_admin(self):
        # User goes to admin login page to gain edit privelages
        self.browser.get('http://127.0.0.1:8000/admin/')

        # User enters correct admin username and password
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys(admin_username)

        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys(admin_password)
        inputbox.send_keys(Keys.ENTER)

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    # def test_webpage_has_correct_title(self):  
    #     self.browser.get('http://127.0.0.1:8000/')
    #     self.assertIn('Jay', self.browser.title) 

    def test_login_as_admin(self):
        self.login_as_admin()
        time.sleep(5)


if __name__ == '__main__':  
    unittest.main()  