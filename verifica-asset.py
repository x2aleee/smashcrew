#!/usr/bin/env python3
"""Controlla e prepara la pubblicazione del sito Smash Crew.

Uso:
    python verifica-asset.py                 # controlla i file del progetto (offline)
    python verifica-asset.py --live          # controlla anche cosa serve il sito online
    python verifica-asset.py --export        # costruisce _deploy/ con il pacchetto da pubblicare
    python verifica-asset.py --live --export

Cosa verifica, in ordine:
  1. che ogni immagine, video, font o foglio di stile citato dagli HTML e dai CSS
     abbia un percorso RELATIVO e non un percorso del disco locale o un link temporaneo;
  2. che il nome di ogni file citato corrisponda al millesimo al file reale, maiuscole
     e minuscole comprese (Windows non distingue i due casi, il server si');
  3. che ogni file citato sia tracciato da git, e se non lo e' dice QUALE regola di
     .gitignore lo blocca;
  4. con --live, che il sito online serva davvero quei file: se una richiesta torna
     una pagina HTML al posto dell'immagine, la pubblicazione e' senza asset ed e'
     esattamente il guasto di ottobre 2026.

Esce con codice 1 se qualcosa non torna: serve come gate prima di pubblicare.
Nessuna dipendenza esterna, solo libreria standard.
"""
import argparse
import hashlib
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

RADICE = pathlib.Path(__file__).resolve().parent

# Le pagine che finiscono online. I file index-v1/v2/legacy sono iterazioni locali
# e non vengono pubblicati, quindi non si controllano.
PAGINE = ["index.html", "index_giallo.html", "404.html"]

# File di configurazione della pubblicazione (Cloudflare li legge solo se presenti).
EXTRA_DA_PUBBLICARE = ["_headers", "_redirects"]

ESTENSIONI_ASSET = {
    ".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".svg", ".ico",
    ".mp4", ".webm", ".mov", ".mp3", ".woff", ".woff2", ".ttf", ".otf",
    ".css", ".js", ".json", ".webmanifest",
}

# Host di appoggio: se un asset punta qui, il giorno dopo non c'e' piu'.
HOST_TEMPORANEI = (
    "wetransfer.com", "we.tl", "transfer.sh", "0x0.st", "tmpfiles.org", "file.io",
    "gofile.io", "drive.google.com", "docs.google.com", "dropbox.com", "mega.nz",
    "postimg.cc", "imgur.com", "ibb.co", "prnt.sc", "snipboard.io",
    "localhost", "127.0.0.1", "192.168.", "10.0.", "file://",
)

RE_ATTRIBUTI = re.compile(
    r"\b(src|href|poster|data-src|srcset|content)\s*=\s*\"([^\"]*)\"", re.IGNORECASE)
RE_URL_CSS = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.IGNORECASE)
RE_SCHEMA = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
RE_UNITA_ABSOLUTA = re.compile(r"^(?:[a-zA-Z]:[\\/]|\\\\|/Users/|/home/|/mnt/|/Volumes/)")

ESITO = {"ok": [], "avvisi": [], "errori": []}


def segna(esito, messaggio):
    ESITO[esito].append(messaggio)


def e_asset(percorso):
    return pathlib.PurePosixPath(percorso).suffix.lower() in ESTENSIONI_ASSET


# ------------------------------------------------------------------ riferimenti
def riferimenti_da_html(percorso):
    """Estrae ogni indirizzo citato da un file HTML: attributi, srcset e url() inline."""
    testo = percorso.read_text(encoding="utf-8", errors="replace")
    fuori = []
    for attributo, valore in RE_ATTRIBUTI.findall(testo):
        valore = valore.strip()
        if not valore:
            continue
        attributo = attributo.lower()
        if attributo == "srcset":
            for pezzo in valore.split(","):
                pezzo = pezzo.strip().split(" ")[0]
                if pezzo:
                    fuori.append((attributo, pezzo))
        elif attributo == "content":
            # Solo anteprime social (og:image, twitter:image): devono essere immagini.
            if valore.startswith(("http://", "https://")) and e_asset(
                    urllib.parse.urlparse(valore).path):
                fuori.append(("content", valore))
        else:
            fuori.append((attributo, valore))
    for indirizzo in RE_URL_CSS.findall(testo):
        fuori.append(("url()", indirizzo.strip()))
    return fuori


