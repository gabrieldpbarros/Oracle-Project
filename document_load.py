import os

from fake_useragent import UserAgent # usado para garantir que conseguiremos acessar o site
import streamlit as st
from langchain_community.document_loaders import (WebBaseLoader, # sites
                                                  YoutubeLoader, # youtube
                                                  CSVLoader, #csv
                                                  PyPDFLoader, #pdf
                                                  TextLoader) #txt
from time import sleep

# EXAMPLE: url_web = "https://google.com/"
def load_site(url_web):
    document = ''
    for i in range(5):
        try:
            os.environ["USER_AGENT"] = UserAgent().random
            loader = WebBaseLoader(url_web, raise_for_status=True) # raise_for_status puxa um erro, que é capturado pelo except
            documents_list = loader.load() # método de carregamento em si
            document = "\n\n".join([doc.page_content for doc in documents_list]) # extrai apenas o conteúdo da lista recebida pelo WebBaseLoader
            break
        except:
            print(f"Erro ao carregar o site {i + 1} vez")
            sleep(3) # evita bloquear o site

    if (document == ''):
        st.error("Não foi possível carregar o site")
        st.stop()
    return document

# O loader do youtube carrega apenas as legendas do vídeo.
# Existem formas de receber o vídeo em si, mas essa é a
# mais simples e leve de utilizar   
# EXAMPLE: video_id = "QJZdpFvFL0E"
def load_video(video_id):
    loader = YoutubeLoader(video_id, add_video_info=False, language=["pt"]) # não adiciona as informações do vídeo e carrega as legendas em português
    subtitles_list = loader.load() # método de carregamento em si
    document = "\n\n".join([doc.page_content for doc in subtitles_list]) # extrai apenas o conteúdo da lista recebida pelo loader
    return document

# EXAMPLE: path_pdf = "LLaMP Large Language Model Made Powerful for High-fidelity Materials Knowledge Retrieval and Distillation.pdf"
def load_pdf(path_pdf):
    loader = PyPDFLoader(path_pdf)
    data_list = loader.load()
    document = "\n\n".join([doc.page_content for doc in data_list])
    return document

# EXAMPLE: path_csv = "ipeadata.csv"
def load_csv(path_csv):
    loader = CSVLoader(path_csv)
    data_list = loader.load()
    document = "\n\n".join([doc.page_content for doc in data_list])
    return document

# EXAMPLE: path_txt = ".pdf"
def load_txt(path_txt):
    loader = TextLoader(path_txt)
    data_list = loader.load()
    document = "\n\n".join([doc.page_content for doc in data_list])
    return document

# doc = load_csv(path_csv)
# print(doc)