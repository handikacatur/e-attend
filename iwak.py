from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import datetime
import time

print('\n>>> E-ATTEND UNTUK E-LEARNING v0.1 (beta) <<<')

username = input('Username: ')
password = getpass()
links = []

driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://sso.unej.ac.id/cas/login?service=https%3A%2F%2Fmmp.unej.ac.id%2Flogin%2Findex.php')

username_form = driver.find_element_by_id('username')
password_form = driver.find_element_by_id('password')

username_form.send_keys(username)
password_form.send_keys(password)

driver.find_element_by_name('submit').click()

events = driver.find_elements_by_class_name('event')

for i in events:
    if i.find_element_by_class_name('date').find_element_by_xpath('./a').text == 'Today':
        links.append(i.find_element_by_xpath('./a').get_attribute('href'))
    # links.append(i.find_element_by_xpath('./a').get_attribute('href'))

def status_matkul(status):
    print('\n\n>>> ', end='')
    print(driver.find_element_by_class_name('page-header-headings').find_element_by_xpath('./h1').text, end=' : ')
    print(status)

def absenin():
    driver.find_elements_by_class_name('statuscol')[1].find_element_by_xpath('./a').click()
    driver.find_element_by_xpath('//input[@name="status"][1]').click()
    driver.find_element_by_xpath('//input[@name="submitbutton"]').click()

for i in links:
    driver.get(i)
    try:
        wait(driver, 120).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'event'))
        )
    except:
        print('Not Connected')
        driver.close()
    finally:
        jam = 0
        menit = 0
        if ':' in driver.find_element_by_class_name('date').text[7:9]:
            if 'PM' in driver.find_element_by_class_name('date').text[12:14]:
                jam = int('0' + driver.find_element_by_class_name('date').text[7]) + 12
                menit = int(driver.find_element_by_class_name('date').text[9:11])
            else:
                jam = int('0' + driver.find_element_by_class_name('date').text[7])
                menit = int(driver.find_element_by_class_name('date').text[9:11])
        else:
            jam = int(driver.find_element_by_class_name('date').text[7:9])
            menit = int(driver.find_element_by_class_name('date').text[10:12])
        target = datetime.datetime.combine(datetime.date.today(), datetime.time(hour = jam, minute = menit))

        driver.find_element_by_class_name('calendar_event_attendance').find_element_by_xpath('./a').click()

        now = datetime.datetime.now()

        if (target-now).total_seconds() > 0:
            status_matkul('Absen dimulai pukul ' + str(target))
            print('\nSantuy ya, ntar pas udah lebih 4 menit gw absenin')
            time.sleep((target-now).total_seconds() + 240)
            driver.refresh()
            if driver.find_elements_by_class_name('statuscol')[1].text == 'Present':
                status_matkul('Sudah Absen!')
            else:
                if driver.find_elements_by_class_name('statuscol')[1].find_element_by_xpath('./a').text == 'Submit attendance':
                    absenin()
                    if driver.find_elements_by_class_name('statuscol')[1].text == 'Present':
                        status_matkul('Sudah Absen!')
                    else:
                        print('\n>> Error absen dari mmp. Coba lu hubungin ketua kelas atau dosennya.')
                else:
                    print('\n>> Error absen dari mmp. Coba lu hubungin ketua kelas atau dosennya.')
        else:
            if driver.find_elements_by_class_name('statuscol')[1].text == 'Present':
                status_matkul('Sudah Absen')
            else:
                if driver.find_elements_by_class_name('statuscol')[1].find_element_by_xpath('./a').text == 'Submit attendance':
                    absenin()
                    if driver.find_elements_by_class_name('statuscol')[1].text == 'Present':
                        status_matkul('Sudah Absen!')
                    else:
                        print('\n>> Error absen dari mmp. Coba lu hubungin ketua kelas atau dosennya.')
                else:
                    print('\n>> Error absen dari mmp. Coba lu hubungin ketua kelas atau dosennya.')
                
                
print('\n>>> Udah ga ada absen buat hari ini. Jangan lupa besok jalanin gw lagi ya. Selamat bersantuy...')
print('\n\n>>> Program dihentikan <<<')
driver.close()