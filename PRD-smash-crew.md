# PRD — Sito one-page Smash Crew (Smash Burger House, Civitanova Marche)

- **Versione:** 1.0 — 5 settembre 2026
- **Stato:** bozza da approvare
- **Fonte dati:** brief cliente (brand, menu, contatti, orari, toni, identità visiva). Ogni dato non fornito è marcato **DA CONFERMARE**.
- **File collegati:** `demo/smashcrew/index.html` (build v1 della landing)

---

## 1. Overview del progetto

### 1.1 Obiettivo del sito
Landing page monopagina in italiano che trasforma visite in **ordini** (WhatsApp, Deliveroo) e **visite al locale** (Via Regina Elena 56, Civitanova Marche). Presenta brand, menu e canali di ordine di Smash Crew con testi definitivi, senza segnaposto.

### 1.2 Contesto
Smash Crew è una smash burgeria piccola e di tendenza a Civitanova Marche, a gestione femminile, tono giovane e diretto, payoff operativo **WeGrillYouChill**. Valutazione 4,9 su 80 recensioni, scontrino medio 10–20 €. Orari dichiarati: martedì–domenica 19–23. Servizi: consumo sul posto, asporto, consegna a domicilio, prenotazioni. Ambiente casual, LGBTQ friendly.

### 1.3 Posizionamento
Smash burger come prodotto **veloce, croccante, autentico**: carne pressata sulla piastra rovente, crosta da reazione di Maillard, cuore succoso, montaggio preciso. Niente hamburger gonfi, niente scorciatoie.

### 1.4 Valore differenziante
- Prodotto riconoscibile (smash + fritti come Patate Dippers e nuggets di pulled pork).
- Prova sociale forte (4,9/80) per un locale piccolo.
- Ordine diretto e umano via WhatsApp + delivery su Deliveroo.
- Identità inclusiva e locale (Civitanova Marche, gestione femminile).

---

## 2. Obiettivi di business e KPI

| ID | Obiettivo | KPI | Target indicativo v1 | Strumento |
|----|-----------|-----|----------------------|-----------|
| KPI-01 | Aumentare ordini diretti | Click "Ordina su WhatsApp" / visite | DA CONFERMARE col cliente | Analytics eventi |
| KPI-02 | Aumentare delivery | Click link Deliveroo / visite | DA CONFERMARE col cliente | Analytics eventi |
| KPI-03 | Portare traffico al locale | Click telefono + click indicazioni / visite | DA CONFERMARE col cliente | Analytics eventi |
| KPI-04 | Crescita social | Click Instagram e Linktree / visite | DA CONFERMARE col cliente | Analytics eventi |
| KPI-05 | Qualità traffico locale | % visite da Civitanova/Macerata e da mobile | DA CONFERMARE col cliente | Analytics geo/device |
| KPI-06 | Coinvolgimento | Scroll depth 75% e tempo mediano pagina | DA CONFERMARE col cliente | Analytics scroll/tempo |

> I target numerici sono DA CONFERMARE: si fissano dopo 30 giorni di baseline.

---

## 3. Target e personas

### P1 — Studente fuori sede (18–24)
- **Bisogni:** mangiare bene spendendo 10–20 €, ordinare in fretta dal telefono.
- **Comportamenti:** mobile-first, cerca "smash burger vicino a me", ordina via WhatsApp o Deliveroo la sera.
- **Job to be done:** "Stasera voglio lo smash senza sbatti: ordino e ritiro."

### P2 — Giovane coppia / famiglia locale (25–40)
- **Bisogni:** posto affidabile e recensito per la cena, orari chiari, prenotazione facile.
- **Comportamenti:** legge recensioni Google, controlla orari e mappa, chiama per prenotare.
- **Job to be done:** "Trovo dove cenare venerdì senza sorprese."

### P3 — Gruppo di amici, serata (18–35)
- **Bisogni:** locale casual e inclusivo, asporto per il gruppo, condivisione social.
- **Comportamenti:** arriva da Instagram/Linktree, condivide il menu in chat, ordina in gruppo.
- **Job to be done:** "Organizziamo la cena: mando il link e ognuno sceglie."