def riferimenti_da_css(percorso):
    testo = percorso.read_text(encoding="utf-8", errors="replace")
    return [("url()", indirizzo.strip()) for indirizzo in RE_URL_CSS.findall(testo)]


def classifica(origine, attributo, valore):
    """Traduce un indirizzo grezzo in: ('locale'|'esterno'|'ignora', percorso, urlo)."""
    valore = valore.strip()
    if not valore or valore.startswith("#"):
        return ("ignora", "", "")
    if valore.startswith("//"):
        return ("esterno", "", "https:" + valore)
    schema = RE_SCHEMA.match(valore)
    if schema and schema.group(0).lower() in ("data:", "blob:", "javascript:", "mailto:", "tel:"):
        return ("ignora", "", "")
    if RE_UNITA_ABSOLUTA.match(valore) or valore.lower().startswith("file://"):
        return ("disco", valore, "")
    if schema and schema.group(0).lower() in ("http:", "https:"):
        parti = urllib.parse.urlparse(valore)
        if parti.netloc.endswith("pages.dev") and parti.path not in ("", "/"):
            # Anteprima social che punta al sito: il file vero e' il percorso locale.
            return ("locale", urllib.parse.unquote(parti.path.lstrip("/")), valore)
        return ("esterno", "", valore)
    if valore.startswith("/"):
        return ("radice", valore, "")
    pulito = urllib.parse.unquote(valore.split("#")[0].split("?")[0])
    return ("locale", pulito, "")


# ------------------------------------------------------------------ controlli
def risolvi_maiuscole(percorso_rel):
    """Cerca il file distinguendo le maiuscole. Ritorna (esito, percorso_reale, nome_errato)."""
    attuale = RADICE
    for pezzo in pathlib.PurePosixPath(percorso_rel).parts:
        if not attuale.is_dir():
            return ("assente", None, pezzo)
        try:
            voci = os.listdir(attuale)
        except OSError:
            return ("assente", None, pezzo)
        if pezzo in voci:
            attuale = attuale / pezzo
            continue
        candidate = [v for v in voci if v.lower() == pezzo.lower()]
        if candidate:
            return ("caso", attuale / candidate[0], pezzo)
        return ("assente", None, pezzo)
    return ("ok", attuale, None)


