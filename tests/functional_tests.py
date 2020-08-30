from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

admin_username = 'xxxx'
admin_password = 'xxxx'

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

    def test_cv_page_has_correct_title(self):  
        self.browser.get('http://127.0.0.1:8000/cv/')
        self.assertIn('My CV', self.browser.title) 

    def test_non_admin_cannot_add_cv_section(self):
        # Non-admin user sneakily tries to add a new cv section
        self.browser.get('http://127.0.0.1:8000/cv/new/')

        # User adds data to validate the form
        inputbox = self.browser.find_element_by_id('id_title')
        inputbox.send_keys('Sneaky CV section')
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('This is the body of the CV section')

        # User presses save
        save_button = self.browser.find_element_by_id('id_save_cv_section')
        save_button.click()
        
        # User goes back to blog list to check if it is there
        self.browser.get('http://127.0.0.1:8000/cv/')
        html = self.browser.page_source

        # Their title should not be in the HTML source
        self.assertFalse('Sneaky CV section' in html)

    def test_admin_can_add_cv_section(self):
        # Admin user logs in
        self.login_as_admin()

        # User goes to add a new cv section
        self.browser.get('http://127.0.0.1:8000/cv/new/')

        # User adds data to validate the form
        inputbox = self.browser.find_element_by_id('id_title')
        inputbox.send_keys('My test CV section')
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('This is the body of the CV section')

        # User presses save
        save_button = self.browser.find_element_by_id('id_save_cv_section')
        save_button.click()
        
        # User goes back to blog list to check if it is there
        self.browser.get('http://127.0.0.1:8000/cv/')
        html = self.browser.page_source

        # Their title should be in the HTML source
        self.assertTrue('My test CV section' in html)

    def test_non_admin_cannot_delete_cv_section(self):
        # Admin initially makes a CV section
        self.login_as_admin()

        self.browser.get('http://127.0.0.1:8000/cv/new/')

        inputbox = self.browser.find_element_by_id('id_title')
        inputbox.send_keys('My test CV section')

        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('This is the body of the CV section')

        save_button = self.browser.find_element_by_id('id_save_cv_section')
        save_button.click()

        # Admin logs out (non-admin accesses site)
        self.browser.get('http://127.0.0.1:8000/admin/logout/')

        # Non-admin user brute forces URLs to find edit page for the CV section
        brute_force_attempts = 50
        for i in range(brute_force_attempts):
            self.browser.get('http://127.0.0.1:8000/cv/{}/edit/'.format(i))
            if 'My test CV section' in self.browser.page_source:
                break
            if i == brute_force_attempts-1:
                self.fail("Couldn't find admin's CV section")

        # User tries to delete section
        delete_button = self.browser.find_element_by_id('id_delete_cv_section')
        delete_button.click()

        # Admin's CV section should still be there
        self.browser.get('http://127.0.0.1:8000/cv/')
        self.assertTrue('My test CV section' in self.browser.page_source)

    def test_admin_can_delete_cv_section(self):
        # Admin makes a CV section
        self.login_as_admin()

        self.browser.get('http://127.0.0.1:8000/cv/new/')

        inputbox = self.browser.find_element_by_id('id_title')
        inputbox.send_keys('My test CV section to delete')

        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('This is the body of the CV section')

        save_button = self.browser.find_element_by_id('id_save_cv_section')
        save_button.click()

        # Admin user brute forces URLs to find edit page for the CV section (not sure how to make it click on the correct edit button)
        brute_force_attempts = 50
        for i in range(brute_force_attempts):
            self.browser.get('http://127.0.0.1:8000/cv/{}/edit/'.format(i))
            if 'My test CV section to delete' in self.browser.page_source:
                break
            if i == brute_force_attempts-1:
                self.fail("Couldn't find admin's CV section")

        # User tries to delete section
        delete_button = self.browser.find_element_by_id('id_delete_cv_section')
        delete_button.click()

        # CV section should no longer be there
        self.browser.get('http://127.0.0.1:8000/cv/')
        self.assertFalse('My test CV section to delete' in self.browser.page_source)


if __name__ == '__main__':  
    unittest.main()  