---

## 4. Scope

### In scope (v1)
- One-page statica in un solo file HTML (CSS/JS inline), IT, mobile-first.
- Sezioni: header sticky, hero, fiducia, best seller, menu, metodo, recensioni, come ordinare, info+mappa, FAQ, footer, call bar mobile.
- CTA: WhatsApp, Deliveroo, click-to-call, indicazioni stradali.
- Mappa Google embed, JSON-LD Restaurant, meta/OG SEO locale.
- Tracking eventi base sui click principali.

### Out of scope (v1 → v2)
- E-commerce o carrello proprietario; pagamenti online.
- Form contatti/prenotazione proprietario (v1 usa WhatsApp/telefono; form valutabile in v2 — DA CONFERMARE col cliente).
- Multilingua, blog, area riservata, CMS.
- Pop-up promo (valutabile solo se richiesto — DA CONFERMARE).
- Integrazione API Just Eat (si rimanda alla ricerca in app — URL diretto DA CONFERMARE).

---

## 5. Architettura della one-page

Legenda priorità: **Must** = obbligatoria v1 · **Should** = inclusa se a costo zero · **Could** = solo se avanza tempo.

| # | Sezione | Scopo | Contenuti | Elementi UI | CTA | Priorità | ID |
|---|---------|-------|-----------|-------------|-----|----------|----|
| 1 | Header sticky | Orientare e convertire sempre | Logo testuale, nav anchor, bottone WhatsApp, burger mobile | Barra fissa, menu mobile fullscreen | Ordina su WhatsApp | Must | SEC-01 |
| 2 | Hero | Promessa + azione in 5 secondi | Kicker locale, H1, sottotitolo, rating 4,9/80 | Titolo condensed, 2 bottoni, badge rating | WhatsApp / Vedi menu | Must | SEC-02 |
| 3 | Striscia fiducia | Ridurre incertezza | 4,9/80 · 10–20 € · Mar–Dom 19–23 · asporto+delivery | 4 celle, mobile 2×2 | — | Must | SEC-03 |
| 4 | Best seller | Vetrina appetito | 3 schede: Smash Cheese, Patate Dippers, Nuggets Pulled Pork | Card con visual CSS, prezzo | WhatsApp | Must | SEC-04 |
| 5 | Menu completo | Informare e indirizzare | Smash burger, hot dog & fritti, bevande; prezzi DA CONFERMARE; nota onesta + rimando WhatsApp | Lista con leader puntinati, 2 colonne | Menu WhatsApp | Must | SEC-05 |
| 6 | Metodo smash | Differenziare | 3 passi: Pressiamo / Caramelliamo / Montiamo | 3 step numerati | — | Should | SEC-06 |
| 7 | Recensioni | Prova sociale | 3 citazioni reali + link a tutte le recensioni | Quote card | Leggi su Google | Must | SEC-07 |
| 8 | Come ordinare | Convertire per canale | WhatsApp, Deliveroo, locale/telefono | 3 card canale | 3 CTA dirette | Must | SEC-08 |
| 9 | Info + mappa | Trovare e contattare | Indirizzo, orari, telefono, social, mappa embed | 2 colonne + iframe | Indicazioni / Chiama | Must | SEC-09 |
| 10 | FAQ | Sciogliere dubbi | Prenotazioni, sul posto/asporto, orari, menu aggiornato | Accordion accessibile | WhatsApp | Should | SEC-10 |
| 11 | Footer | Chiudere e recapitare | Brand, payoff, link, contatti, orari, copyright | 3 colonne + barra legale | — | Must | SEC-11 |
| 12 | Call bar mobile | Conversione mobile | Chiama / WhatsApp / Menu | Barra fissa solo mobile | 3 CTA | Must | SEC-12 |

---

## 6. Requisiti funzionali

