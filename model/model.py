import networkx as nx

from database.DAO import DAO
from model.edge import Edge


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._products = []
        self._idMapProducts = {}
        self._allEdges = []

        self._bestPath = []
        self._bestScore = 0


    def buildGraph(self, color, year):
        self._graph.clear()
        self._products = self.getProductsByColor(color)
        self._graph.add_nodes_from(self._products)
        self._allEdges = self.getAllEdges(color, year)
        for e in self._allEdges:
            self._graph.add_edge(e.p1, e.p2, weight=e.peso)


    def getBestPath(self, productNumber):
        source = self._idMapProducts[productNumber]
        parziale = []
        self._ricorsione(parziale, source, 0)
        print("final", len(self._bestPath), [i[2]["weight"] for i in self._bestPath])


    def _ricorsione(self, parziale, ultimoNodo, livello):
        archiViciniAmmissibili = self.getArchiViciniAmmissibili(ultimoNodo, parziale)
        #condizione terminale
        if len(archiViciniAmmissibili) == 0:
            if len(parziale) > len(self._bestPath):
                self._bestPath = list(parziale)
                print(len(self._bestPath), [ii[2]["weight"] for ii in self._bestPath])
        #ricorsione
        for a in archiViciniAmmissibili:
            parziale.append(a)
            self._ricorsione(parziale, a[1], livello + 1)
            parziale.pop()


    def getArchiViciniAmmissibili(self, ultimoNodo, parziale):
        archiVicini = self._graph.edges(ultimoNodo, data=True)
        result = []
        for a in archiVicini:
            if self.isAscendent(a, parziale) and self.isNovel(a, parziale):
                result.append(a)
        return result


    def isAscendent(self, e, parziale):
        if len(parziale) == 0:
            print("parziale vuoto in isAscendent")
            return True
        return e[2]["weight"] >= parziale[-1][2]["weight"]


    def isNovel(self, e, parziale):
        if len(parziale) == 0:
            print("parziale vuoto in isNovel")
            return True
        e_inv = (e[1], e[0], e[2])
        return (e_inv not in parziale) and (e not in parziale)


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()


    def getArchiMaggiori(self):
        listaArchi = self._allEdges
        listaArchi.sort(reverse=True)
        maggiori = listaArchi[0:3]
        ripetuti = self.getRipetizioniNodi(maggiori)
        return maggiori, ripetuti


    def getRipetizioniNodi(self, lista):
        visti = []
        ripetuti = []
        for n in lista:
            if n.p1.Product_number in visti:
                ripetuti.append(n.p1.Product_number)
            else:
                visti.append(n.p1.Product_number)
            if n.p2.Product_number in visti:
                ripetuti.append(n.p2.Product_number)
            else:
                visti.append(n.p2.Product_number)
        return ripetuti


    def getAllEdges(self, color, year):
        self._allEdges = DAO.getAllEdges(color, year, self._idMapProducts)
        return self._allEdges


    def getAllColors(self):
        return DAO.getAllColors()


    def getAllYears(self):
        return DAO.getAllYears()


    def getProductsByColor(self, color):
        self._products = DAO.getAllProductsByColor(color)
        for product in self._products:
            self._idMapProducts[product.Product_number] = product
        return self._products
