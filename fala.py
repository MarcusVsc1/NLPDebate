class Fala:
        
        media_movel_neg = []
        media_movel_pos = []


        #construtor
        def __init__(self, candidato, conteudo, sentimentos):
            self.candidato = candidato
            self.conteudo = conteudo
            self.sentimentos = sentimentos
            self.media_movel_neg = self.calcula_media_movel('neg')
            self.media_movel_pos = self.calcula_media_movel('pos')

        #função que cria a média móvel de um sentimento específico e retorna em lista
        def calcula_media_movel(self, polar):
            num1 = 0
            num2 = 0
            num3 = 0
            media_movel = []
            #verifica se a quantidade de sentenças é menor que 3, para evitar de entrar no laço
            if(len(self.sentimentos) <= 3 ):
                mm = 0
                for sent in self.sentimentos:
                    for k, v in sent.items():
                        if(k == polar):
                            mm += v
                media_movel.append(mm/len(self.sentimentos))
            #laço que faz a média móvel
            for i in range(0, len(self.sentimentos)-3):
                for k, v in self.sentimentos[i].items():
                    if(k == polar):
                        num1 = v
                for k, v in self.sentimentos[i+1].items():
                    if(k == polar):
                        num2 = v
                for k, v in self.sentimentos[i+2].items():
                    if(k == polar):
                        num3 = v
                media_movel.append((num1+num2+num3)/3)
                #print(len(media_movel))
            return media_movel
        

            
        
        
            

        