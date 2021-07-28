from tkinter import *
from tkinter import  Tk
import networkx as nx

class App():

    def __init__(self):
        self.ventana=Tk()
        self.ventana.geometry("600x450")
        self.listaBotonesAzules=[] #para manipulacion de botnes
        self.posicionesAzules=[]
        self.listaLabelsRojos=[] #para manipulacion de labels rojos
        self.listaPosicionesRojos=[] #lista de las posiciones de los espacios para saber su ubicacion
        self.listaEspacios=[] #lista de los labels de ls espacios para poder manipularlos
        self.posicionesEspaciones=[]

        self.inicio=[]#ubicacion del boton inicial
        self.fin=[]#ubicacion del boton final

        self.puertoARojos=[0,6,12,18,24]
        self.puertoBRojos=[5,11,17,23,29]

        self.puertoAAzules=[0,1,2,3,4]
        self.puertoBAzules=[25,26,27,28,29]

        self.grafoRojos=nx.Graph()
        self.caminoRojo=nx.Graph()
        self.caminoAzules=nx.Graph()

        start=Button(self.ventana, text="START", bg="green",fg="white", command=lambda: [self.partida(self.listaBotonesAzules,self.posicionesAzules,self.listaLabelsRojos,self.listaPosicionesRojos,
                                                                        self.listaEspacios,self.posicionesEspaciones)])
        start.place(x=400,y=200)

        self.turno=Label(self.ventana, text="Turno del jugador")
        self.turno.place(x=400,y=300)
        self.turno.config(state="disabled")

        self.ventana.mainloop()

    def asignarVertices(self,lista,G):
        for i in range(0,len(lista)):

            r=lista[i][0]
            c=lista[i][1]

            #vecino izquierdo
            if c!=0:
                auxC=c-2
                for j in range(0,len(lista)):
                    if r==lista[j][0] and auxC==lista[j][1] and i!=j:
                        G.add_edge(i,j)

            #vecino arriba
            if r!=0:
                auxR=r-2
                for j in range(0,len(lista)):
                    if auxR==lista[j][0] and c==lista[j][1] and i!=j:
                        G.add_edge(i,j)

            #vecino derecho
            if c!=10:
                auxC=c+2
                for j in range(0,len(lista)):
                    if r==lista[j][0] and auxC==lista[j][1] and i!=j:
                        G.add_edge(i,j)

            #vecino abajo
            if r!=10:
                auxR=r+2
                for j in range(0,len(lista)):
                    if auxR==lista[j][0] and c==lista[j][1] and i!=j:
                        G.add_edge(i,j)

    def encontrarEspacio(self, inicio, fin,listaEspacios, posEspacios,color):

        if inicio[0][1]==fin[0][1]: #verificar si la conexion es vertical
            c=inicio[0][1]
            if inicio[0][0]>fin[0][0]:
                r=inicio[0][0]-1
            else:
                r=inicio[0][0]+1
            #buscando el espacio correspondiente al punto r,c
            for i in range(len(listaEspacios)):
                #conexiones verticales
                if r==posEspacios[i][0] and c==posEspacios[i][1]:

                    posicion1=inicio[0][2]
                    posicion2=fin[0][2]
                    if color=="azul":
                        listaEspacios[i].config(bg="blue")
                        #agregar nodos de los puntos Azules que ahora tienen un camino
                        self.caminoAzules.add_node(posicion1)
                        self.caminoAzules.add_node(posicion2)
                        self.caminoAzules.add_edge(posicion1,posicion2)

                        self.comprobarWin('jugador')
                    else:
                        listaEspacios[i].config(bg="red")
                        self.caminoRojo.add_node(posicion1)
                        self.caminoRojo.add_node(posicion2)
                        self.caminoRojo.add_edge(posicion1,posicion2)
                        self.comprobarWin('PC')
        else: #los puntos estan la en misma fila //se movio verticalmente

            r=inicio[0][0]

            if inicio[0][1]>fin[0][1]:
                c=inicio[0][1]-1
            else:
                c=inicio[0][1]+1
            #buscando el espacio correspondiente al punto r,c
            for i in range(len(listaEspacios)):
                #conexiones verticales

                if r==posEspacios[i][0] and c==posEspacios[i][1]:
                    if color=="azul":

                        listaEspacios[i].config(bg="blue")
                        #agregar nodos de los puntos Azules que ahora tienen un camino
                        self.caminoAzules.add_node(inicio[0][2])
                        self.caminoAzules.add_node(fin[0][2])
                        self.caminoAzules.add_edge(inicio[0][2],fin[0][2])
                        self.comprobarWin('jugador')

        return r,c

    def eliminarVertice(self,lista, idBoton, listaEspacios, posEspacios,posRojos,G):

        #identificar el la conexion entre puntos azule
        r=c=0 #fila y columna del punto de conexion entre botones
        if len(self.inicio)==0:
            self.inicio.append(lista[idBoton])
            #self.inicio[0].append(idBoton)
        elif len(self.fin)==0:
            self.fin.append(lista[idBoton])
            #self.fin[0].append(idBoton)

        if (self.inicio)!=0 and len(self.fin)!=0:
            r,c=self.encontrarEspacio(self.inicio,self.fin, self.listaEspacios,self.posicionesEspaciones,"azul")

            #buscamos los puntos del vertice que hay que eliminar
            auxIzq=c-1 #putno de la izquierda del espacio
            auxDer=c+1 #punto de la derecha del espacio
            izquierda=0
            derecha=0

            for i in range(len(posRojos)):

                if r==posRojos[i][0] and auxIzq==posRojos[i][1]:
                    izquierda=i
                if r==posRojos[i][0] and auxDer==posRojos[i][1]:
                    derecha=i

                if  G.has_edge(izquierda,derecha) is True:
                    G.remove_edge(izquierda,derecha)

    def encontrarCamino(self,gRojos,posRojos,posEspacios):
        self.turno.config(state="disabled", bg='gray')
        corto=0
        pPartida=0 #punto de partida
        pLlegada=0 #putno de llegada
        aux=r=c=0
        posicion1=posicion2=0
        for i in range(len(self.puertoARojos)):
            for j in range(len(self.puertoBRojos)):
                if nx.has_path(gRojos,self.puertoARojos[i],self.puertoBRojos[j]) is  True:
                    aux=len(nx.dijkstra_path(gRojos,self.puertoARojos[i],self.puertoBRojos[j]))

                    if corto>aux and i!=0 and j!=0:
                        corto=aux
                        pPartida=self.puertoARojos[i]
                        pLlegada=self.puertoBRojos[j]
                    else:
                        corto=len(nx.dijkstra_path(gRojos,self.puertoARojos[i],self.puertoBRojos[j]))
                else:
                    self.puertoBRojos.pop(j)

        #dibujar conexion
        caminoCorto=nx.dijkstra_path(gRojos,pPartida,pLlegada)
        inicio=[]
        fin=[]


        for i in range(len(caminoCorto)):

            if i<len(caminoCorto)-1:
                posicion1=caminoCorto[i]
                posicion2=caminoCorto[i+1]
                inicio.append(posRojos[posicion1])
                inicio[0].append(posicion1)
                fin.append(posRojos[posicion2])
                fin[0].append(posicion2)
                r,c=self.encontrarEspacio(inicio,fin, self.listaEspacios,self.posicionesEspaciones,"rojo")

            if len(inicio)>0 and len(fin)>0:
                for i in range(len(self.inicio)):
                    inicio.pop(i)
                for i in range(len(self.fin)):
                    fin.pop(i)

            if [r,c] in posEspacios:
                aux=posEspacios.index([r,c])
                if self.listaEspacios[aux].cget('bg')!="red":
                    self.listaEspacios[aux].config(bg="red")
                    #agregar nodos de los puntos rojos que ahora tienen un camino
                    self.caminoRojo.add_node(posicion1)
                    self.caminoRojo.add_node(posicion2)
                    self.caminoRojo.add_edge(posicion1,posicion2)
                    self.comprobarWin('PC')

                    print(nx.edges(self.caminoRojo))

                    break

    def turnoUsuario(self):
        self.turno.config(state="normal",bg='green')

        if len(self.inicio)>0 and len(self.fin)>0:
            #funcion que activa a la computadora
            self.encontrarCamino(self.grafoRojos,self.listaPosicionesRojos, self.posicionesEspaciones)
            #ya al encontrar el camino limpia las listas inicio y fin
            for i in range(len(self.inicio)):
                self.inicio.pop(i)
            for i in range(len(self.fin)):
                self.fin.pop(i)

    def comprobarWin(self,jugador):
        if jugador=='PC':
            for i in range(len(self.puertoARojos)):
                for j in range(len(self.puertoBRojos)):
                    if self.caminoRojo.has_node(self.puertoARojos[i]) is True and self.caminoRojo.has_node(self.puertoBRojos[j]) and nx.has_path(self.caminoRojo,self.puertoARojos[i],self.puertoBRojos[j]) is True:
                        #self.win=True

                        Label(self.ventana,text='usted ha perdido', bg='red',fg='white').place(x=400,y=350)
        else:
            for i in range(len(self.puertoAAzules)):
                for j in range(len(self.puertoBAzules)):
                    if self.caminoAzules.has_node(self.puertoAAzules[i]) is True and self.caminoAzules.has_node(self.puertoBAzules[j]) and nx.has_path(self.caminoAzules,self.puertoAAzules[i],self.puertoBAzules[j]) is True:

                        Label(self.ventana,text='usted ha ganado', bg='green',fg='white').place(x=400,y=350)

    def partida(self,listaBotonesAzules,posicionesAzules,listaLabelsRojos,listaPosicionesRojos,listaEspacios,posicionesEspaciones):
        i=j=k=0 #indice par botones azules,rojos y espacios


        #creando botones azules, labels rojos y espacios
        for r in range(0,11):
            for c in range(0,11):
                if r%2==0:
                    if c%2!=0:
                        posicionesAzules.append([r,c,i])
                        listaBotonesAzules.append(Button(self.ventana, text=str(i),width=2,fg="white", bg="blue",
                        command=lambda id=i: [self.turnoUsuario(),self.eliminarVertice(posicionesAzules,id,
                        listaEspacios,posicionesEspaciones,listaPosicionesRojos,self.grafoRojos)]))


                        listaBotonesAzules[i].grid(row=r,column=c)
                        i=i+1
                    else:
                        #espacio=Label(width=2).grid(row=r,column=c)
                        posicionesEspaciones.append([r,c])
                        listaEspacios.append(Label(width=2))
                        listaEspacios[k].grid(row=r,column=c)
                        k=k+1
                else:
                    if c%2==0:
                        listaLabelsRojos.append(Label(self.ventana, text=str(j),fg="white", bg="red",width=2 ))
                        listaLabelsRojos[j].grid(row=r,column=c)
                        listaPosicionesRojos.append([r,c])
                        #botonRojo=Button(self.ventana, text=str(j),fg="white", bg="red",width=2).grid(row=r,column=c)
                        #listaBotonesRojos.append([botonRojo,r,c])
                        self.grafoRojos.add_node(j)
                        j=j+1
                    else:
                        #espacio=Label(width=2).grid(row=r,column=c)
                        posicionesEspaciones.append([r,c])
                        listaEspacios.append(Label(width=2))
                        listaEspacios[k].grid(row=r,column=c)
                        k=k+1

        self.asignarVertices(self.listaPosicionesRojos, self.grafoRojos)


if __name__ == '__main__':
    App()
