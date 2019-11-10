from selenium import webdriver
from time import sleep

dir = r'\despesa'

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", dir)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
fp.set_preference("dom.disable_deforeunload", True)

options = webdriver.FirefoxOptions()
# options.add_argument('-headless')

driver = webdriver.Firefox(fp, options=options)

url = 'http://web.transparencia.pe.gov.br/despesas/despesa-geral/'
driver.get(url)
sleep(10)

js = "document.getElementById('iframe').contentWindow.document.getElementsByClassName('chzn-select')" \
     "[1].style.display = 'inline';"
driver.execute_script(js)

driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
options = driver.find_elements_by_xpath("//*[@id='html_selectug']/select/option")

#orgaos = [option.text for option in options]

btn_exp = driver.find_element_by_id('exportTable')
btn_exp.click()


