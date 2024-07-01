from PyQt5 import QtWidgets,uic
import sys, resorce
from sub import *

app = QtWidgets.QApplication([])


login = uic.loadUi("login.ui")
Home =  uic.loadUi("main_page.ui")
detect = uic.loadUi("detect.ui")


def gui_login():
    name = login.lineEdit.text()
    password = login.lineEdit_3.text()
    if len(name)==0 or len(password)==0:
        login.label_8.setText('please enter your name and password')
        
    elif name != 'santhosh' or password != '1234': 
        login.label_8.setText('wrong password')   
        
    elif name == 'santhosh' and password == '1234':
        gui_Home()   
        
    else:
        gui_login()    
        
        
        

def gui_Home():
    login.hide()
    Home.show() 
      
    
def gui_detect():
    Home.hide()
    combined_function() 
    
        
        
   
def gui_go():
    detect.hide()
    Home.show() 
             
        
login.pushButton.clicked.connect(gui_login)  
Home.taxi2.clicked.connect(gui_detect)     
   

detect.Home.clicked.connect(gui_go) 


login.show()
app.exec()