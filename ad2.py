from menu import menuPrincipal
from menu import menuRelatorios
from menu import informMatriculaInvalida
from aluno import retornaTuplaAluno
from aluno import matriculaExiste
from aluno import cadastrar
from aluno import lancarNotas
from aluno import exibir
from aluno import editar
from aluno import excluir
from relatorio import gerarFrequencia
from relatorio import gerarNotas
from relatorio import gerarResumo
from database import criarEstrutura

alunos = list()
notas = list()
opcao = 0
if not criarEstrutura():
    while True:
        menuPrincipal()
        opcao = input('Selecione uma opção: ')
        if opcao.isnumeric():
            opcao = int(opcao)
            if opcao == 99:
                print('\033[32mObrigado por usar nosso aplicativo\033[0;0m\n\033[34m>> A FADAM AGRADECE <<\033[0;0m')
                break
            elif opcao == 1: #cadastrar
                cadastrar()
            elif opcao in (2,3,4,5):
                matricula = input('Informe a matrícula do aluno: ')
                if matricula.isnumeric():
                    matricula = int(matricula)
                    if matriculaExiste(matricula):
                        if opcao == 2: #buscar
                            exibir(retornaTuplaAluno(matricula))
                        elif opcao == 3: #editar
                            editar(retornaTuplaAluno(matricula))
                        elif opcao == 4: #excluir
                            aluno = retornaTuplaAluno(matricula)
                            exc = str(input(f'Você deseja realmente excluir o aluno \033[31m{aluno[1].upper()}\033[0;0m? Pressione [S] para SIM'))
                            if exc in ('S','s'):
                                excluir(matricula)
                            else:
                                input('\033[31mO processo de exclusão foi cancelado, pressione qualquer tecla para continuar...\033[0;0m')
                        elif opcao == 5: #lancar notas
                            lancarNotas(matricula)
                    else:
                        informMatriculaInvalida()
            elif opcao == 6: #relatórios
                while True:
                    menuRelatorios()
                    opcao = input('Informe a opção: ')
                    if opcao.isnumeric():
                        opcao = int(opcao)
                        if opcao == 99:
                            break
                        elif opcao == 1:
                            gerarFrequencia()
                        elif opcao == 2:
                            gerarNotas()
                        elif opcao == 3:
                            gerarResumo()
                        if opcao in (1,2,3):
                            input('Pressione qualquer tecla para continuar...')
                            break