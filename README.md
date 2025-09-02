# AI Hide and Seek

## Table of Contents

1. [Authors](#authors)
2. [Motivation](#motivation)
3. [How to contribute](#how-to-contribute)
4. [How to run](#how-to-run)

## Authors:

- [Bobei Bogdan](https://github.com/WolfishAtom7515)
    - Q-Learning
    - Code restructure

- [Barbu Alexandru](https://github.com/AlexandruDanielBarbu)
    - Game Graphics
    - map and hide and seek mechanics

## Motivation

This project was created as part of a `Game AI and Computer Vision` **summer course**, serving as a practical demonstration of **fundamental AI implementation** within a game environment.

> [!NOTE]
> The core development was completed over a two-week period with a friend.

## How to contribute

> [!CAUTION]
> Create a new branch just for you!!

> [!CAUTION]
> The code was developed on wsl 2, as a result I recommend running the code on a linux based system.

> [!IMPORTANT]
> After successfully cloning the project:

```bash
# Step 1.1 - create a virtual env
python -m venv env  # venv called `env`
```
```bash
# Step 1.2 - activate virtual env
source env/bin/activate
```
```bash
# Step 2 - intall dependencies
pip install -r requirements.txt
```

## How to run

> [!CAUTION]
> Run the `main.py` from the root of the project, otherwise the assets will not be found.

> [!IMPORTANT]
> After creating the virtual environment and downloading the dependencies:

```bash
# Step 3 - run the code
python3 main.py
```

## Developing experience

La început, când am folosit versiunea simplă a algoritmului Q-learning, mi-am dat seama imediat că exista o problemă gravă: agentul meu dura prea mult să se miște în direcții greșite și nici măcar nu se apropia de locul unde apăreau recompensele. Am efectuat teste timp de două ore, dar agentul a rămas blocat în aceleași locuri, fără niciun progres vizibil.

Prima soluție pentru îmbunătățirea procedurii a fost utilizarea unei penalizări pentru celulele deja vizitate. Ideea era că agentul ar învăța să nu mai urmeze rute inutile și ar fi „obligat” să călătorească mai mult. Deși mecanismul s-a dovedit a fi util la început, pe termen lung am înțeles că era prea sever: penalizările negative s-au acumulat și au dus la confuzia completă a agentului, limitând învățarea.

Al doilea lucru a fost modificarea alegerii acțiunilor. Am aplicat softmax, ceea ce ne-a oferit un echilibru mai bun între explorare și exploatare. De asemenea, am optat să elimin recompensele negative și să redefinim funcția de recompensă: dacă agentul făcea mai mult de un număr gigantic de pași (mai mult de 400), ultima recompensă era 0, iar în caz contrar, era 400 / numărul de pași. Această idee s-a dovedit a fi de succes, iar agentul a început să rezolve, dar încă avea un număr foarte mare de pași (între 500 și 900).

Apoi am adăugat distanța Manhattan și funcția phi ca recompense orientative în etapa finală. Astfel, agentul a primit feedback intermediar în funcție de proximitatea sa față de obiectiv, ceea ce a contribuit la accelerarea semnificativă a învățării. De asemenea, am reintrodus în mod selectiv unele penalizări negative, pentru a elimina comportamentul aberant fără a-l confunda complet.

Una dintre descoperirile uimitoare pe care le-am făcut a fost influența numărului de zone de recompensă. Am început testarea de la 10, apoi am scăzut treptat la 3, iar când am testat cu doar 2 zone de recompensă, agentul a început să învețe extrem de repede. În decurs de 10 minute de antrenament, a fost capabil să găsească ruta optimă care le conecta, convergând în mod consecvent către cea mai bună soluție.