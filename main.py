from selenium import webdriver
from time import sleep
from datetime import date
import os
import re


def get_driver():
    # setting driver
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", os.getcwd() + "/extracao/despesa")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
    fp.set_preference("dom.disable_deforeunload", True)

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')

    # creating driver and getting the url
    driver = webdriver.Firefox(fp, options=options)
    driver.get('http://web.transparencia.pe.gov.br/despesas/despesa-geral/')
    sleep(10)

    # removing the fixed bar and selecting iframe
    topo = driver.find_element_by_class_name('topo-fixed')
    driver.execute_script("arguments[0].style.position='absolute';", topo)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    return driver


def enable_options(driver):
    ops_xpath = '/html/body/main/section/div/div[5]/div/div/div[2]/div[1]/div[1]/div[4]/div/select'
    ops = driver.find_elements_by_xpath(ops_xpath)
    driver.execute_script("arguments[0].style.display='inline';", ops[0])
    options = driver.find_elements_by_xpath("//*[@id='html_selectugtabela']/select/option")
    return options


def get_uge_list(driver):
    options = enable_options(driver)
    dpts = [option.text for option in options]
    return dpts


def export_table(driver):
    btn_table = driver.find_element_by_xpath('//*[@id="exportTable"]')
    driver.execute_script('arguments[0].scrollIntoView(true);', btn_table)
    btn_table.click()


def get_today():
    today = date.today().timetuple()
    today_str = '{}{}{}'.format(today.tm_mday, today.tm_mon, today.tm_year)
    return today_str


def rename_file(uge):
    uge = re.sub('[!@#$/]', '-', uge)
    path = os.getcwd() + r'/extracao/despesa/'
    filename_path = path + r'Despesa_' + get_today() + '.xls'
    new_filename = path + uge + '_' + get_today() + '.xls'
    try:
        os.rename(filename_path, new_filename)
    except FileNotFoundError as e:
        print(e)
    except FileExistsError as e:
        print(e)


driver = get_driver()
orgaos = get_uge_list(driver)

for orgao in orgaos:
    print('Gerando {} de {}.'.format(orgaos.index(orgao), len(orgaos)))
    ops = enable_options(driver)
    for op in ops:
        if op.text == orgao:
            print('Extraindo planilha {}.'.format(orgao))
            break
    op.click()
    sleep(5)
    export_table(driver)
    sleep(5)
    rename_file(orgao)


