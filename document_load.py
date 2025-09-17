from langchain_community.document_loaders import (WebBaseLoader, # sites
                                                  YoutubeLoader, # youtube
                                                  CSVLoader, #csv
                                                  PyPDFLoader, #pdf
                                                  TextLoader) #txt

url = "https://google.com/"

def load_site():
    loader = WebBaseLoader(url)
    documents_list = loader.load() # metodo de carregamento em si
    document = "\n\n".join([doc.page_content for doc in documents_list]) # extrai apenas o conteúdo da lista recebida pelo WebBaseLoader
    return document