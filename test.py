import win10toast
import time
import sys

def toaster(msg):
    toast = win10toast.ToastNotifier()
    toast.show_toast('Python', msg[1])

toaster(sys.argv)

time.sleep(10)

toaster('Hello again')