| ID | Requisito | Priorità | Accettazione |
|----|-----------|----------|--------------|
| FR-01 | Header sticky con anchor link a tutte le sezioni | Must | Tutti gli anchor raggiungono la sezione corretta su mobile e desktop |
| FR-02 | Menu mobile (burger) apribile/chiudibile, chiude alla selezione | Must | Funziona a 360px, focus gestito, `aria-expanded` corretto |
| FR-03 | CTA WhatsApp con link `https://wa.me/393501684896` in header, hero, menu, ordina, call bar | Must | Ogni bottone apre la chat corretta in nuova scheda |
| FR-04 | CTA Deliveroo con URL ufficiale fornito, in "Come ordinare" e footer | Must | Link esatto invariato dal brief |
| FR-05 | Click-to-call `tel:+393501684896` in contatti e call bar | Must | Su mobile avvia la chiamata |
| FR-06 | Pulsante indicazioni stradali verso la mappa fornita | Must | Apre il link mappe fornito |
| FR-07 | Mappa Google embed dell'indirizzo con `loading="lazy"` e titolo accessibile | Must | Mappa visibile, nessun blocco del caricamento |
| FR-08 | Link Instagram e Linktree ufficiali in contatti e footer | Must | URL esatti invariati dal brief |
| FR-09 | Riferimento Just Eat solo come testo "cerca Smash Crew Civitanova Marche" (URL diretto DA CONFERMARE) | Must | Nessun URL inventato |
| FR-10 | FAQ ad accordion con tastiera e `aria-expanded` | Should | Apertura/chiusura da tastiera e screen reader |
| FR-11 | Anno copyright automatico | Should | Anno corrente senza intervento manuale |
| FR-12 | Form proprietario con validazione e anti-spam | Out (v2) | DA CONFERMARE col cliente se serve |

---

## 7. Requisiti di design e UX

| ID | Requisito | Dettaglio |
|----|-----------|-----------|
| DS-01 | Direzione estetica | Smash bold moderno: fondo carbone quasi nero, accenti fuoco giallo e rosso, texture griglia sottile, kicker maiuscoli distanziati |
| DS-02 | Tipografia | Titoli: condensed maiuscolo impattante (es. Anton via Google Fonts con fallback system) · Testi: carattere geometrico leggibile (es. Manrope con fallback system). Titoli < 60 caratteri |
| DS-03 | Palette | Fondo `#0E0D0B`, superfici `#181410`, testo crema `#F5EFE3`, giallo fuoco `#FFC21C`, rosso brace `#FF3B2E`, muted caldo. Contrasto testo/sfondo ≥ 4.5:1 |
| DS-04 | Gerarchia | Una sola H1; H2 per sezione con kicker; paragrafi compatti; CTA primaria gialla sempre riconoscibile |
| DS-05 | Micro-interazioni | Reveal on scroll sobrio, hover su card/bottoni, marquee payoff; tutto disattivato con `prefers-reduced-motion` |
| DS-06 | Accessibilità WCAG 2.1 AA | Skip-link, landmark semantici, alt/aria-label descrittivi, focus visibile, target touch ≥ 44px, nessun contenuto solo-colore |
| DS-07 | Responsive | Breakpoint 360 / 768 / 1024 / 1440; mobile-first; call bar fissa solo sotto 860px; nessuna scroll orizzontale a 320px |
| DS-08 | Imagery | Nessuna foto generica: visual CSS astratti con slot commentati per foto reali; quando arrivano, `loading="lazy"` e alt descrittivi |

---

## 8. Requisiti non funzionali

