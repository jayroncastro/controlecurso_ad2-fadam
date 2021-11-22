import platform
import os
import re
from conexao import criarConexao
from conexao import fecharConexao

def limpaTela():
    so = platform.system()
    print(so)
    if so == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
        print("\x1b[2J")

def validarTelefone(numero):
    ret = False
    pattern = "^[0-9]{2}-[0-9]{9}$"
    if re.match(pattern,numero) != None:
        ret = True
    return ret

def retornaNomeAluno(matricula, alunos):
    nome = ''
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            nome = aluno["nome"]
            break
    return str(nome)

def retornaDicionarioNota(matricula, notas):
    achou = False
    nota = dict()
    for x in notas:
        if x["matricula"] == matricula:
            achou = True
            nota = x
            break
    if not achou:
        nota["matricula"] = matricula
    return nota

def dicionarioNotaExiste(matricula, notas):
    ret = False
    for nota in notas:
        if nota["matricula"] == matricula:
            ret = True
    return ret

def retornaDicionarioAluno(matricula, alunos):
    aluno = dict()
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            break
    return aluno

def ehNotaValida(nota):
    ret = False
    if not nota.isalpha():
        nota = float(nota)
        if nota >= 0 and nota <= 10:
            ret = True
    return ret

def retornaQuantidadeAlunos():
    cnn = ""
    cur = ""
    try:
        cnn = criarConexao()
        cur = cnn.cursor()
        sql = "select count(*) from aluno"
        a = cur.execute(sql).fetchone()
        return a[0]
    except NameError as erro:
        print("Erro ao pesquisar aluno: ", erro)
    finally:
        cur.close()
        fecharConexao(cnn)

def retornaPercentualAprovados(quantidade,notas):
    #para ser aprovado a media deve ser superior a 7 ou a recuperação deve ser superior a 7
    quant_aprovados = 0
    percentual = 0
    for nota in notas:
        ad1 = float(f'{"-1" if nota[1] is None else nota[1]}')
        ad2 = float(f'{"-1" if nota[2] is None else nota[2]}')
        recuperacao = float(f'{"-1" if nota[3] is None else nota[3]}')
        if ad1 > -1 and ad2 > -1:
            media = (ad1 + ad2) / 2
            if media < 7:
                if recuperacao >= 7:
                    quant_aprovados += 1
            else:
                quant_aprovados += 1
    if quant_aprovados > 0:
        percentual = (quant_aprovados * 100) / quantidade
    return percentual

def retornaMatriculaMaiorMedia(notas):
    matricula = 0
    media_geral = 0
    for nota in notas:
        ad1 = float(f'{"-1" if nota[1] is None else nota[1]}')
        ad2 = float(f'{"-1" if nota[2] is None else nota[2]}')
        recuperacao = float(f'{"-1" if nota[3] is None else nota[3]}')
        if ad1 > -1 and ad2 > -1:
            media = (ad1 + ad2) / 2
            if media > media_geral:
                matricula = f'{"-1" if nota[0] is None else nota[0]}'
                media_geral = media
            if media < 7:
                if recuperacao > media_geral:
                    matricula = f'{"-1" if nota[0] is None else nota[0]}'
                    media_geral = recuperacao
    return matricula

def retornaMediaTurma(quantidade, notas):
    media_geral = 0
    media = 0
    for nota in notas:
        ad1 = float(f'{"-1" if nota[1] is None else nota[1]}')
        ad2 = float(f'{"-1" if nota[2] is None else nota[2]}')
        recuperacao = float(f'{"-1" if nota[3] is None else nota[3]}')
        if ad1 > -1 and ad2 > -1:
            media = (ad1 + ad2) / 2
        if media < 7 and recuperacao > -1:
            media = recuperacao
        media_geral += media
    return media_geral / quantidade