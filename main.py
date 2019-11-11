from selenium import webdriver
from time import sleep
import os


def get_driver():
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", os.getcwd() + "/extracao/despesa")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
    fp.set_preference("dom.disable_deforeunload", True)

    options = webdriver.FirefoxOptions()
    # options.add_argument('-headless')

    driver = webdriver.Firefox(fp, options=options)
    url = 'http://web.transparencia.pe.gov.br/despesas/despesa-geral/'
    driver.get(url)

    return driver


def get_options(driver):
    js = "document.getElementById('iframe').contentWindow.document.getElementsByClassName('chzn-select')" \
         "[1].style.display = 'inline';"
    driver.execute_script(js)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    options = driver.find_elements_by_xpath("//*[@id='html_selectug']/select/option")
    return options


def extract_table(driver):
    btn_table = driver.find_element_by_xpath('//*[@id="exportTable"]')
    driver.execute_script('arguments[0].scrollIntoView(true);', btn_table)
    btn_table.click()
