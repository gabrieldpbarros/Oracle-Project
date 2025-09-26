<div align="center">

# The Oracle <img src="./assets/spy.png" style="height: 60px;" aling="center" justify="center">

</div>

Your **personal** know-it-all chatbot. The Oracle stores provided data and gives insights on everything involving that data.

## Features

- Access to well-established Large Language Models (LLMs), such as *Llama-3.3-70b* and *GPT-4o-mini*;
- Simple and customizable interface;
- Support for YouTube and sites URLs, PDFs, CSVs and TXTs;
- Data memory.

## Installation

Since this project uses **Streamlit** as framework, make sure to run `streamlit run .\web.py` to have access to the tool.

### Option 1: Download ZIP

In the repository page, look for the **green Code button** and press it. Then, go to the **Download ZIP** option and click it.

A copy of the repository should start downloading with .zip format. Extract the folder on any directory, open it with the terminal and run:

```bash
$ pip install -r .\requirements.txt
```

> [!NOTE]
> You can run it on your own machine, but it's preferable to run on a virtual environment

Finally, you can run the Streamlit initiation command and start using The Oracle.

### Option 2: From source

```bash
$ git clone git@github.com:gabrieldpbarros/Oracle-Project.git
$ cd Oracle-Project/
$ pip install -r .\requirements.txt
$ streamlit run .\web.py
```

## Usage

Accessing the web app, the user needs to select a model in the **Model Selection** tab and insert the corresponding API Key

> [!IMPORTANT]
> The user must request an API Key from the provider externally. If you want to run a *Groq* model, you must have access to a *Groq API* key, for example.

Then, you can return to the **Archive Upload** tab and select whichever type of upload as you desire. 

With all this completed, now you can run the model and start chatting with it.