def file_tracciati():
    try:
        esito = subprocess.run(["git", "ls-files"], cwd=RADICE, capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
    except OSError:
        return None
    if esito.returncode != 0:
        return None
    return {riga.strip().replace("\\", "/") for riga in esito.stdout.splitlines() if riga.strip()}


def regola_che_blocca(percorso_rel):
    """Ritorna la riga di .gitignore che ignora davvero il file, altrimenti None.

    git check-ignore -v mostra anche le regole di eccezione (!...), che al contrario
    escludono il file dalla regola precedente: l'esito vero lo dice -q, che esce con
    codice 0 solo quando il file e' ignorato.
    """
    prova = subprocess.run(["git", "check-ignore", "-q", "--", percorso_rel], cwd=RADICE,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    if prova.returncode != 0:
        return None
    dettaglio = subprocess.run(["git", "check-ignore", "-v", "--", percorso_rel], cwd=RADICE,
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
    riga = dettaglio.stdout.strip().split("\t")[0]
    return riga or "regola di .gitignore"


def raccogli_asset():
    """Raccoglie i riferimenti delle pagine pubblicate. Ritorna (asset_locali, fonti)."""
    asset = {}
    for nome in PAGINE:
        percorso = RADICE / nome
        if not percorso.is_file():
            segna("errori", "pagina mancante nel progetto: %s" % nome)
            continue
        for attributo, valore in riferimenti_da_html(percorso):
            tipo, pulito, urlo = classifica(nome, attributo, valore)
            if tipo == "disco":
                segna("errori", "%s: %s=\"%s\" e' un percorso del disco locale" % (nome, attributo, valore))
            elif tipo == "radice":
                segna("avvisi", "%s: %s=\"%s\" parte dalla radice del sito invece che dal file"
                      % (nome, attributo, valore))
            elif tipo == "esterno":
                if any(ospite in urlo.lower() for ospite in HOST_TEMPORANEI):
                    segna("errori", "%s: %s punta a un servizio temporaneo: %s"
                          % (nome, attributo, urlo))
            elif tipo == "locale":
                asset.setdefault(pulito, set()).add(nome)
    # I CSS del progetto possono richiamare a loro volta immagini.
    for percorso in sorted((RADICE / "assets").glob("*.css")):
        for attributo, valore in riferimenti_da_css(percorso):
            tipo, pulito, urlo = classifica(percorso.name, attributo, valore)
            if tipo == "locale":
                relativo = str(pathlib.PurePosixPath("assets") / pulito)
                asset.setdefault(relativo, set()).add(percorso.name)
    return asset


def controlla_offline(asset):
    tracciati = file_tracciati()
    if tracciati is None:
        segna("avvisi", "git non disponibile: controllo del tracciamento saltato")
    for percorso_rel, fonti in sorted(asset.items()):
        esito, reale, pezzo = risolvi_maiuscole(percorso_rel)
        dove = ", ".join(sorted(fonti))
        if esito == "assente":
            segna("errori", "%s: citato da %s ma non esiste (manca \"%s\")"
                  % (percorso_rel, dove, pezzo))
            continue
        if esito == "caso":
            segna("errori", "%s: maiuscole diverse dal file reale \"%s\" (citato da %s)"
                  % (percorso_rel, reale.relative_to(RADICE).as_posix(), dove))
            continue
        if esito == "ok" and tracciati is not None:
            if percorso_rel not in tracciati:
                regola = regola_che_blocca(percorso_rel)
                if regola:
                    # Una regola di .gitignore puo' anche nascondere il file alla
                    # pubblicazione: e' il caso da bloccare.
                    segna("errori", "%s: esiste ma git lo ignora (%s)" % (percorso_rel, regola))
                else:
                    segna("avvisi", "%s: presente sul disco, da aggiungere a git" % percorso_rel)
    for nome in EXTRA_DA_PUBBLICARE:
        if not (RADICE / nome).is_file():
            continue
        if tracciati is not None and nome in tracciati:
            segna("ok", "%s presente e versionato: verra' pubblicato" % nome)
        elif tracciati is not None:
            # _headers e' un file che Cloudflare legge solo dalla pubblicazione: se
            # una regola di .gitignore lo nasconde, non arriva mai al sito online.
            regola = regola_che_blocca(nome)
            if regola:
                segna("errori", "%s esiste ma git lo ignora (%s): non arriverebbe online"
                      % (nome, regola))
            else:
                segna("avvisi", "%s: presente sul disco, da aggiungere a git" % nome)
        else:
            segna("avvisi", "%s presente: verra' pubblicato" % nome)
    return len(asset)


def controlla_live(base, asset):
    """Sonda il sito: un asset che torna text/html significa pubblicazione senza file."""
    def scarica(urlo):
        richiesta = urllib.request.Request(urlo, headers={"User-Agent": "verifica-asset"})
        with urllib.request.urlopen(richiesta, timeout=30) as risposta:
            return risposta.status, risposta.headers.get("Content-Type", ""), risposta.read()

    def impronta(dati):
        return hashlib.sha256(dati).hexdigest()[:16]

    # Le due pagine pubblicate devono essere identiche a quelle del progetto.
    for pagina in PAGINE[:2]:
        percorso = RADICE / pagina
        if not percorso.is_file():
            continue
        locale = percorso.read_bytes()
        indirizzo = base + "/" + pagina
        if pagina == "index.html":
            indirizzo = base + "/"
        try:
            stato, tipo, remoto = scarica(indirizzo)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as errore:
            segna("errori", "online %s non risponde: %s" % (indirizzo, errore))
            continue
        if remoto == locale:
            segna("ok", "online %s identico al progetto (sha %s)" % (indirizzo, impronta(locale)))
        else:
            segna("errori", "online %s diverso dal progetto (locale %s, online %s)"
                  % (indirizzo, impronta(locale), impronta(remoto)))

    for percorso_rel in sorted(asset):
        percorso = RADICE / percorso_rel
        if not percorso.is_file():
            continue
        indirizzo = base + "/" + urllib.parse.quote(percorso_rel)
        try:
            stato, tipo, remoto = scarica(indirizzo)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as errore:
            segna("errori", "online %s non risponde: %s" % (indirizzo, errore))
            continue
        atteso = percorso.read_bytes()
        if stato != 200:
            segna("errori", "online %s risponde %s" % (indirizzo, stato))
        elif tipo.lower().startswith("text/html"):
            segna("errori", "online %s torna una pagina HTML al posto del file: "
                  "la pubblicazione non contiene gli asset" % indirizzo)
        elif remoto != atteso:
            segna("errori", "online %s ha contenuto diverso dal file locale (%s contro %s byte)"
                  % (indirizzo, len(remoto), len(atteso)))
        else:
            segna("ok", "online %s servito correttamente (%s byte)" % (indirizzo, len(atteso)))


def esporta(asset, destinazione):
    import shutil

    if ESITO["errori"]:
        segna("errori", "esportazione annullata: prima vanno risolti gli errori qui sopra")
        return
    if destinazione.exists():
        shutil.rmtree(destinazione)
    destinazione.mkdir(parents=True)
    copiati = 0
    byte_totali = 0

    def copia(percorso_rel):
        nonlocal copiati, byte_totali
        origine = RADICE / percorso_rel
        if not origine.is_file():
            return
        arrivo = destinazione / percorso_rel
        arrivo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origine, arrivo)
        copiati += 1
        byte_totali += origine.stat().st_size

    for nome in PAGINE:
        copia(nome)
    for nome in EXTRA_DA_PUBBLICARE:
        copia(nome)
    for percorso_rel in sorted(asset):
        if e_asset(percorso_rel):
            copia(percorso_rel)
    megabyte = byte_totali / (1024 * 1024)
    segna("ok", "pacchetto pronto in %s/: %d file, %.1f MB"
          % (destinazione.name, copiati, megabyte))
    print("   il contenuto e' pronto per la pubblicazione:")
    print("   npx wrangler pages deploy %s --project-name=smashcrew --branch=main --commit-dirty=true"
          % destinazione.name, flush=True)


def main():
    analizzatore = argparse.ArgumentParser(description="Controllo e preparazione del sito Smash Crew.")
    analizzatore.add_argument("--live", action="store_true", help="controlla anche il sito online")
    analizzatore.add_argument("--url", default="https://smashcrew.pages.dev", help="indirizzo del sito")
    analizzatore.add_argument("--export", action="store_true", help="costruisce la cartella da pubblicare")
    analizzatore.add_argument("--dir", default="_deploy", help="nome della cartella da pubblicare")
    opzioni = analizzatore.parse_args()

    print("=== SITO SMASH CREW - CONTROLLO ASSET ===")
    print("Progetto: %s" % RADICE)
    print()

    asset = raccogli_asset()
    quanti = controlla_offline(asset)
    print("=== FILE DEL PROGETTO ===")
    print("  riferimenti locali controllati: %d" % quanti)
    print("  comuni: %s" % (", ".join("%s" % n for n in PAGINE if (RADICE / n).is_file()) or "nessuna pagina"))

    if opzioni.live:
        print()
        print("=== SITO ONLINE (%s) ===" % opzioni.url)
        controlla_live(opzioni.url.rstrip("/"), asset)

    print()
    for messaggio in ESITO["ok"]:
        print("  OK      %s" % messaggio)
    for messaggio in ESITO["avvisi"]:
        print("  AVVISO  %s" % messaggio)
    for messaggio in ESITO["errori"]:
        print("  ERRORE  %s" % messaggio)
    print()

    if ESITO["errori"]:
        print("ESITO: %d problemi da risolvere" % len(ESITO["errori"]))
        return 1

    if opzioni.export:
        esporta(asset, RADICE / opzioni.dir)
        if ESITO["errori"]:
            print()
            for messaggio in ESITO["errori"]:
                print("  ERRORE  %s" % messaggio)
            return 1

    print("ESITO: nessun problema (%d controlli superati, %d avvisi)"
          % (len(ESITO["ok"]), len(ESITO["avvisi"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
