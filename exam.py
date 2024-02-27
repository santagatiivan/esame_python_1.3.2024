# Definizione di una classe personalizzata per la gestione delle eccezioni
class ExamException(Exception):
    pass

# Definizione della classe principale per la gestione dei file CSV contenenti serie temporali
class CSVTimeSeriesFile:
    def __init__(self, name):
        # Il costruttore prende come argomento il nome del file da aprire
        self.name = name

    # Metodo per leggere i dati dal file CSV e restituirli come lista di liste
    def get_data(self):
        # Tentativo di apertura del file, gestisce l'eccezione se il file non esiste
        try:
            my_file = open(self.name, 'r')
        except FileNotFoundError:
            raise ExamException("Il file non esiste")
        except Exception as e:
            raise ExamException(f"Errore nell'apertura del file: {e}")

        data = []
        last_year, last_month = 0, 0  # Variabili per controllare l'ordine temporale dei dati
        for line in my_file:
            elements = line.split(',')
            # Ignora le righe che non rispettano il formato atteso (es. numero errato di colonne)
            if len(elements) < 2 or len(elements) > 3:
                continue
            try:
                # Estrae anno, mese e passeggeri, convertendo le stringhe in numeri
                year, month = map(int, elements[0].split('-'))
                passengers = int(elements[1])

                # Ignora i valori non validi (es. numero di passeggeri negativo o nullo)
                if passengers <= 0:
                    continue
                
                # Controlla che i dati siano in ordine cronologico e non duplicati
                if year < last_year or (year == last_year and month <= last_month):
                    raise ExamException("Timestamp fuori ordine o duplicato")
                last_year, last_month = year, month

                # Aggiunge i dati validi alla lista
                data.append([f"{year}-{str(month).zfill(2)}", passengers])
            except ValueError:
                # Ignora le righe con valori non numerici
                continue

        my_file.close()

        # Se non sono stati trovati dati validi, lancia un'eccezione
        if len(data) == 0:
            raise ExamException("Nessun dato valido trovato")

        return data

# Funzione per trovare il minimo e il massimo numero di passeggeri per ogni anno
def find_min_max(time_series):
    if len(time_series) < 2:
        return {}

    yearly_data = {}
    for record in time_series:
        year, value = record[0].split('-')[0], record[1]
        if year not in yearly_data:
            yearly_data[year] = {'min': [float('inf'), []], 'max': [float('-inf'), []]}

        # Aggiorna il record di minimo e massimo passeggeri per l'anno
        if value < yearly_data[year]['min'][0]:
            yearly_data[year]['min'] = [value, [record[0][5:]]]
        elif value == yearly_data[year]['min'][0]:
            yearly_data[year]['min'][1].append(record[0][5:])

        if value > yearly_data[year]['max'][0]:
            yearly_data[year]['max'] = [value, [record[0][5:]]]
        elif value == yearly_data[year]['max'][0]:
            yearly_data[year]['max'][1].append(record[0][5:])

    # Prepara il risultato finale ordinando i mesi e formattando l'output
    result = {}
    for year, data in yearly_data.items():
        min_months = sorted(data['min'][1])  # Ordina i mesi del minimo
        max_months = sorted(data['max'][1])  # Ordina i mesi del massimo
        result[year] = {'min': min_months, 'max': max_months}
    
    return result

# Blocco principale che esegue il programma
if __name__ == "__main__":
    try:
        file_name = "data.csv"  # Nome del file da analizzare
        time_series_file = CSVTimeSeriesFile(name=file_name)
        time_series_data = time_series_file.get_data()  # Ottiene i dati
        min_max_results = find_min_max(time_series_data)  # Calcola min e max

        # Stampa i risultati
        print("Risultati Minimo e Massimo per anno:")
        for year in min_max_results:
            print(f"Anno {year}: Min = {min_max_results[year]['min']}, Max = {min_max_results[year]['max']}")
    except ExamException as e:
        # Gestisce le eccezioni mostrando l'errore
        print(f"Errore: {e}")
