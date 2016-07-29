import itertools

def separate(T,c,i):
	# A funcao recebe uma lista T e retorna duas listas:
	#t1: Contem todos os elementos de T que contem a cor "c" ma posicao "i"
	#t2: Eh o complemento da lista t1
	
	#Inicia as listas que serão retornadas (t1 e t2):
	t1 = []
	t2 = []

	#Percorre todos os elementos da lista T
	for j in T:
		#flag indica se a cor "c" esta na posicao "i" da string j
		flag = False
		for k in i:
			#Em caso afirmativo, o elemento j da lista T vai para t1
			if j[k] == c:
				t1.append(j)
				flag = True

				#Esse break esta aqui pois ele eh "necessario" na hora de eliminar as strings candidatas
				#a solucao do problema que violam a restricao do mesmo, na funcao graph_coloring().
				#Ao encontrarmos um vertice que ja viola a restricao, nao precisamos percorrer o resto da
				#string, pois aquela string ja nao serve mais para ser solucao do problema. O que eu
				#tentei fazer aqui foi isso: parar de percorrer a string quando ja fossem encontrados dois
				#vertices adjacentes com a mesma cor.
				#Um comentario maior sobre a funcao esta descrito no final do codigo.
				break
		# Em caso negativo, o elemento j da lista T vai para t2
		if not flag:
			t2.append(j)
	return t1,t2

def merge(a,b,c):
	#A funcao apenas recebe tres listas, concatena essas listas e retorna uma nova lista,
	#que eh a concatenacao das tres listas passadas como argumento para a funcao
	T = a + b + c
	return T

def detect(T):
	#Como eu tentei seguir tudo que esta escrito no livro, o resultado final do algoritmo
	#ficou desse jeito.

	#A funcao verifica se T eh um conjunto nao-vazio
	#Se T eh nao-vazio, retorna TRUE
	if len(T) > 0:
		print ("TRUE")

	#Caso contrario, retona FALSE
	else:
		print ("FALSE")

def multi_conjunto_inicial(n):
	#Essa funcao eh usada para gerar o multi-conjunto inicial, que eh o conjunto que contem
	#todas as coloracoes que sao candidatas a solucao para o problema de coloracao de um
	#grafo. Nesse conjunto, estao presentes coloracoes que nao sao solucoes validas para
	#o problema, ou seja, solucoes em que dois vertices adjacentes estao coloridos com a
	#mesma cor.

	#O que essa funcao faz eh gerar uma lista, que eh um arranjo com repeticao essencialmente,
	#que tem como elemento todas as sequencias possiveis, com tamanho "n", de "r", "g" e "b",
	#sendo que os elementos podem estar repetidos nessas sequencias (por isso um arranjo com 
	#repeticao). No caso, o tamanho da lista retornada sera 3 * 3 * 3 * ... * 3 = 3^n. 
    T = list(itertools.product(['r','g','b'],repeat=n))
    return T

