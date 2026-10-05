# Prompt — Video turntable panino Smash Crew (chroma key)

> Prompt pronto per modelli **image-to-video** (Veo 3, Kling 2.x, Runway Gen-4).
> Modalità image/video della skill `prompt-optimizer`: prosa inglese, niente XML,
> niente chain-of-thought, UN solo aspect ratio, blocco "Avoid" incluso.

---

## Come si usa (3 passi)

1. **Preparo io il frame di partenza**: dal PNG trasparente del panino composito
   il panino centrato su sfondo verde croma puro `#00FF00` (canvas quadrato,
   panino al centro con margine ~15% per lato). Ti carico questo file.
2. **Tu generi**: apri il modello video in modalità image-to-video, carichi il
   frame verde come immagine iniziale, incolli il prompt qui sotto, generi.
3. **Tu mi consegni**: scarichi l'MP4 alla qualità massima disponibile e me lo
   mandi. Da lì in avanti è tutto mio: estrazione frame, rimozione sfondo,
   sequenza WebP, codice scroll.

**Impostazioni consigliate nel tool:** durata 4–5 s · aspect ratio 1:1 ·
risoluzione massima disponibile (1080×1080 min, 4K se c'è) · 24 o 30 fps ·
modalità image-to-video con il frame verde come first frame.

---

## ⭐ PROMPT (copia tutto il blocco)

```
01 ROLE
You are a senior commercial food-film director with 20 years of studio product
turntable shots for fast-food advertising, in the style of high-end burger chain
commercials shot by professional food stylist teams.

02 SUBJECT & MOTION
The exact smash burger from the input image stays perfectly centered in frame
and rotates slowly and uniformly around its vertical axis, completing one full
360-degree turn across the whole clip. The burger keeps its exact shape, layers,
ingredients and lighting from the first frame to the last: toasted golden bun
with warm highlights (#E8A33D) and deep shadows (#B26E1F), melted cheddar
flowing over the edges (#F2A93B), crispy bacon edges (#8C4A1F), creamy sauce
drips (#D97B2F), charred smash crust on the beef (#5C3317), fresh green flecks
of onion (#7FA65A). No ingredient moves on its own, nothing drips, nothing
deforms, no toppings fall.

03 CAMERA & RHYTHM
The camera is completely locked on a tripod: no pan, no tilt, no zoom, no dolly,
no shake, no breathing focus. Static macro product shot, 50mm lens look, f/8,
eye level with the middle of the burger. The rotation speed is constant from
start to finish, with no easing and no pauses.

04 BACKGROUND & LIGHT
Seamless pure chroma-key green background (#00FF00), perfectly even and flat,
with no gradients, no vignette, no shadows cast on the backdrop and no green
spill on the burger. Warm studio key light from the upper left (#FFD9A0), soft
amber rim light from the right rear (#FFB347), gentle fill bounce from below.
Moody high-end fast-food commercial grade, photorealistic, high detail.

05 TECHNICAL
One single continuous clip. Square 1:1 aspect ratio. 1080x1080 minimum
resolution. 24 fps. 4 to 5 seconds duration. The burger floats centered with no
plate, no board and no contact shadow beneath it. No text, no logos, no
watermarks, no people, no hands, no props, no steam, no smoke, no dust
particles.

AVOID: any camera movement, zoom, background change or texture, gradient or
vignette on the green backdrop, burger deformation or melting, ingredient
morphing, falling toppings, steam or smoke, depth-of-field breathing, flickering
light, text or watermarks, hands or tools, plate or surface under the burger,
motion blur on the rotation.
```

---

## Perché il video contiene SOLO la rotazione

La discesa, la traslazione orizzontale, la scala e l'atterraggio nella sezione 2
**non vanno mai nel video**: lo scroll è controllato dall'utente (avanti,
indietro, veloce, lento) e un video ha una sua timeline fissa che non si può
"scrubbare" in modo fluido. Il video serve solo a dare le **fasi di rotazione**
del panino; posizione e percorso li anima il codice legato allo scroll
(GSAP ScrollTrigger in modalità scrub). Così il panino segue il dito
dell'utente in entrambe le direzioni.

Se invece ci accontentiamo di una rotazione "leggera" (tilt 3D + oscillazione
sulla foto singola), il video non serve affatto: basta il PNG trasparente e il
codice lo fa tutto. Consigliato come primo passo, il turntable si aggiunge dopo.
