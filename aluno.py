from util import validarTelefone
from util import ehNotaValida
from menu import menuNotas
from menu import informRecuperacao
from conexao import criarConexao
from conexao import fecharConexao

def matriculaExiste(matricula):
    ret = False
    cnn = ""
    cur = ""
    matricula = int(matricula)
    if matricula > 0:
        try:
            cnn = criarConexao()
            cur = cnn.cursor()
            sql = "select count(*) from aluno where id =?"
            a = cur.execute(sql,(matricula,)).fetchone()
            if a[0] == 1:
                ret = True
        except NameError as erro:
            print("Erro ao pesquisar aluno: ", erro)
        finally:
            cur.close()
            fecharConexao(cnn)
    return ret

def notaExiste(matricula):
    ret = False
    cnn = ""
    cur = ""
    matricula = int(matricula)
    if matricula > 0:
        try:
            cnn = criarConexao()
            cur = cnn.cursor()
            sql = "select count(*) from nota where id_aluno =?"
            a = cur.execute(sql,(matricula,)).fetchone()
            if a[0] == 1:
                ret = True
        except NameError as erro:
            print("Erro ao pesquisar nota: ", erro)
        finally:
            cur.close()
            fecharConexao(cnn)
    return ret

def cadastrar():
    opcao = 0
    aluno = list()
    cnn = ""
    cur = ""
    while True:
        matricula = input('Entre com a matricula do aluno: ')
        if matricula.isnumeric():
            matricula = int(matricula)
            if matricula > 0:
                if not matriculaExiste(matricula):
                    aluno.append(matricula)
                    aluno.append(input('Entre com o nome do aluno: '))
                    while True:
                        telefone = input('Entre com o telefone celular do aluno 99-999999999: ')
                        if validarTelefone(telefone):
                            aluno.append(telefone)
                            break
                    aluno.append(input('Entre com o endereço do aluno: '))
                    break
                else:
                    print('\033[31m'+'ERRO - A matricula informada já está cadastrada'+'\033[0;0m')
                    opcao = input('ENTER para continuar ou 99 para voltar: ')
                    if opcao.isnumeric():
                        opcao = int(opcao)
                        if opcao == 99:
                            break
    if opcao != 99:
        try:
            cnn = criarConexao()
            cur = cnn.cursor()
            sql = "insert into aluno(id,nome,telefone,endereco) values(?,?,?,?)"
            cur.execute(sql,tuple(aluno))
            cnn.commit()
            print(f'\033[1;35mAluno inserido com sucesso...\033[0;0m')
            input('Pressione qualquer tecla para continuar.')
        except NameError as erro:
            print("Erro ao inserir aluno: ", erro)
        finally:
            cur.close()
            fecharConexao(cnn)

def lancarNotas(matricula):
    aluno = retornaTuplaAluno(matricula)
    possuiNota = notaExiste(matricula)
    while True:
        atualiza = False
        print(f'Lançar notas do aluno \033[32m{aluno[1].upper()}\033[0;0m com matrícula \033[32m{aluno[0]}\033[0;0m: ')
        menuNotas()
        opcao = input('Informe a opção: ')
        if opcao.isnumeric():
            opcao = int(opcao)
            if opcao == 99:
                break
            elif opcao == 1: #lancar AD1
                ad1 = input('Entre com a nota da AD1: ')
                if ehNotaValida(ad1):
                    atualiza = True
                    if possuiNota:
                        sql = f'update nota set ad1 = {float(ad1)} where id_aluno = {aluno[0]}'
                    else:
                        sql = f'insert into nota(id_aluno,ad1) values({aluno[0]},{float(ad1)})'
            elif opcao == 2: #lancar AD2
                ad2 = input('Entre com a nota da AD2: ')
                if ehNotaValida(ad2):
                    atualiza = True
                    if possuiNota:
                        sql = f'update nota set ad2 = {float(ad2)} where id_aluno = {aluno[0]}'
                    else:
                        sql = f'insert into nota(id_aluno,ad2) values({aluno[0]},{float(ad2)})'
            elif opcao == 3: #lancar Recuperação
                media = retornaMediaNota(matricula)
                if (media > -1) and (media < 7.0):
                    recuperacao = input('Entre com a nota de recuperação: ')
                    if ehNotaValida(recuperacao):
                        atualiza = True
                        if possuiNota:
                            sql = f'update nota set recuperacao = {float(recuperacao)} where id_aluno = {aluno[0]}'
                        else:
                            sql = f'insert into nota(id_aluno,recuperacao) values({aluno[0]},{float(recuperacao)})'
                else:
                    atualiza = False
                    informRecuperacao()
        if atualiza:
            try:
                cnn = criarConexao()
                cur = cnn.cursor()
                cur.execute(sql)
                cnn.commit()
            except NameError as erro:
                print("Erro ao listar nota: ", erro)
            finally:
                cur.close()
                fecharConexao(cnn)

