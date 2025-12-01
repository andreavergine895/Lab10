import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        txt_valore = self._view.guadagno_medio_minimo.value

        # --- VALIDAZIONE INPUT
        if txt_valore is None or str(txt_valore).strip() == "":
            self._view.show_alert("Inserire un valore di soglia (in euro).")
            return

        try:
            soglia = float(txt_valore)
        except ValueError:
            self._view.show_alert("Valore non valido: inserire un numero (es. 300).")
            return

        # --- COSTRUZIONE GRAFO
        self._model.costruisci_grafo(soglia)

        # --- PULIZIA DELLA LISTA NELLA VIEW
        self._view.lista_visualizzazione.controls.clear()

        # --- INFO RIASSUNTIVE
        num_hub = self._model.get_num_nodes()
        num_tratte = self._model.get_num_edges()

        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Hub presenti: {num_hub}",size=14))
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Tratte: {num_tratte}",size=14))
        self._view.lista_visualizzazione.controls.append(ft.Divider())

        # --- LISTA DETTAGLIATA DELLE TRATTE
        edges = self._model.get_all_edges()

        if not edges:
            self._view.lista_visualizzazione.controls.append(
                ft.Text("Nessuna tratta soddisfa la soglia."))
        else:
            for (h1, h2, attr) in edges:
                hub1 = self._model.get_hub_by_id(h1)
                hub2 = self._model.get_hub_by_id(h2)

                nome1 = hub1.nome
                nome2 = hub2.nome

                valore = attr.get("weight", 0)  #accede a dizionario attr e da valore weight se esiste se no 0

                riga = f"[{nome1}  ->  {nome2}] -- guadagno medio per spedizione:  {valore:.2f} €"
                self._view.lista_visualizzazione.controls.append(ft.Text(riga))

        # --- UPDATE DELLA PAGINA
        self._view.update()