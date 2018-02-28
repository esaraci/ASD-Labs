# Lab.1 - Analisi citazionale di articoli scientifici

Questo primo laboratorio si occupa di analizzare un problema reale: come vengono citati gli articoli scientifici? 

Il laboratorio va svolto a gruppi di massimo tre persone. E' sufficiente che uno solo dei componenti sottometta i risultati, specificando nel testo della risposta i nomi dei componenti del gruppo.

**Il Grafo delle Citazioni**

L'obiettivo di questo laboratorio è di analizzare la struttura del grafo generato dalla rete delle citazioni presenti negli articoli scientifici. Ogni articolo scientifico cita sempre diversi altri articoli, tipicamente qualche decina, ma in alcuni casi anche centinaia di articoli diversi. Tuttavia, non è sempre detto che gli autori conoscano nel dettaglio i contenuti dei lavori che citano. La domanda a cui vogliamo rispondere è la seguente: gli articoli che vengono citati sono scelti in modo casuale (fra gli articoli della stessa disciplina) o c'è qualche "regolarità nascosta"?

Poiché ci dobbiamo occupare della relazione "articolo cita articolo", i dati sulle citazioni verranno rappresentati con un grafo orientato (un grafo delle citazioni) in cui i vertici corrispondono agli articoli e c'è un arco dal vertice u al vertice v se l'articolo corrispondente a u cita l'articolo corrispondente a v. 

Poiché siamo interessati a capire come vengono citati gli articoli, analizzeremo la distribuzione del grado entrante del grafo, e la confronteremo con quella generata dai due processi casuali visti a lezione.

**Domanda 1**

Questa domanda richiede di analizzare il grafo delle citazioni di 27770 articoli di fisica delle alte energie. Il grafo ha 352807 archi ed è contenuto nel file allegato. Ogni articolo del dataset è identificato da un numero.  Ogni riga del file contiene un arco del grafo dove il primo numero è la coda ed il secondo la testa dell'arco.

Il compito da svolgere per questa domanda è di calcolare la distribuzione del grado entrante del grafo delle citazioni. La distribuzione deve essere normalizzata (i valori devono sommare a 1). Il risultato deve essere mostrato in un grafico di dispersione (o plot) dei punti con doppia scala logaritmica (log-log plot). Il file con l'immagine del grafico va caricata nell'apposito spazio che compare dopo aver premuto sul bottone "Aggiungi consegna".

**Domanda 2**

A lezione abbiamo visto l'algoritmo ER(n, p) per generare grafi casuali. Confrontate la forma della distribuzione che avete ottenuto nella Domanda 1 con quella generata da ER. Per farlo potete generare diversi grafi casuali per valori diversi di n e di p. Rispondete quindi alle seguenti domande:

- Com'è fatta la distribuzione del grado entrate di un grafo generato con ER? Descrivete a parole la sua forma.
- Ha una forma simile a quella del grafo delle citazioni oppure no? Spiegate brevemente le differenze e le somiglianze tra le due distribuzioni.

Inserite le risposte nella casella di testo che appare dopo aver premuto sul bottone "Aggiungi consegna"

Domanda 3

Considerate ora l'Algoritmo DPA(m, n) per generare grafi casuali visto a lezione. Implementate l'algoritmo e usatelo per generare un grafo casuale con un numero di nodi e di archi simile al grafo delle citazioni. Scegliere il valore n da passare all'algoritmo è facile: basta usare un valore vicino al numero di nodi del grafo delle citazioni. Siccome ogni iterazione dell'algoritmo aggiunge m archi al grafo, usare un valore intero vicino al grado uscente medio del grafo delle citazioni è una buona scelta per m.

Dopo aver scelto m e n, generate il grafo casuale e calcolate la distribuzione del grado entrate normalizzata. Specificare i valori di m e n che avete scelto nella casella di testo che appare dopo aver premuto sul bottone "Aggiungi consegna" e allegate il file con il grafico di dispersione in scala log-log come nella Domanda 1.

**Domanda 4**

Confrontate le distribuzioni del grado entrate che avete ottenuto per la Domanda 1 e per la Domanda 4. Considerate le somiglianze e le differenze tra le distribuzioni e quali potrebbero essere le cause delle somiglianze. Per aiutarvi nell'analisi considerate i seguenti fenomeni:

- Il fenomeno dei "sei gradi di separazione"
- Il fenomeno "rich get richer"
- Il fenomeno della "struttura gerarchica delle reti"

Considerate come questi fenomeni possono spiegare i risultati che avete ottenuto rispondendo alle seguenti domande nella casella di testo che appare dopo aver premuto sul bottone "Aggiungi consegna"

- La distribuzione del grafo delle citazioni assimiglia a quella del grafo ottenuto con DPA? Spiegate brevemente similitudini e differenze.

- Quale dei tre fenomeni spiega meglio il comportamento dell'algoritmo DPA? Spiegate brevemente perché.

- Quale dei tre fenomeni spiega meglio la struttura del grafo delle citazioni? Spiegate brevemente perché.

**Domanda 5**

Allegate il codice sorgente della vostra soluzione come un unico archivio compresso (in formato .zip, tar.gz, ecc ...).