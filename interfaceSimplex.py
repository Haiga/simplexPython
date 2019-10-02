import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import tkinter
from tkinter import messagebox

import simplex

def definirScrollBar(layout):
        widgetTemp = QtWidgets.QWidget()
        widgetTemp.setLayout(layout)
        areaRolagem = QScrollArea()
        areaRolagem.setWidget(widgetTemp)
        areaRolagem.verticalScrollBar()
        layoutTemp = QVBoxLayout()
        layoutTemp.addWidget(areaRolagem)
        return layoutTemp
    
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Xelpmis'
        self.left = 50
        self.top = 50
        self.width = 550
        self.height = 650
        self.initUI()

    def closeEvent(self, event):
        self.widgetsClose()
        self.messageForUser.destroy()
        event.accept()

    def widgetsClose(self):
        self.widget1.close()
        self.widget2.close()
        self.widget3.close()
        self.widget4.close()
        self.messageForUser.destroy()
        self.messageForUser = tkinter.Tk()

    def setVarSincronization(self):
        self.numVarWidget1 = 1
        self.numRestricWidget1 = 1
        self.numVarWidget2 = 0
        self.numRestricWidget2 = 0
        self.numVarWidget3 = 0
        self.numRestricWidget3 = 0
        self.numVarWidget4 = 0
        self.numRestricWidget4 = 0

    def defineTypes(self):
        self.widget1 = QtWidgets.QDialog()
        self.widget2 = QtWidgets.QDialog()
        self.widget3 = QtWidgets.QDialog()
        self.widget4 = QtWidgets.QDialog()
        
        self.messageForUser = tkinter.Tk()
        
        self.labels = {}
        self.labels2 = {}
        self.labels3 = {}
        self.labels4 = {}
        self.labelsF = {}
        self.labelsx = {}

    def initUserInteraction(self):
        self.defineTypes()
        self.setVarSincronization()
        self.criarTelaVariaveis()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        
        self.button = QLabel('MÉTODO SIMPLEX', self)
        self.button.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.button.setAlignment(Qt.AlignCenter)
        self.button.resize(500,40)
        self.button.move(25,10)
        
        self.button1 = QPushButton('Número de Variáveis e Restrições', self)
        self.button1.resize(250,30)
        self.button1.move(150,60)

        self.button2 = QPushButton('Variáveis Livres', self)
        self.button2.resize(250,30)
        self.button2.move(150,90)

        self.button3 = QPushButton('Matriz de Restrições', self)
        self.button3.resize(250,30)
        self.button3.move(150,120)

        self.button4 = QPushButton('Função Objetivo', self)
        self.button4.resize(250,30)
        self.button4.move(150,150)

        self.button5 = QPushButton('Obter Resultado',self)
        self.button5.resize(250,30)
        self.button5.move(150,180)
        
        
        self.button1.clicked.connect(self.mostrarTelaVariaveis)
        self.button2.clicked.connect(self.criarTelaVarLivres)
        self.button3.clicked.connect(self.criarTelaMatriz)
        self.button4.clicked.connect(self.criarTelaFuncao)
        self.button5.clicked.connect(self.iniciarVerificacaoParaCalcular)

        self.show()
        self.initUserInteraction()
        

    def mostrarTelaVariaveis(self):
        self.widgetsClose()
        self.widget1.move(70,285)
        self.widget1.show()
        
    def criarTelaVariaveis(self):
        self.widgetsClose()
        layout = QtWidgets.QGridLayout()

        #Força o usuário a digitar apenas números maiores ou iguais 1
        #pois o número de variáveis e retrições devem ser inteiros maiores ou iguais a 1

        #Nota: Verificar depois um número limite para esses campos
        #Possíveis problemas: Estouro de memória se o valor for muito grande
        integerValidator = QRegExpValidator(QRegExp("[1-9]{1}[0-9]{1,20}"));

        self.labels[(0,0)] = QLabel('Número de Variáveis:')
        self.labels[(0,1)] = QLineEdit()
        self.labels[(0,1)].setMaximumWidth(50)
        self.labels[(0,1)].setText('1')
        self.labels[(0,1)].setValidator(integerValidator)

        self.labels[(1,0)] = QLabel('Número de restrições:')
        self.labels[(1,1)] = QLineEdit()
        self.labels[(1,1)].setMaximumWidth(50)
        self.labels[(1,1)].setText('1')
        self.labels[(1,1)].setValidator(integerValidator)
        
        layout.addWidget(QLabel('Informe:'),0,0, 2, 0)
        layout.addWidget(QLabel(' '), 0, 0)
        layout.addWidget(QLabel(' '), 1, 0)
 
        layout.addWidget(QLabel(' '), 0, 1)
        layout.addWidget(QLabel(' '), 1, 1)
        
        layout.addWidget(self.labels[(0, 0)], 3, 0)
        layout.addWidget(self.labels[(0, 1)], 3, 1)
        layout.addWidget(self.labels[(1, 0)], 4, 0)
        layout.addWidget(self.labels[(1, 1)], 4, 1)
        
        self.widget1.setLayout(layout)
        self.widget1.setWindowTitle("Variáveis e Restrições")
        self.widget1.move(70,285)
        self.widget1.show()
        
    def mostrarTelaFuncao(self):
        self.widgetsClose()
        self.widget4.move(70,285)
        self.widget4.show()


        
    def criarTelaFuncao(self):
        self.widgetsClose()

        #Problema: Usuário não digita nada para número de Variáveis ou número de Restrições
        #Mandamos ele novamente para essa tela, até que informe esse valor

        #Possibilidade: Colocar o label vermelho, ou escrever uma mensagem abaixo informando-o

        #Organização: Separar esse tratamento de exceção dessa função(já que é usada em outra parte)
        try:
            self.numVarWidget1 = int(self.labels[(0,1)].text())
            self.numRestricWidget1 = int(self.labels[(1,1)].text())
        except:
            self.mostrarTelaVariaveis()
            return

        #Caso o usuário clique novamente no botão(sem ter alterado o número de Variáveis)
        #Nesse caso não precisamos recriar todo o label
        if ((self.numVarWidget4==self.numVarWidget1)):
            self.mostrarTelaFuncao()
            return

        numVariaveis = self.numVarWidget1
        self.numVarWidget4 = numVariaveis

        #Força o usuário a digitar apenas números (reais)
        floatValidate = QRegExpValidator(QRegExp("[+\-]?[0-9]{1,20}\.[0-9]{1,20}"));

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QLabel('Informe a função:'),0,0, 4, 0)
        for i in range(3):
            layout.addWidget(QLabel(' '),i+1,0)
            layout.addWidget(QLabel(' '),i+1,1)
            
        for j in range(2):
            for i in range(numVariaveis+1):
                if(i==0) and (j==0):
                    self.labelsF[(i,j)] = QLabel(' ')
                elif(j==0):
                    self.labelsF[(i,j)] = QLabel('X<SUB>%d'%((i)))
                elif(i==0):
                    self.labelsF[(i,j)] = QLabel('Z = ')
                else:
                    self.labelsF[(i,j)] = QLineEdit()
                    self.labelsF[(i,j)].setMaximumWidth(50)
                    self.labelsF[(i,j)].setText('0')
                    self.labelsF[(i,j)].setValidator(floatValidate)
                layout.addWidget(self.labelsF[(i,j)],j+3,i)
                
        self.labelsF[(0,2)] = QComboBox()
        self.labelsF[(0,2)].addItem("Máximo")
        self.labelsF[(0,2)].addItem("Mínimo")
        
        layout.addWidget(self.labelsF[(0,2)],2 + 3,0)

        self.widget4 = QtWidgets.QDialog()
        self.widget4.setLayout(definirScrollBar(layout))
        self.widget4.setWindowTitle("Função")

        self.widget4.move(70,285)
        self.widget4.show()

    
    def mostrarTelaVarLivres(self):
        self.widgetsClose()
        self.widget2.move(70,285)
        self.widget2.show()

    def criarTelaVarLivres(self):
        self.widgetsClose()

        #Problema: Usuário não digita nada para número de Variáveis ou número de Restrições
        #Mandamos ele novamente para essa tela, até que informe esse valor
        try:
            self.numVarWidget1 = int(self.labels[(0,1)].text())
            self.numRestricWidget1 = int(self.labels[(1,1)].text())
        except:
            self.mostrarTelaVariaveis()
            return

        #Caso o usuário clique novamente no botão(sem ter alterado o número de Variáveis)
        #Nesse caso não precisamos recriar todo o label
        
        if (self.numVarWidget2==self.numVarWidget1):
            self.mostrarTelaVarLivres()
            return

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QLabel('Informe quem é variável Livre:'),0,0, 4, 0)
        
        numVariaveis = int(self.labels[(0,1)].text())
        self.numVarWidget2 = numVariaveis
        
        for i in range(3):
            layout.addWidget(QLabel(' '),i+1,0)
            layout.addWidget(QLabel(' '),i+1,1)
        for i in range(numVariaveis):
            self.labels2[(i,0)] = QLabel('X<SUB>%d'%((i)+1))
            layout.addWidget(self.labels2[(i,0)],i+3,0)
            self.labels2[(i,1)] = QComboBox()
            self.labels2[(i,1)].addItem("Não")
            self.labels2[(i,1)].addItem("Sim")
            layout.addWidget(self.labels2[(i,1)],i+3,1)
        
        self.widget2 = QtWidgets.QDialog()
        self.widget2.setLayout(definirScrollBar(layout))
        self.widget2.setWindowTitle(" ")

        self.widget2.setWindowTitle("Variáveis Livres")
        self.widget2.move(70,285)
        self.widget2.show()

    def mostrarTelaMatriz(self):
        self.widgetsClose()
        self.widget3.move(70,285)
        self.widget3.show()

    def criarTelaMatriz(self):
        self.widgetsClose()
        try:
            self.numVarWidget1 = int(self.labels[(0,1)].text())
            self.numRestricWidget1 = int(self.labels[(1,1)].text())
        except:
            self.mostrarTelaVariaveis()
            return
        
        if not((self.numVarWidget3!=self.numVarWidget1) or (self.numRestricWidget3!=self.numRestricWidget1)):
            self.mostrarTelaMatriz()
            return

        floatValidate = QRegExpValidator(QRegExp("[+\-]?[0-9]{1,20}\.[0-9]{1,20}"));


        numVariaveis = int(self.labels[(0,1)].text())
        numRestricoes = int(self.labels[(1,1)].text())

        self.numRestricWidget3 = numRestricoes
        self.numVarWidget3 = numVariaveis
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(QLabel('Informe as restrições:'),0,0, 4, 0)
        for i in range(3):
            layout.addWidget(QLabel(' '),i+1,0)
            layout.addWidget(QLabel(' '),i+1,1)
        
        for i in range(numRestricoes + 1):
            for j in range(numVariaveis + 2):
                if(j==numVariaveis) and (i!=0):
                    self.labels3[(i,j)] = QComboBox()
                    self.labels3[(i,j)].addItem("≤")
                    self.labels3[(i,j)].addItem("=")
                    self.labels3[(i,j)].addItem("≥")
                elif(i!=0) and (j!= numVariaveis + 1):
                    self.labels3[(i,j)] = QLineEdit()
                    self.labels3[(i,j)].setMaximumWidth(50)
                    self.labels3[(i,j)].setText('0')
                    self.labels3[(i,j)].setValidator(floatValidate)
                elif(i==0) and (j<numVariaveis):
                    self.labels3[(i,j)] = QLabel('X<SUB>%d'%((j)+1))
                elif(i==0) and (j == numVariaveis ):
                    self.labels3[(i,j)] = QLabel(' ')
                elif(i==0) and (j == numVariaveis+1):
                    self.labels3[(i,j)] = QLabel('b')
                else:
                    self.labels3[(i,j)] = QLineEdit()
                    self.labels3[(i,j)].setMaximumWidth(50)
                    self.labels3[(i,j)].setText('0')
                    self.labels3[(i,j)].setValidator(floatValidate)
                self.labels3[(i,j)].setMaximumWidth(50)
                layout.addWidget(self.labels3[(i,j)],i+3,j)

        
        self.widget3 = QtWidgets.QDialog()
        self.widget3.setLayout(definirScrollBar(layout))
        self.widget3.setWindowTitle("Restrições")

        self.widget3.move(70,285)
        self.widget3.show()     

        
    def iniciarVerificacaoParaCalcular(self):
        self.widgetsClose()
        try:
            self.numVarWidget1 = int(self.labels[(0,1)].text())
            self.numRestricWidget1 = int(self.labels[(1,1)].text())
        except:
            self.mostrarTelaVariaveis()
            return

        if ((self.numVarWidget2!=self.numVarWidget1)):
            self.messageForUser.iconify()
            messagebox.showinfo("Information","Você precisa atualizar as Variáveis Livres")
            self.messageForUser.iconify()
            self.criarTelaVarLivres()
            return
        if ((self.numVarWidget3!=self.numVarWidget1) or (self.numRestricWidget3!=self.numRestricWidget1)):
            self.messageForUser.iconify()	
            messagebox.showinfo("Information","Você precisa atualizar as Restrições")
            self.messageForUser.iconify()
            self.criarTelaMatriz()
            return
        if ((self.numVarWidget4!=self.numVarWidget1)):
            self.messageForUser.iconify()	
            messagebox.showinfo("Information","Você precisa atualizar a Função")
            self.messageForUser.iconify()	
            self.criarTelaFuncao()
            return
        self.obterResultados()

    def obterResultados(self):
        numVariaveis = int(self.labels[(0,1)].text())
        numRestricoes = int(self.labels[(1,1)].text())

        
        if(self.labelsF[(0,2)].currentIndex()==0):
            maxORmin = 1
        else:
            maxORmin = -1

        
        variaveisLivres = simplex.criar_vetor(numVariaveis)
        for i in range(numVariaveis):
            if(self.labels2[(i,1)].currentIndex()==0):
                variaveisLivres[i] = 0
            else:
                variaveisLivres[i] = 1


        funcao = simplex.criar_vetor(numVariaveis)      
        for i in range(numVariaveis):
            #Assumo como zero nesse caso, pois é conveniente
            try:
                funcao[i] = float(self.labelsF[(i+1,1)].text())
            except:
                funcao[i] = 0


        condicoes = simplex.criar_vetor(numRestricoes)
        for i in range(numRestricoes):
            if(self.labels3[(i+1,numVariaveis)].currentIndex() == 0):
                condicoes[i] = 0
            elif(self.labels3[(i+1,numVariaveis)].currentIndex() == 1):
                condicoes[i] = 2
            else:
                condicoes[i] = 1
        
        matrizRestricoes = simplex.criar_matriz(numRestricoes, numVariaveis + 1)
        for i in range(numRestricoes + 1):
            for j in range(numVariaveis + 2):
                if(j==numVariaveis) and (i!=0):
                    a=2
                elif(i!=0) and (j!= numVariaveis + 1):
                    #Assumo como zero nesse caso, pois é conveniente
                    try:
                        matrizRestricoes[i-1][j] = float(self.labels3[(i,j)].text())
                    except:
                        matrizRestricoes[i-1][j] = 0
                elif(i==0) and (j<=numVariaveis):
                    a=2
                else:
                    #Assumo como zero nesse caso, pois é conveniente
                    try:
                        matrizRestricoes[i-1][j-1] = float(self.labels3[(i,j)].text())
                    except:
                        matrizRestricoes[i-1][j-1] = 0

        resultado = simplex.obterM(numVariaveis, numRestricoes,funcao, maxORmin, variaveisLivres, matrizRestricoes, condicoes)
        #tirar parametro numVariaveis, numRestricoes
        #retorno da função par chave, var folga, var livres,  x1, x2 , x3 ...
        #message for user
        # ou usar algo novo ...

        self.messageForUser.iconify()	
        messagebox.showinfo("Information",resultado)
        self.messageForUser.iconify()	

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
