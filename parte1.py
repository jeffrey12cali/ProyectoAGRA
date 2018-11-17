from sys import stdin
from collections import deque
from sys import setrecursionlimit
from datetime import datetime

setrecursionlimit(100000)

INF = float('inf')


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

    i = len(line) - 3
    while i > 0:

        # for i in range(len(line)):

        if date1:

            if line[i] != '|':
                date += line[i]

            else:
                date1 = False
                i -= 1
                date = date[::-1]

                # print(date)
                continue

        if id1 and not(date1):
            if line[i] != '|':

                id += line[i]
            else:
                # print("Entre al condi")
                id1 = False
                # print(body)
                i -= 1
                id = id[::-1]
                # print(id)
                continue

        if not(id1) and downs1:

            while line[i] != '|':
                # print(line[i])
                downstr += line[i]
                i -= 1

            # print("SSS")
            downs1 = False
            downs = int(downstr[::-1])
            # print(downs)
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
            # print(ups)
            i -= 1
            continue

        if not(ups1) and author1:

            # print(line[i])
            if line[i] != '[':
                author += line[i]
            else:
                author1 = False
                i -= 1
                author = author[::-1]
                # print(author)
                break

        i -= 1

    if not(author1) and arrow1:
        j = 0
        while line[j] != '>':
            arrow += 1
            j += 1
        arrow1 = False
        j += 1

    if not(arrow1) and body1:
        while j <= i:
            body += line[j]
            j += 1
        body1 = False

    comment = Comment(arrow // 2, body, author, ups, downs, id, date)

    return comment


def make_tree(tree, i, inTree, line):
    # Esta función se encarga de construir el árbol
    # Recibe un árbol (vacío) y un iterador (que se usa para la lista de usuarios)

    ## Esta parte (de abajo) se utiliza para reunir los usuarios en el diccionario ##
    global users

    flag = True

    # Se comprueba que no haya llegado al final del input file
    if len(line) == 0:
        # retorna una línea vacía
        return ''
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
        # Se comprueba que ya no esté leyéndose en un árbol
        if inTree is False:
            tree.root = comment
            tree.levels.append([comment])
            inTree = True
            return make_tree(tree, i, inTree, stdin.readline())
        # Si ya se está leyendo otro árbol, se retorna la linea en la que empieza el siguiente
        else:
            return line
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
        return make_tree(tree, i, inTree, stdin.readline())


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


def makeGraph(root, dic, G):
    global ans
    # Esta fuńción se encarga de imprimir el preorder del árbol

    Stack = deque([])
    Stack.append(root)
    while len(Stack) > 0:
        curr = Stack.pop()
        ady = avgTime(curr, dic)
        for i in range(len(ady)):
            flag = False
            if i != dic[curr.author] and ady[i] != [0, 0]:
                for j in range(len(G[dic[curr.author]])):
                    if G[dic[curr.author]][j][0] == i:
                        G[dic[curr.author]][j][1] = G[dic[curr.author]][j][1] + (ady[i][0] // ady[i][1])
                        # G[i][j][1] = G[i][j][1] + (ady[i][0] // ady[i][1])
                        flag = True

                if flag is False:
                    G[dic[curr.author]].append([i, ady[i][0] // ady[i][1]])
                    G[i].append([dic[curr.author], ady[i][0] // ady[i][1]])

        for i in curr.children[::-1]:
            Stack.append(i)

    for i in range(len(G)):
        for j in range(len(G[i])):
            G[i][j][1] = G[i][j][1] // ans[i][1] if G[i][j][1] // ans[i][1] > 0 else 1

    return G


def avgTime(root, dic):
    sums = [[0, 0] for _ in range(len(dic))]
    Stack = deque([])
    Stack.append(root)
    while len(Stack) > 0:

        curr = Stack.pop()

        sums[dic[curr.author]][0] += diff(root.date, curr.date)
        sums[dic[curr.author]][1] += 1

        for i in curr.children[::-1]:
            Stack.append(i)

    return sums


def parseDate(date):
    time = date[-8:]
    hour = int(time[0:2])
    min = int(time[3:5])
    sec = int(time[6:8])
    date = date[-19:-9]
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    return year, month, day, hour, min, sec


def diff(date_ini, date_end):
    yearI, monthI, dayI, hourI, minI, secI = parseDate(date_ini)
    yearE, monthE, dayE, hourE, minE, secE = parseDate(date_end)
    return (datetime(yearE, monthE, dayE, hourE, minE, secE) - datetime(yearI, monthI, dayI, hourI, minI, secI)).seconds


def main():
    # Global: users (utilizado en la función getUsernames()), sumN (utilizado en la función
    # sumOfNodes)
    global users, ans
    # Se lee la primera línea
    line = stdin.readline()
    while len(line) != 0:
        # Fin de las variables globales
        users = {}
        # Comienzo del código principal
        # Se crea una instancia árbol con un nodo 0, que luego será reescrito
        tree = kTree(0)
        # Se arma el árbol con el árbol declarado anteriormente
        line = make_tree(tree, 0, False, line)
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
        # ans.sort(key=lambda tup: (-tup[1], tup[0]))

        ##########################################################

        G = [list() for _ in range(len(users))]
        makeGraph(tree.root, users, G)
        print(G)


main()
