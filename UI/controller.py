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
        self._listYear = self._model.getAllYears()
        self._listColor = self._model.getAllColors()
        for y in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(y))
        for color in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))


    def handle_graph(self, e):
        color = self._view._ddcolor.value
        yearInput = self._view._ddyear.value
        if color is None or yearInput is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text(f"Attenzione, selezionare correttamente anno e colore.",
                                                           color="red"))
            self._view.update_page()
            return
        year = int(yearInput)
        self._model.buildGraph(color, year)
        n, e = self._model.getGraphDetails()
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {n}. Numero di archi {e}"))
        maggiori, ripetuti = self._model.getArchiMaggiori()
        for e in maggiori:
            self._view.txtOut.controls.append(ft.Text(e))
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {ripetuti}"))
        self.fillDDProduct()
        self._view.btn_search.disabled = False
        self._view.update_page()


    def fillDDProduct(self):
        self._view._ddnode.options.clear()
        products = self._model._graph.nodes
        for p in products:
            self._view._ddnode.options.append(ft.dropdown.Option(p.Product_number))


    def handle_search(self, e):
        prodNumberStr = self._view._ddnode.value
        if prodNumberStr is None:
            self._view.txtOut2.controls.clear()
            self._view.txtOut2.controls.append(ft.Text(f"Attenzione, selezionare prodotto.",
                                                           color="red"))
            self._view.update_page()
            return
        prodNumber = int(prodNumberStr)
        self._model.getBestPath(prodNumber)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {len(self._model._bestPath)}"))
        self._view.update_page()
