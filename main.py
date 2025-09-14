import streamlit as st
import pdfplumber as pb
import pandas as pd

abas = ['Buscar', 'Infrequência']
buscar, infrequancia = st.tabs(abas)


# aba de buscar o arquivo
with buscar:
    st.header('Selecione o arquivo abaixo')
    arquivo = st.file_uploader("arquivo")

    # se o arquivo não for vazio, deve aparecer a opção de download
    if arquivo is not None:
        st.success("ARQUIVO ENCONTRADO COM SUCESSO")
        st.download_button('download', arquivo, 'dados.pdf')


# função de exibir a infrequência dos alunos
def retornar_tabelas(arquivo_recebido):
    if arquivo_recebido is not None:
        with pb.open(arquivo_recebido) as arquivo:
            paginas = arquivo.pages

            pagina_1 = paginas[0].extract_table()
            pagina_2 = paginas[1].extract_table()

            return pagina_1, pagina_2


# verifica se há arquivo selecionado
if arquivo is not None:
    tabelas = retornar_tabelas(arquivo)


# convertando tabelas em dataframes
def converter_dataframe(tabelas_recebidas):
    if tabelas is not None:
        dataframe1 = pd.DataFrame(tabelas_recebidas[0])
        dataframe2 = pd.DataFrame(tabelas_recebidas[1])
        
        return dataframe1, dataframe2


# verificando se tem tabelas para converter e transformando datagrames
if "tabelas" in globals():
    dataframes_1 = converter_dataframe(tabelas)[0]
    dataframes_2 = converter_dataframe(tabelas)[1]

if "dataframes_1" and "dataframes_2" in globals():
    
    def adicionar_coluna_faltas():
        nova_tabela_1 = dataframes_1.iloc[1:, :-6:2].replace(",", ".")
        nova_tabela_1['Total_Faltas'] = nova_tabela_1.iloc[:, 1:].astype(float).sum(axis=1)
        nova_tabela_2 = dataframes_2.iloc[1:, :-6:2].replace(",", ".")
        nova_tabela_2['Total_Faltas'] = nova_tabela_2.iloc[:, 1:].astype(float).sum(axis=1)

        infrequencia_geral = pd.concat([nova_tabela_1, nova_tabela_2], ignore_index=True)

        return infrequencia_geral

    with infrequancia:
        st.header("INFREQUÊNCIA DOS ALUNOS")
        st.write("DESLISE A TABELA PARA A DIREITA E VEJA O TOTAL DE FALTAS")
        infrequancia_geral = adicionar_coluna_faltas()
        dados_selecionado = st.dataframe(infrequancia_geral,  on_select="rerun")


