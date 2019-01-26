#-*-coding:utf-8-*-

import time
import pyautogui
import re
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import QNetworkAccessManager,QNetworkRequest
from ui import Ui_Dialog
from replace_logic import *

class Dialog(QObject,Ui_Dialog):
    def __init__(self):
        QObject.__init__(self)
        Ui_Dialog.__init__(self)
    def init(self):
        self.pushButton_use.clicked.connect(self.pushButton_use_down)
        self.pushButton_revoke.clicked.connect(self.pushButton_revoke_down)
        
        self.radioButton_all_replace.clicked.connect(self.radioButton_all_replace_down)
        self.radioButton_line_replace.clicked.connect(self.radioButton_line_replace_down)
        self.radioButton_TorF.clicked.connect(self.radioButton_TorF_down)
        self.radioButton_LorR.clicked.connect(self.radioButton_LorR_down)
        self.radioButton_ai_replace.clicked.connect(self.radioButton_ai_replace_down)
        self.radioButton_deleate_head.clicked.connect(self.radioButton_deleate_head_down)
        self.radioButton_deleate_back.clicked.connect(self.radioButton_deleate_back_down)
        self.radioButton_add_head.clicked.connect(self.radioButton_add_head_down)
        self.radioButton_add_end.clicked.connect(self.radioButton_add_end_down)
        self.radioButton_beautiful_code.clicked.connect(self.radioButton_beautiful_code_down)
        self.radioButton_beautiful_end.clicked.connect(self.radioButton_beautiful_end_down)
        
        self.radioButton_add_last.clicked.connect(self.radioButton_add_last_down)
        self.radioButton_add_replace.clicked.connect(self.radioButton_add_replace_down)
        
        self.radioButton_ai_add_last.clicked.connect(self.radioButton_ai_add_last_down)
        self.radioButton_ai_add_replace.clicked.connect(self.radioButton_ai_add_replace_down)
        
        self.run_button.clicked.connect(self.replace_run)
        
        self.radioButton_all_replace_down()
        self.old = ''
        self.new = ''
    def replace_run(self):
        if self.radioButton_all_replace.isChecked():
            return self.replace_all()
        if self.radioButton_line_replace.isChecked():
            return self.replace_line()
        if self.radioButton_TorF.isChecked():
            return self.replace_TF()
        if self.radioButton_LorR.isChecked():
            return self.replace_LR()
        if self.radioButton_ai_replace.isChecked():
            return self.replace_ai()
        if self.radioButton_deleate_head.isChecked():
            return self.replace_head()
        if self.radioButton_deleate_back.isChecked():
            return self.replace_back()
        if self.radioButton_add_head.isChecked():
            return self.add_head()
        if self.radioButton_add_end.isChecked():
            return self.add_end()
        if self.radioButton_beautiful_code.isChecked():
            return self.beautiful_code()
        if self.radioButton_beautiful_end.isChecked():
            return self.beautiful_end()
    def replace_all(self):
        #覆盖所有
        old = str(self.text_textEdit.toPlainText())
        old_char = str(self.lineEdit_all_replace_old.text())
        new_char = str(self.lineEdit_all_replace_new.text())
        self.return_textEdit.setText(replace_all(old,old_char,new_char))
    def replace_line(self):
        #覆盖一行
        text = str(self.text_textEdit.toPlainText())
        old_char = str(self.lineEdit_line_old.text())
        new_char = str(self.lineEdit_line_new.text())        
        change_char = str(self.lineEdit_line_replace_char.text())
        auto_number = self.radioButton_add_last.isChecked()
        self.return_textEdit.setText(replace_one_by_one(text,old_char,new_char,auto_number,change_char))
    def replace_TF(self):
        #TF翻转
        text = str(self.text_textEdit.toPlainText())
        must_same = self.checkBox_TF_all_same.isChecked()
        self.return_textEdit.setText(turn_TF(text,must_same))
    def replace_LR(self):
        #左右互换
        text = str(self.text_textEdit.toPlainText())
        self.return_textEdit.setPlainText(turn_LR(text))
    def replace_head(self):
        #干掉开头空白
        text = str(self.text_textEdit.toPlainText())
        self.return_textEdit.setPlainText(deleate_head(text))
    def replace_back(self):
        #干掉结尾空白
        text = str(self.text_textEdit.toPlainText())
        self.return_textEdit.setPlainText(deleate_back(text))
    def add_head(self):
        #添加头
        text = str(self.text_textEdit.toPlainText())
        add_key = str(self.lineEdit_add_key.text())
        self.return_textEdit.setPlainText(add_by_head(text,add_key))
    def add_end(self):
        text = str(self.text_textEdit.toPlainText())
        add_key = str(self.lineEdit_add_key.text())
        self.return_textEdit.setPlainText(add_by_end(text,add_key))
    def beautiful_code(self):
        #关键字对齐
        text = str(self.text_textEdit.toPlainText())
        key = str(self.lineEdit_beautiful_code_key.text())
        self.return_textEdit.setPlainText(symbol_alignment(text,key))
    def beautiful_end(self):
        #结尾对齐
        text = str(self.text_textEdit.toPlainText())
        self.return_textEdit.setPlainText(end_alignment(text))        
    def replace_ai(self):
        #智能替换
        text = str(self.text_textEdit.toPlainText())
        old_char = str(self.lineEdit_ai_old.text())
        new_char = str(self.lineEdit_ai_new.text())        
        lines = text.split('\n')
        change_char = str(self.lineEdit_ai_replace_char.text())
        new = ''
        i = 1
        bc = -1
        for line in lines:
            bc_bak = 0
            for j in line:
                if j == ' ':
                    bc_bak = bc_bak + 1
                else:
                    break
            if bc == -1 :
                if old_char in line:
                    bc = bc_bak
                else:
                    pass
            else:
                if bc == bc_bak:
                    i = i + 1
            if self.radioButton_ai_add_last.isChecked():
                new = new + line.replace(old_char,new_char+str(i))+'\n'
            else:
                new_char_bak = new_char.replace(change_char, str(i))
                new = new + line.replace(old_char,new_char_bak)+'\n'
        self.return_textEdit.setText(new)
    #==========================按钮响应部分=============================
    def pushButton_use_down(self):
        self.old = self.text_textEdit.toPlainText()
        self.new = self.return_textEdit.toPlainText()
        self.text_textEdit.setPlainText(self.return_textEdit.toPlainText())
        self.return_textEdit.clear()
    #button lo
    def pushButton_revoke_down(self):
        self.text_textEdit.setPlainText(self.old)
        self.return_textEdit.setPlainText(self.new)
    #G 1
    def radioButton_all_replace_down(self):
        self.radioButton_set_group1(1)
    def radioButton_line_replace_down(self):
        self.radioButton_set_group1(2)
    def radioButton_TorF_down(self):
        self.radioButton_set_group1(3)
    def radioButton_LorR_down(self):
        self.radioButton_set_group1(4)
    def radioButton_ai_replace_down(self):
        self.radioButton_set_group1(5)
    def radioButton_deleate_head_down(self):
        self.radioButton_set_group1(6)
    def radioButton_deleate_back_down(self):
        self.radioButton_set_group1(7)
    def radioButton_add_head_down(self):
        self.radioButton_set_group1(8)
    def radioButton_add_end_down(self):
        self.radioButton_set_group1(9)
    def radioButton_beautiful_code_down(self):
        self.radioButton_set_group1(10)
    def radioButton_beautiful_end_down(self):
        self.radioButton_set_group1(11)
    def radioButton_set_group1(self,number=1):
        #全部替换
        flag = number == 1
        self.radioButton_all_replace.setChecked(flag)
        self.lineEdit_all_replace_old.setEnabled(flag)
        self.lineEdit_all_replace_new.setEnabled(flag)
        #逐行替换
        flag = number == 2
        self.radioButton_line_replace.setChecked(flag)
        self.lineEdit_line_old.setEnabled(flag)
        self.lineEdit_line_new.setEnabled(flag)
        self.radioButton_add_last.setEnabled(flag)
        self.radioButton_add_replace.setEnabled(flag)
        self.lineEdit_line_replace_char.setEnabled(flag)
        if flag:
            self.radioButton_add_last_down()
        else:
            self.radioButton_add_last.setChecked(flag)
            self.radioButton_add_replace.setChecked(flag)
        #TF翻转
        flag = number == 3
        self.radioButton_TorF.setChecked(flag)
        self.checkBox_TF_all_same.setEnabled(flag)
        #左右互换
        flag = number == 4
        self.radioButton_LorR.setChecked(flag)
        #智能替换
        flag = number == 5
        self.radioButton_ai_replace.setChecked(flag)
        self.lineEdit_ai_old.setEnabled(flag)
        self.lineEdit_ai_new.setEnabled(flag)
        self.radioButton_ai_add_last.setEnabled(flag)
        self.radioButton_ai_add_replace.setEnabled(flag)
        self.lineEdit_ai_replace_char.setEnabled(flag)
        if flag:
            self.radioButton_ai_add_last_down()
        else:
            self.radioButton_ai_add_last.setChecked(flag)
            self.radioButton_ai_add_replace.setChecked(flag)
        #清除开头空白
        flag = number == 6
        self.radioButton_deleate_head.setChecked(flag)
        #清除结尾空白
        flag = number == 7
        self.radioButton_deleate_back.setChecked(flag)
        
        flag = number in (8,9)
        self.lineEdit_add_key.setEnabled(flag)
        #开头追加
        flag = number == 8
        self.radioButton_add_head.setChecked(flag)
        #结尾追加
        flag = number == 9
        self.radioButton_add_end.setChecked(flag)
        #符号对齐
        flag = number == 10
        self.radioButton_beautiful_code.setChecked(flag)
        self.lineEdit_beautiful_code_key.setEnabled(flag)
        #结尾对齐
        flag = number == 11
        self.radioButton_beautiful_end.setChecked(flag)
        
    #G 2
    def radioButton_add_last_down(self):
        self.radioButton_set_group2(1)
    def radioButton_add_replace_down(self):
        self.radioButton_set_group2(2)
    def radioButton_set_group2(self,number=1):
        if number==1:
            flag = True
        else:
            flag = False
        self.radioButton_add_last.setChecked(flag)
        if number==2:
            flag = True
        else:
            flag = False
        self.radioButton_add_replace.setChecked(flag)
        self.lineEdit_line_replace_char.setEnabled(flag)
    #G 3
    def radioButton_ai_add_last_down(self):
        self.radioButton_set_group3(1)
    def radioButton_ai_add_replace_down(self):
        self.radioButton_set_group3(2)
    def radioButton_set_group3(self,number=1):
        if number==1:
            flag = True
        else:
            flag = False
        self.radioButton_ai_add_last.setChecked(flag)
        if number==2:
            flag = True
        else:
            flag = False
        self.radioButton_ai_add_replace.setChecked(flag)
        self.lineEdit_ai_replace_char.setEnabled(flag)        
if __name__=="__main__":
    app=QApplication(sys.argv)  
    widget=QWidget()  
    ui=Dialog()  
    ui.setupUi(widget)
    ui.init()
    widget.show()  
    sys.exit(app.exec_())  