import tkinter
from tkinter import messagebox

def arredondar(num):
    return float( '%g' % ( num ) )



def mostrar_matriz(matriz, n_linhas, n_colunas):
    for i in range(n_linhas):
        for j in range(n_colunas):
            print(arredondar(matriz[i][j])," ", end="")
        print ('\n')
    print ('\n')

def criar_vetor(tamanho):
    vetor = []
    for i in range(tamanho):
        vetor.append(0)
    return vetor

def criar_matriz(n_linhas, n_colunas):
    matriz = []
    for i in range(n_linhas):
        linha = []
        for j in range(n_colunas):
            linha.append(0)
        matriz.append(linha)
    return matriz

def posicaoMax(arranjo):
    for j in range(len(arranjo)):
        if arranjo[j]==max(arranjo):
            return j

def posicaoMin(arranjo):
    for j in range(len(arranjo)):
        if (arranjo[j]==min(arranjo)):
            return j



def obterM(numVariaveis, numRestricoes, funcao, max_or_min, variaveisLivres, matrizRestricoes, condicoes):
    
    numVariaveisLivres = variaveisLivres.count(1)
    numVariaveisFolga = condicoes.count(0) + condicoes.count(1)
    numVariaveisA = condicoes.count(1) + condicoes.count(2)
    numColunas = numVariaveis + numVariaveisLivres + numVariaveisFolga + numVariaveisA + 1
    matrizMetodo = preecherMatriz(max_or_min, numVariaveis,funcao,variaveisLivres, numRestricoes, matrizRestricoes, condicoes, numColunas)
    matrizMetodoTemp = criar_matriz(numRestricoes + 2, numColunas)


    solNaoBasica = []
    solBasica = []

    varFolga = 0
    varA = 0

    for i in range(numRestricoes):
        if(condicoes[i]==0):
            solBasica.append(numVariaveis + numVariaveisLivres + varFolga)
            varFolga = varFolga + 1
        else:
            solBasica.append(numVariaveis + numVariaveisLivres + numVariaveisFolga + varA)
            varA = varA + 1

    for i in range(numColunas):
        if(i not in solBasica):
            solNaoBasica.append(i)

    if(numVariaveisA != 0):
        linha_referencia = numRestricoes + 1
    else:
        linha_referencia = 0
        ###
    multiplasSolucoes = 0
    solBasTemp = []
    solnaoBasTemp = []
    #matrizMetodoTemp = []
    if(funcao.count(0)==numVariaveis):
        return "Essa função só assume o valor: 0 (zero)"
    while(1):
        label: fimfase1
        minimo = min(matrizMetodo[linha_referencia][0:numColunas-1])#numColunas - numVariveisA
        coluna_minimo = posicaoMin(matrizMetodo[linha_referencia][0:numColunas-1])
        #mostrar_matriz(matrizMetodo,numRestricoes + 2, numColunas)
        if(minimo>=-1e-13):
            if(linha_referencia != 0) and (abs(matrizMetodo[linha_referencia][numColunas-1])<=1e-13):#Há solução
                linha_referencia = 0
                for i in range(numRestricoes + 2):
                    for j in range(varA):
                        matrizMetodo[i][numVariaveis + numVariaveisLivres + numVariaveisFolga + j] = 0
                goto :fimfase1
            elif(linha_referencia != 0):#Não Há solução
                #messagebox.showinfo("Information", "Não há solução")
                return "Não há solução"
                #break;
            else:#Mostrar solução#se alguma variável de decisão não-básica tem um valor 0 na fila Z, significa que existe outra solução# quest d
                
                if(multiplasSolucoes == 0):
                    multiplasSolucoes = 1
                    for i in solNaoBasica:
                        if(abs(matrizMetodo[0][i])<1e-13):
                            coluna_minimo = i
                            solBasTemp = solBasica[:]
                            solnaoBasTemp = solNaoBasica[:]
                            for i in range(numRestricoes +2):
                                for j in range(numColunas):
                                    matrizMetodoTemp[i][j] = matrizMetodo[i][j]
                           
                            multiplasSolucoes = 3
                            break
                if(multiplasSolucoes == 1):
                    return printSolut(max_or_min,matrizMetodo,numColunas, numVariaveis,numRestricoes, solBasica)
                    #break
                if(multiplasSolucoes == 2):
                    #messagebox.showinfo("Information", "Múltiplas Soluções")
                    return printMultiSolut(max_or_min,matrizMetodo, matrizMetodoTemp, numColunas, numVariaveis,numRestricoes, solBasica, solBasTemp)
                    #break
                #break# haverá esse break mas se não for multipla,se for multipla set coluna_minimo na mão 0 2 0/1 0 1... pega os dois e calcula a reta
        else:#verificar se pra baixo é tudo negativo, se sim ilimitado
            all_negative = 1
            for i in range(numRestricoes):
                if(matrizMetodo[1+i][coluna_minimo]>0):
                    all_negative = 0
            if(all_negative):
                if(coluna_minimo<numVariaveis) or (coluna_minimo>numVariaveis+numVariaveisLivres):
                    #messagebox.showinfo("Information", "Solução ilimitada")#Falta o se não é variável livre
                    return "Solução ilimitada \n"+printSolut(max_or_min,matrizMetodo,numColunas, numVariaveis,numRestricoes, solBasica)
                    #break;
                else:
                    return printSolut(max_or_min,matrizMetodo,numColunas, numVariaveis,numRestricoes, solBasica);
                    #break;
        
        if(multiplasSolucoes ==3):
            all_negative = 1
            for i in range(numRestricoes):
                if(matrizMetodo[1+i][coluna_minimo]>0):
                    all_negative = 0
            if(all_negative):
                return printSolut(max_or_min,matrizMetodo,numColunas, numVariaveis,numRestricoes, solBasica);
            multiplasSolucoes = 2
        divisao = criar_vetor(numRestricoes)
        for i in range(numRestricoes):
            if(matrizMetodo[i+1][numColunas-1]<=0) or (matrizMetodo[i+1][coluna_minimo]<=0):
                divisao[i] = float("inf")
            else:
                divisao[i] = matrizMetodo[i+1][numColunas-1]/matrizMetodo[i+1][coluna_minimo]

        linha_minimo = posicaoMin(divisao) + 1
        sai = 0
        for i in range(numRestricoes):
            if(matrizMetodo[linha_minimo][solBasica[i]]==1):
                sai = solBasica[i]
                break
        pivo = matrizMetodo[linha_minimo][coluna_minimo]
        for i in range(numColunas):
            matrizMetodo[linha_minimo][i] = matrizMetodo[linha_minimo][i]/pivo

        for i in range(numRestricoes + 2):
            if(i!=linha_minimo):
                temp = -1*matrizMetodo[i][coluna_minimo]
                for j in range(numColunas):
                    matrizMetodo[i][j] = matrizMetodo[i][j] + temp*matrizMetodo[linha_minimo][j]

        if(sai!=coluna_minimo):
            solBasica[solBasica.index(sai)] = coluna_minimo
            solNaoBasica[solNaoBasica.index(coluna_minimo)] = sai
                    
        
