"""
geraprova.py
Versão 1.0.2

Como executar:
Em Linux: Abra um terminal, navegue até o diretório deste arquivo e execute o seguinte comando
python3 geraprova.py

Este programa é licenciado como Software Livre: 
Você pode redistribuí-lo e/ou modificá-lo sob os termos da 
Licença Pública Geral GNU, conforme publicada pela Free Software Foundation, 
seja na versão 3 da Licença ou (a seu critério) qualquer versão posterior.
 
Este programa é distribuído na esperança de que seja útil, mas SEM NENHUMA GARANTIA; 
sem mesmo a garantia implícita de COMERCIABILIDADE ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. 
Veja a Licença Pública Geral GNU para mais detalhes.

Você deveria ter recebido uma cópia da Licença Pública Geral GNU junto com este programa. 
Se não recebeu, consulte https://www.gnu.org/licenses/.

ChangeLog
1.0.0 28/11/2023: Versão operacional
1.0.1 2/12/2023: Otimização de desempenho
1.0.2 5/12/2023: Inclusão de tratamento de erro em abertura de arquivo

Cid R. Andrade
 
Gera questões de múltipla escolha

O arquivo que é importado deve conter uma lista com diversas tuplas de questões
Cada tupla deve conter o enunciado e as cinco opções, sendo a primeira delas a correta
Exemplo: [("Enunciado", "Correta", "Distrator 1", "Distrator 2", "Distrator 3", "Distrator 4")]
 
"""

# A biblioteca ast é utilizada para avaliar se o arquivo externo está corretamente formatado
# como uma expressão Python válida
import ast
# A biblioteca random é utilizada para embaralhar questões e opções
import random

# Defina o arquivo com as questoes
# IMPORTANTE: Selecione aqui o arquivo com as questões da prova antes de executar esse código
fonte = "php.txt"

# Utilidades
abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Funções
# A função intInput recebe uma String e força uma entrada numérica inteira válida
def intInput(t):
	while True:
		try:
			v = int(input(t))
			return v
		except ValueError:
			print("Digite um número inteiro válido")

# Código principal

# Tenta abrir o arquivo com as questões
try:
	with open(fonte, 'r') as fonteRead:
		questoes = ast.literal_eval(fonteRead.read())

 # Pergunta quantos modelos de prova devem ser feitos
	numProvas = intInput("Deseja quantas provas: ")
	# Prossegue se a quantidade de provas for entre 1 e 26
	if 0 < numProvas <= len(abc):
		# Pergunta a quantidade de questões e valor de cada uma
		numQuest = intInput("Deseja quantas questões por prova: ")
		valQuest = input("Quanto vale cada questão: ")
		# Obtém a quantidade de questões disponíveis
		tamQuestoes = len(questoes)

		# Prossegue se a quantidade de questões desejada for menor ou igual à quantidade disponível
		if numQuest <= tamQuestoes:
			# A variável 'prova' conterá o texto das provas
			prova = ""

			# Cria as provas com nomes A, B, C e assim por diante
			for nome in abc[:numProvas]:
				# Obtém lista com números únicos das questões selecionadas
				questSelecionadas = random.sample(range(tamQuestoes-1), numQuest)
				# Escreve a identificação da prova (Ex.: 'Prova A') e a palavra 'Gabarito'
				prova += f"Prova {nome}\nGabarito\n"
				# A variável questDaProva conterá as questões da prova
				questDaProva = ""

				# Laço para tratar cada uma das questões
				for numQuestao in range(numQuest):
					# Escreve o número da questão e seu valor
					# Exemplo: 'QUESTÃO 1 - 0,25 PONTO'
					questDaProva += f"\nQUESTÃO {numQuestao + 1} - {valQuest} PONTO\n\n"
					# Escreve o enunciado da questão
					questDaProva += questoes[questSelecionadas[numQuestao]][0] + '\n\n'
					# Obtém uma lista com a ordem das opções
					ordemOpcoes = random.sample(range(1,6),5)
					# A variável 'opcoes' terá as opções da questão
					opcoes = ""

					# Laço para lidar com as opções da questão
					for identOpcao, j in enumerate(ordemOpcoes):
						# Escreve cada opção
						# Exemplo: '(A) blá, blá, blá'
						opcoes += f"({abc[identOpcao]}) {questoes[questSelecionadas[numQuestao]][j]}\n"

						# Se a opção for a primeira delas (com índice '1'), indicando ser a correta
						if (ordemOpcoes[j-1] == 1):
							# Escreva a entrada do gabarito da questão
							# Exemplo: '1: A'
							prova += f"{numQuestao + 1}: {abc[j-1]}\n"

					# Appenda na questão as opções dela
					questDaProva += opcoes

				# Appenda na prova todas as questões
				prova += "Questões\n" + questDaProva

				# Escreve arquivo 'prova.txt' com o conteúdo de todas as provas
				with open("prova.txt", 'w') as arqProva:
					arqProva.write(prova)

			print ("Prova armazenada no arquivo prova.txt")

		else:
			print("Tenho somente",tamQuestoes,"questões disponíveis")

	else:
		print ("Não é possível gerar", numProvas, "provas")

except FileNotFoundError:
	print (f"O arquivo {fonte} não foi encontrado!!!")
except Exception as e:
	print (f"Ocorreu um erro: {e}")