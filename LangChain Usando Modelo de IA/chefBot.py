import os
from dotenv import load_dotenv
from tkinter.filedialog import askopenfilenames
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

chat = ChatGroq(model='llama-3.3-70b-versatile')

def carrega_site():
  url_site = input('Digite a url do site: ')
  loader = WebBaseLoader(url_site)
  lista_documentos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento = documento + doc.page_content
  return documento

def carrega_pdf():
    paths = askopenfilenames(title="Selecione os PDFs", filetypes=[("PDF Files", "*.pdf")])
    if not paths:
        return ""
    conteudo_total = ""
    for path in paths:
        loader = PyPDFLoader(path)
        list_documents = loader.load()
        conteudo_total += ''.join(doc.page_content for doc in list_documents)
    return conteudo_total

def carrega_youtube():
  url_youtube = input('Digite a url do vídeo: ')
  loader = YoutubeLoader.from_youtube_url(url_youtube, language=['pt'])
  lista_documentos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento = documento + doc.page_content
  return documento

def resposta_bot(mensagens, documento):
  mensagem_system = '''Você é um assistente virtual chamado ChefBot, um chef de cozinha e nutricionista altamente especializado.
  Sua missão é criar dietas personalizadas e elaborar receitas que sejam ao mesmo tempo saudáveis, saborosas e adaptadas às necessidades individuais.
  Para formular suas respostas, você sempre considera as seguintes informações: {informacoes}.
  Mantenha um tom amigável, acolhedor e profissional ao interagir.
  '''
  mensagens_modelo = [('system', mensagem_system)]
  mensagens_modelo += mensagens
  template = ChatPromptTemplate.from_messages(mensagens_modelo)
  chain = template | chat
  return chain.invoke({'informacoes': documento}).content

print('''\n                             Bem-vindo ao ChefBot!
    Estou aqui para te ajudar dentro da cozinha sem ficar de barriga vazia!\n''')

texto_selecao = '''1. Enviar um PDF
2. Enviar um Site
3. Enviar um vídeo do Youtube
4. Não desejo enviar referências\n\n
Usuário: '''

while True:
  selecao = input(texto_selecao)
  global documento
  if selecao == '1':
    documento = carrega_pdf()
    break
  if selecao == '2':
    documento = carrega_site()
    break
  if selecao == '3':
    documento = carrega_youtube()
    break
  if selecao == '4':
    documento = ''
    break
  print('Número inválido!')


mensagens = []
while True:
  pergunta = input('\nUsuario: ')
  if pergunta.lower() == 'x':
    break
  mensagens.append(('user', pergunta))
  resposta = resposta_bot(mensagens, documento)
  mensagens.append(('assistant', resposta))
  print(f'\nBot: {resposta}')

print('Muito obrigado por usar o AsimoBot')