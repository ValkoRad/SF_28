from time import sleep
from settings import *
from auth_page import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def test_001_vision(browser):  # тест 001 - общий вид формы (сохранить скриншот)
    form = AuthForm(browser)
    form.driver.save_screenshot('screen.jpg')



def test_002_by_phone(browser):  # тест 002 - проверка, что по-умолчанию выбрана форма авторизации по телефону
    form = AuthForm(browser)
    assert form.placeholder.text == 'Мобильный телефон'



def test_003_change_placeholder(browser):  # тест 003 - проверка автосмены "таб ввода"
    form = AuthForm(browser)

    form.username.send_keys(valid_phone)  # ввод телефона
    form.password.send_keys('_')
    sleep(5)
    assert form.placeholder.text == 'Мобильный телефон'

    form.username.send_keys(Keys.CONTROL, 'a')   # очистка поля логина
    form.username.send_keys(Keys.DELETE)
 
    form.username.send_keys(valid_email)  # ввод почты
    form.password.send_keys('_')
    sleep(5)
    assert form.placeholder.text == 'Электронная почта'

    form.username.send_keys(Keys.CONTROL, 'a')   # очистка поля логина
    form.username.send_keys(Keys.DELETE)

    form.username.send_keys('MyLogin')  # ввод логина
    form.password.send_keys('_')
    sleep(5)
    assert form.placeholder.text == 'Логин'



def test_004_positive_by_phone(browser):  # тест 004 - проверка позитивного сценария авторизации по телефону
    form = AuthForm(browser)

    form.username.send_keys(valid_phone)   # ввод телефона
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()
    assert form.get_current_url() != '/account_b2c/page'



def test_005_negative_by_phone(browser):  # тест 005 - проверка негативного сценария авторизации по телефону
    form = AuthForm(browser)

    form.username.send_keys('+1064564785')  # ввод некорректного телефона
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'



def test_006_positive_by_email(browser):  # тест 006 - проверка позитивного сценария авторизации по почте
    form = AuthForm(browser)

    form.username.send_keys(valid_email)  # ввод почты
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()
    assert form.get_current_url() != '/account_b2c/page'



def test_007_negative_by_email(browser):  # тест 007 - проверка негативного сценария авторизации по почте
    form = AuthForm(browser)

    form.username.send_keys('aa@aa.aa')  # ввод некоректной почты
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'



def test_008_get_code(browser):  # тест 008 - проверка получения временного кода на телефон и открытия формы для ввода кода
    form = CodeForm(browser)

    form.address.send_keys(valid_phone)   # ввод телефона

    sleep(30) # длительная пауза, предназначеная для ручного ввода капчи, при необходимости
    form.get_click()
    rt_code = form.driver.find_element(By.ID, 'rt-code-0')
    assert rt_code



def test_009_forgot_pass(browser):  # тест 009 - проверка перехода в форму восстановления пароля и её открытия
    form = AuthForm(browser)

    form.forgot.click()  # клик по надписи "Забыл пароль"
    sleep(5)
    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')
    assert reset_pass.text == 'Восстановление пароля'



def test_010_register(browser):  # тест 010 - проверка перехода в форму регистрации и её открытия
    form = AuthForm(browser)

    form.register.click()  # клик по надписи "Зарегистрироваться"
    sleep(5)
    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')
    assert reset_pass.text == 'Регистрация'



def test_011_agreement(browser):  # тест 011 - проверка открытия пользовательского соглашения
    form = AuthForm(browser)

    original_window = form.driver.current_window_handle
    form.agree.click()  # клик по надписи "Пользовательским соглашением" в подвале страницы
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    win_title = form.driver.execute_script("return window.document.title")
    assert win_title == 'User agreement'



def test_012_auth_vk(browser):  # тест 012 - проверка перехода по ссылке авторизации пользователя через вконтакте
    form = AuthForm(browser)
    form.vk_btn.click()
    sleep(5)
    assert form.get_base_url() == 'oauth.vk.com'



def test_013_auth_ok(browser):  # тест 013 - проверка перехода по ссылке авторизации пользователя через одноклассники
    form = AuthForm(browser)
    form.ok_btn.click()
    sleep(5)
    assert form.get_base_url() == 'connect.ok.ru'



def test_014_auth_mailru(browser):  # тест 014 - проверка перехода по ссылке авторизации пользователя через майлру
    form = RegistrPage(browser)
    form.mailru_btn.click()
    sleep(5)
    assert form.get_base_url() == 'connect.mail.ru'



def test_015_auth_ya(browser):  # тест 015 - проверка перехода по ссылке авторизации пользователя через яндекс
    form = AuthForm(browser)
    form.ya_btn.click()
    sleep(5)
    assert form.get_base_url() == 'passport.yandex.ru'
