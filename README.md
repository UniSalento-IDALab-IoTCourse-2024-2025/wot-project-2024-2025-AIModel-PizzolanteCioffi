# WatchApp
## Descrizione del progetto

Questo progetto nasce con l’obiettivo di sviluppare un sistema intelligente, innovativo e non invasivo per il monitoraggio continuo di pazienti affetti da malattie neurodegenerative come Alzheimer, Parkinson o SLA.

Utilizzando uno smartwatch, il sistema raccoglie automaticamente dati vitali e comportamentali, tra cui frequenza cardiaca, sonno, tempo passato all’esterno e minuti di conversazione telefonica. Questi dati vengono trasmessi via **Bluetooth Low Energy (BLE)** a uno smartphone, che funge da gateway verso il **cloud**, dove sono elaborati da algoritmi di intelligenza artificiale.

Il sistema è progettato per:
- Rilevare segnali di deterioramento sociale;
- Notificare il paziente in caso di comportamenti anomali;
- Allertare caregiver in caso di persistenza del problema;
- Visualizzare lo stato clinico in tempo del paziente attraverso una dashboard intuitiva.

Questa soluzione è progettata per garantire:

- Facilità d’uso, anche da parte di utenti anziani o con capacità cognitive ridotte;
- Basso costo di implementazione e scalabilità per l’adozione su larga scala;
- Sicurezza e tutela della privacy, nella gestione dei dati sensibili raccolti.
## Architettura del Sistema

Il sistema è progettato secondo un’architettura a microservizi, scalabile e modulare, che consente la gestione indipendente dei diversi componenti funzionali. L’infrastruttura si basa su servizi backend containerizzati (Docker) e su un'app mobile utilizzata dal paziente.

<p align="center">
  <img src="https://github.com/user-attachments/assets/e789da38-c2d2-4d80-9cba-3dfba9060f5c" alt="Architettura del sistema" width="600"/>
</p>

### Servizi Backend

- **User Service**: è responsabile della gestione degli utenti all'interno del sistema. In particolare, si occupa delle operazioni di registrazione, autenticazione, autorizzazione e aggiornamento dei dati di profilo. È il primo punto di contatto per l’accesso ai servizi dell’applicazione, e garantisce che ogni richiesta sia associata a un utente valido.

- **DataCollector Service**: ha il compito di ricevere, filtrare e memorizzare i dati raccolti dallo smartwatch e dallo smartphone del paziente. I dati includono informazioni biometriche (come la frequenza cardiaca), dati di posizione, durata delle chiamate e dati relativi al sonno. Questo microservizio rappresenta il punto di ingresso dei dati grezzi nel sistema.

- **DataPrediction Service**: è responsabile dell’elaborazione dei dati aggregati relativi allo stato fisico e sociale dell’utente, comprendente sia aspetti comportamentali (quali i minuti trascorsi fuori casa) sia parametri fisici (quali la frequenza cardiaca, la durata del sonno e delle chiamate). L’obiettivo è produrre una valutazione complessiva tramite il modello di intelligenza artificiale, utile per monitorare la socialità e il benessere generale del paziente.
In particolare DataPrediction prende i dati aggregati da DataCollector, li riorganizza e li struttura secondo il formato previsto dal modello, richiamando poi il microservizio Python dedicato all’inferenza. Il risultato dell’elaborazione è una stima del comportamento sociale dell’utente “behaviour” (che può essere buono, normale o cattivo rispettivamente) in base ai dati più recenti raccolti dal sistema.

- **AIModel Service**: è il componente responsabile dell’elaborazione predittiva finale all’interno del sistema. Il suo compito principale consiste nell’analizzare un insieme eterogeneo di dati raccolti quotidianamente per ogni paziente (frequenza cardiaca, durata delle chiamate, durata del sonno, spostamenti) e fornire una valutazione del comportamento sociale dell’utente sotto forma di etichetta predittiva (label).

- **Notification Service**: si occupa della gestione delle notifiche inviate agli assistenti o agli utenti del sistema. Le notifiche possono riguardare, ad esempio, la registrazione dell’utente, la conferma di eventi importanti o l’avviso di situazioni di bassa socialità rilevate dal modello predittivo. Le notifiche vengono salvate nel database e sono consultabili attraverso apposite interfacce o endpoint dedicati.


### Frontend Mobile

- **Applicazione mobile (frontend)**  
Il frontend mobile dell’applicazione è stato sviluppato in React Native ed è progettato per operare su dispositivi Android, in quanto alcune funzionalità fondamentali, come l’accesso al registro delle chiamate, richiedono permessi speciali non disponibili su iOS.
L’applicazione consente all’utente di visualizzare in tempo reale i dati raccolti durante la giornata corrente (frequenza cardiaca, ore totali di sonno, posizione e durata chiamate), oltre a eventuali notifiche o segnalazioni provenienti dai modelli di intelligenza artificiale. 

## Repositori dei componenti

