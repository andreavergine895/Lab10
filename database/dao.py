from database.DB_connect import DBConnect
from model.hub import Hub


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def readAllHubs():
        """
        Legge tutti gli hub dalla tabella 'hub' e ritorna un dizionario id->Hub.
        Questo permette al Model / View di mostrare nomi e altri dettagli degli hub.
        """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM hub """
        cursor.execute(query)
        hubs = {}
        for row in cursor:
            # Creiamo oggetti Hub (dataclass)
            h = Hub(
                id=row["id"],
                codice=row["codice"],
                nome=row["nome"],
                citta=row["citta"],
                stato=row["stato"],
                latitudine=row["latitudine"],
                longitudine=row["longitudine"]
            )
            hubs[row["id"]] = h
        cursor.close()
        conn.close()
        return hubs

    @staticmethod
    def readTratte():
        """
        Legge dal DB le tratte aggregate (considerando le due direzioni come una sola),
        calcolando il valore medio per spedizione (AVG(valore_merce)) e il numero di spedizioni.
        Ritorna una lista di dizionari con chiavi: hub1, hub2, valore_medio, numero_spedizioni.
        """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        # Usiamo LEAST/GREATEST per raggruppare A-B e B-A insieme come consigliato dalla consegna
        query =   """ SELECT 
                        LEAST(id_hub_origine, id_hub_destinazione) AS hub1,
                        GREATEST(id_hub_origine, id_hub_destinazione) AS hub2,
                        AVG(valore_merce) AS valore_medio,
                        COUNT(*) AS numero_spedizioni
                    FROM spedizione
                    GROUP BY hub1, hub2 """
        cursor.execute(query)
        result = []
        for row in cursor:
            # Normalizziamo i tipi (float/int) e salviamo il dizionario
            item = {
                "hub1": row["hub1"],
                "hub2": row["hub2"],
                "valore_medio": float(row["valore_medio"]),
                "numero_spedizioni": int(row["numero_spedizioni"])
            }
            result.append(item)
        cursor.close()
        conn.close()
        return result