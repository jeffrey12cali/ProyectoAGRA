###################PROYECTO ARBOLES Y GRAFOS 2018###########################
"""
Estudiantes:
    Jeffrey García Gallego
    Mauricio Diaz Ćortés
"""

from sys import stdin
from collections import deque
from sys import setrecursionlimit

setrecursionlimit(1000)


class Comment():
    # Esta clase contiene información sobre los comentarios

    def __init__(self, arrow, body, author, ups, downs, id, date):
        # La inicialización muestra todos los atributos de la clase
        self.arrow = arrow
        self.body = body
        self.author = author
        self.ups = ups
        self.downs = downs
        self.id = id
        self.date = date
        # Todos los subcomentarios del comentario (self) se almacenan en la siguiente lista
        self.children = []


class kTree():
    # Esta clase será la estructura contenedora de los comentarios en general

    def __init__(self, data):
        # La inicialización del árbol recibe un dato que será el nodo raíz
        self.root = data        # Raíz
        self.levels = []        # Lista donde se almacenan los nodos por nivel
        self.nodes = 1          # Variable que lleva la cuenta de los nodos

    def __len__(self):
        # Retorna la cantidad de nodos en el árbol
        return self.nodes

    def makeChild(self, Comment, level):
        # Esta función se encarga asignar un nodo como hijo de otro
        # Para esto recibe el Comentario que será el hijo y el nivel del padre correspondiente
        self.levels[level][-1].children.append(Comment)
        self.nodes += 1


def parse_input(line):


    body, author, upstr, downstr, id, date = ('',) * 6

    arrow, ups, downs = (0,) * 3

    arrow1, body1, author1, ups1, downs1, id1, date1 = (True,) * 7

    i = len(line)-3
    while i > 0:
        
        
        # for i in range(len(line)):

        if date1:

            if line[i] != '|':
                date += line[i]
                
            else:
                date1 = False
                i -= 1
                date=date[::-1]

                #print(date)
                continue

        if id1 and not(date1):
            if line[i] != '|':

                id += line[i]
            else:
                # print("Entre al condi")
                id1 = False
                # print(body)
                i -= 1
                id=id[::-1]
                #print(id)
                continue

        if not(id1) and downs1:
            
            while line[i] != '|':
                #print(line[i])
                downstr += line[i]
                i -= 1

            #print("SSS")
            downs1 = False
            downs=int(downstr[::-1])
            #print(downs)
            i -= 1
            continue
        
