from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
from datetime import date
import os
import re

PAYMENTS = 'payment'
RECEIPTS = 'receipt'
PATH_PAYMENTS = os.getcwd() + r'/extracao/despesa/'
PATH_RECEIPT = os.getcwd() + r'/extracao/receita/'


class FinancasPE:
    def __init__(self, headless=True):
        self.headless = headless

    def _get_driver(self):
        # setting driver
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", os.getcwd() + "/extracao/despesa")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
        fp.set_preference("dom.disable_deforeunload", True)

        options = webdriver.FirefoxOptions()
        if self.headless:
            options.add_argument('-headless')

        # creating driver and getting the url
        driver = webdriver.Firefox(fp, options=options)
        sleep(5)
        return driver

    def account_type(self, driver, account):
        # account type is the right url to access
        if account == PAYMENTS:
            driver.get('http://web.transparencia.pe.gov.br/despesas/despesa-geral/')
        else:
            driver.get('http://web.transparencia.pe.gov.br/receitas/painel-de-receitas/')
        sleep(25)

        # removing the fixed bar and selecting iframe
        topo = driver.find_element_by_class_name('topo-fixed')
        driver.execute_script("arguments[0].style.position='absolute';", topo)
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

    def select_year(self, driver, year):
        ops = driver.find_elements_by_xpath("//*[@id='html_anotabelaselector']/select")
        driver.execute_script("arguments[0].style.display='inline';", ops[0])

        sel_year_options = driver.find_elements_by_xpath("//*[@id='html_anotabelaselector']/select/option")
        for option in sel_year_options:
            try:
                if option.text == str(year):
                    option.click()
                    print('Ano selecionado.')
                    sleep(10)
            except StaleElementReferenceException as e:
                print('resolver ano', e)

    def enable_options(self, driver):
        # making options visible - by each page refresh the options got hided.
        ops_xpath = '/html/body/main/section/div/div[5]/div/div/div[2]/div[1]/div[1]/div[4]/div/select'
        ops = driver.find_elements_by_xpath(ops_xpath)
        driver.execute_script("arguments[0].style.display='inline';", ops[0])
        options = driver.find_elements_by_xpath("//*[@id='html_selectugtabela']/select/option")
        return options

    def get_uge_list(self, driver):
        options = self.enable_options(driver)
        dpts = [option.text for option in options]
        return dpts

    def export_table(self, driver):
        btn_table = driver.find_element_by_xpath('//*[@id="exportTable"]')
        driver.execute_script('arguments[0].scrollIntoView(true);', btn_table)
        self.click_element(driver, btn_table)
        sleep(10)

    def click_element(self, driver, el):
        # sometimes, is necessary put focus in element before the click
        driver.execute_script("arguments[0].click();", el)

    def get_today(self):
        today = date.today().timetuple()
        today_str = '{}{}{}'.format(today.tm_mday, today.tm_mon, today.tm_year)
        return today_str

    def rename_file(self, uge, year):
        uge = re.sub('[!@#$/]', '-', uge)
        filename_path = PATH_PAYMENTS + r'Despesa_' + self.get_today() + '.xls'
        new_filename = PATH_PAYMENTS + uge + '_' + self.get_today() + '_' + str(year) + '_despesa.xls'
        try:
            os.rename(filename_path, new_filename)
        except FileNotFoundError as e:
            print(e)
        except FileExistsError as e:
            print(e)
        finally:
            sleep(10)

    def verify_files(self):
        files_list = os.listdir(PATH_PAYMENTS)
        for file in files_list:
            if 'Despesa' in file:
                os.remove(PATH_PAYMENTS + file)

    def despesas(self, year):
        driver = self._get_driver()
        self.account_type(driver, PAYMENTS)
        self.select_year(driver, year)
        uge = self.get_uge_list(driver)
        for ug in uge:
            self.verify_files()
            print('Gerando {} de {}.'.format(uge.index(ug), len(uge)))
            ops = self.enable_options(driver)
            for op in ops:
                if op.text == ug:
                    op.click()
                    print('Extraindo planilha {}.'.format(ug))
                    break
            sleep(10)
            self.export_table(driver)
            self.rename_file(ug, year)
        driver.close()
        print('Extração concluída.')