def preecherMatriz(max_or_min, numVariaveis,funcao,variaveisLivres, numRestricoes, matrizRestricoes, condicoes, numColunas):
    matrizMetodo = criar_matriz(numRestricoes + 2, numColunas)
    for i in range(numVariaveis):
        matrizMetodo[0][i] = max_or_min*funcao[i]*(-1)

    for i in range(numRestricoes):
        for j in range(numVariaveis+1):
            if(j == numVariaveis):
                matrizMetodo[i+1][numColunas-1] = matrizRestricoes[i][j]
            else:
                matrizMetodo[i+1][j] = matrizRestricoes[i][j]


    contVL = 0
    for j in range(numVariaveis):
        if(variaveisLivres[j]==1):
            for i in range(numRestricoes):
                matrizMetodo[i+1][numVariaveis + contVL] = matrizRestricoes[i][j]*(-1)
            contVL = contVL + 1

    contVF = 0
    for i in range(numRestricoes):
        if(condicoes[i]==0):
            matrizMetodo[i+1][numVariaveis +contVL + contVF] = 1
        elif(condicoes[i]==1):
            matrizMetodo[i+1][numVariaveis +contVL + contVF] = -1
        else:
            contVF = contVF -1
        contVF = contVF +1

    contVA = 0
    for i in range(numRestricoes):
        if(condicoes[i]!=0):
            matrizMetodo[i+1][numVariaveis +contVL + contVF + contVA] = 1
            contVA = contVA + 1

    for j in range(numVariaveis + contVL + contVF):
        soma = 0
        for i in range(numRestricoes):
            if(condicoes[i]!=0):
                soma = soma + matrizMetodo[i+1][j]
        matrizMetodo[numRestricoes + 1][j] = -1*soma

    soma = 0
    for i in range(numRestricoes):
        if(condicoes[i]!=0):
            soma = soma + matrizMetodo[i+1][numColunas -1]
    matrizMetodo[numRestricoes+1][numColunas-1] = -1*soma
    return matrizMetodo
    
        

