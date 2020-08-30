from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

admin_username = 'xxxxx'
admin_password = 'xxxxx'

class NewVisitorTest(unittest.TestCase): 

    # Function to login as admin that can be used before other testing other functionality
    def login_as_admin(self):
        # User goes to admin login page to gain edit privileges
        self.browser.get('http://127.0.0.1:8000/admin/')

        # User enters correct admin username and password
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys(admin_username)

        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys(admin_password)
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    # def test_webpage_has_correct_title(self):  
    #     self.browser.get('http://127.0.0.1:8000/')
    #     self.assertIn('Jay', self.browser.title) 

    def test_non_admin_cannot_add_blog_post(self):
        # Non-admin user sneakily tries to add a new blog post
        self.browser.get('http://127.0.0.1:8000/post/new')

        # User adds data to validate the form
        inputbox = self.browser.find_element_by_id('id_title')
        inputbox.send_keys('Sneaky blog post')
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('This is the body of the post')

        # User presses save
        save_button = self.browser.find_element_by_id('id_save_post')
        save_button.click()
        
        # User goes back to blog list to check if it is there
        self.browser.get('http://127.0.0.1:8000/')
        html = self.browser.page_source

        # Their title should not be in the HTML source
        self.assertFalse('Sneaky blog post' in html)

        time.sleep(5)


if __name__ == '__main__':  
    unittest.main()  