| ID | Requisito | Target |
|----|-----------|--------|
| NFR-01 | Performance | LCP < 2,5 s · INP < 200 ms · CLS < 0,1 su mobile 4G; peso pagina < 500 KB senza foto |
| NFR-02 | Single-file | Un solo `.html` autocontenuto (CSS/JS inline), zero build, zero dipendenze JS esterne salvo Google Fonts |
| NFR-03 | SEO locale on-page | Title + meta description con "Civitanova Marche" e "smash burger"; H1 unica; OG tag; `lang="it"` |
| NFR-04 | Dati strutturati | JSON-LD `Restaurant` con nome, indirizzo, telefono, orari, `aggregateRating` 4,9/80, `sameAs` reali |
| NFR-05 | Google Business | Scheda esistente collegata (link recensioni/mappa); proprietà e accessi DA CONFERMARE |
| NFR-06 | Sicurezza | Deploy solo HTTPS; nessun form v1 quindi nessuna superficie di input; link esterni con `rel="noopener"` |
| NFR-07 | Privacy/GDPR | Nessun cookie di profilazione v1; se si aggiunge Analytics: banner consenso + cookie policy prima dell'attivazione — DA CONFERMARE |
| NFR-08 | Compatibilità | Chrome/Edge, Firefox, Safari (ultime 2 major) + browser mobile stock; degrado elegante senza JS |
| NFR-09 | Dominio e URL | Dominio/canonical DA CONFERMARE; nessun URL inventato |

---

## 9. Requisiti di contenuto

| ID | Asset | Stato | Responsabile |
|----|-------|-------|--------------|
| CT-01 | Testi IT definitivi 900–1400 parole, tono energico-locale | Pronti in `index.html` | Redazione (già consegnati) |
| CT-02 | Prezzi per piatto | **DA CONFERMARE** — in pagina solo "DA CONFERMARE" + nota onesta | Cliente |
| CT-03 | Ingredienti/allergeni dettagliati | **DA CONFERMARE** — rimando a WhatsApp per menu aggiornato | Cliente |
| CT-04 | Foto reali (hero, 3 best seller, locale) con alt | **DA CONFERMARE** — slot pronti, visual CSS temporanei | Cliente/fotografo |
| CT-05 | Logo/marchio ufficiale | **DA CONFERMARE** — in pagina solo logotipo testuale | Cliente |
| CT-06 | URL diretto Just Eat | **DA CONFERMARE** — intanto solo testo di ricerca | Cliente |
| CT-07 | Eventuali promo/pop-up | **DA CONFERMARE** — esclusi v1 | Cliente |

Vincoli editoriali: niente promesse su consegna gratuita o tempi garantiti; niente ingredienti inventati come certi; coerenza con WeGrillYouChill; rispetto per gestione femminile e ambiente inclusivo; linguaggio diretto senza volgarità.

---

## 10. Stack tecnologico e hosting

| Opzione | Proposta | Motivo | Contro |
|---------|----------|--------|--------|
| **A — File statico (raccomandata v1)** | `index.html` unico, hosting Netlify/Vercel/GitHub Pages + HTTPS | Zero costi, zero manutenzione, performance massime, aggiornabile da chiunque | Menu prezzi aggiornati a mano nel file |
| B — CMS headless/WordPress | Solo se il cliente vuole autonomia totale | Editing visuale | Costi, plugin, superficie di attacco, overkill per one-page |
| C — Site builder (Wix/Squarespace) | Solo se già in uso dal cliente | Semplicità | Costi ricorrenti, SEO/limits tecnici |

**Aggiornamento menu v1:** catalogo ufficiale su WhatsApp (`wa.me/c/393501684896`) come fonte verità; la pagina rimanda lì. Modifica prezzi/foto = edit del singolo file + redeploy (minuti). Processo documentato in 5 righe nel footer del repo — DA CONFERMARE col cliente.

---

## 11. Analytics e tracciamento

| ID | Evento | Trigger | Priorità |
|----|--------|---------|----------|
| AN-01 | `click_whatsapp` (+ posizione: header/hero/menu/ordina/callbar) | Click CTA WhatsApp | Must |
| AN-02 | `click_deliveroo` | Click CTA Deliveroo | Must |
| AN-03 | `click_call` | Click telefono | Must |
| AN-04 | `click_directions` | Click indicazioni/mappa | Must |
| AN-05 | `click_social` (+ rete) | Click Instagram/Linktree | Should |
| AN-06 | `scroll_75` | Profondità scroll 75% | Should |

Strumento: GA4 o alternativa privacy-first (es. Plausible) — **scelta DA CONFERMARE**; attivazione solo dopo banner/consenso (vedi NFR-07).

---

## 12. Piano di rilascio

