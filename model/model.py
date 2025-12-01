from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        # 1) Leggiamo gli hub e le tratte aggregate dal DAO
        self._nodes = DAO.readAllHubs()     # dict: id → Hub
        tratte = DAO.readTratte()           # lista di dict

        # 2) Pulizia del grafo (ripartenza)
        self.G.clear()

        # 3) Aggiungiamo *tutti* gli hub al grafo
        for hub_id, hub_obj in self._nodes.items():    # ci dà tupla chiave valore
            self.G.add_node(hub_id, hub=hub_obj)

        # 4) Filtriamo e aggiungiamo gli archi/tratte che superano la soglia
        edges_list = []   # lista finale di tratte accettate

        for t in tratte:
            h1 = t["hub1"]
            h2 = t["hub2"]
            valore = t["valore_medio"]
            nsped = t["numero_spedizioni"]

            # controlliamo che gli hub esistano nella tabella hub
            if h1 not in self._nodes or h2 not in self._nodes:
                continue

            # soglia economica
            if valore >= threshold:
                # aggiungiamo l’arco al grafo
                self.G.add_edge(h1, h2, weight=valore, numero_spedizioni=nsped)

                # salviamo anche nell’elenco che userà il controller
                edges_list.append((h1, h2, valore, nsped))

        # salvo gli edges filtrati dentro _edges
        self._edges = edges_list

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return self.G.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return self.G.number_of_nodes()

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return list(self.G.edges(data=True))  #data=True serve per ottenere anche gli attributi dell’arco

    def get_hub_by_id(self, hub_id):
        """
        Restituisce l'oggetto Hub dato il suo id.
        """
        if self._nodes is None:
            return None
        return self._nodes.get(hub_id, None)
