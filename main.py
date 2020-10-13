from PyQt5 import QtWidgets
from mydesign import Ui_MainWindow as win1 # импорт нашего сгенерированного файла
from reg import Ui_MainWindow as win2
from sqlalchemy import Column, Integer, String,MetaData,Table
from sqlalchemy import func, and_, or_, not_
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base

import sys




engine = create_engine('postgresql://postgres:steller0ff@localhost/Users')

meta = MetaData()
conn = engine.connect()



users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), unique=True),
    Column('password', String(500))
)

values =[]
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = win1()
        self.ui.setupUi(self)
        self.ui.button_reg.clicked.connect(self.Registration)
        self.ui.still_reg.clicked.connect(self.ChangeWindow)

    def Registration(self):
        login = self.ui.reg_login.text()
        password = self.ui.reg_pass.text()
        sec_password = self.ui.reg_pass1.text()
        if all([not i == "" for i in [login, password,sec_password]]):
            if password == sec_password:
                s = users.select().where(users.c.username == login)
                result = conn.execute(s)
                if not result.fetchone():
                    ins = users.insert().values(username=login, password=password)
                    conn.execute(ins)
                    self.ChangeWindow()
                else:
                    print("Такой пользователь уже существует")
            else:
                print("Пароли не совпадают")
        else:
            print("Не все поля заполнены")



    def ChangeWindow(self):
        self.hide()
        self.z1 = mywindow1()
        self.z1.show()





class mywindow1(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow1, self).__init__()
        self.ui = win2()
        self.ui.setupUi(self)
        self.ui.avtor_button.clicked.connect(self.Autorisation)


    def Autorisation(self):

        sign_login = self.ui.avtor_login.text()
        sign_password = self.ui.avtor_pass.text()
        if all ([not i == "" for i in [sign_login, sign_password]]):
            s = users.select().where(and_(users.c.username == sign_login, users.c.password == sign_password))
            result = conn.execute(s)
            if result.fetchone():
                print("Успешно вошли")
            else:
                print("Такого пользователя не существует")
        else:
            print("Не все поля заполнены")




app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())