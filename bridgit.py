from tkinter import *
from tkinter import  Tk
import networkx as nx

class App():

    def __init__(self):
        self.ventana=Tk()
        self.ventana.geometry("800x450")

        self.listaBotonesAzules=[] #para manipulacion de botnes
        self.posicionesAzules=[]
        self.listaLabelsRojos=[] #para manipulacion de labels rojos
        self.listaPosicionesRojos=[] #lista de las posiciones de los espacios para saber su ubicacion
        self.listaEspacios=[] #lista de los labels de ls espacios para poder manipularlos
        self.posicionesEspaciones=[]

        self.inicio=[]#ubicacion del boton inicial
        self.fin=[]#ubicacion del boton final
        #self.turnoJugador=True
        self.win=False

        self.puertoAR=[0,6,12,18,24]
        self.puertoBR=[5,11,17,23,29]
        self.grafoRojos=nx.Graph()
        self.caminoRojo=nx.Graph()
        self.caminoAzules=nx.Graph()

        start=Button(self.ventana, text="START", command=lambda: [self.partida(self.listaBotonesAzules,self.posicionesAzules,self.listaLabelsRojos,self.listaPosicionesRojos,
                                                                        self.listaEspacios,self.posicionesEspaciones)])
        start.place(x=500,y=350)

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
                    if color=="azul":
                        listaEspacios[i].config(bg="blue")
                        #agregar nodos de los puntos Azules que ahora tienen un camino
                        self.caminoAzules.add_node(inicio[0][2])
                        self.caminoAzules.add_node(fin[0][2])
                        self.caminoAzules.add_edge(inicio[0][2],fin[0][2])
                    else:
                        listaEspacios[i].config(bg="red")
                        self.caminoRojo.add_node(caminoCorto[i])
                        self.caminoRojo.add_node(caminoCorto[i+1])
                        self.caminoRojo.add_edge(caminoCorto[i],caminoCorto[i+1])
                        print(nx.edges(self.caminoRojo))
                        self.comprobarWin()
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

        return r,c

    def eliminarVertice(self,lista, idBoton, listaEspacios, posEspacios,posRojos,G):

        #identificar el la conexion entre puntos azule
        r=c=0 #fila y columna del punto de conexion entre botones
        if len(self.inicio)==0:
            self.inicio.append(lista[idBoton])
            self.inicio[0].append(idBoton)
        elif len(self.fin)==0:
            self.fin.append(lista[idBoton])
            self.fin[0].append(idBoton)

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
        corto=0
        pPartida=0 #punto de partida
        pLlegada=0 #putno de llegada
        aux=0
        for i in range(len(self.puertoAR)):
            for j in range(len(self.puertoBR)):
                if nx.has_path(gRojos,self.puertoAR[i],self.puertoBR[j]) is  True:
                    aux=len(nx.dijkstra_path(gRojos,self.puertoAR[i],self.puertoBR[j]))

                    if corto>aux and i!=0 and j!=0:
                        corto=aux
                        pPartida=self.puertoAR[i]
                        pLlegada=self.puertoBR[j]
                    else:
                        corto=len(nx.dijkstra_path(gRojos,self.puertoAR[i],self.puertoBR[j]))
                else:
                    self.puertoBR.pop(j)

        #dibujar conexion
        caminoCorto=nx.dijkstra_path(gRojos,pPartida,pLlegada)
        inicio=[]
        fin=[]


        for i in range(len(caminoCorto)):
            print(caminoCorto)
            if i<len(caminoCorto)-1:
                posicion1=caminoCorto[i]
                posicion2=caminoCorto[i+1]
                inicio.append(posRojos[posicion1])
                fin.append(posRojos[posicion2])
                print(posicion1,posicion2)
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

                    print(nx.edges(self.caminoRojo))
                    self.comprobarWin()
                    break

    def turnoUsuario(self):
        Label(self.ventana, text="Turno del jugador").place(x=500,y=400)

        if len(self.inicio)>0 and len(self.fin)>0:
            #funcion que activa a la computadora
            self.encontrarCamino(self.grafoRojos,self.listaPosicionesRojos, self.posicionesEspaciones)
            #ya al encontrar el camino limpia las listas inicio y fin
            for i in range(len(self.inicio)):
                self.inicio.pop(i)
            for i in range(len(self.fin)):
                self.fin.pop(i)

    def comprobarWin(self):

        for i in range(len(self.puertoAR)):
            for j in range(len(self.puertoBR)):
                #print(i,j)
                #print(self.puertoAR[i],self.puertoBR[j])
                #print(nx.has_path(self.caminoRojo,self.puertoAR[i],self.puertoBR[j]))

                #print(self.puertoAR[i],self.puertoBR[j])
                if self.caminoRojo.has_node(self.puertoAR[i]) is True and self.caminoRojo.has_node(self.puertoBR[j]) and nx.has_path(self.caminoRojo,self.puertoAR[i],self.puertoBR[j]) is True:
                    #self.win=True
                    print('usted ha perdido')
                    Label(self.ventana,text='usted ha perdido').place(x=500,y=200)

    def partida(self,listaBotonesAzules,posicionesAzules,listaLabelsRojos,listaPosicionesRojos,listaEspacios,posicionesEspaciones):
        i=j=k=0 #indice par botones azules,rojos y espacios


        #creando botones azules, labels rojos y espacios
        for r in range(0,11):
            for c in range(0,11):
                if r%2==0:
                    if c%2!=0:
                        posicionesAzules.append([r,c])

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
