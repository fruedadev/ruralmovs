"""
Module containing the page objects for the Ruralvia web page.
"""

from keyring import get_credential

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Base:
    """
    Base class for the Page Objects
    """

    BASE_URL = "https://bancadigital.ruralvia.com/CA-FRONT/NBE/web/particulares"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 9)

    def nav_to(self, url):
        """
        Navigates to the given url
        """

        self.driver.get(url)

    def back(self):
        """
        Navigates back
        """

        self.driver.back()

    def wait_clickable(self, locator):
        """
        Waits for an element to be available
        """

        return self.wait.until(EC.element_to_be_clickable(locator))

    def find(self, locator):
        """
        Finds an element given by the locator
        """

        return self.driver.find_element(*locator)

    def find_all(self, locator):
        """
        Finds the list of elements given by the locator
        """

        return self.driver.find_elements(*locator)

class Login(Base):
    """
    Class for the login page in the Ruralvia site
    """

    DNI = (By.NAME, "dniNie")
    PASSWORD = (By.NAME, "Alias")
    ACCESS = (By.XPATH, "//button[@type='submit' and contains(., 'Acceder')]")
    SECURITY = (By.XPATH, 
                "//h4[text()='¡Para nosotros tu seguridad es lo más importante!']")
    UNDERSTAND = (By.XPATH, "//button[span='Entendido']")

    def do_login(self, username: str):
        cred = get_credential("system", username)
        if cred == None:
            exit(f"The user {username} has not been found in the keyring")

        self.nav_to("https://bancadigital.ruralvia.com")
        self.find(self.DNI).send_keys(cred.username)
        element = self.wait_clickable(self.PASSWORD)
        element.send_keys(cred.password)

        self.find(self.ACCESS).click()

        if self.find_all(self.SECURITY):
            self.find(self.UNDERSTAND).click()

        return Home(self.driver)

class Home(Base):
    """
    Class for the home page
    """ 

    ALL_ACCOUNTS = (By.CLASS_NAME, "nbe-web-view-global-accounts-cards__button")
    ACCEPT_COOKIES = (By.XPATH, "//a[@class='c-button' and text()='Aceptar']")
    REJECT_COOKIES = (By.XPATH, "//a[@class='c-button' and text()='Rechazar']")

    def __init__(self, driver):
        super().__init__(driver)
        
        self.wait_clickable(self.REJECT_COOKIES).click()

    def get_accounts(self):
        """ Gets the accounts in the home page"""

        accounts = self.find_all(self.ALL_ACCOUNTS)
        names = []
        for account in accounts:
            names.append(account.text)

        return names

    def nav_account(self, account):
        """ Navigates to an account, given by the link element """

        ACCOUNT = (By.XPATH,
                   f"//button[contains(@class, 'nbe-web-view-global-accounts-cards__button') and span='{account}']")

        self.wait_clickable(ACCOUNT).click()

        return Account(self.driver)

class Account(Base):
    """
    Class for an account's page
    """
    
    ACCOUNT_NAME = (By.ID, "accountName")
    EXCEL_BTN = (By.XPATH, "//button[span='Excel']")

    def get_name(self):
        """ Gets the account's name """

        return self.wait_clickable(self.ACCOUNT_NAME).text

    def download(self):
        """ Downloads the Excel file with the movements """

        self.wait_clickable(self.EXCEL_BTN).click()