def retornaMediaNota(matricula):
    cnn = ""
    cur = ""
    if notaExiste(matricula):
        try:
            cnn = criarConexao()
            cur = cnn.cursor()
            sql = "select ad1 from nota where id_aluno=?"
            ad1 = cur.execute(sql,(matricula,)).fetchone()
            sql = "select ad2 from nota where id_aluno=?"
            ad2 = cur.execute(sql,(matricula,)).fetchone()
            if (ad1[0] is not None) and (ad2[0] is not None):
                sql = "select (ad1 + ad2)/2 from nota where id_aluno=?"
                nota = cur.execute(sql,(matricula,)).fetchone()
                nota = nota[0]
            else:
                nota = -1
            return nota
        except NameError as erro:
            print("Erro ao listar nota: ", erro)
        finally:
            cur.close()
            fecharConexao(cnn)
    else:
        return -1

def retornaTuplaAluno(matricula):
    cnn = ""
    cur = ""
    try:
        cnn = criarConexao()
        cur = cnn.cursor()
        sql = "select * from aluno_nota where id=?"
        return cur.execute(sql,(matricula,)).fetchone()
    except NameError as erro:
        print("Erro ao listar aluno: ", erro)
    finally:
        cur.close()
        fecharConexao(cnn)

def exibir(aluno):
    print('\033[36m-=\033[0;0m' * 18)
    print('\033[36m|          DADOS PESSOAIS          |\033[0;0m')
    print('\033[36m-=\033[0;0m' * 18)
    print(f'\033[36mMATRÍCULA:\033[0;0m\t \033[33m{aluno[0]}\033[0;0m')
    print(f'\033[36mNOME:\033[0;0m\t\t \033[33m{aluno[1]}\033[0;0m')
    print(f'\033[36mTELEFONE:\033[0;0m\t \033[33m{aluno[2]}\033[0;0m')
    print(f'\033[36mENDEREÇO:\033[0;0m\t \033[33m{aluno[3]}\033[0;0m')
    print('\033[36m-=\033[0;0m' * 18)
    print('\033[36m|               NOTAS              |\033[0;0m')
    print('\033[36m-=\033[0;0m' * 18)
    print(f'\033[36mAD1:\033[0;0m\t\t \033[33m{"Não existe nota lançada" if aluno[4] is None else aluno[4]}\033[0;0m')
    print(f'\033[36mAD2:\033[0;0m\t\t \033[33m{"Não existe nota lançada" if aluno[5] is None else aluno[5]}\033[0;0m')
    print(f'\033[36mRECUPERAÇÃO:\033[0;0m \033[33m{"Não existe nota lançada" if aluno[6] is None else aluno[6]}\033[0;0m')
    input('Pressione qualquer tecla para continuar.')

def editar(aluno):
    virgula = False
    sql = 'update aluno set '
    print('\033[1m'+'\033[31mPressione ENTER caso não queira alterar o valor\033[0;0m')
    print(f'\033[36mNOME ATUAL:\033[0;0m \033[33m{aluno[1]}\033[0;0m')
    nome = input('Altere o nome do aluno:')
    if len(nome) != 0:
        sql += f'nome = \'{nome}\''
        virgula = True
    while True:
        print(f'\033[36mCELULAR ATUAL:\033[0;0m \033[33m{aluno[2]}\033[0;0m')
        telefone = input('Altere o telefone celular do aluno 99-999999999: ')
        if len(telefone) != 0:
            if validarTelefone(telefone):
                if virgula:
                    sql += ','
                sql += f'telefone = \'{telefone}\''
                virgula = True
                break
        else:
            break
    print(f'\033[36mENDEREÇO ATUAL:\033[0;0m \033[33m{aluno[3]}\033[0;0m')
    endereco = input('Altere o endereço do aluno: ')
    if len(endereco) != 0:
        if virgula:
            sql += ','
        sql += f'endereco = \'{endereco}\''
    if len(sql) > 17:
        sql += f' where id = {aluno[0]}'
        try:
            cnn = criarConexao()
            cur = cnn.cursor()
            print(sql)
            cur.execute(sql)
            cnn.commit()
            print(f'\033[1;35mAluno atualizado com sucesso...\033[0;0m')
            input('Pressione qualquer tecla para continuar.')
        except NameError as erro:
            print("Erro ao atualizar aluno: ", erro)
        finally:
            cur.close()
            fecharConexao(cnn)

def excluir(matricula):
    try:
        cnn = criarConexao()
        cur = cnn.cursor()
        sql = "delete from aluno where id = ?"
        aluno = cur.execute(sql,(matricula,)).rowcount
        cnn.commit()
        if aluno > -1:
            print(f'\033[1;35mProcesso de exclusão realizado com sucesso...\033[0;0m')
        else:
            print(f'\033[31mNão houve a exclusão do aluno...\033[0;0m')
        input('Pressione qualquer tecla para continuar.')
    except NameError as erro:
        print("Erro ao excluir aluno: ", erro)
    finally:
        cur.close()
        fecharConexao(cnn)