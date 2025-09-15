import streamlit as st

VALID_ARCH_TYPES = [
    "Site", "Youtube", "PDF", "CSV", "TXT"
]

VALID_PROVIDERS = {"Groq": {"models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]},
                   "OpenAI": {"models": ["gpt-4o-mini", "gpt-oss-120b", "gpt-oss-20b"]}}

def chat_page():
    """
        ESTRUTURA DE CHAT

        Engloba o título de saudação e o funcionamento do chat (memória e mensagens aparecendo)
    """
    # Título que aparece na página principal (parâmetro 'divider' coloca uma divisória abaixo do título)
    st.header("👾 Welcome to your personal Oracle!", divider=True)

    # Esse é o formato de "messages" 
    # EX_MESSAGE = [
    #     ("user", "Hello!"), # (role, content)
    #     ("assistant", "What's up?"),
    #     ("user", "Not much.")
    # ]

    # Session state é a memória do Streamlit 
    messages = st.session_state.get("messages", []) # retorna uma lista vazia se não encontrar mensagens anteriores
    for message in messages:
        chat = st.chat_message(message[0]) # formatação de chat (role)
        chat.markdown(message[1]) # escreve no chat criado (conteúdo)

    user_input = st.chat_input("Write here")
    if user_input:
        messages.append(("user", user_input)) # salva a mensagem na lista de tuplas
        st.session_state["messages"] = messages # salva na memória do Streamlit
        st.rerun() # roda a função novamente

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

def main():
    chat_page()
    with st.sidebar: # tudo que estiver dentro deste método vai ser exibido na sidebar do Streamlit
        sidebar() # modelo que construímos

if __name__ == "__main__":
    main()