def graph_coloring(T,adj):
	#Essa eh a funcao que efetivamente implementa o algoritmo do modelo irrestrito
	#apresentado na ultima reuniao sobre a IC

	#O "for" abaixo percorre todos os vertices do grafo. Para cada vertice, executamos o
	#seguinte algoritmo:  
	for i in range(0,n):

		#Iniciamos as listas auxiliares, para realizarmos a filtragem do conjunto T
		T_r = []
		T_bg = []
		T_g = []
		T_b = []
		#Em alguns passos do algoritmo, eh interessante utilizar apenas um dos 2 conjuntos
		#retornados pela funcao separate(). Por isso, criei mais uma lista auxiliar, para ser
		#o "coletor de lixo"
		GARBAGE_COLLECTOR = []

		#Vamos dividir o conjunto T em dois conjuntos: 
		#T_r, que so contem elementos de T com a cor "r" na posicao "i", e
		#T_bg, que eh o complemento de T_r 
		T_r,T_bg = separate(T,'r',[i])

		#Agora, vamos dividir o conjunto T_bg em dois conjuntos:
		#T_b, que so contem elementos de T_bg com a cor "b" na posicao "i", e
		#T_g, que so contem elementos de T_bg com a cor "g" na posicao "i".
		T_b,T_g = separate(T_bg,'b',[i])

		#Com isso, dividimos o nosso conjunto inicial T em tres conjuntos:
		#T_r, que so contem elementos de T com a cor "r" na posicao i;
		#T_g, que so contem elementos de T com a cor "g" na posicao i;
		#T_b, que so contem elementos de T com a cor "b" na posicao i;

		#A partir de agora, vamos eliminar as sequencias candidatas a solucao que violam a
		#restricao do problema que esta sendo considerado: Dois vertices adjacentes nao podem
		#ter a mesma cor.
		#Nas proximas 3 linhas, retiramos de T_r, T_g e T_b, os vizinhos do vertice "i" (que
		#estao em adj[i]) que estao coloridos com "r", "g" e "b", respectivamente.
		GARBAGE_COLLECTOR,T_r = separate(T_r,'r',adj[i])
		GARBAGE_COLLECTOR,T_g = separate(T_g,'g',adj[i])
		GARBAGE_COLLECTOR,T_b = separate(T_b,'b',adj[i])

		#Apos elmiminarmos as strings que violam a restricao do problema, juntamos as listas
		#T_r, T_g e T_b em uma nova lista T, que eh a concatenacao dessas tres.
		T = merge(T_r,T_g,T_b)
		#Agora repetimos o mesmo algoritmo para o proximo vertice

	#Ao final da execucao do algoritmo, se T eh nao-vazio, entao existe alguma coloracao possivel
	#para o grafo que respeite a restricao de cor entre vertices adjacentes; caso contrario, ou seja,
	#se T for vazio, o grafo nao admite nenhuma coloracao utilizando 3 cores que respeite a restricao.
	detect(T)

#Vamos aplicar o algoritmo ao grafo de Petersen, que tem 10 vertices
n = 10

#Vamos gerar o multi-conjunto inicial:
T = multi_conjunto_inicial(n)

#O trecho a seguir resolve um problema que surge por causa da forma do conjunto T, que eh retornada
#pela funcao multi_conjunto_inicial() (Vou chamar de MCS() a partir de agora, o nome original eh muito grande).
#A MSC() retorna uma lista, e cada elemento da lista eh uma tupla, e cada elemento dessa tupla eh um unico
#caracter. Para ilustrar o que eu quero dizer, uma parte do retorno da MSC() eh isso:

#[('r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'), ('r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'g')]

#So que nao eh isso que eu quero. O que eu desejo eh que T seja uma lista e cada elemento da lista seja uma 
#string. Ou seja, eu quero transformar ('r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r') em 
#'rrrrrrrrrr'. Eh exatamente isso o que esse trecho de codigo abaixo faz:

lista = []
#tam recebe o tamanho de T. No caso do grafo de Petersen, tam = 3^(10) = 59049
tam = len(T)

#Para cada elemento de T
for j in range(0,tam):
	#Armazeno o elemento da lista T na posicao "j" em uma variavel auxiliar
	#Por exemplo, quando j = 0, aux = ('r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r')
    aux = T[j]
    #A variavel palavra sera uma variavel auxiliar
    palavra = ''
    for k in range(0,n):
    	#Para cada elemento k na tupla aux, eu concateno o elemento k, convertido para string,
    	#no final da variavel palavra
        palavra = palavra + str(aux[k])
    
    #Ao da primeira execucao "for", palavra = 'rrrrrrrrrr' 
    # Ao final da execucao do "for" mais "interno" do codigo, eu adiciono a variavel 
    #palavra a lista de strings que estao no formato que eu quero.
    lista.append(palavra)
#Ao final, T esta da forma desejada
T = lista

#Defino a lista de adjacencias
adj = [[1,4,5],[0,2,6],[1,3,7],[2,4,8],[0,3,9],[0,7,8],[1,8,9],[2,5,9],[3,5,6],[4,6,7]]

#Chamo a funcao que roda o algoritmo
graph_coloring(T,adj)
