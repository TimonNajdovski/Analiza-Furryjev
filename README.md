# Analiza-Furryjev

Furryji so navdušenci nad živalskimi liki s človeškimi osebnostmi, zlasti ljudje, ki se identificirajo s nekim živalskim likom (svojo fursono, fur + persona) in se oblačijo v kostum (fursuit) tega lika.  
Analiziral bom uporabnike spletne strani https://db.fursuit.me/, kjer uporabniki lahko ustvarijo račun in objavijo svoj fursuit.

#### Za vsakega uporabnika bom zajel:
- Državo prebivališča
- Spol
- Starost
- Spol fursone
- Živalsko vrsto fursone
- Leto, ko je ustvaril račun
- Leto, ko je kupil fursuit

## Hipoteze
- Obstaja korelacija med spolom in vrsto živali  
- Najpogostejše vrste so iz redu zveri
- Povprečen uporabnik kupi fursuit v svojih srednjih dvajsetih letih
- Živali, rangirane po popularnosti, bodo tvorile obratno sorazmerno krivuljo

## Delovanje programa
Program, ki sem ga spisal, najprej naloži stran, na kateri so vidni vsi fursuiti in z nje zbere identifikacijske številke fursuitov in imena njihovih lastnikov. Z uporabo tih nato v dve datoteki naloži posamezne strani vseh fursuitov in vseh uporabnikov, ki so na stran objavili svoj fursuit.  
Iz posamezne spletnih strani nato zbere več podatkov, združi podatke fursuita in njegovega lastnika ter nazadnje shrani podatke kot csv datoteko.
