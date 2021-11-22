from util import retornaQuantidadeAlunos
from util import retornaPercentualAprovados
from util import retornaMatriculaMaiorMedia
from util import retornaMediaTurma
from conexao import criarConexao
from conexao import fecharConexao

def gerarFrequencia():
    print('|' + '-' * 118 + '|')
    print(f'| {"LISTA DE FREQUENCIA".center(116)} |')
    print('|' + '-' * 118 + '|')
    print(f'|{"MATRICULA".center(11)} | {"ALUNO".center(40)} | {"ASSINATURA".center(60)} |')
    try:
        cnn = criarConexao()
        cur = cnn.cursor()
        sql = "select id,nome from aluno"
        alunos = cur.execute(sql).fetchall()
        for aluno in alunos:
            matricula = "00" + str(aluno[0])
            print(f'|{matricula[-3:].center(11)} | {aluno[1].title().ljust(40)} | ____________________________________________________________ |')
    except NameError as erro:
        print("Erro ao pesquisar aluno: ", erro)
    finally:
        cur.close()
        fecharConexao(cnn)
        print('|' + '-' * 118 + '|')

def gerarNotas():
    print('|' + '-' * 111 + '|')
    print(f'| {"RELATÓRIO DE NOTAS".center(109)} |')
    print('|' + '-' * 111 + '|')
    print(f'|{"MATRICULA".center(11)} | {"ALUNO".center(40)} | {"AD1".center(10)} | {"AD2".center(10)} | {"MÉDIA".center(10)} | {"RECUPERAÇÃO".center(14)} |')
    try:
        cnn = criarConexao()
        cur = cnn.cursor()
        sql = "select id,nome,ad1,ad2,recuperacao from aluno_nota"
        alunos = cur.execute(sql).fetchall()
        for aluno in alunos:
            matricula = "00" + str(aluno[0])
            ad1 = f'{"-" if aluno[2] is None else aluno[2]}'
            ad2 = f'{"-" if aluno[3] is None else aluno[3]}'
            recuperacao = f'{"-" if aluno[4] is None else aluno[4]}'
            if ad1 != "-" and ad2 != "-":
                media = str((float(ad1) + float(ad2)) / 2)
            else:
                media = "-"
            print(f'|{matricula[-3:].center(11)} | {aluno[1].title().ljust(40)} | {ad1.rjust(10)} | {ad2.rjust(10)} | {media.rjust(10)} | {recuperacao.rjust(14)} |')
    except NameError as erro:
        print("Erro ao pesquisar aluno: ", erro)
    finally:
        cur.close()
        fecharConexao(cnn)
        print('|' + '-' * 111 + '|')

def gerarResumo():
    aprovados = 0
    reprovados = 0
    matricula = 0
    media_geral = 0.0
    try:
        cnn = criarConexao()
        cur = cnn.cursor()
        sql = "select * from nota"
        notas = cur.execute(sql).fetchall()
        totalAlunos = retornaQuantidadeAlunos()
        if totalAlunos > 0:
            aprovados = round(retornaPercentualAprovados(totalAlunos,notas),2)
            reprovados = round(100.0 - aprovados,2)
            matricula = retornaMatriculaMaiorMedia(notas)
            media_geral = round(retornaMediaTurma(totalAlunos, notas),2)
            print('|' + '-' * 44 + '|')
            print(f'| {"RESUMO DO CURSO".center(42)} |')
            print('|' + '-' * 44 + '|')
            print(f'| \033[36m\033[1mTOTAL DE ALUNOS CADASTRADOS:\033[0;0m \t\t{str(totalAlunos).rjust(6)}\t |')
            print(f'| \033[36m\033[1mTOTAL DE ALUNOS APROVADOS (%):\033[0;0m \t{str(aprovados).rjust(6)}\t |')
            print(f'| \033[36m\033[1mTOTAL DE ALUNOS REPROVADOS (%):\033[0;0m \t{str(reprovados).rjust(6)}\t |')
            print(f'| \033[36m\033[1mMATRÍCULA COM MAIOR MÉDIA FINAL:\033[0;0m \t{str(matricula).rjust(6)}\t |')
            print(f'| \033[36m\033[1mMÉDIA GERAL DA TURMA:\033[0;0m \t\t\t{str(media_geral).rjust(6)}\t |')
            print('|' + '-' * 44 + '|')
        else:
            print(f'\033[31mNão existem alunos cadastrados...\033[0;0m')
            input('Pressione qualquer tecla para continuar...')
    except NameError as erro:
        print("Erro ao pesquisar aluno: ", erro)
    finally:
        cur.close()
        fecharConexao(cnn)