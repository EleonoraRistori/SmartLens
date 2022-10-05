# Content based image retrieval

L'applicativo consente l'estrazione di features da un dataset di opere d'arte
da utilizzare per il retrieval delle immagini della webcam dell'applicazione mobile.

Per ottenere i risultati di cui sopra è necessaria l'esecuizione dei seguenti scripts:
1. prepairData4descriptors.py / prepairData5descriptors.py
2. build_dataset.py
3. build_features.py


### prepairData.py

Lo script preleva i dati da una cartella /data contenente alcune delle principali opere
del museo degli Uffizi ne realizza una suddivisione in 4 parti uguali che vengono salvate 
in subdirectories della cartella /Particolari immagini assieme all'intera opera ed ai particolari ritagliati manualmente.
Tali dati saranno utilizzati per l'estrazione delle features.

### build_dataset.py

Lo script accede alla cartella /Particolari immagini e costruisce il file .csv utilizzato
dalla rete MobileNet per l'estrazione di features. Tale file contiene il path di ciascuna
immagine da processare con associato il nome dell'opera e del dettaglio (o l'indicazione
che si tratti dell'intera opera).

### build_features.py
Realizza la vera e propria estrazione di features delle immagini riportate nel file .csv.
Lo script consente di utilizzare MobileNet in tutte le sue versioni dalla prima alla
terza nelle due versioni Small e Large. La rete da utilizzare risulta MobileNet v3 Small
per specularità con l'applicativo mobile che ne utilizza la versione javascript.
Le features vengono salvate in un file .pck.


## Trasferimento delle features al database
È necessaria la creazione di un database di tipo MySQL su cui eseguire l'upload delle
features. Al suo interno è necessario creare una tabella pythonfeatures con due colonne
* artwork, chiave primaria che conterrà l'id dell'opera (varchar(200));
* features, che conterrà l'array delle features dell'opera/dettaglio (text)
Lo script to_db.py consente l'upload dei dati su tale tabella semplicemente modificando i campi
relativi ad utente e password configurati. Tale script provvede in automatico alla conversione
da .pck a JSON, formato utilizzato per l'upload sul server.






