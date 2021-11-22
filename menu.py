def menuPrincipal():
    print("1 - Cadastrar aluno")
    print("2 - Buscar aluno")
    print("3 - Editar dados do aluno")
    print("4 - Excluir aluno")
    print("5 - Lançar notas")
    print("6 - Relatórios")
    print("99 - Sair")

def menuNotas():
    print("1 - Lançar AD1")
    print("2 - Lançar AD2")
    print("3 - Lançar Recuperação")
    print("99 - Voltar")

def menuRelatorios():
    print("1 - Gerar lista de frequencia")
    print("2 - Gerar relatório de notas")
    print("3 - Gerar relatório final da disciplina")
    print("99 - Voltar")

def informRecuperacao():
    print('\033[31mImpossível lançar nota de recuperação.\033[0;0m')
    input('Pressione qualquer tecla para continuar.')

def informMatriculaInvalida():
    print('\033[31mA matrícula informada não existe.\033[0;0m')
    input('Pressione qualquer tecla para continuar')