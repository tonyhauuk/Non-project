# -*- coding: utf-8 -*-

from time import sleep
from pywinauto.application import Application


class ControlApp:
    def __init__(self):
        self.appName = 'notepad.exe'
        # self.appName = r'C:\Program Files\Windows NT\Accessories\wordpad.exe'

    def startApp(self):
        self.app = Application().start(self.appName)


    def demoNotepad(self):
        self.app.UntitledNotepad.menu_select('帮助(&H)->关于记事本(&A)')
        sleep(2)
        ABOUT = u'关于“记事本”'
        OK = u'确定'
        self.app[ABOUT][OK].click()

        fileName = 'test7.txt'

        self.app.UntitledNotepad.Edit.type_keys('pywinauto Works! \n\n ', with_spaces = True, with_newlines = True)  # 在记事本窗口中写入内容，并换行
        self.app.UntitledNotepad.Edit.type_keys('第二行中文字符串', with_spaces = True, with_newlines = True)
        sleep(2)
        self.app['无标题-记事本'].MenuSelect('文件->另存为...')  # 打开记事本的另存为窗口
        self.app['另存为']['edit'].TypeKeys(fileName)  # 将文件名键入
        self.app['另存为']['保存'].click()  # 更改文件名之后保存

        self.app.UntitleNotepad.menu_select('文件->退出')  # 选择菜单退出



    def demoWordpad(self):
        self.app.wordpadclass.RICHEDIT50W.type_keys('this is wordpad.exe', with_spaces = True, with_newlines = True)

        sleep(1)
        self.app.wordpadclass.RICHEDIT50W.TypeKeys('^a')
        sleep(1)
        self.app.wordpadclass.RICHEDIT50W.RightClickInput(coords=(500, 100))
        sleep(1)
        self.app.wordpadclass.RICHEDIT50W.ClickInput(coords=(550, 150))
        self.app.wordpadclass.RICHEDIT50W.TypeKeys('^s')

        fileName = 'test6.rtf'
        # self.app['文档-写字板'].MenuSelect('文件->另存为...')  # 打开写字板的另存为窗口
        # self.app['另存为']['edit'].TypeKeys(fileName)  # 将文件名键入
        # self.app['另存为']['保存'].click()  # 更改文件名之后保存
        # self.app.wordpadclass.menu_select('文件->退出')  # 选择菜单退出
        # self.app['记事本']['保存'].click()  # 保存写好的记事本


        saveDlg = self.app.window(title_re = u'保存为', class_name = '#32770')
        saveDlg.edit.TypeKeys(u'D:\\' + fileName)
        self.app[u'保存为'][u'保存(S)'].SetFocus()
        self.app[u'保存为'][u'保存(S)'].Click()


    def demoClass(self):
        self.app.Notepad.menu_select('帮助->关于记事本')

        about_dlg = self.app.window(title_re = u'关于', class_name = '#32770')  #
        print('-'*10, 'identifiers start','-'*10, '\n')
        about_dlg.print_control_identifiers()
        print('-'*10, 'identifiers finish','-'*10, '\n')
        self.app.window(title_re = u'关于“记事本”').window(title_re = u'确定').Click()
        sleep(.5)



    def printIdent(self):
        self.app.print_control_identifiers()

if __name__ == '__main__':
    app = ControlApp()
    app.startApp()

    # app.demoNotepad()
    # app.demoWordpad()
    app.demoClass()
