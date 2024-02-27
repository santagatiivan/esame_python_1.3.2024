# esame-python
leggi il README per le ultime info

## DA RIVEDERE!
-formattazione
-nomi variabili

### breve recap
*-Definizione di una classe di eccezione*: Per gestire errori specifici al contesto.
*-Classe CSVTimeSeriesFile*: Gestisce l'apertura e la lettura di un file CSV, verificando la correttezza e l'ordine dei dati.
*-Metodo get_data: Legge i dati dal file, verificando che siano in ordine cronologico e validi (escludendo dati non numerici o in formati errati).
*-Funzione find_min_max*: Analizza i dati per anno, trovando il minimo e il massimo numero di passeggeri e gestendo anche i casi di più mesi con lo stesso valore minimo o massimo.
*-Esecuzione e gestione delle eccezioni*: Il blocco principale esegue le funzioni sopra definite, gestendo eventuali errori e stampando i risultati.

####
La classe ExamException estende Exception, fornendo una gestione specifica degli errori che possono emergere durante l'apertura del file o l'elaborazione dei dati. Questo meccanismo di eccezioni personalizzate facilita l'identificazione e la gestione di errori specifici, migliorando la resilienza e la manutenibilità del codice.

"CSVTimeSeriesFile" è una classe progettata per caricare e leggere i dati da file CSV, con un costruttore che accetta come argomento il nome del file. Il metodo "get_data()" apre il file in modalità lettura, gestendo eccezioni quali "FileNotFoundError" per file inesistenti e errori generici nell'apertura, attraverso il rilancio di "ExamException" con messaggi di errore specifici.

All'interno di "get_data()", il codice effettua parsing e validazione dei dati, scartando record non conformi e assicurando che i dati siano in ordine cronologico senza duplicazioni. Le validazioni includono la verifica del formato delle righe, la conversione di anno, mese e numero di passeggeri da stringhe a interi, e il controllo sulla validità dei valori numerici (escludendo, ad esempio, numeri di passeggeri negativi o nulli). In caso di dati fuori sequenza temporale o duplicati, viene sollevata un'"ExamException".

La funzione esterna "find_min_max" analizza la serie temporale per determinare i valori minimi e massimi di passeggeri per ogni anno, gestendo casi di multiple occorrenze del minimo o massimo annuale. La struttura del risultato finale consente una facile interpretazione delle tendenze annuali, organizzando i dati per anno con i corrispondenti valori minimo e massimo.

Nel blocco if "__name__" == "__main__":, il codice dimostra l'utilizzo pratico delle classi e delle funzioni definiti, eseguendo l'analisi su un file CSV specificato, calcolando i minimi e massimi annuali dei passeggeri, e stampando i risultati. Questa sezione illustra anche la gestione delle eccezioni attraverso ExamException, enfatizzando l'approccio strutturato all'elaborazione e analisi di dati di serie temporali in Python.
