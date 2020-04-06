from selenium import webdriver
from getpass import getpass
import platform
import win10toast
import datetime
import time
import sys

print('\n>>> E-ATTEND UNTUK E-LEARNING v1.0 (beta) <<<')

username = ''
password = ''
links = []
sso = 'https://sso.unej.ac.id/cas/login?service=https%3A%2F%2Fmmp.unej.ac.id%2Flogin%2Findex.php'
driver = None

def toaster(msg):
    toast = win10toast.ToastNotifier()
    toast.show_toast('E-Attendance', str(msg))

def initChrome():
    global driver

    # initiate headless chrome
    toaster('Initiating headless Chrome')
    if 'Windows' in platform.system():
        driver = webdriver.PhantomJS('./webdrivers/phantomjs.exe')
    elif 'Linux' in platform.system():
        driver = webdriver.PhantomJS('./webdrivers/phantomjs')

def getUserInfo(inf):
    global username
    global password
    username = inf[1]
    password = inf[2]

def doLogin():
    # getting the username and password forms
    username_form = driver.find_element_by_id('username')
    password_form = driver.find_element_by_id('password')

    # sending keys to username and password forms
    username_form.send_keys(username)
    password_form.send_keys(password)

    # click the login button
    driver.find_element_by_name('submit').click()

def loggingIn():
    logged_in = False
    
    while logged_in == False:
        if 'Single Sign On' in getTitle():
            doLogin()
            if 'Dashboard' in getTitle():
                name = driver.find_element_by_class_name('usermenu').find_element_by_xpath('./ul/li/a').text
                print('\n>>> %s: BERHASIL LOGIN <<<' %name)
                toaster('%s BERHASIL LOGIN' %name)
                logged_in = True
            else:
                print('\n!!! LOGIN GAGAL !!!')
                toaster('!!! LOGIN GAGAL !!!')
                if 'Bad Gateway' in getTitle():
                    print('\nServer sedang error.')
                    toaster('Server error')
                else:
                    print('\nUsername atau password salah.')
                    toaster('Username atau password salah')
                print('\nProgram dihentikan...')
                driver.close()
                break
        elif 'Bad Gateway' in getTitle():
            toaster('Bad Gateway')
        else:
            print('>>> Gagal login. Mencoba login kembali')
            driver.refresh()
    

def getTitle():
    return driver.title

def getEvents():
    global links
    events = driver.find_elements_by_class_name('event')

    for i in events:
        if i.find_element_by_class_name('date').find_element_by_xpath('./a').text == 'Today':
            links.append(i.find_element_by_xpath('./a').get_attribute('href'))

    toaster('Event hari ini berhasil diambil')

def status_matkul(status):
    matkul = driver.find_element_by_class_name('page-header-headings').find_element_by_xpath('./h1').text

    print('\n\n>>> ', end='')
    print(matkul, end=' : ')
    print(status)
    toaster('%s : %s' %(matkul, status))

def absenin():
    driver.find_elements_by_class_name('statuscol')[1].find_element_by_xpath('./a').click()
    driver.find_element_by_xpath('//input[@name="status"][1]').click()
    driver.find_element_by_xpath('//input[@name="submitbutton"]').click()

def getStatus():
    if driver.find_elements_by_class_name('statuscol')[1].text == 'Present':
        status_matkul('Sudah Absen!')
    else:
        if driver.find_elements_by_class_name('statuscol')[1].find_element_by_xpath('./a').text == 'Submit attendance':
            absenin()
            if driver.find_elements_by_class_name('statuscol')[1].text == 'Present':
                status_matkul('Sudah Absen!')
            else:
                print('\n>> Error absen dari mmp. Coba lu hubungin ketua kelas atau dosennya.')
                toaster('Error absen dari mmp. Coba lu hubungin ketua kelas atau dosennya.')
        else:
            print('\n>> Error absen dari mmp. Coba lu hubungin ketua kelas atau dosennya.')
            toaster('Error absen dari mmp. Coba lu hubungin ketua kelas atau dosennya.')

def checkAttendance():
    global links
    hour = 0
    minutes = 0
    error = True

    for i in links:
        driver.get(i)
        
        if ':' in driver.find_element_by_class_name('date').text[7:9]:
            if 'PM' in driver.find_element_by_class_name('date').text[12:14]:
                hour = int('0' + driver.find_element_by_class_name('date').text[7]) + 12
                minutes = int(driver.find_element_by_class_name('date').text[9:11])
            else:
                hour = int('0' + driver.find_element_by_class_name('date').text[7])
                minutes = int(driver.find_element_by_class_name('date').text[9:11])
        else:
            hour = int(driver.find_element_by_class_name('date').text[7:9])
            minutes = int(driver.find_element_by_class_name('date').text[10:12])

        target = datetime.datetime.combine(datetime.date.today(), datetime.time(hour = hour, minute = minutes))
        now = datetime.datetime.now()

        driver.find_element_by_class_name('calendar_event_attendance').find_element_by_xpath('./a').click()

        if (target-now).total_seconds() > 0:
            status_matkul('Absen dimulai pada ' + str(target))
            print('\nSantuy ya, ntar pas udah lebih 4 menit gw absenin')
            toaster('Santuy ya, ntar pas udah lebih 4 menit gw absenin')

            time.sleep((target-now).total_seconds() + 240)

            driver.refresh()

            while error == True:
                if 'Sign On' in getTitle():
                    doLogin()
                else:
                    getStatus()
                    error = False
        else:
            getStatus()
                
toaster('program is running on background')

# getting user info
getUserInfo(sys.argv)

# initiate the driver
initChrome()

# opening sso login
driver.get(sso)

# logging in
loggingIn()

# getting events
getEvents()

# checking attendance in events
checkAttendance()

# end
print('\n>>> Udah ga ada absen buat hari ini. Jangan lupa besok jalanin gw lagi ya. Selamat bersantuy...')
print('\n\n>>> Program dihentikan <<<')
toaster('Udah ga ada absen buat hari ini. Jangan lupa besok jalanin gw lagi ya. Selamat bersantuy...')
toaster('PROGRAM DIHENTIKAN')
driver.close()