import networkx as nx
from colorama import  Fore
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._products=[]
        self._sales=[]
        self._idMap={}
        self._solBest = []

    def getIDMap(self):
        return self._idMap
    def create_graph(self,year,color):
        self._grafo.clear()
        nodes=self._products
        products=[]
        for node in nodes:
            if node.Product_color==color:
                if node.Product_number not in products:
                    self._grafo.add_node(node)
                    products.append(node.Product_number)
        sales=DAO.getSalesYear(year,products)
        checked=[]
        i=0
        edges=[]
        for retailer in sales:
            for sale1 in sales[retailer]:
                for sale2 in sales[retailer]:
                    i+=1
                    if sale1.product_number!=sale2.product_number and sale1.retailer_code==sale2.retailer_code:
                        if (self._idMap[sale1.product_number], self._idMap[sale2.product_number]) not in checked and (self._idMap[sale2.product_number], self._idMap[sale1.product_number]) not in checked:
                            checked.append((self._idMap[sale1.product_number], self._idMap[sale2.product_number]))
                            weight=DAO.getWeight(sale1.product_number,sale2.product_number,year)
                            if (self._idMap[sale1.product_number], self._idMap[sale2.product_number], weight) not in self._grafo.edges and weight>0:
                                edges.append((self._idMap[sale1.product_number],self._idMap[sale2.product_number], weight))
                                print(Fore.RED+f"{self._idMap[sale1.product_number]}, {self._idMap[sale2.product_number]} ,weight={weight}, colors={self._idMap[sale1.product_number].Product_color};{self._idMap[sale2.product_number].Product_color}, yer={sale2.date};{sale1.date}","red")
                    else:
                            print(Fore.WHITE+str(i))

        for u,v,w in edges:
            self._grafo.add_edge(u,v,weight=w)
        return edges


    def get_products(self):
        self._products=DAO.getAllProducts()
        for product in self._products:
            self._idMap[product.Product_number] = product
            print(product)
        return self._products


    def searchPath(self, product_number):
        nodoSource = self._idMap[product_number]

        parziale = []

        self.ricorsione(parziale, nodoSource, 0)


        print("final", len(self._solBest), [i[2]["weight"] for i in self._solBest])

    def ricorsione(self, parziale, nodoLast, livello):
        archiViciniAmmissibili = self.getArchiViciniAmm(nodoLast, parziale)
        print("s")
        if len(archiViciniAmmissibili) == 0:
            if len(parziale) > len(self._solBest):
                self._solBest = list(parziale)
                print(len(self._solBest), [ii[2]["weight"] for ii in self._solBest])

        for a in archiViciniAmmissibili:
            parziale.append(a)
            self.ricorsione(parziale, a[1], livello + 1)
            parziale.pop()

    def getArchiViciniAmm(self, nodoLast, parziale):

        archiVicini = self._grafo.edges(nodoLast, data=True)
        result = []
        for a1 in archiVicini:
            if self.isAscendent(a1, parziale) and self.isNovel(a1, parziale):
                result.append(a1)
        return result

    def isAscendent(self, e, parziale):
        if len(parziale)==0:
            print("parziale is empty in isAscendent")
            return True
        return e[2]["weight"] >= parziale[-1][2]["weight"]
    def isNovel(self, e, parziale):
        if len(parziale)==0:
            print("parziale is empty in isnovel")
            return True
        e_inv = (e[1], e[0], e[2])
        return (e_inv not in parziale) and (e not in parziale)

        #if (e_inv not in partial_edge) and (e not in partial_edge):
        #    return True
        #else:
        #    return False

    def get_sales(self):
        self._sales=DAO.getAllSales()
        return self._sales

    def getNumNodes(self):
        return self._grafo.number_of_nodes()
    def getNumEdges(self):
        return self._grafo.number_of_edges()
    def getNodes(self):
        return self._grafo.nodes()
    def getEdges(self):
        return self._grafo.edges()

    def getGrafo(self):
        return self._grafo