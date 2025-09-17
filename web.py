import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

VALID_ARCH_TYPES = [
    "Site", "Youtube", "PDF", "CSV", "TXT"
]

VALID_PROVIDERS = {"Groq":
                        {"models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "openai/gpt-oss-120b", "openai/gpt-oss-20b" , "gemma2-9b-it", "deepseek-r1-distill-llama-70b"],
                         "chat": ChatGroq},
                   "OpenAI":
                        {"models": ["gpt-4o-mini"],
                         "chat": ChatOpenAI},
                    "Google":
                        {"models" : ["gemini-2.5-flash", "gemini-2.5-pro"],
                         "chat": ChatGoogleGenerativeAI}}

MEMORY = ConversationBufferMemory()
# Demonstração básica de memória
# MEMORY.chat_memory.add_user_message("Hello, AI!")
# MEMORY.chat_memory.add_ai_message("Hello, human!")

def load_model(provider: str, model: str, api_key: str):
    """
        CARREGA O MODELO ESPECIFICADO PELOS PARÂMETROS

        Insere as informações passadas à função em uma variável padronizada e a salva na memória do Streamlit
    """
    # Padronização para qualquer modelo
    chat = VALID_PROVIDERS[provider]["chat"](model=model, api_key=api_key) # carrega a classe responsável pela inicialização do modelo e fornece os parâmetros requeridos
    st.session_state["chat"] = chat # salva na memória do Streamlit o modelo utilizado, evitando a necessidade de retornar a variável


def chat_page():
    """
        ESTRUTURA DE CHAT

        Engloba o título de saudação e o funcionamento do chat (memória e mensagens aparecendo)
    """
    # Título que aparece na página principal (parâmetro 'divider' coloca uma divisória abaixo do título)
    st.header("👾 Welcome to your personal Oracle!", divider=True)

    # Session state é a memória do Streamlit 
    chat_model = st.session_state.get("chat") # puxa da memória o chat
    memory = st.session_state.get("memory", MEMORY)
    for message in memory.buffer_as_messages:
        chat = st.chat_message(message.type) # formatação de chat (role)
        chat.markdown(message.content) # escreve no chat criado (conteúdo)

    user_input = st.chat_input("Write here")
    if user_input:
        # Parte responsável por fazer o texto aparecer sequencialmente no chat
        chat = st.chat_message("human") # cria uma nova janela do usuário
        chat.markdown(user_input) # mostra a mensagem que o usuário enviou
        chat = st.chat_message("ai") # cria uma nova janela da IA
        answer = chat.write_stream(chat_model.stream(user_input)) # escreve a mensagem em stream

        memory.chat_memory.add_user_message(user_input) # salva a mensagem do usuário (langchain)
        # answer = chat_model.invoke(user_input).content # armazena a mensagem que será passada para o modelo (OLD)
        memory.chat_memory.add_ai_message(answer) # salva a mensagem do modelo (langchain)
        st.session_state["memory"] = memory # atualiza a memória do Streamlit

def sidebar():
    """
        ESTRUTURA DE SIDEBAR

        Inclui duas abas principais, uma de upload de arquivos e outra de seleção do modelo.

        A primeira aba inclui a seleção do formato que será utilizado e caixa de texto/botão
        de upload para anexar a fonte.

        A segunda aba engoloba a seção do modelo que o usuário vai escolher para compor o
        Oráculo.
    """
    tabs = st.tabs(["Archive Upload", "Model Selection"])
    # Editamos a primeira aba (upload de arquivos)
    with tabs[0]:
        arch_type = st.selectbox("Select the archive type", VALID_ARCH_TYPES)
        # Seleção de formato de envio dos arquivos
        if (arch_type == "Site" or arch_type == "Youtube"):
            arch = st.text_input("URL")
        if (arch_type == "PDF"):
            arch = st.file_uploader("Upload", type=[".pdf"])
        if (arch_type == "CSV"):
            arch = st.file_uploader("Upload", type=[".csv"])
        if (arch_type == "TXT"):
            arch = st.file_uploader("Upload", type=[".txt"])

    # Editamos a segunda aba (seleção do LLM)
    with tabs[1]:
        provider = st.selectbox("Select the provider", VALID_PROVIDERS.keys())
        model = st.selectbox("Select the model", VALID_PROVIDERS[provider]["models"])
        api_key = st.text_input(
            f"Insert your API key for {provider}",
            value=st.session_state.get(f"api_key_{provider}"))

        # Armazena na memória do Streamlit o valor inserido na caixa de texto da chave da API
        st.session_state[f"api_key_{provider}"] = api_key # salva uma variável chamada "api_key_{provedor}" na memória

    if st.button("Initialize Oracle", use_container_width=True): # o segundo parâmetro apenas ajusta o botão para o mesmo tamanho das selectboxes
        load_model(provider, model, api_key)

def main():
    chat_page()
    with st.sidebar: # tudo que estiver dentro deste método vai ser exibido na sidebar do Streamlit
        sidebar() # modelo que construímos

if __name__ == "__main__":
    main()

# algum bug acontece que reinicia os texboxes quando converso com o modelo, corrigir isso
# CORREÇÃO: o st.rerun() no condicional do input do usuário, na função chat_page, por algum motivo estava reiniciando o que aparecia na sidebar