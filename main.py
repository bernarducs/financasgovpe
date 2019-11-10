from selenium import webdriver
from time import sleep

driver = webdriver.Firefox()
url = 'http://web.transparencia.pe.gov.br/despesas/despesa-geral/'
driver.get(url)
sleep(10)

js = "document.getElementById('iframe').contentWindow.document.getElementsByClassName('chzn-select')" \
     "[1].style.display = 'inline';"
driver.execute_script(js)

driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
options = driver.find_elements_by_xpath("//*[@id='html_selectug']/select/option")
options[4].click()
