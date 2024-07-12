import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        products=self._model.get_products()
        for product in products:
            if product.Product_color not in self._listColor:
                self._listColor.append(product.Product_color)
        sales=self._model.get_sales()
        for sale in sales:
            if sale.date.year not in self._listYear:
                self._listYear.append(sale.date.year)
        for color in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))
        for year in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(year))

    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        if self._view._ddyear.value==None:
            self._view._txtOut.controls.append(ft.Text("Errore nell'anno inserito"))
            return
        if self._view._ddcolor.value==None:
            self._view._txtOut.controls.append(ft.Text("Errore nell colore inserito"))
            return
        edges=self._model.create_graph(self._view._ddyear.value,self._view._ddcolor.value)
        nodes=self._model.getNumNodes()
        numEdges=self._model.getNumEdges()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {nodes} Numero di archi: {numEdges}"))
        #edges=list(self._model.getEdges())
        edges.sort(key=lambda x:x[2], reverse=True)
        nodi=[]
        ripetuti=[]
        for i in range(3):
            self._view.txtOut.controls.append(ft.Text(f"arco da {edges[i][0]} a {edges[i][1]}, peso={edges[i][2]}"))
            if edges[i][0] not in nodi:
                nodi.append(edges[i][0])
            elif edges[i][0] in ripetuti:
                continue
            else:
                ripetuti.append(edges[i][0].Product_number)
            if edges[i][1] not in nodi:
                nodi.append(edges[i][1])
            elif edges[i][1] in ripetuti:
                continue
            else:
                ripetuti.append(edges[i][1].Product_number)
        self._view.txtOut.controls.append(ft.Text(f"i nodi ripetuti sono{ripetuti}"))
        self.fillDDProduct()
        self._view.update_page()
    def fillDDProduct(self):
        products = self._model.getNodes()
        for product in products:
            self._view._ddnode.options.append(ft.dropdown.Option(data=product,text=product.Product_number))

    def handle_search(self, e):
        self._model.searchPath(int(self._view._ddnode.value))
        self._view.txtOut2.controls.append(
            ft.Text(f"Numero archi percorso più lungo: {len(self._model._solBest)}"))
        self._view.update_page()

    def recursive(self,grafo,v0,percorsi,parziale,last):
        parziale.append(v0)
        for node in grafo.neighbors(v0):
            if (last<grafo[v0][node]["weight"]):
                parziale.append(node)
                last=grafo[v0][node]["weight"]
                self.recursive(grafo,v0,percorsi,parziale,last)

        percorsi.append(parziale)