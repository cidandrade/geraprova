"""
#####################################################################
geraprova.py
Versão 1.0.5
Gera trechos de provas com questões de múltipla escolha

Autor: Cid R Andrade (profandrade@gmail.com)
Data da versão original: 28/novembro/2023
Data desta versão:       23/maio/2024

Como executar:
Em Linux: Abra um terminal, navegue até o diretório deste arquivo e 
          execute o seguinte comando
          python3 geraprova.py
Em Windows ou Mac: Não faço ideia

Este programa é licenciado como Software Livre: 
Você pode redistribuí-lo e/ou modificá-lo sob os termos da Licença 
Pública Geral GNU, conforme publicada pela Free Software Foundation, 
seja na versão 3 da Licença ou (a seu critério) qualquer versão 
posterior. Este programa é distribuído na esperança de que seja útil, 
mas SEM NENHUMA GARANTIA; sem mesmo a garantia implícita de 
COMERCIABILIDADE ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. 
Veja a Licença Pública Geral GNU para mais detalhes.
Você deveria ter recebido uma cópia da Licença Pública Geral GNU 
junto com este programa. Se não recebeu, consulte 
https://www.gnu.org/licenses/.

ChangeLog
1.0.0 28/11/2023: Versão operacional
1.0.1 2/12/2023:  Otimização de desempenho
1.0.2 5/12/2023:  Inclusão de tratamento de erro em abertura de 
                  arquivo
1.0.3 13/12/2023: Organiza nomes de variáveis, 
				  seleciona arquivo automaticamente
1.0.4 1º/5/2024:  Simplifica processos
1.0.5 23/5/2024: Ordena lista de arquivos disponíveis
 
O arquivo que é importado deve conter o enunciado das questões 
seguidos da alternativa correta e dos quatro distratores
Exemplo: 

Questão 1
Alternativa correta 1
Distrator 1 da questão 1
Distrator 2 da questão 1
Distrator 3 da questão 1
Distrator 4 da questão 1

#####################################################################
"""

import os
import random

# Utilidades
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Funções
# A função intInput recebe uma String e força uma entrada numérica 
# inteira válida
def intInput(p):
	while True:
		try:
			v = int(input(p))
			return v
		except ValueError:
			print("Digite um número inteiro válido")

# A função exibirMenu exibe um menu com opções
def exibirMenu(o, s):
	print (s)
	for i, st in enumerate(o, start=1):
		print (f"{i}. {st}")

# A função obterEscolha exibe um menu e obtém uma opção válida
def obterEscolha(o, s):
	q = len(o)
	exibirMenu(o, s)
	while True:
		e = intInput(f"Digite a opção desejada (1 a {q}): ")
		if 1 <= e <= q:
			return e
		else:
			print (f"Digite um número válido entre 1 e {q}")

# A função listaArquivos lista arquivos com questões de provas
def listaArquivos():
	currDir = os.path.dirname(os.path.abspath(__file__))
	arqs = [arq for arq in 
		os.listdir(currDir) if arq.endswith('.txt') 
		and not arq.startswith('prova_')]
	return sorted(arqs)

# A função getNumLinhas retorna quantas linhas tem em um arquivo
def getNumLinhas(nomeFonte):
	try:
		with open(nomeFonte, 'r') as arqFonte:
			return sum(1 for linha in arqFonte)
	except FileNotFoundError:
		print (f"O arquivo {nomeFonte} não foi encontrado!!!")
		return -1
	except Exception as e:
		print (f"Ocorreu um erro: {e}")
		return -1

# A função getQuestoes extrai as questões do arquivo
def getQuestoes(nomeFonte):
	quests = []
	try:
		with open(nomeFonte, 'r') as arqFonte:
			linhaCorrente, nLinhas = 0, getNumLinhas(nomeFonte)
			while linhaCorrente < nLinhas:
				qst = arqFonte.readline().strip()
				corr = arqFonte.readline().strip()
				distr = []
				for _ in range(4):
					distr.append(arqFonte.readline().strip())
				quests.append((qst, corr, *distr))
				linhaCorrente += 6
	except FileNotFoundError:
		print(f"O arquivo {nomeFonte} não foi encontrado!!!")
	except Exception as e:
		print (f"Ocorreu um erro: {e}")
	finally:
		return quests

# A função gravaProva gera um arquivo com cada tipo de prova
def gravaProva(idntf, txtProva):
	nomeArq = f"prova_{idntf}.txt"
	try:
		with open(nomeArq, 'w') as arqProva:
			arqProva.write(txtProva)
	except Exception as e:
		print(f"Ocorreu um erro gravando a prova: {e}")
		nomeArq = ""
	finally:
		return nomeArq

# Código principal

# Defina o arquivo com as questoes
arquivos = listaArquivos()
selArquivo = obterEscolha(arquivos, 
	"Qual arquivo contém as questões de prova?")
nomeFonte = arquivos[selArquivo - 1]

# Importa as questoes
questoes = getQuestoes(nomeFonte)

# Pergunta quantos modelos de prova devem ser feitos
qtProvas = intInput("Deseja quantas provas: ")

# Prossegue se a quantidade de provas for entre 1 e 26
if 0 < qtProvas <= len(ABC):
	# Pergunta a quantidade de questões e valor de cada uma
	qtQuest = intInput("Deseja quantas questões por prova: ")
	valQuest = input("Quanto vale cada questão: ")
	# Obtém a quantidade de questões disponíveis
	tamQuestoes = len(questoes)
	# Prossegue se a quantidade de questões desejada for menor 
	# ou igual a quantidade disponível
	if qtQuest <= tamQuestoes:
		# Cria as provas com nomes A, B, C e assim por diante
		nmProvas = []
		for nome in ABC[:qtProvas]:
			# A variável prova conterá o texto da prova
			prova, gabarito = "", "GABARITO\n"
			# Obtém lista com números únicos das 
			# questões selecionadas
			qSelec = random.sample(range(tamQuestoes - 1), qtQuest)
			# A variável qProva conterá as questões da prova
			qProva = ""
			# Laço para tratar cada uma das questões
			for qtQst in range(qtQuest):
				# Escreve o número da questão e seu valor
				# Exemplo: 'QUESTÃO 1 - 0,25 PONTO'
				qProva += f"\nQUESTÃO {qtQst + 1}"
				qProva += f" - {valQuest} PONTO\n\n"
				# Escreve o enunciado da questão
				qProva += questoes[qSelec[qtQst]][0] + '\n\n'
				# Obtém uma lista com a ordem das opções
				ordemOpcoes = random.sample(range(1,6),5)
				# A variável 'opcoes' terá as opções da questão
				opcoes = ""

				# Laço para lidar com as opções da questão
				for iOpc, j in enumerate(ordemOpcoes):
					# Escreve cada opção
					# Exemplo: '(A) blá, blá, blá'
					opcoes += f"({ABC[iOpc]}) "
					opcoes += f"{questoes[qSelec[qtQst]][j]}\n"

				# Inclue a opção correta no gabarito
				gabarito += f"{qtQst + 1}: {ABC[ordemOpcoes.index(1)]}\n"

				# Appenda na questão as opções dela
				qProva += opcoes

			# Appenda na prova todas as questões
			prova += "Questões\n" + qProva + gabarito

			nmProvas.append(gravaProva(nome, prova))

		if len(nmProvas) > 0:
			print("Provas geradas:")
			for nmPrv in nmProvas:
				print(nmPrv)
		else:
			print("Nenhuma prova foi gerada!!!")
	else:
		print(f"Tenho somente {tamQuestoes} questões")
else:
	print (f"Não é possível gerar {qtProvas} provas")
