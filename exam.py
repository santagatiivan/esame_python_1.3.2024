# Classe personalizzata per la gestione delle eccezioni specifiche dell'esame
class ExamException(Exception):
    pass

# Classe per la gestione dei file CSV contenenti serie temporali
class CSVTimeSeriesFile:
    def __init__(self, name):
        # Costruttore che inizializza l'oggetto con il nome del file
        self.name = name

    def get_data(self):
        # Tenta di aprire il file, solleva eccezioni specifiche se non trova il file o in caso di altri errori
        try:
            my_file = open(self.name, 'r')
        except FileNotFoundError:
            raise ExamException("Il file non esiste")
        except Exception as e:
            raise ExamException(f"Errore nell'apertura del file: {e}")

        data = []  # Lista per raccogliere i dati letti
        last_year, last_month = 0, 0  # Variabili di controllo per l'ordine temporale
        for line in my_file:
            elements = line.strip().split(',')  # Divide la riga in elementi
            # Ignora le righe con un numero di elementi non valido
            if len(elements) < 2 or len(elements) > 3:
                continue
            try:
                # Estrae anno e mese, convertendoli in interi, e il numero di passeggeri
                year, month = map(int, elements[0].split('-'))
                passengers = int(elements[1])
                # Ignora i dati non validi (passeggeri <= 0)
                if passengers <= 0:
                    continue
                # Controlla l'ordine dei dati; ignora i dati fuori sequenza o duplicati
                if year < last_year or (year == last_year and month <= last_month):
                    continue
                last_year, last_month = year, month  # Aggiorna le variabili di controllo
                # Aggiunge i dati validi alla lista
                data.append([f"{year}-{str(month).zfill(2)}", passengers])
            except ValueError:
                # Ignora le righe con valori non convertibili in interi
                continue

        my_file.close()  # Chiude il file dopo l'uso
        return data  # Ritorna i dati come lista di liste

def find_min_max(time_series):
    # Controlla che la serie temporale non sia vuota
    if not time_series:
        raise ExamException("La serie temporale è vuota")

    yearly_data = {}  # Dizionario per raccogliere i dati minimi e massimi per ogni anno
    for record in time_series:
        year, month = record[0].split('-')[0], record[0].split('-')[1]
        value = record[1]
        # Inizializza il dizionario per l'anno se non esiste
        if year not in yearly_data:
            yearly_data[year] = {'min': [float('inf'), []], 'max': [float('-inf'), []]}

        # Aggiorna i dati minimi e massimi per l'anno
        if value < yearly_data[year]['min'][0]:
            yearly_data[year]['min'] = [value, [month]]
        elif value == yearly_data[year]['min'][0]:
            yearly_data[year]['min'][1].append(month)
        if value > yearly_data[year]['max'][0]:
            yearly_data[year]['max'] = [value, [month]]
        elif value == yearly_data[year]['max'][0]:
            yearly_data[year]['max'][1].append(month)

    # Formatta l'output per avere mesi minimi e massimi ben organizzati
    formatted_output = {}
    for year, data in yearly_data.items():
        min_months = [month.zfill(2) for month in sorted(data['min'][1])]
        max_months = [month.zfill(2) for month in sorted(data['max'][1])]
        formatted_output[year] = {"min": min_months, "max": max_months}

    return formatted_output  # Ritorna il dizionario formattato

# Punto di ingresso principale del programma
if __name__ == "__main__":
    try:
        file_name = "data.csv"  # Nome del file da leggere. Utilizza data_modified.csv per testare le exception come: 
                                # mesi non validi, numero di passeggeri negativo o nullo, valori non numerici per i 
                                # passeggeri, mancanza di dati, numero eccessivo di colonne, separatori errati, timestamp 
                                # fuori ordine e duplicati
        time_series_file = CSVTimeSeriesFile(name=file_name)
        time_series_data = time_series_file.get_data()  # Ottiene i dati dal file
        min_max_results = find_min_max(time_series_data)  # Trovai valori minimi e massimi per ogni anno

        # Stampa l'output in modo formattato, ogni anno su una nuova riga
        print('{')
        for year in min_max_results:
            print(f'    "{year}": {min_max_results[year]}')
        print('}')
    except ExamException as e:
        # Gestisce le eccezioni, stampando il messaggio di errore
        print(f"Errore: {e}")
