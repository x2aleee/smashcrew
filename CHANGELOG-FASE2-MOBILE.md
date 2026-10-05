# Changelog Fase 2 — Mobile / Motion / Performance

> 3 ottobre 2026. Modifiche applicate a `demo/smashcrew/index.html` (unico file toccato).
> Backup dell'originale: `demo/Smash_Crew_Original/` (mai modificato).
> Verifica: 31/31 check Playwright passati (iPhone 13 + desktop 1440); aggiornato a **37/37 il 4 ottobre** dopo il refactor del drawer. Screenshot in `tools/skill-vetting/shots/`.

## Da audit e skill (Fase B)

1. **Font — payload ridotto.** URL Google Fonts riscritto: rimossi gli assi italici di DM Sans e Montserrat, mai usati nel file (0 tag `<em>/<i>`, 0 `font-style`). `display=swap` già presente, confermato. Nessun `preload` aggiunto: i font critici sono display-only e il testo regge il FOUT.
2. **Immagini — lazy loading completo.** Le uniche 2 `<img>` senza `loading` erano il logo navbar (sopra la piega, resta eager) e il logo footer: aggiunto `loading="lazy" decoding="async"` a quello del footer. Tutte le altre 27 già lazy: aggiunto `decoding="async"` dove mancava.
3. **CSS costoso su mobile — spento.** Dentro `max-width: 768px`: rimosso `backdrop-filter: blur(14px)` dalle card menu (su GPU mobile è il filtro più caro durante lo scroll), `will-change: transform` disattivato su card e immagini (troppi layer promossi = memoria GPU), hover-lift della card disattivato (su touch non serve). Sfondo card sostituito con gradiente solido equivalente.
4. **Tap — igiene.** `-webkit-tap-highlight-color: transparent` + `touch-action: manipulation` sulle CTA (elimina il ritardo 300ms residuo), feedback `:active` con scale su bottoni e filtri.
5. **Leaflet/hero**: nessun cambiamento al JS della mappa e dell'hero: funzionano già bene su mobile e non sono stati toccati.

## Da richieste mobile specifiche (Fase C)