def printSolut(max_or_min,matrizMetodo,numColunas, numVariaveis,numRestricoes, solBasica):#ainda falta reconverter as variáveis livres
    string = " "
    if(max_or_min==1):
        string = string + "Maximo: "
    else:
        string = string + "Minimo: "

    string = string + repr(matrizMetodo[0][numColunas-1]*max_or_min) + '\n'
    for i in range(numVariaveis):
        if(i in solBasica):
            for j in range(numRestricoes):
                if(matrizMetodo[j+1][i]==1):
                    string = string + "x" + repr(i+1) + "=" + repr(matrizMetodo[j+1][numColunas-1]) + '\n'
        else:
            string = string + "x" + repr(i+1) + "=" + "0" + '\n'
    #messagebox.showinfo("Information", string)
    return string
                    
def printMultiSolut(max_or_min,matrizMetodo, matrizMetodoTemp, numColunas, numVariaveis,numRestricoes, solBasica, solBasTemp):#ainda falta reconverter as variáveis livres
    string = "Múltiplas Soluções: \n"
    if(max_or_min==1):
        string = string + "Maximo: "
    else:
        string = string + "Minimo: "

    string = string + repr(matrizMetodo[0][numColunas-1]*max_or_min) + '\n'
    string = string + "("
    for i in range(numVariaveis):
        string = string + "X%d"%(i+1) +", "
    string = string[:-2] + ") = "
    string = string + "("
    result1 = [0]*numVariaveis
    

    for i in range(numVariaveis):
        if(i not in solBasica):
           string = string + "0, "
           
        else:
            for j in range(numRestricoes):
                if(matrizMetodo[j+1][i]==1):
                    string = string + repr(matrizMetodo[j+1][numColunas-1]) + ", "
                    result1[i] = matrizMetodo[j+1][numColunas-1]
                    break
    string = string[:-2]
    string = string + ") + T * ("
    
    for i in range(numVariaveis):
        if(i not in solBasTemp):
           string = string + repr(-result1[i])+", "
        else:
            for j in range(numRestricoes):
                if(matrizMetodoTemp[j+1][i]==1):
                    string = string + repr(matrizMetodoTemp[j+1][numColunas-1]-result1[i]) + ", "
                    break
    string = string[:-2]
    string = string +")"
    string = string + "\n com 0 ≤ T ≤ 1"
    #messagebox.showinfo("Information", string)
    return string
    

        

        
                
            
        






def setValores():
	numVariaveis = 3 #PAUSEHERE
	numRestricoes = 3#PAUSEHERE

	#Feito isso verificamos quais são livres, se é variável livre no vetor será 1
	variaveisLivres = criar_vetor(numVariaveis)
	variaveisLivres = [0,1, 0]#PAUSEHERE

	#Obtemos então a função que se deseja maximizar ou minimizar
	funcao = criar_vetor(numVariaveis)
	funcao = [1, 1, 2]#PAUSEHERE
	max_or_min = 1 #máximo set 1, mínimo set -1

	#Obtenção da matriz de restrições
	matrizRestricoes = criar_matriz(numRestricoes, numVariaveis + 1)#PAUSEHERE

	matrizRestricoes[0][0] = 1
	matrizRestricoes[0][1] = 2
	matrizRestricoes[0][2] = 0
	matrizRestricoes[0][3] = 10
	matrizRestricoes[1][0] = 3
	matrizRestricoes[1][1] = 4
	matrizRestricoes[1][2] = 1
	matrizRestricoes[1][3] = 20
	matrizRestricoes[2][0] = 1
	matrizRestricoes[2][1] = 1
	matrizRestricoes[2][2] = -1
	matrizRestricoes[2][3] = 15




	#Condição, adotaremos 0 como menor ou igual, 1 como maior ou igual e 2 como igual
	condicoes = criar_vetor(numRestricoes)#PAUSEHERE
	condicoes = [0,0,0]
	obterM(numVariaveis, numRestricoes,funcao, max_or_min, variaveisLivres, matrizRestricoes, condicoes)