| Fase | Deliverable | Criteri di accettazione per sezione |
|------|-------------|-------------------------------------|
| F1 Contenuti (chiusa) | Brief validato, testi, link reali | Tutti i link del brief presenti e identici; prezzi ignoti marcati DA CONFERMARE |
| F2 Build | `index.html` single-file | SEC-01–12 presenti nell'ordine richiesto; zero segnaposto; zero URL inventati |
| F3 QA | Test mobile 360px, desktop 1440px, tastiera, contrasto | FR-01–11 e NFR-01–04,08 verificati; checklist go-live spuntata |
| F4 Dati mancanti | Prezzi, foto, logo, Just Eat, dominio | CT-02–06 risolti o restano DA CONFERMARE espliciti |
| F5 Go-live | Deploy HTTPS + Analytics | NFR-05–07, AN-01–04 attivi; monitoraggio 30 giorni per fissare target KPI |

---

## 13. Rischi e dipendenze

| ID | Rischio | Impatto | Mitigazione |
|----|---------|---------|-------------|
| RK-01 | Prezzi/foto/logo non arrivano | Pagina incompleta o con visual temporanei | Marcatura DA CONFERMARE + slot pronti; go-live possibile comunque |
| RK-02 | Link delivery di terze parti cambiano | CTA rotte | URL in unico punto del file + controllo mensile DA CONFERMARE (owner) |
| RK-03 | Tutto l'ordine passa da WhatsApp/telefono | Picco serale non gestito | Orari e prenotazioni evidenti; valutare form in v2 |
| RK-04 | Aspettative da locale piccolo | Delusione su posti/waiting | Copy onesto ("locale piccolo, prenota"), prenotazione via WhatsApp in evidenza |
| RK-05 | Recensioni citate diventano datate | Prova sociale stanca | Link "leggi tutte" verso Google sempre aggiornato |

---

## 14. Domande aperte / punti DA CONFERMARE

| ID | Domanda | Owner | Blocca go-live? |
|----|---------|-------|-----------------|
| Q-01 | Prezzi per piatto e bevande? | Cliente | No (marcati DA CONFERMARE) |
| Q-02 | Ingredienti e allergeni per piatto? | Cliente | No (rimando WhatsApp) |
| Q-03 | Foto reali: chi le fornisce e quando? | Cliente | No (slot pronti) |
| Q-04 | Logo ufficiale disponibile? | Cliente | No (logotipo testuale) |
| Q-05 | URL diretto Just Eat? | Cliente | No (testo di ricerca) |
| Q-06 | Dominio e hosting scelti? | Cliente | Sì, per il go-live |
| Q-07 | Analytics sì/no e quale strumento + consenso? | Cliente | Sì, prima di attivare tracking |
| Q-08 | Form prenotazione proprietario in v1 o resta WhatsApp? | Cliente | No (default: WhatsApp) |
| Q-09 | Opzioni vegetariane/vegane e senza glutine? | Cliente | No (non dichiarate in pagina) |
| Q-10 | Target KPI numerici dopo baseline 30 giorni? | Cliente + PM | No |

---

## Checklist di accettazione finale (go-live)

- [ ] Titolo e meta description con Civitanova Marche + smash burger presenti.
- [ ] Tutte le 12 sezioni nell'ordine richiesto, testi definitivi, zero lorem ipsum.
- [ ] Zero prezzi inventati: ogni piatto senza prezzo ufficiale riporta DA CONFERMARE + nota WhatsApp.
- [ ] WhatsApp, Deliveroo, telefono, mappa, Instagram, Linktree: URL identici al brief, tutti cliccabili.
- [ ] Nessun URL inventato (Just Eat solo come testo di ricerca).
- [ ] Mobile 360px: call bar visibile, nessuna scroll orizzontale, titoli compatti.
- [ ] Contrasto testo/sfondo ≥ 4,5:1; navigazione completa da tastiera; `prefers-reduced-motion` rispettato.
- [ ] JSON-LD Restaurant valido; H1 unica; `lang="it"`.
- [ ] Deploy HTTPS su dominio confermato; Analytics solo dopo consenso.
