import math
import random


def dectobin(decimal, formatar):  # função para converter um número de decimal para binário e formatar ele para dada
    # quantidade de bits
    lista = list()
    if decimal == 0:
        lista.append('0')
    else:
        while decimal > 1:
            decimal = decimal / 2
            if decimal.is_integer():
                lista.append('0')
            else:
                lista.append('1')
            decimal = int(decimal)
        lista.append('1')
    while len(lista) != formatar:  # laço responsável por normalizar o número binário na quantidade especificada de bits
        lista.append('0')

    lista.reverse()
    string = ''.join(lista)
    return string


def bintodec(binario):  # função para converter um número em base decimal para um em base binária
    binario = list(binario)
    binario.reverse()
    final = 0
    ordem = 0
    for x in binario:
        calculo = 2 ** ordem * int(x)
        final += calculo
        ordem += 1
    return final


potencia_celulas = {  # dicionário usado para traduzir os múltiplos em potências (de dois)
    "K": 10,
    "M": 20,
    "G": 30,
    "None": 0
}

partenumero = []
parteletra = "None"  # define um valor default para caso não haja letra a ser convertida em potência

ram = input("Entre com o número de células da memória: ")

for i in list(ram):  # condicional que vai isolar o número inserido e categorizar o múltiplo
    if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        partenumero.append(i)
    else:
        parteletra = i

partenumero = ''.join(partenumero)  # junta a lista criada no laço condicional em uma string

potencia = int(math.log2(int(partenumero)) + potencia_celulas[parteletra])  # decompõe o número em sua devida
# potência de dois e soma com o valor do múltiplo inserido

ram = [None] * int(2 ** potencia)  # cria uma lista que vai servir como nosso bloco de memória principal,
# onde o index é o endereço da célula e o conteúdo é a palavra contida na célula (aqui cria-se uma memória
# essencialmente vazia)

for i in range(0, int(2 ** potencia)):  # esse laço for será responsável por preencher todas as células da memória com
    # número aleatório (número é dado em decimal e a função dectobin transforma o número em um binário de 8 bits)
    ram[i] = dectobin(random.randint(0, 255), 8)


def end_cache(end_ram):
    split_end = []  # lista para guardar, respectivamente, a tag, a linha e o byte da memoria cache nos espaços 0, 1 e 2
    controle = 1  # variável de controle para o loop for

    for index in range(0, len(end_ram), int(int(potencia / 3))):  # loop for responsável por separar os conjuntos de
        # bits que serão usados para a tag, a linha e o byte e colocar cada um em seu devido espaço na lista
        # split_end. o raciocínio começa dividindo o número de bits usados para endereçar a memória por 3,
        # o resultado será o número de bits que serão usados para endereçar a tag e as linhas. o restante dos bits
        # contidos na variavel end_ram serão os bits guardados na linha correspondente na memoria cache
        split_end.append(end_ram[index: index + int(potencia / 3)])
        if controle == 2:  # if usado para determinar quando o loop for já tiver agrupado os bits da tag e das linhas,
            # nesse caso ele irá agrupar o restante dos bits em seu próprio espaço da lista e sairá do loop
            split_end.append(end_ram[index + int(potencia / 3): potencia])
            break
        controle += 1
    return split_end


end_memoria = end_cache(dectobin(2 ** potencia - 1, potencia))  # pega o maior endereço da memória ram e joga na
# função end_cache
n_linha_cache = 2 ** len(end_memoria[1])  # calcula a quantidade de linhas da cache
n_coluna_cache = 1 + 2 ** len(end_memoria[2])  # calcula a quantidade de colunas da cache
memoria_cache = [None] * n_coluna_cache  # cria a primeira linha da cache com o número devido de colunas
memoria_cache = [memoria_cache]  # coloca essa linha dentro de uma lista
for i in range(0, n_linha_cache - 1):  # loop for responsavel por adicionar a quantidade devida de linhas na cache
    memoria_cache += [[None] * n_coluna_cache]

while True:
    celula_ram = input("Digite qual célula da RAM você quer acessar (em binário): ")
    cache = end_cache(celula_ram)  # separa o endereço especificado em uma lista com 3 elementos, sendo eles a tag,
    # a linha e a célula
    boole = False  # variavel booleana que será usada para definir se o endereç especificado se encontra na cache ou não
    tag = cache[0]  # coloca a tag em uma variável própria
    linha = bintodec(cache[1])  # transforma o número da linha em decimal e coloca em uma variável própria
    celula = bintodec(cache[2])  # transforma o número da célula em decimal e coloca em uma variável própria
    if memoria_cache[linha][0] == tag:  # verifica se o bloco se encontra na ram
        boole = True
    if boole == True:  # se o bloco estiver na cache, o programa apenas fará a leitura
        print("Endereço encontrado na memória cache!! Fazendo a leitura...")
        print("Byte contido no endereço solicitado:" + memoria_cache[linha][celula+1])
        print("Na memória principal: " + str(ram[bintodec(celula_ram)]))
        print(memoria_cache)
    else:  # se o bloco não estiver na cache o programa irá no endereço especificado na ram e atualizará a linha
        # correspondente da cache
        print("Endereço não encontrado na memória cache!! Procurando na memória principal...")
        memoria_cache[linha][0] = cache[0]  # atualiza a tag na devida linha
        for i in range(1, n_coluna_cache):  # itera por todas colunas atualizando com o valor de todas as células
            # pertencentes a este bloco da ram
            memoria_cache[linha][i] = ram[int(bintodec(cache[0] + cache[1] + dectobin(i-1, 3)))]
        print("Bloco da memória cache atualizada! O byte contido no endereço correspondente é: " + str(memoria_cache[linha][celula + 1]))
        print("Na memória principal: " + str(ram[bintodec(celula_ram)]))
        print(memoria_cache)