# {indent_arrow}{body}[{author}|{ups}|{downs}|{comment_id}|{date}]

        if not(downs1) and ups1:
            while line[i] != '|':
                upstr += line[i]
                i -= 1

                # print(upstr,1)
            ups = int(upstr[::-1])
            ups1 = False
            #print(ups)
            i -= 1
            continue

        if not(ups1) and author1:

            #print(line[i])
            if line[i] != '[':
                author += line[i]
            else:
                author1 = False
                i -= 1
                author=author[::-1]
                #print(author)
                break

        i -= 1

        
    if not(author1) and arrow1:
        j=0
        while line[j] != '>':
            arrow+=1
            j+=1
        arrow1=False
        j+=1



    if not(arrow1) and body1:
        while j <= i:
            body+=line[j]
            j+=1
        body1=False
                
          
    

    comment = Comment(arrow // 2, body, author, ups, downs, id, date)

    return comment


def make_tree(tree, i):
    # Esta función se encarga de construir el árbol
    # Recibe un árbol (vacío) y un iterador (que se usa para la lista de usuarios)

    ## Esta parte (de abajo) se utiliza para reunir los usuarios en el diccionario ##
    global users

    flag = True

    # Se toma la linea del input
    line = stdin.readline()
    # Se comprueba que no haya llegado al final del input file
    if len(line) == 0:
        return tree
    else:
        # Se crea el nodo comentario correspondiente
        comment = parse_input(line)

    # Se comprueba que el usuario ya esté en el diccionario
    try:
        users[comment.author]
    except:
        flag = False
    # Si no lo está, se añade
    if flag is False:
        users[comment.author] = i
        i += 1

    ## Esta parte (de arriba) se utiliza para reunir los usuarios en el diccionario ##

    # Si es el nodo raíz, se pone ese nodo como raíz en el árbol y se añade a la lista de niveles
    if comment.arrow == 0:
        tree.root = comment
        tree.levels.append([comment])
        make_tree(tree, i)
    # Si es otro nodo distinto al de raíz
    else:
        # Si el nivel de ese comentario no está en la lista de niveles, se agrega
        if comment.arrow not in range(len(tree.levels)):
            tree.levels.append([comment])
        # De lo contrario se añade al nivel correspondiente
        else:
            tree.levels[comment.arrow].append(comment)
        # El comentrio actual se hace hijo de un padre de su nivel anterior
        tree.makeChild(comment, comment.arrow - 1)
        make_tree(tree, i)


def preorderTraversal(root):
    # Esta fuńción se encarga de imprimir el preorder del árbol

    Stack = deque([])
    # La lista Preorder contiene el resultado
    Preorder = []
    Preorder.append(root.id)
    Stack.append(root)
    while len(Stack) > 0:
        # 'flag' verifica que todos los nodos hijos hayan sido visitados
        flag = 0
        # Caso 1: Si el tope de la pila es una hoja, entonces se saca de la pila
        if len((Stack[len(Stack) - 1]).children) == 0:
            X = Stack.pop()
        # Caso 2: Si el tope de la pila es un padre con hijos
        else:
            Par = Stack[len(Stack) - 1]
        # Si se encuentra un hijo no visitado, entonces este se mete a la pila
        # y se guarda en la lista auxiliar marcado como visitado.
        # Se empieza otra vez desde el caso 1, para explorar el nuevo nodo
        for i in range(0, len(Par.children)):
            if Par.children[i].id not in Preorder:
                flag = 1
                Stack.append(Par.children[i])
                Preorder.append(Par.children[i].id)
                break
                # Si todos los nodos hijos han sido visitados, entonces
                # se saca al padre de la pila
        if flag == 0:
            Stack.pop()
    # Se retorna la solución que es la lista en preorder
    return Preorder


def sumOfNodes(node):
    sumN[node.id] = [node.ups, node.downs]

    for s in node.children:
        # print(node.id,"y")

        sumOfNodes(s)
        sumN[node.id][0] += sumN[s.id][0]
        sumN[node.id][1] += sumN[s.id][1]


def getUsernames(root, dic, counts, ans):
    # Esta función se encarga de conseguir los nombres de usuario de los autores
    # como también el número de comentario hechos en el post
    # Recibe como parámetros la raíz del árbol, un diccionario que contiene
    # los nombres de usuarios asociados a un número desde 0 hasta N-1
    # (siendo N el número de usuarios que comentarion en el post),
    # una lista "counts" que va a contener las ocurrencias de cada usuario a lo largo
    # del post y por último "ans" que es la lista donde se almacenará la tupla
    # (nombre_de_usuario, ocurrencias_en_el_post)

    counts[dic[root.author]] += 1
    ans[dic[root.author]] = (root.author, counts[dic[root.author]])
    for node in root.children:
        getUsernames(node, dic, counts, ans)


def main():
    # Global: users (utilizado en la función getUsernames()), sumN (utilizado en la función
    # sumOfNodes)
    global users, sumN
    sumN = {}
    users = {}
    # Fin de las variables globales

    # Comienzo del código principal
    # Se crea una instancia árbol con un nodo 0, que luego será reescrito
    tree = kTree(0)
    # Se arma el árbol con el árbol declarado anteriormente
    make_tree(tree, 0)
    # Se procesa la lista de preorder del árbol
    ans = preorderTraversal(tree.root)
    for id in ans[:-1]:
        print(id, end=" ")
    print(ans[-1], end='')
    sumOfNodes(tree.root)
    print()
    for id in ans[:]:
        print(sumN[id][0], sumN[id][1])
    # Se inicializa la lista donde estará la lista de usuarios con
    # sus respectivas ocurrencias
    ans = [0 for _ in range(len(users))]
    # Se inicializa la lista que cuenta los ocurrencias de los
    # usuarios
    counts = [0 for _ in range(len(users))]
    # Se genera la lista de usuarios y ocurrencias en la lista ans
    # como tuplas
    getUsernames(tree.root, users, counts, ans)
    # Se ordena la lista primero con el criterio de las ocurrencias en
    # orden descendente y se desempata con el orden léxicográfico
    ans.sort(key=lambda tup: (-tup[1], tup[0]))
    # Se imprime cada autor con su respectiva ocurrencia
    for author, count in ans:
        print(author, count)


main()
