class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        # Verifica dell'esistenza del file
        try:
            my_file = open(self.name, 'r')
        except FileNotFoundError:
            raise ExamException("Il file non esiste")
        except Exception as e:
            raise ExamException(f"Errore nell'apertura del file: {e}")

        data = []
        last_year, last_month = 0, 0
        for line in my_file:
            elements = line.split(',')
            # Controlla se ci sono esattamente 2 elementi e ignora righe con errori
            if len(elements) < 2 or len(elements) > 3:
                continue
            try:
                year, month = map(int, elements[0].split('-'))
                passengers = int(elements[1])

                # Controlla se il dato è valido
                if passengers <= 0:
                    continue
                
                # Controlla ordine temporale e duplicati
                if year < last_year or (year == last_year and month <= last_month):
                    raise ExamException("Timestamp fuori ordine o duplicato")
                last_year, last_month = year, month

                data.append([f"{year}-{str(month).zfill(2)}", passengers])
            except ValueError:
                continue

        my_file.close()

        if len(data) == 0:
            raise ExamException("Nessun dato valido trovato")

        return data

def find_min_max(time_series):
    if len(time_series) < 2:
        return {}

    yearly_data = {}
    for record in time_series:
        year, value = record[0].split('-')[0], record[1]
        if year not in yearly_data:
            yearly_data[year] = {'min': [float('inf'), []], 'max': [float('-inf'), []]}

        # Aggiorna il minimo
        if value < yearly_data[year]['min'][0]:
            yearly_data[year]['min'] = [value, [record[0][5:]]]
        elif value == yearly_data[year]['min'][0]:
            yearly_data[year]['min'][1].append(record[0][5:])

        # Aggiorna il massimo
        if value > yearly_data[year]['max'][0]:
            yearly_data[year]['max'] = [value, [record[0][5:]]]
        elif value == yearly_data[year]['max'][0]:
            yearly_data[year]['max'][1].append(record[0][5:])

    result = {}
    for year, data in yearly_data.items():
        min_months = sorted(data['min'][1])
        max_months = sorted(data['max'][1])
        result[year] = {'min': min_months, 'max': max_months}
    
    return result

# Esempio di utilizzo
if __name__ == "__main__":
    try:
        file_name = "data.csv"
        time_series_file = CSVTimeSeriesFile(name=file_name)
        time_series_data = time_series_file.get_data()
        min_max_results = find_min_max(time_series_data)

        print("Risultati Minimo e Massimo per anno:")
        for year in min_max_results:
            print(f"Anno {year}: Min = {min_max_results[year]['min']}, Max = {min_max_results[year]['max']}")
    except ExamException as e:
        print(f"Errore: {e}")
