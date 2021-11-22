from conexao import criarConexao
from conexao import fecharConexao

def criarEstrutura():
    cur = ""
    err = False
    try:
        cnn = criarConexao()
        cur = cnn.cursor()
        cur.execute("create table if not exists aluno (\
                            id int primary key not null,\
                            nome text not null,\
                            telefone text not null,\
                            endereco text not null)")
        cur.execute("create table if not exists nota (\
                            id_aluno int primary key not null,\
                            ad1 real null,\
                            ad2 real null,\
                            recuperacao real null,\
                            constraint fk_aluno \
                                foreign key (id_aluno) \
                                references aluno(id)\
                                on delete cascade)")
        cur.execute("create view if not exists aluno_nota as \
                        select aluno.id, aluno.nome, aluno.telefone, \
                        aluno.endereco, nota.ad1, nota.ad2, nota.recuperacao \
                        from aluno left join nota on id = id_aluno")
    except NameError as erro:
        print("Problemas ao criar estrutura do banco: ", erro)
        err = True
        return err
    finally:
        cur.close()
        fecharConexao(cur)
        return err
