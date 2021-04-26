from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException


import time

#Update Your email id and password Here
USERNAME = "rashid92.m@gmail.com"
PASSWORD = "141296@Juet"

url = input('Insert Job URl of Job Listing page: ')
MaxApply = int(input('MaxApplyCount'))

applyNowButtonArial = ""
company_name=""
ignored_exceptions = (StaleElementReferenceException,)
path = r'C:\Users\Rashid mohammad\Documents\PYTHON DEVELOPMENT\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(path)
driver.implicitly_wait(15) # seconds

driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 30)

xpath_rememberME = '/html/body/div/main/div/section/header/h3[2]'
xpath_cancel_RemenberME = '/html/body/div/main/div/section/footer/form[1]/button'
def minimizeChatWindow():
    xpathofButton = '//*[@id="msg-overlay"]/div[1]/header/section[1]/button'
    try:
        print('sleep for page load..')
        time.sleep(15)
        print('minimizing chat window...')
        downButton= wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpathofButton)))
        downButton.click()
    except TimeoutException:
        print("ERROR: Chat window is not minimized ")

def signOut():
    dropdownButton = driver.find_element_by_css_selector('.artdeco-dropdown__trigger--placement-bottom')
    dropdownButton.click()
    signoutButton = driver.find_element_by_xpath('//*[@href="/m/logout/"]')
    signoutButton.click()


def signIn():
    myDynamicElement = driver.find_element_by_class_name("cta-modal__primary-btn")
    myDynamicElement.click()
    usernameInput = driver.find_element_by_id("username")
    passwordInput = driver.find_element_by_id("password")
    usernameInput.send_keys(USERNAME)
    passwordInput.send_keys(PASSWORD)
    signInButton = driver.find_element_by_xpath("/html/body/div/main/div[2]/div[1]/form/div[3]/button")
    signInButton.click()

    #Check For remeber ME window and click cancel
    try:
        rememberMe= wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath_rememberME)))
        if rememberMe.text == 'Remember me on this browser':
            driver.find_element_by_xpath(xpath_cancel_RemenberME).click()

    except TimeoutException:
        print("ERROR: Remember ME box not avaible,Continue... ")

def discard():
    try:
        cancelButton = driver.find_element_by_css_selector("button.artdeco-modal__dismiss")
        if cancelButton.is_enabled():
            cancelButton.click()
            discardButton = driver.find_element_by_css_selector("button.artdeco-modal__confirm-dialog-btn.artdeco-button--primary")
            if discardButton.is_enabled():
                discardButton.click()
                print(f"Application for {company_name} is discarded")
                return True
            else:
                print("Discard button is not enabled")
                return False
        else:
            print("Cancel button is not enabled")
            return False
    except NoSuchElementException:
        print("ERROR : Unable to click Cancel or Discard button")
        return False
def clickReview():
    try:
        driver.find_element_by_css_selector(
            "footer > div > button.artdeco-button--primary").click()  # review Button
        return True
    except NoSuchElementException:
        print("ERROR : Unable to click review button")
        assert discard(), "Discard Fail"
        return False

def clickSubmit():
    try:
        driver.find_element_by_css_selector(
            "footer > div > button.artdeco-button--primary").click()  # review Button
        return True
    except NoSuchElementException:
        print("ERROR : Unable to click Submit button")
        assert discard(), "Discard Fail"
        return False

def clickNext():
    try:
        driver.find_element_by_css_selector(
            "footer > div > button.artdeco-button--primary").click()  # review Button
        return True
    except NoSuchElementException:
        print("ERROR : Unable to click Next button")
        assert discard(), "Discard Fail"
        return False
def checkSubmitSuccessfull():
    try:
        submitHeading= driver.find_element_by_css_selector("h3.jpac-modal-header")
        submitText = submitHeading.text
        if "Great! Your application was sent to" in submitText:
            print(f"{submitText} ")
        else:
            print(f"{submitText} ")
    except NoSuchElementException:
        print(f"Application submission fails for {applyNowButtonArial} ")
    finally:
        driver.find_element_by_css_selector("button.artdeco-modal__dismiss").click()

def findAllJobsList():
    allJobs = driver.find_elements_by_css_selector("li.jobs-search-results__list-item")
    print(f"Total Jobs listed are {len(allJobs)}")
    for job in range(MaxApply):
        time.sleep(10)
        allJobs[job].is_enabled()
        allJobs[job].click()
        global company_name
        company_name = allJobs[job].find_element_by_css_selector("a.job-card-container__link.job-card-container__company-name").text
        print(f"\nstarting apply process for {company_name}")
        try:
            applyNowButton = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-apply-button")))
            if applyNowButton.is_enabled():
                global applyNowButtonArial
                applyNowButtonArial = applyNowButton.get_attribute('aria-label')
                print(f"applying for {applyNowButtonArial}")
                applyNowButton.click()
                firstbutton = driver.find_element_by_css_selector('form footer button.artdeco-button--primary')
                aria_label = firstbutton.get_attribute("aria-label")
                if aria_label == "Submit application":
                    clickSubmit()
                    checkSubmitSuccessfull()
                elif aria_label == "Continue to next step":
                    clickNext()
                    secondButton = driver.find_element_by_css_selector('form footer button.artdeco-button--primary')
                    aria_label = secondButton.get_attribute("aria-label")
                    if aria_label == "Continue to next step":
                        print(f"Additional information is required to  {applyNowButtonArial}, Hence skipping this Job post")
                        assert discard(), "Discard Fail"
                    else:
                        clickReview()
                        clickSubmit()
                        checkSubmitSuccessfull()
                else:
                    print(f"{aria_label} not handeled ")
                    discard()
            else:
                print(f"Apply Now button is not available for {company_name}")
        except (NoSuchElementException,TimeoutException):
            print(f"Application already submitted")
            pass

if driver.find_element_by_id("cta-modal-header"):
    signIn()
    minimizeChatWindow()
    findAllJobsList()
    # driver.quit()



