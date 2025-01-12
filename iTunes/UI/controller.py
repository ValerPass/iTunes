import this
import time
import warnings

import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAlbum = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        try:
            totDint = int(self._view._txtInDurata.value)
        except ValueError:
            warnings.warn_explicit(message="duration not integer", category=TypeError, filename="controller.py", lineno=18)
            return

        self._model.buildGraph(totDint)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        nN, nE = self._model.getGraphSize()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nN} nodi e {nE} archi!"))

        nodes = self._model.getNodes()
        nodes.sort(key=lambda x: x.Title)
        """
        for n in nodes:
            self._view._ddAlbum.options.append(
                ft.dropdown.Option(
                    data=n,
                    text=n.Title,
                    on_click=self.getSelectedAlbum
                )
            )
        """
        listDD = map(lambda x: ft.dropdown.Option(data=x, text=x.Title, on_click=self.getSelectedAlbum), nodes)
        self._view._ddAlbum.options = listDD

        self._view.update_page()

    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self._choiceAlbum = None
        else:
            self._choiceAlbum = e.control.data

    def handleAnalisiComp(self, e):
        self._view.txt_result.controls.clear()
        if self._choiceAlbum is not None:
            sizeC, totDurata = self._model.getConnessaDetails(self._choiceAlbum)
            self._view.txt_result.controls.append(ft.Text(f"La componente connessa che include {self._choiceAlbum} ha dimensione {sizeC} e durata totale {totDurata}!"))
            self._view.update_page()
        else:
            warnings.warn("Album field not selected")
            return

    def handleGetSetAlbum(self, e):
        self._view.txt_result.controls.clear()
        dTOTtxt = self._view._txtInSoglia.value
        try:
            dTOT = int(dTOTtxt)
        except ValueError:
            warnings.warn("Soglia not integer")
            self._view.txt_result.controls.append(ft.Text("Soglia inserita non valida!"))
            self._view.update_page()
            return

        if self._choiceAlbum is None:
            warnings.warn("Attennzione, album non selezionato!")
            self._view.txt_result.controls.append(ft.Text("Selezionare un album."))
            self._view.update_page()
            return

        start_time = time.time()
        setAlbum, durataTot = self._model.getSetAlbum(self._choiceAlbum, dTOT)
        end_time = time.time()
        self._view.txt_result.controls.append(ft.Text(f"Elapsed time = {end_time-start_time}"))
        self._view.txt_result.controls.append(ft.Text("Set di album ottimo trovato!"))
        self._view.txt_result.controls.append(ft.Text(f"Durata totale degli album: {durataTot}"))
        for s in setAlbum:
            self._view.txt_result.controls.append(ft.Text(f"{s}"))

        self._view.update_page()