1. **NAVBAR (port da PASTA PIU).** Burger rotondo 42px con bordo e sfondo traslucido (stile `#burger` di PASTA PIU). Il drawer full-screen nero è diventato una **card arrotondata 24px** che scende dall'alto sotto la navbar, su overlay con blur — come `#mobileMenu` di PASTA PIU. Aggiunta CTA "Ordina su WhatsApp" (48px) e indirizzo in fondo alla card. **La navbar resta sopra il menu aperto** (z-index nav 1003 > drawer 1001), come su PASTA PIU (nav z-50 > menu z-40): il burger resta il toggle e chiude.
2. **MENU / accordion prodotti.** Su mobile ogni card è richiudibile: da chiusa mostra nome, prezzo e freccia (foto e descrizione nascoste), da aperta rivela foto (280px), descrizione e pulsante "Aggiungi". Una sola card aperta alla volta. Da chiuso: ~5 prodotti visibili in una schermata (card 106px misurati su viewport 844px). Su desktop: classi inerti, layout 3 colonne invariato.
3. **HERO.** Altezza da 100svh a **138svh** (+38%). Titolo da `clamp(1.8–2.8rem)` a `clamp(2.7–4.4rem)`: a 390px misura 48.75px (era ~40px). Allineamento a sinistra confermato, mai centrato. Il titolo resta ancorato al fondo della **prima** viewport (posizione identica a prima, `bottom: 38svh` compensa l'hero più alto): la prima schermata non cambia impatto, il video respira sotto per altri ~35svh.
4. **INGREDIENTI — tap.** Il binding `mouseenter` è ora condizionato a `(hover: hover) and (pointer: fine)`: su desktop l'hover resta il trigger, su mobile il tap passa dal `click` senza doppio binding. Verificato: tap sul secondo pannello attiva lui e disattiva il primo.
5. **DOVE SIAMO + FOOTER.** `.dove__grid` già a colonna singola sotto 960px, confermato e rifinito (padding, altezza mappa `clamp(340–460px)`). Footer: da 3 colonne a **1 colonna** sotto 768px, link con tap target 44px, social 48px, riga legale in colonna. Zero overflow orizzontale verificato a 390px (scrollWidth = clientWidth = 390).

## Motion (Fase D)

- Accordion prodotti: apertura/chiusura con `max-height` + opacity su curva `--ease-out-quint` (0.5s), freccia che ruota 180° e diventa arancione da aperta.
- Drawer navbar: card con `translateY + scale` in ingresso, `--ease-out-expo`.
- Micro-press `:active` su CTA e filtri; tutto con `prefers-reduced-motion` rispettato (transizioni azzerate nel blocco dedicato).
- Nessuna animazione aggiunta che pesi su scroll o che usi keyframes continui.

## Performance (Fase E)

- Font URL alleggerito (meno varianti = meno file scaricati).
- `backdrop-filter` rimosso dalle card su mobile; `will-change` spento; hover disattivato.
- `decoding="async"` sulle immagini sotto la piega.
- `preconnect` a fonts.gstatic già presenti, invariati.
- Hero: il video resta `preload="auto"` (è l'LCP visuale), nessun cambio rischioso.

## File modificati

- `demo/smashcrew/index.html` — tutte le modifiche (CSS in un blocco `MOBILE POLISH`, JS in un blocco finale, 2 attributi img, URL font, 1 fix hover ingredienti, 1 fix markup drawer).
- `demo/Smash_Crew_Original/` — backup, **mai toccato**.
- `../SmashCrew_Compare/` (Desktop) — comparatore Prima/Dopo + server.

## Rischi residui / da testare a mano su iPhone vero

1. **Video hero a 138svh su iOS Safari**: `svh` è supportato da iOS 15.4+, ma la barra dinamica di Safari può cambiare `svh` durante lo scroll. Da verificare che il titolo resti stabile.
2. **Accordion con filtro attivo**: filtrare per categoria e poi aprire una card funziona (delegato sul grid), ma da ri-testare la combinazione filtro + apertura + scroll.
3. **Drawer + rotazione schermo**: card centrata con `max-height: calc(100svh - 32px)` e scroll interno; in landscape stretto il contenuto scorre dentro la card, mentre X e CTA restano in alto, sempre raggiungibili. Da verificare comunque su iPhone vero.
4. **Tap su "Aggiungi" da card chiusa**: il pulsante è nascosto da chiuso (`display:none`), quindi non è cliccabile per errore. Verificato da aperto.

## Aggiornamento 4 ottobre 2026 — Drawer versione definitiva + fix centratura

- **Drawer mobile, versione finale.** La card ha ora la barra header [logo Smash Crew | CTA "ORDINA ORA" | bottone X], i link impilati in bold uppercase (MENU, I PIÙ VENDUTI → Best Seller, IL METODO, DOVE SIAMO, DELIVERY, CONTATTI → footer) e la caption "SMASH CREW — CIVITANOVA MARCHE, ITALIA". Il backdrop a pieno schermo con blur copre anche la navbar (drawer z 1001 > nav 1000: prima il rapporto era invertito): si chiude con la X, Esc, tap sul backdrop o su una voce; il burger resta il toggle di apertura.
- **Fix centratura.** Misurate a 390px: le testate di Menu, Metodo e Ingredienti erano già centrate; Dove Siamo era l'unica a sinistra. Ora `.dove__kicker`/`.dove__title` sono centrati e `.dove__sub` ha `margin: 0 auto`. La colonna di testo della card Delivery resta a sinistra di proposito (layout a card con immagine, non testata di sezione).
- **JS drawer.** Focus trap esteso al bottone X; nuova chiusura automatica se il viewport supera 769px mentre il menu è aperto (rotazione/resize).
- **Verifica.** 37/37 check Playwright (6 nuovi: backdrop sopra navbar, logo, X 44px, caption, chiusura con X, testata Dove centrata) + `check-drawer-head.mjs` (ordine [logo|CTA|X] su mobile 390 e tablet 800, barra dentro il viewport, backdrop sopra la navbar, 7 anchor validi) + `check-centering.mjs`. Screenshot aggiornati in `tools/skill-vetting/shots/`.