- User Service: [User](https://github.com/UniSalento-IDALab-IoTCourse-2024-2025/wot-project-2024-2025-User-PizzolanteCioffi)
- DataCollector Service: [DataCollector](https://github.com/UniSalento-IDALab-IoTCourse-2024-2025/wot-project-2024-2025-DataCollector-PizzolanteCioffi)
- DataPrediction Service: [DataPrediction](https://github.com/UniSalento-IDALab-IoTCourse-2024-2025/wot-project-2024-2025-DataPrediction-PizzolanteCioffi)
- Notification Service: [Notification](https://github.com/UniSalento-IDALab-IoTCourse-2024-2025/wot-project-2024-2025-Notification-PizzolanteCioffi)
- AIModel Service: [AIModel](https://github.com/UniSalento-IDALab-IoTCourse-2024-2025/wot-project-2024-2025-AIModel-PizzolanteCioffi)
- Frontend: [Frontend](https://github.com/UniSalento-IDALab-IoTCourse-2024-2025/wot-project-2024-2025-Frontend-PizzolanteCioffi)
- Pagina web: [Presentation](https://github.com/UniSalento-IDALab-IoTCourse-2024-2025/wot-project-2024-2025-Presentation-PizzolanteCioffi)

## AIModel Service

Il microservizio riceve tramite API una richiesta HTTP POST contenente un oggetto JSON strutturato, composto da tre elementi principali:
- l’indirizzo di residenza dell’utente;
- la lista delle posizioni GPS registrate durante la giornata;
- i dati biometrici raccolti per ogni ora.

Tali informazioni vengono preprocessate e combinate per costruire un record giornaliero aggregato. In particolare:
- l’indirizzo viene geocodificato per ottenere le coordinate geografiche;
- le posizioni vengono analizzate con un algoritmo unsupervised (DBSCAN combinato con la distanza da casa) per stabilire le ore passate fuori casa;
- le informazioni biometriche vengono fuse con le predizioni comportamentali orarie per costruire un dataset finale;
- il dataset viene infine aggregato in un singolo record rappresentativo della giornata.

A partire da questo record, il microservizio applica un supervised model di machine learning (RandomForestClassifier) precedentemente addestrato in locale su un dataset generato tramite uno script Python (sempre in locale). Tale approccio si è reso necessario in quanto non sono disponibili dataset pubblici contenenti simultaneamente le caratteristiche richieste dal sistema, ovvero frequenza cardiaca, durata delle chiamate, durata del sonno e tempo trascorso fuori casa. Il modello, una volta addestrato, è stato serializzato (cioè è stato salvato lo stato del modello addestrato su disco in formato binario) e viene ora utilizzato per restituire in tempo reale una predizione del comportamento dell’utente (buono, normale o cattivo) sulla base dei dati giornalieri aggregati.
La risposta restituita contiene:
- l’identificativo del paziente;
- il livello di comportamento stimato (etichetta che rappresenta il behaviour e assume dei valori interi pari a 1,2 o 3).

In caso di valori critici (es. comportamento cattivo), il risultato viene poi utilizzato da altri microservizi (es. DataPrediction, Notification) per aggiornare lo stato dell’utente o generare notifiche di allerta.
Il microservizio è sviluppato in Python utilizzando il framework FastAPI, ed espone un singolo endpoint HTTP POST protetto tramite autenticazione JWT. La logica del modello e della trasformazione dei dati è suddivisa in servizi modulari riutilizzabili (es. geocoding, build_final_dataset, inference, process_positions). Questo approccio modulare e asincrono consente di garantire alta manutenibilità, integrazione semplice e inferenza in tempo reale.

La validazione prestazionale del sistema si è focalizzata sulla valutazione dell’affidabilità e dell’efficienza dei principali componenti software, nonché sull’accuratezza del modello di machine learning impiegato per la classificazione del comportamento.
Tali prestazioni sono state misurate tramite metriche standard su un dataset di test e ciò ha consentito di individuare eventuali punti critici, validare l’efficacia del processo di inferenza e garantire un comportamento stabile e coerente del sistema in scenari reali.
Per valutare l’efficacia del modello supervisionato implementato all’interno del microservizio AIModel, è stata condotta una fase di test su un sottoinsieme separato del dataset, non utilizzato durante l’addestramento.
Il modello, basato su un RandomForestClassifier, è stato addestrato in locale su dati generati tramite uno script Python manuale, poiché non erano disponibili dataset pubblici con le stesse caratteristiche biometriche e comportamentali.
Durante la validazione sono state misurate diverse metriche standard nel campo del machine learning, come precision, recall, F1-score e accuracy, per ciascuna classe di comportamento prevista: critico, normale e buono.
Queste metriche offrono una visione approfondita della capacità del modello di distinguere correttamente tra i diversi stati comportamentali dell’utente, e di farlo in modo bilanciato anche in presenza di dati non uniformemente distribuiti.

<p align="center">
  <img src="https://github.com/user-attachments/assets/994181b9-1e99-440b-8f7a-8803be3fc1bc" alt="Metriche di valutazione" width="58%" style="margin-right:10px;"/>
  <img src="https://github.com/user-attachments/assets/e71609cb-f42a-4eda-aed3-ec69bedc1404" alt="Matrice di confusione" width="30%"/>
</p>

<p align="center">
  A sinistra sono riportate le metriche di precision, recall e F1-score per ciascuna classe.  
  A destra la matrice di confusione.
</p>


