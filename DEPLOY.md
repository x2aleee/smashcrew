# Pubblicare il sito Smash Crew

## Cosa e' successo il 13 ottobre 2026

Il sito online serviva le due pagine aggiornate ma **non i file in `assets/`**: ogni richiesta di
immagine tornava la pagina HTML della home, quindi le foto non comparivano. Il progetto non c'entra:
`index.html` e `index_giallo.html` sul server sono identici, byte per byte, a quelli del PC.

La causa e' l'ultima pubblicazione. Cloudflare sostituisce **l'intera** pubblicazione a ogni
caricamento, e l'ultima conteneva solo quattro file (`index.html`, `index_giallo.html`, `_headers`
e la sola immagine di anteprima social creata durante il lavoro sui metadati). Delle 44 risorse
richieste dalle pagine ne e' rimasta online una. Spostare le cartelle sul PC non ha alcun effetto
sul sito: le foto erano e restano versionate su GitHub.

## Stato del versionamento

- `assets/`: 53 file versionati, **nessuna regola di `.gitignore` li blocca**.
- Le immagini sono presenti su GitHub e raggiungibili (verificato su `raw.githubusercontent.com`).
- Unica eccezione corretta in questa sede: `_headers` era coperto dalla regola `_*`; ora e' esentato,
  perche' e' un file che Cloudflare legge solo dalla pubblicazione.

## 1. Controllare

```bash
python verifica-asset.py          # percorso, maiuscole e versionamento di ogni asset
python verifica-asset.py --live   # e cosa serve davvero il sito online
```

Il controllo esce con codice 1 se un file citato manca, se il nome ha maiuscole diverse da quelle
reali, se non e' versionato o se online torna una pagina HTML al posto dell'immagine.

## 2. Preparare il pacchetto

```bash
python verifica-asset.py --export
```

Costruisce `_deploy/`: le tre pagine pubblicate, `_headers` e i soli asset citati (circa 21 MB).
La cartella e' rigenerabile e non va versionata.

## 3. Pubblicare

```bash
npx wrangler pages deploy _deploy --project-name=smashcrew --commit-dirty=true
```

In alternativa, dalla dashboard: Workers & Pages, progetto `smashcrew`, Create deployment, carica la
cartella `_deploy`. Poi ripetere `python verifica-asset.py --live`: deve finire senza errori.

## 4. Rendere il guasto impossibile (una volta sola)

Collegare il progetto Pages alla repository GitHub `x2aleee/smashcrew`, branch `main`, comando di
build vuoto, cartella di output `/`. Da quel momento **ogni push pubblica tutto il progetto**, foto
comprese, e il sito non dipende piu' dalla cartella sul PC: e' la difesa contro il guasto di oggi.
