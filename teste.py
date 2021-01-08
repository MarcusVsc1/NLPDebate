#importações
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import csv
from fala import Fala
import spacy
from spacy.tokens import Doc
from spacy.pipeline import SentenceSegmenter
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pt_core_news_sm

#inicializa o spacy
spacy.prefer_gpu()
nlp = spacy.load('pt')


#função que retorna valores de sentimento
def sentiment_scores(docx):
    return sent_analyzer.polarity_scores(docx.text)

#inicializa o analisador de sentimento
sent_analyzer = SentimentIntensityAnalyzer();
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)

#leitura do debate.csv
arquivo = open('debate.csv')
linhas = csv.reader(arquivo)

#define qual o candidato vai ser exportado para o heatmap
candidato_escolhido = 'DILMA ROUSSEFF'

#tamanho do eixo x da tabela de dados
df_x_axys = 0

#cria uma lista de falas do candidato escolhido
falas_debate = []
for linha in linhas:
    nova_fala=''
    for palavra in linha:
        palavra.replace('"','')
        nova_fala = nova_fala + palavra
    falaECand = nova_fala.split(';')
    doc = nlp(falaECand[1])
    lista = []
    lista = list(doc.sents)
    listaPolar = []
    for frase in lista:
        f = sentiment_scores(frase)
        listaPolar.append(f)
    #este if filtra o candidato. se tirar, ficarão todas as falas do debate
    if(falaECand[0] == candidato_escolhido):
        fala_nova = Fala(falaECand[0], lista, listaPolar)
        falas_debate.append(fala_nova)
        if(len(fala_nova.media_movel_neg) > df_x_axys):
            df_x_axys = len(fala_nova.media_movel_neg)

#cria a tabela de dados
tabela = []
for fala in falas_debate:
    linha_prot = fala.media_movel_neg
    while(len(linha_prot)< df_x_axys):
        linha_prot.append(np.nan)
    linha = np.array(linha_prot)
    tabela.append(linha)
tabela_f = np.array(tabela)


#cria heatmap
plt.figure(figsize=(20, 20))
df = pd.DataFrame(data=tabela_f)
cmap = sns.cubehelix_palette(as_cmap=True, light=1)
cmap.set_under(".9")
ax = plt.axes()
polaridade = 'negativo'
ax.set_title('Mapa de calor '+polaridade+': Candidato '+candidato_escolhido, fontsize = 30)
with sns.axes_style("white"):
    sns.set(font_scale = 1.4)
    heat_map = sns.heatmap(df, ax = ax, xticklabels=False, annot = True, mask = df.isnull(), cbar_kws={'label': 'Escala de sentimento', 'orientation': 'vertical'})
    heat_map.set_yticklabels(heat_map.get_yticklabels(), fontsize = 18, rotation=35)
    heat_map.figure.axes[-1].yaxis.label.set_size(20)
plt.xlabel("Média móvel das sentenças de cada fala", fontsize = 28)
plt.ylabel("Falas do candidato", fontsize = 28)
plt.savefig('Mapa_de_calor.png')

#escrita em arquivo csv das falas com cada sentimento
with open('sentimentos.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow('Fala;Candidato;Sentença;Sentimento')
    for fala in falas_debate:
            for sentenca in fala.conteudo:
                valor = fala.sentimentos[fala.conteudo.index(sentenca)]
                spamwriter.writerow(str(falas_debate.index(fala))+';'+fala.candidato+';'+str(sentenca)+';'+str(valor))
