"""
Hilfsfunktionen für den Python-Kurs: Sentimentanalyse von Grimms Märchen.

Dieses Modul stellt bereit:
- Prüffunktionen für die Übungen in jedem Kapitel
- Hilfsfunktionen zum Laden und Bereinigen von Texten (kommt später)
- Wortlisten: Stoppwörter, positive/negative Wörter (kommt später)

Aufbau der Prüffunktionen:
- Jede Funktion heißt: pruefe_XX_aufgabe_Y()
  XX = Kapitelnummer, Y = Aufgabennummer
- Die Funktionen verraten keine Lösungen, sondern geben nur Hinweise.
- Studierende rufen sie mit einer einzigen Zeile auf, z.B.: pruefe_01_aufgabe_1a()
"""

import inspect


# ============================================================
# Interne Hilfsfunktionen (nicht für Studierende)
# ============================================================

def _hole_variablen():
    """
    Holt die Variablen aus dem aufrufenden Notebook.
    Wird intern von allen Prüffunktionen genutzt.
    """
    frame = inspect.stack()[2][0]
    return frame.f_globals


def _pruefe_variable(variablen, name, erwarteter_wert, erwarteter_typ=None):
    """
    Prüft eine einzelne Variable und gibt hilfreiche Hinweise.
    Gibt True zurück wenn alles stimmt, sonst False.
    """
    if name not in variablen:
        print(f"  ❌ Variable '{name}' nicht gefunden. Wurde die Zelle darüber ausgeführt?")
        return False

    wert = variablen[name]

    # Typ prüfen, falls gewünscht
    if erwarteter_typ is not None:
        if not isinstance(wert, erwarteter_typ):
            print(f"  ❌ '{name}' hat den falschen Datentyp. Erwartet wird: {erwarteter_typ.__name__}")
            return False

    # Wert prüfen
    if isinstance(erwarteter_wert, (int, float)) and isinstance(wert, (int, float)):
        if wert != erwarteter_wert:
            if wert > erwarteter_wert:
                print(f"  ❌ '{name}' ist zu hoch.")
            else:
                print(f"  ❌ '{name}' ist zu niedrig.")
            return False
    elif wert != erwarteter_wert:
        print(f"  ❌ '{name}' hat nicht den erwarteten Wert.")
        return False

    return True

# ============================================================
# WORTLISTEN UND LEXIKA
# ============================================================
# Enthält:
# - GERMAN_STOPWORDS: Deutsche Stoppwortliste (entspricht NLTK)
# - GRIMM_SENTIMENT_LEXIKON: Sentiment-Lexikon für Grimms Märchen
# - NEGATION_TRIGGERS: Negationswörter für die Negationserkennung
# - berechne_sentiment(): Sentiment Score berechnen
# - berechne_sentiment_mit_negation(): Score mit Negationserkennung
# ============================================================


# Deutsche Stoppwortliste (entspricht nltk.corpus.stopwords.words("german"))
GERMAN_STOPWORDS = [
    "aber", "alle", "allem", "allen", "aller", "allerdings", "alles",
    "also", "am", "an", "ander", "andere", "anderem", "anderen",
    "anderer", "anderes", "anderm", "andern", "anderr", "anders",
    "auch", "auf", "aus", "außerdem",
    "bei", "beide", "beiden", "beider", "beiderlei", "beides",
    "beim", "beispiel", "bekannt", "bereits", "besser", "beste",
    "bestem", "besten", "besser", "bin", "bis", "bisher", "bist",
    "bitte",
    "da", "dabei", "dadurch", "dafür", "dagegen", "daher", "dahin",
    "damals", "damit", "danach", "daneben", "dank", "dann", "daran",
    "darauf", "daraus", "darf", "darfst", "darüber", "darum",
    "darunter", "das", "dasselbe", "dass", "davon", "davor", "dazu",
    "dein", "deine", "deinem", "deinen", "deiner", "deines",
    "dem", "den", "denn", "dennoch", "der", "deren", "des",
    "deshalb", "dessen", "dich", "die", "dies", "diese", "dieselbe",
    "dieselben", "diesem", "diesen", "dieser", "dieses", "dir",
    "doch", "dort", "drei", "drin", "dritte", "dritten", "dritter",
    "drittes", "du", "dumm", "durch", "dürfen",
    "eben", "ebenso", "ehe", "ein", "einander", "eine", "einem",
    "einen", "einer", "einige", "einigem", "einigen", "einiger",
    "einiges", "einmal", "er", "erst", "erste", "erstem", "ersten",
    "erster", "erstes", "es", "etwa", "etwas", "euch", "euer",
    "eure", "eurem", "euren", "eurer", "eures",
    "für",
    "ganz", "gar", "gegen", "gehen", "gemacht", "genug", "gerade",
    "gering", "gern", "gerne", "gewesen", "gewiß", "groß", "große",
    "großem", "großen", "großer", "großes", "grund", "gut", "guten",
    "guter", "gutes",
    "hab", "habe", "haben", "habt", "hast", "hat", "hatte",
    "hätte", "her", "heraus", "herein", "hier", "hin", "hinter",
    "hoch",
    "ich", "ihm", "ihn", "ihnen", "ihr", "ihre", "ihrem", "ihren",
    "ihrer", "ihres", "im", "immer", "in", "indem", "infolge",
    "innen", "ins", "irgend", "ist",
    "ja", "jahr", "jahre", "jahren", "je", "jede", "jedem",
    "jeden", "jeder", "jedes", "jedoch", "jemals", "jene", "jenem",
    "jenen", "jener", "jenes", "jetzt", "jung", "junge", "jungem",
    "jungen", "junger", "junges",
    "kam", "kann", "kannst", "kein", "keine", "keinem", "keinen",
    "keiner", "keines", "klar", "klein", "kleine", "kleinem",
    "kleinen", "kleiner", "kleines", "kommen", "konnte", "können",
    "könnte", "kurz",
    "lang", "lange", "langem", "langen", "langer", "langes",
    "längst", "längstens", "lassen", "laß", "laut", "lediglich",
    "leer", "legen", "leid", "leider", "lesen", "letzte", "letzten",
    "leute", "licht", "lieb", "lieber", "los",
    "machen", "macht", "mädchen", "mag", "magen", "manche",
    "manchem", "manchen", "mancher", "mancherlei", "manchmal", "man",
    "mehr", "mein", "meine", "meinem", "meinen", "meiner", "meines",
    "mich", "mir", "mit", "mittel", "morgen", "morgens", "müssen",
    "muß", "mußt", "musste",
    "nach", "nachdem", "nachher", "nächst", "nah", "nahe", "name",
    "natürlich", "neben", "nehmen", "nein", "neu", "neue", "neuem",
    "neuen", "neuer", "neues", "nicht", "nichts", "nie", "niemand",
    "nimmer", "nirgend", "nirgends", "noch", "nun", "nur",
    "ob", "oben", "oder", "offen", "ohne",
    "rechts", "recht", "richtig", "ruhig", "rund",
    "schlecht", "schließen", "schlimm", "schnell", "schon",
    "schön", "schreiben", "schuld", "schwer", "schwierig",
    "sehen", "sehr", "seid", "sein", "seine", "seinem", "seinen",
    "seiner", "seines", "seit", "seitdem", "selbst", "sich",
    "sicher", "sicherlich", "sie", "sind", "so", "sofort", "sogar",
    "solch", "solche", "solchem", "solchen", "solcher", "soll",
    "sollen", "sollte", "sollten", "solltest", "sondern", "sonst",
    "sorgen", "soviel", "sowie", "sprechen", "staat", "stark",
    "statt", "steht",
    "über", "überall", "überhaupt", "übrigens", "um", "ums",
    "und", "uns", "unser", "unsere", "unserem", "unseren",
    "unserer", "unseres", "unten", "unter",
    "viel", "vielleicht", "viele", "vielem", "vielen", "vielmals",
    "vier", "voll", "völlig", "vom", "von", "vor", "vorbei",
    "vorher", "vorn", "vorne",
    "wann", "warum", "was", "weder", "weil", "weit", "weiter",
    "weitere", "weiteren", "weiteres", "welch", "welche", "welchem",
    "welchen", "welcher", "welches", "wem", "wen", "wenig",
    "wenige", "wenigem", "wenigen", "weniger", "wenigstens", "wenn",
    "wer", "werde", "werden", "wessen", "wie", "wieder", "will",
    "wir", "wird", "wirklich", "wo", "wohl", "wollen", "wollt",
    "wollte", "wollten", "worden", "wurde", "würde", "würden",
    "zu", "zum", "zunächst", "zur", "zurück", "zusammen",
    "zwanzig", "zwar", "zwei", "zwischen",
]


# Grimm-spezifisches Sentiment-Lexikon
# Positiv = +1, Negativ = -1
GRIMM_SENTIMENT_LEXIKON = {
    # --- POSITIV (+1) ---
    "gut": 1, "fromm": 1, "fleißig": 1, "gehorsam": 1, "treu": 1, "ehrlich": 1,
    "klug": 1, "weise": 1, "gerecht": 1, "barmherzig": 1, "unschuldig": 1,
    "rein": 1, "sanft": 1, "geduldig": 1, "demütig": 1, "tapfer": 1, "kühn": 1,
    "beherzt": 1, "listig": 1, "schön": 1, "bildschön": 1, "wunderschön": 1,
    "hübsch": 1, "fein": 1, "zart": 1, "weiß": 1, "gold": 1, "golden": 1,
    "glänzend": 1, "strahlend": 1, "sauber": 1, "reinlich": 1, "geschmückt": 1,
    "herrlich": 1, "glück": 1, "glücklich": 1, "froh": 1, "fröhlich": 1,
    "vergnügt": 1, "freude": 1, "lust": 1, "lustig": 1, "selig": 1,
    "zufrieden": 1, "gesund": 1, "satt": 1,
    "lebendig": 1, "geliebt": 1, "reich": 1, "reichtum": 1,
    "schatz": 1, "edelstein": 1, "perle": 1, "könig": 1, "königin": 1,
    "prinz": 1, "königstochter": 1, "schloss": 1, "hochzeit": 1, "braut": 1,
    "fest": 1, "mahl": 1, "geschenk": 1, "segen": 1, "himmel": 1,
    "erlösung": 1, "gewinn": 1, "lachen": 1, "lächeln": 1, "singen": 1,
    "tanzen": 1, "springen": 1, "küssen": 1, "streicheln": 1, "trösten": 1,
    "retten": 1, "erlösen": 1, "helfen": 1, "schenken": 1, "belohnen": 1,
    "gelingen": 1, "siegen": 1, "hold": 1, "lieblich": 1, "wacker": 1,
    "stattlich": 1, "gemach": 1,

    # --- NEGATIV (-1) ---
    "böse": -1, "schlecht": -1, "gottlos": -1, "falsch": -1, "tückisch": -1,
    "faul": -1, "hochmütig": -1, "stolz": -1, "neidisch": -1, "missgünstig": -1,
    "gierig": -1, "geizig": -1, "grausam": -1, "hart": -1, "unbarmherzig": -1,
    "wild": -1, "garstig": -1, "dumm": -1, "einfältig": -1, "hässlich": -1,
    "schwarz": -1, "finster": -1, "dunkel": -1, "schmutzig": -1, "rußig": -1,
    "alt": -1, "krank": -1, "blass": -1, "widerlich": -1, "angst": -1,
    "furcht": -1, "schreck": -1, "entsetzen": -1, "bange": -1, "traurig": -1,
    "betrübt": -1, "einsam": -1, "verlassen": -1, "arm": -1, "elend": -1,
    "not": -1, "jammer": -1, "kummer": -1, "sorge": -1, "zorn": -1, "wut": -1,
    "hass": -1, "neid": -1, "schmerz": -1, "qual": -1, "pein": -1,
    "hunger": -1, "durst": -1, "müde": -1, "erschöpft": -1, "tod": -1,
    "tot": -1, "sterben": -1, "leiche": -1, "sarg": -1, "grab": -1,
    "blut": -1, "wunde": -1, "gift": -1, "giftig": -1, "strafe": -1,
    "gefängnis": -1, "kerker": -1, "fessel": -1, "hölle": -1, "teufel": -1,
    "hexe": -1, "wolf": -1, "ungeheuer": -1, "wald": -1, "weinen": -1,
    "klagen": -1, "jammern": -1, "schreien": -1, "tob": -1, "schlagen": -1,
    "stoßen": -1, "hauen": -1, "töten": -1, "umbringen": -1, "fressen": -1,
    "verschlingen": -1, "beißen": -1, "kratzen": -1, "lügen": -1,
    "betrügen": -1, "stehlen": -1, "rauben": -1, "quälen": -1, "leiden": -1,
    "fliehen": -1, "verirren": -1, "verstoßen": -1, "auslachen": -1,
    "spotten": -1, "grämen": -1, "herzeleid": -1, "drangsal": -1,
    "arg": -1, "unheil": -1, "verderben": -1,
}


# Negationswörter — drehen das Vorzeichen von Sentiment-Wörtern um
NEGATION_TRIGGERS = {
    # Standard-Negationen
    "nicht", "nichts",
    # "Kein"-Familie
    "kein", "keine", "keinen", "keinem", "keiner", "keines", "keins",
    # Zeit & Person
    "nie", "niemals", "nimmer", "nimmermehr",
    "niemand", "nirgends", "nirgendwo",
    # Konjunktionen
    "weder",
}


# ============================================================
# ANALYSE-FUNKTIONEN
# ============================================================

def berechne_sentiment(wort_liste, lexikon=None):
    """
    Berechnet den Sentiment Score einer Wortliste (ohne Negationserkennung).

    Parameter:
        wort_liste (list): Liste von Wörtern
        lexikon (dict): Sentiment-Lexikon (Standard: GRIMM_SENTIMENT_LEXIKON)

    Rückgabe:
        tuple: (score, gefundene_woerter)
    """
    if lexikon is None:
        lexikon = GRIMM_SENTIMENT_LEXIKON

    score = 0
    gefundene = []

    for wort in wort_liste:
        if wort in lexikon:
            score += lexikon[wort]
            gefundene.append(wort)

    return score, gefundene


def berechne_sentiment_mit_negation(wort_liste, lexikon=None, negationen=None):
    """
    Berechnet den Sentiment Score mit Negationserkennung.

    Wenn ein Negationswort (z.B. "nicht", "kein") innerhalb von 3 Wörtern
    VOR einem Sentiment-Wort steht, wird das Vorzeichen umgedreht.
    Beispiel: "nicht böse" → +1 statt -1

    Parameter:
        wort_liste (list): Liste von Wörtern
        lexikon (dict): Sentiment-Lexikon (Standard: GRIMM_SENTIMENT_LEXIKON)
        negationen (set): Negationswörter (Standard: NEGATION_TRIGGERS)

    Rückgabe:
        tuple: (score, details)
        details ist eine Liste von Tupeln: (wort, originalwert, negiert, endwert)
    """
    if lexikon is None:
        lexikon = GRIMM_SENTIMENT_LEXIKON
    if negationen is None:
        negationen = NEGATION_TRIGGERS

    score = 0
    details = []

    for i, wort in enumerate(wort_liste):
        if wort in lexikon:
            wert = lexikon[wort]

            # Schaue die 3 Wörter DAVOR an
            vorherige = wort_liste[max(0, i - 3):i]
            ist_negiert = any(neg in negationen for neg in vorherige)

            if ist_negiert:
                endwert = wert * -1
            else:
                endwert = wert

            score += endwert
            details.append((wort, wert, ist_negiert, endwert))

    return score, details


# ============================================================
# Kapitel 01: Variablen und Zahlentypen
# ============================================================

def pruefe_01_aufgabe_1a():
    """Aufgabe 1a: print() üben mit masse_goldkugel_kg und durchmesser_goldkugel_cm."""
    v = _hole_variablen()
    if "masse_goldkugel_kg" in v and "durchmesser_goldkugel_cm" in v:
        print("  ℹ️ Die Variablen sind vorhanden.")
        print("     Haben Sie sich die Werte mit print() ausgeben lassen?")
        print("     Die erwarteten Werte sind: masse_goldkugel_kg = 3.47, durchmesser_goldkugel_cm = 7")
    else:
        print("  ❌ Die Variablen wurden nicht gefunden. Haben Sie die Zelle darüber ausgeführt?")


def pruefe_01_aufgabe_1b():
    """Aufgabe 1b: print() üben mit masse_neu und durchmesser_neu."""
    v = _hole_variablen()
    if "masse_neu" in v and "durchmesser_neu" in v:
        print("  ✅ Gut gemacht! Die Variablen sind vorhanden.")
        print("  ℹ️ Bei dieser Aufgabe ging es darum, print() auszuprobieren.")
        print("     Vergleichen Sie Ihre Ausgabe oben mit den erwarteten Werten:")
        print("     masse_neu = 6.94, durchmesser_neu = 12")
    else:
        print("  ❌ Die Variablen wurden nicht gefunden. Haben Sie die Zelle darüber ausgeführt?")


def pruefe_01_aufgabe_2():
    """Prüft Aufgabe 2: Datentypen von x, y, z."""
    v = _hole_variablen()
    fehler = 0

    for name, erwarteter_typ, typ_name in [
        ("x", float, "Float"),
        ("y", int, "Integer"),
        ("z", str, "String"),
    ]:
        if name not in v:
            print(f"  ❌ Variable '{name}' nicht gefunden. Haben Sie x, y und z definiert?")
            fehler += 1
        elif not isinstance(v[name], erwarteter_typ):
            print(f"  ❌ '{name}' sollte ein {typ_name} sein. Prüfen Sie den zugewiesenen Wert.")
            fehler += 1

    if fehler == 0:
        print("  ✅ Richtig! Alle drei Variablen haben den erwarteten Datentyp.")


def pruefe_01_aufgabe_3():
    """Aufgabe 3: Verständnisfrage zum Dreieckstausch."""
    v = _hole_variablen()
    if "x" in v and "y" in v and "swap" in v:
        print("  ℹ️ Haben Sie erkannt, was passiert ist?")
        print("     Die drei Zeilen tauschen die Werte von x und y.")
        print("     Die Hilfsvariable 'swap' speichert den alten Wert zwischendurch.")
        print("     swap = x  #  x = 1.0 y = 3.0 swap = 1.0")
        print("     x = y     #  x = 3.0 y = 3.0 swap = 1.0")
        print("     y = swap  #  x = 3.0 y = 1.0 swap = 1.0")
        print("     Das nennt man 'Dreieckstausch'.")
    else:
        print("  ❌ Haben Sie die Zelle oben ausgeführt?")


def erklaere_01_aufgabe_4():
    """Aufgabe 4: Auflösung und Erklärung."""
    v = _hole_variablen()
    if "position" not in v:
        print("  ❌ Haben Sie die Zelle oben ausgeführt?")
        return

    print(f"  Der Wert von 'position' ist: '{v['position']}'")
    print()
    print("  ℹ️ Erklärung:")
    print("     initial = 'left'       # initial bekommt den Wert 'left'")
    print("     position = initial     # position bekommt den aktuellen Wert von initial: 'left'")
    print("     initial = 'right'      # initial wird geändert, aber position bleibt 'left'")
    print()
    print("     Python merkt sich den Wert, nicht die Verbindung zur anderen Variable.")


# ============================================================
# Kapitel 02: Strings und Booleans
# ============================================================

def pruefe_02_aufgabe_1():
    """Aufgabe 1: Erklärung der verschiedenen Slicing-Formen."""
    print("  ℹ️ Hier die Auflösung:")
    print()
    print("     title[low:]   → Beginnt beim Index 'low' und gibt den Rest aus.")
    print("     title[:high]  → Beginnt am Anfang und endet vor dem Index 'high'.")
    print("     title[:]      → Gibt die gesamte Zeichenkette aus (eine Kopie).")
    print("     title[n:-m]   → Beginnt bei Index n und endet m Zeichen vor dem Ende.")
    print()
    print("     Negative Indizes zählen vom Ende: -1 ist das letzte Zeichen,")
    print("     -2 das vorletzte, usw.")

def erklaere_02_slice_zahlen():
    """Erklärt, warum Slicing bei Zahlen nicht funktioniert."""
    print("  ℹ️ Auflösung:")
    print()
    print('     a = 123')
    print('     print(a[1])  → TypeError!')
    print()
    print("     Zahlen werden nicht als Zeichenketten gespeichert.")
    print("     Daher kann man auf einzelne Ziffern nicht per Index zugreifen.")
    print()
    print('     Aber: a = "123" macht aus der Zahl dank der Anführungszeichen einen String.')
    print('     print(a[1])  → 2')
    print()
    print("     Als String funktioniert Slicing — aber rechnen kann man")
    print("     mit dem String dann nicht mehr.")

# ============================================================
# Kapitel 03: Listen
# ============================================================

def pruefe_03_aufgabe_1():
    """Prüft Aufgabe 1: Liste figuren erstellen, Länge und erstes Element."""
    v = _hole_variablen()
    fehler = 0

    if "figuren" not in v:
        print("  ❌ Variable 'figuren' nicht gefunden. Haben Sie die Liste erstellt?")
        return

    figuren = v["figuren"]

    if not isinstance(figuren, list):
        print("  ❌ 'figuren' sollte eine Liste sein. Nutzen Sie eckige Klammern: [...]")
        return

    if len(figuren) != 3:
        print(f"  ❌ Die Liste sollte 3 Einträge haben, hat aber {len(figuren)}.")
        fehler += 1

    erwartet = ['Stiefmutter', 'Prinz', 'Ritter']
    for i, name in enumerate(erwartet):
        if i < len(figuren) and figuren[i] != name:
            print(f"  ❌ Element {i} sollte nicht '{figuren[i]}' sein. Prüfen Sie die Schreibweise.")
            fehler += 1

    if fehler == 0:
        print("  ✅ Richtig! Die Liste 'figuren' ist korrekt erstellt.")


def pruefe_03_aufgabe_2():
    """Prüft Aufgabe 2: Zahlenliste und Slicing."""
    v = _hole_variablen()

    if "numbers" not in v:
        print("  ❌ Variable 'numbers' nicht gefunden. Haben Sie die Liste erstellt?")
        return

    numbers = v["numbers"]

    if not isinstance(numbers, list):
        print("  ❌ 'numbers' sollte eine Liste sein.")
        return

    if numbers == [1, 2, 3, 4, 5, 6]:
        print("  ✅ Die Liste 'numbers' ist korrekt.")
        print("  ℹ️ Haben Sie die ersten und letzten drei Elemente per Slicing ausgegeben?")
        print("     Die ersten drei: numbers[0:3] oder numbers[:3]")
        print("     Die letzten drei: numbers[3:6] oder numbers[3:]")
    elif len(numbers) != 6:
        print(f"  ❌ Die Liste sollte 6 Elemente haben, hat aber {len(numbers)}.")
    else:
        print("  ❌ Die Werte in der Liste stimmen nicht. Erwartet: [1, 2, 3, 4, 5, 6]")


def pruefe_03_aufgabe_3():
    """Prüft Aufgabe 3: Lücken ausfüllen mit append und slice."""
    v = _hole_variablen()

    if "values" not in v:
        print("  ❌ Variable 'values' nicht gefunden. Haben Sie die Zelle ausgeführt?")
        return

    values = v["values"]

    if not isinstance(values, list):
        print("  ❌ 'values' sollte eine Liste sein.")
        return

    if values == [3, 5]:
        print("  ✅ Richtig! Die Lücken wurden korrekt ausgefüllt.")
    elif values == [1, 3, 5]:
        print("  ❌ Fast! Die erste Ausgabe stimmt, aber das Slicing am Ende fehlt noch.")
        print("     Tipp: Welches Slice ergibt [3, 5] aus [1, 3, 5]?")
    elif values == []:
        print("  ❌ Die Liste ist leer. Haben Sie die Lücken ____ schon ersetzt?")
    else:
        print(f"  ❌ Die Liste enthält: {values}")
        print("     Erwartet wird am Ende: [3, 5]")
        print("     Tipp: Nutzen Sie .append() zum Hinzufügen und [start:stop] zum Slicen.")


def erklaere_03_aufgabe_4():
    """Aufgabe 4: Erklärung negativer Indexwerte."""
    print("  ℹ️ Auflösung:")
    print()
    print("     Ein negativer Index zählt vom Ende der Liste:")
    print("     -1 ist das letzte Element, -2 das vorletzte, usw.")
    print()
    print("     resources[-1] gibt also 'Wörterbücher' aus,")
    print("     weil das der letzte Eintrag in der Liste ist.")
    print()
    print("     del resources[-1] würde das letzte Element entfernen.")
    print("     Die Liste wäre danach: ['Märchen', 'Sagen', 'wissenschaftliche Arbeiten']")

# ============================================================
# Kapitel 04: Texte einlesen und bereinigen
# ============================================================

def pruefe_04_aufgabe_1():
    """Prüft die Übung: Text einlesen, bereinigen und Wörter zählen."""
    from collections import Counter
    v = _hole_variablen()
    schritt = 0

    # Schritt 1: Text eingelesen?
    if "uebung_text" not in v:
        print("  ❌ Schritt 1: Variable 'uebung_text' nicht gefunden.")
        print("     Haben Sie den Text mit open() eingelesen und in 'uebung_text' gespeichert?")
        return

    if not isinstance(v["uebung_text"], str):
        print("  ❌ Schritt 1: 'uebung_text' sollte ein String sein.")
        return

    if len(v["uebung_text"]) < 100:
        print("  ❌ Schritt 1: 'uebung_text' scheint zu kurz. Wurde die richtige Datei eingelesen?")
        return

    print("  ✅ Schritt 1: Text erfolgreich eingelesen.")
    schritt += 1

    # Schritt 2: Kleingeschrieben?
    if "uebung_klein" not in v:
        print("  ❌ Schritt 2: Variable 'uebung_klein' nicht gefunden.")
        print("     Haben Sie den Text mit .lower() kleingeschrieben und in 'uebung_klein' gespeichert?")
        return

    if v["uebung_klein"] != v["uebung_text"].lower():
        if v["uebung_klein"] == v["uebung_text"]:
            print("  ❌ Schritt 2: Der Text ist noch nicht kleingeschrieben. Nutzen Sie .lower()")
        else:
            print("  ❌ Schritt 2: 'uebung_klein' hat nicht den erwarteten Inhalt.")
        return

    print("  ✅ Schritt 2: Text erfolgreich kleingeschrieben.")
    schritt += 1

    # Schritt 3: Satzzeichen entfernt?
    if "uebung_bereinigt" not in v:
        print("  ❌ Schritt 3: Variable 'uebung_bereinigt' nicht gefunden.")
        print("     Haben Sie die Satzzeichen entfernt und das Ergebnis in 'uebung_bereinigt' gespeichert?")
        return

    bereinigt = v["uebung_bereinigt"]
    fehlende = []
    for zeichen in [".", ",", "'", "?"]:
        if zeichen in bereinigt:
            fehlende.append(zeichen)

    if fehlende:
        print(f"  ❌ Schritt 3: Folgende Satzzeichen sind noch im Text: {fehlende}")
        print("     Nutzen Sie .replace() für jedes Satzzeichen.")
        return

    print("  ✅ Schritt 3: Satzzeichen erfolgreich entfernt.")
    schritt += 1

    # Schritt 4: In Wörter zerlegt?
    if "uebung_woerter" not in v:
        print("  ❌ Schritt 4: Variable 'uebung_woerter' nicht gefunden.")
        print("     Haben Sie den Text mit .split() in Wörter zerlegt und in 'uebung_woerter' gespeichert?")
        return

    if not isinstance(v["uebung_woerter"], list):
        print("  ❌ Schritt 4: 'uebung_woerter' sollte eine Liste sein. Nutzen Sie .split()")
        return

    if len(v["uebung_woerter"]) < 50:
        print("  ❌ Schritt 4: Die Wortliste scheint zu kurz. Wurde .split() auf den bereinigten Text angewendet?")
        return

    print("  ✅ Schritt 4: Text erfolgreich in Wörter zerlegt.")
    schritt += 1

    # Schritt 5: Wörter gezählt?
    if "uebung_haeufigkeiten" not in v:
        print("  ❌ Schritt 5: Variable 'uebung_haeufigkeiten' nicht gefunden.")
        print("     Haben Sie Counter() auf die Wortliste angewendet und in 'uebung_haeufigkeiten' gespeichert?")
        return

    if not isinstance(v["uebung_haeufigkeiten"], Counter):
        print("  ❌ Schritt 5: 'uebung_haeufigkeiten' sollte ein Counter-Objekt sein.")
        print("     Nutzen Sie: uebung_haeufigkeiten = Counter(uebung_woerter)")
        return

    print("  ✅ Schritt 5: Wörter erfolgreich gezählt.")
    schritt += 1

    # Alles geschafft!
    print()
    print(f"  🎉 Alle {schritt} Schritte erfolgreich abgeschlossen!")
    print(f"     Ihre Wortliste enthält {len(v['uebung_woerter'])} Wörter.")
    print(f"     Die 5 häufigsten: {v['uebung_haeufigkeiten'].most_common(5)}")


# ============================================================
# Kapitel 05: Text bereinigen, Schleifen, Bedingungen
# ============================================================
# Füge diesen Block in kurs_helpers.py unter dem Kapitel-05-Kommentar ein.
#
# WICHTIG: Die Funktion lade_bereinigten_text() gehört in den
# allgemeinen Hilfsfunktionen-Bereich (z.B. nach _pruefe_variable),
# da sie auch in späteren Kapiteln genutzt wird.
# ============================================================


# --- Diese Funktion in den allgemeinen Bereich einfügen ---

def lade_bereinigten_text(dateiname):
    """
    Lädt ein Märchen aus dem maerchen_texte-Ordner,
    bereinigt es (Kleinschreibung, Satzzeichen entfernen)
    und gibt den bereinigten Text und die Wortliste zurück.

    Wird in Kapitel 05+ genutzt, um den Textvorbereitungs-
    Code aus Kapitel 04 nicht wiederholen zu müssen.

    Parameter:
        dateiname (str): Name der Textdatei, z.B. '153_Die_Sternthaler.txt'

    Rückgabe:
        tuple: (bereinigter_text, wort_liste)
    """
    import os

    # Pfad relativ zum Notebook in Teil_1/ oder Teil_2/ etc.
    pfad = os.path.join('..', 'maerchen_texte', dateiname)

    with open(pfad, 'r', encoding='utf-8') as datei:
        text = datei.read()

    text_klein = text.lower()
    bereinigt = text_klein.replace(".", "").replace(",", "").replace("'", "").replace("?", "")
    wort_liste = bereinigt.split()

    return bereinigt, wort_liste


# --- Diese Funktion unter Kapitel 05 einfügen ---

def pruefe_05_aufgabe_1():
    """Prüft Aufgabe 1: Stoppwortliste mit append erstellt."""
    v = _hole_variablen()

    if "stopwords" not in v:
        print("  ❌ Variable 'stopwords' nicht gefunden.")
        print("     Haben Sie die Liste erstellt? Beginnen Sie mit: stopwords = []")
        return

    stopwords = v["stopwords"]

    if not isinstance(stopwords, list):
        print("  ❌ 'stopwords' sollte eine Liste sein. Nutzen Sie: stopwords = []")
        return

    if len(stopwords) == 0:
        print("  ❌ Die Liste ist noch leer. Fügen Sie Wörter mit stopwords.append('wort') hinzu.")
        return

    # Prüfe ob alle Einträge Strings sind
    nicht_strings = [w for w in stopwords if not isinstance(w, str)]
    if nicht_strings:
        print("  ❌ Alle Einträge sollten Zeichenketten sein (in Anführungszeichen).")
        return

    # Prüfe ob Wörter kleingeschrieben sind
    gross = [w for w in stopwords if w != w.lower()]
    if gross:
        print(f"  ⚠️ Einige Wörter sind nicht kleingeschrieben: {gross}")
        print("     Da unser Text kleingeschrieben ist, sollten auch die Stoppwörter klein sein.")

    if len(stopwords) < 5:
        print(f"  ⚠️ Sie haben {len(stopwords)} Stoppwörter. Versuchen Sie mindestens 5 hinzuzufügen.")
        print("     Typische Stoppwörter: 'und', 'oder', 'der', 'die', 'das', 'in', 'ein', ...")
    else:
        print(f"  ✅ Gut gemacht! Ihre Stoppwortliste enthält {len(stopwords)} Wörter:")
        print(f"     {stopwords}")


# ============================================================
# Kapitel 06: Abschlussprüfung Teil I
# ============================================================
# Füge diesen Block in kurs_helpers.py unter dem Kapitel-06-Kommentar ein.
#
# ⚠️ HINWEIS:
# Diese Prüffunktion ist als Selbstprüfung konzipiert.
# Noch zu entscheiden:
# - Soll die Selbstprüfung drin bleiben oder raus?
# - Soll stattdessen/zusätzlich eine Abgabe (Download + Moodle) erfolgen?
# - Falls Abgabe: Soll die Prüffunktion trotzdem als Hilfe bleiben,
#   damit Studierende vor der Abgabe selbst prüfen können?
# ============================================================

def pruefe_06_abschlusspruefung():
    """Prüft alle Schritte der Abschlussprüfung Teil I."""
    from collections import Counter
    v = _hole_variablen()
    schritte_ok = 0
    schritte_gesamt = 7

    # --- Schritt 1: Text eingelesen? ---
    if "frauholle" not in v:
        print("  ❌ Schritt 1: Variable 'frauholle' nicht gefunden.")
        print("     Lesen Sie die Datei mit open() ein.")
        return
    if not isinstance(v["frauholle"], str) or len(v["frauholle"]) < 100:
        print("  ❌ Schritt 1: 'frauholle' scheint keinen vollständigen Text zu enthalten.")
        return
    print("  ✅ Schritt 1: Text erfolgreich eingelesen.")
    schritte_ok += 1

    # --- Schritt 2: Kleingeschrieben? ---
    if "frauholle_klein" not in v:
        print("  ❌ Schritt 2: Variable 'frauholle_klein' nicht gefunden.")
        print("     Nutzen Sie .lower() und speichern Sie das Ergebnis in 'frauholle_klein'.")
        return
    if v["frauholle_klein"] != v["frauholle"].lower():
        if v["frauholle_klein"] == v["frauholle"]:
            print("  ❌ Schritt 2: Der Text ist noch nicht kleingeschrieben.")
        else:
            print("  ❌ Schritt 2: 'frauholle_klein' hat nicht den erwarteten Inhalt.")
        return
    print("  ✅ Schritt 2: Text erfolgreich kleingeschrieben.")
    schritte_ok += 1

    # --- Schritt 3: Satzzeichen entfernt? ---
    if "bereinigter_text" not in v:
        print("  ❌ Schritt 3: Variable 'bereinigter_text' nicht gefunden.")
        print("     Nutzen Sie .replace() für jedes Satzzeichen.")
        return
    fehlende = []
    for z in [".", ",", "?", "!", ":"]:
        if z in v["bereinigter_text"]:
            fehlende.append(z)
    if fehlende:
        print(f"  ❌ Schritt 3: Folgende Satzzeichen sind noch im Text: {fehlende}")
        return
    print("  ✅ Schritt 3: Satzzeichen erfolgreich entfernt.")
    schritte_ok += 1

    # --- Schritt 4: Wortliste erstellt? ---
    if "wort_liste_frauholle" not in v:
        print("  ❌ Schritt 4: Variable 'wort_liste_frauholle' nicht gefunden.")
        print("     Nutzen Sie .split() und speichern Sie das Ergebnis in 'wort_liste_frauholle'.")
        return
    if not isinstance(v["wort_liste_frauholle"], list):
        print("  ❌ Schritt 4: 'wort_liste_frauholle' sollte eine Liste sein.")
        return
    if len(v["wort_liste_frauholle"]) < 50:
        print("  ❌ Schritt 4: Die Wortliste scheint zu kurz.")
        return
    print(f"  ✅ Schritt 4: Wortliste erstellt ({len(v['wort_liste_frauholle'])} Wörter).")
    schritte_ok += 1

    # --- Schritt 5: Häufigkeiten gezählt? ---
    if "haeufigkeiten_frauholle" not in v:
        print("  ❌ Schritt 5: Variable 'haeufigkeiten_frauholle' nicht gefunden.")
        print("     Nutzen Sie Counter() aus der collections-Bibliothek.")
        return
    if not isinstance(v["haeufigkeiten_frauholle"], Counter):
        print("  ❌ Schritt 5: 'haeufigkeiten_frauholle' sollte ein Counter-Objekt sein.")
        return
    print("  ✅ Schritt 5: Wörter erfolgreich gezählt.")
    schritte_ok += 1

    # --- Schritt 6: Zahlen und Stoppwörter entfernt? ---
    # 6.1: Zahlen
    zahlen_in_liste = [w for w in v["wort_liste_frauholle"] if w.isdigit()]
    if zahlen_in_liste:
        print(f"  ⚠️ Schritt 6.1: Es sind noch Zahlen in der Wortliste: {zahlen_in_liste}")
    else:
        print("  ✅ Schritt 6.1: Zahlen erfolgreich entfernt.")

    # 6.2: Stoppwörter
    if "listeOhneStoppwoerter" not in v:
        print("  ❌ Schritt 6.2: Variable 'listeOhneStoppwoerter' nicht gefunden.")
        print("     Filtern Sie die Stoppwörter mit einer for-Schleife heraus.")
        return
    if not isinstance(v["listeOhneStoppwoerter"], list):
        print("  ❌ Schritt 6.2: 'listeOhneStoppwoerter' sollte eine Liste sein.")
        return
    if len(v["listeOhneStoppwoerter"]) >= len(v["wort_liste_frauholle"]):
        print("  ❌ Schritt 6.2: Die Liste scheint nicht kürzer geworden zu sein.")
        print("     Wurden die Stoppwörter wirklich herausgefiltert?")
        return
    print(f"  ✅ Schritt 6.2: Stoppwörter entfernt ({len(v['listeOhneStoppwoerter'])} Wörter übrig).")
    schritte_ok += 1

    # --- Schritt 7: Endergebnis? ---
    if "haeufigkeitenOhneStoppwoerter" not in v:
        print("  ❌ Schritt 7: Variable 'haeufigkeitenOhneStoppwoerter' nicht gefunden.")
        print("     Nutzen Sie Counter() auf die gefilterte Liste.")
        return
    if not isinstance(v["haeufigkeitenOhneStoppwoerter"], Counter):
        print("  ❌ Schritt 7: 'haeufigkeitenOhneStoppwoerter' sollte ein Counter-Objekt sein.")
        return
    print("  ✅ Schritt 7: Häufigkeiten ohne Stoppwörter berechnet.")
    schritte_ok += 1

    # --- Zusammenfassung ---
    print()
    if schritte_ok == schritte_gesamt:
        print(f"  🎉 Alle {schritte_gesamt} Schritte erfolgreich abgeschlossen!")
        print()
        print("  Die 10 häufigsten Wörter in 'Frau Holle' (ohne Stoppwörter):")
        for wort, anzahl in v["haeufigkeitenOhneStoppwoerter"].most_common(10):
            print(f"     {wort}: {anzahl}")
    else:
        print(f"  {schritte_ok} von {schritte_gesamt} Schritten abgeschlossen. Weiter so!")


# ============================================================
# Kapitel 07: Emotionale Wörter / Sentimentanalyse
# ============================================================
# HINWEIS: Die Prüffunktion erwartet nun:
# - score_frauholle (mit Negationserkennung berechnet)
# - gefundene_frauholle (Liste der gefundenen Wörter)
# ============================================================

def pruefe_07_aufgabe_1():
    """Prüft Aufgabe 1: Sentiment Score für Frau Holle berechnen."""
    v = _hole_variablen()

    # Score vorhanden?
    if "score_frauholle" not in v:
        print("  ❌ Variable 'score_frauholle' nicht gefunden.")
        print("     Berechnen Sie den Sentiment Score und speichern Sie ihn in 'score_frauholle'.")
        return

    if not isinstance(v["score_frauholle"], (int, float)):
        print("  ❌ 'score_frauholle' sollte eine Zahl sein.")
        return

    # Gefundene Wörter vorhanden?
    if "gefundene_frauholle" not in v:
        print("  ❌ Variable 'gefundene_frauholle' nicht gefunden.")
        print("     Speichern Sie die gefundenen emotionalen Wörter in 'gefundene_frauholle'.")
        return

    if not isinstance(v["gefundene_frauholle"], list):
        print("  ❌ 'gefundene_frauholle' sollte eine Liste sein.")
        return

    if len(v["gefundene_frauholle"]) == 0:
        print("  ❌ Es wurden keine emotionalen Wörter gefunden.")
        print("     Wurde der Text bereinigt und das Sentiment-Lexikon genutzt?")
        return

    score = v["score_frauholle"]
    woerter = v["gefundene_frauholle"]

    print(f"  ✅ Sentiment Score für 'Frau Holle' berechnet: {score}")
    print(f"     Gefundene emotionale Wörter: {len(woerter)}")
    print()

    # Aufschlüsselung
    positive = [w for w in woerter if GRIMM_SENTIMENT_LEXIKON.get(w, 0) > 0]
    negative = [w for w in woerter if GRIMM_SENTIMENT_LEXIKON.get(w, 0) < 0]
    print(f"     Positive Wörter ({len(positive)}): {positive}")
    print(f"     Negative Wörter ({len(negative)}): {negative}")
    print()

    if score > 0:
        print("     📖 Frau Holle hat eine insgesamt positive Stimmung!")
    elif score < 0:
        print("     📖 Frau Holle hat eine insgesamt negative Stimmung!")
    else:
        print("     📖 Frau Holle ist stimmungsmäßig ausgewogen — genau neutral!")


# ============================================================
# Kapitel 08: Sentimentanalyse vertiefen
# ============================================================


def pruefe_08_aufgabe_1():
    """Prüft Aufgabe 1: Sentiment Score für ein frei gewähltes Märchen."""
    v = _hole_variablen()

    # Märchenname vorhanden?
    if "maerchen_name" not in v:
        print("  ❌ Variable 'maerchen_name' nicht gefunden.")
        print("     Speichern Sie den Dateinamen in 'maerchen_name', z.B. 'Dornroeschen.txt'.")
        return

    name = v["maerchen_name"]
    if not isinstance(name, str) or name == "..." or len(name) < 3:
        print("  ❌ Bitte tragen Sie einen gültigen Dateinamen in 'maerchen_name' ein.")
        print("     Beispiel: maerchen_name = 'Dornroeschen.txt'")
        return

    # Score vorhanden?
    if "score_aufgabe" not in v:
        print(f"  ❌ Variable 'score_aufgabe' nicht gefunden.")
        print("     Berechnen Sie den Sentiment Score und speichern Sie ihn in 'score_aufgabe'.")
        return

    if not isinstance(v["score_aufgabe"], (int, float)):
        print("  ❌ 'score_aufgabe' sollte eine Zahl sein.")
        return

    # Details vorhanden?
    if "details_aufgabe" not in v:
        print("  ❌ Variable 'details_aufgabe' nicht gefunden.")
        print("     Nutzen Sie berechne_sentiment_mit_negation() und speichern Sie")
        print("     das zweite Ergebnis in 'details_aufgabe'.")
        return

    if not isinstance(v["details_aufgabe"], list):
        print("  ❌ 'details_aufgabe' sollte eine Liste sein.")
        return

    if len(v["details_aufgabe"]) == 0:
        print("  ❌ Es wurden keine emotionalen Wörter gefunden.")
        print("     Wurde der Text bereinigt und das Lexikon genutzt?")
        return

    score = v["score_aufgabe"]
    details = v["details_aufgabe"]

    # Aufschlüsselung
    positive = [(w, end) for w, orig, neg, end in details if end > 0]
    negative = [(w, end) for w, orig, neg, end in details if end < 0]
    negierte = [(w, orig, end) for w, orig, neg, end in details if neg]

    print(f"  ✅ Sentiment Score für '{name}' berechnet: {score}")
    print(f"     Gefundene emotionale Wörter: {len(details)}")
    print(f"     Davon positiv: {len(positive)}, negativ: {len(negative)}")
    print()

    if negierte:
        print(f"     Negation hat {len(negierte)} Wörter umgedreht:")
        for wort, orig, end in negierte:
            print(f"       '{wort}': {orig:+d} → {end:+d}")
        print()

    if score > 0:
        print(f"     📖 '{name}' hat eine insgesamt positive Stimmung!")
    elif score < 0:
        print(f"     📖 '{name}' hat eine insgesamt negative Stimmung!")
    else:
        print(f"     📖 '{name}' ist stimmungsmäßig ausgewogen — genau neutral!")


# ============================================================
# Kapitel 09: Visualisierung (AKTUALISIERT)
# ============================================================


def pruefe_09_aufgabe_1():
    """Prüft Aufgabe 1: Stimmungsverlauf für ein frei gewähltes Märchen."""
    v = _hole_variablen()

    if "maerchen_name_aufgabe" not in v:
        print("  ❌ Variable 'maerchen_name_aufgabe' nicht gefunden.")
        print("     Speichern Sie den Dateinamen, z.B. maerchen_name_aufgabe = 'Dornroeschen.txt'")
        return

    name = v["maerchen_name_aufgabe"]
    if not isinstance(name, str) or name == "..." or len(name) < 3:
        print("  ❌ Bitte tragen Sie einen gültigen Dateinamen in 'maerchen_name_aufgabe' ein.")
        return

    if "verlauf_aufgabe" not in v:
        print("  ❌ Variable 'verlauf_aufgabe' nicht gefunden.")
        print("     Berechnen Sie den Stimmungsverlauf und speichern Sie ihn in 'verlauf_aufgabe'.")
        return

    verlauf = v["verlauf_aufgabe"]

    if not isinstance(verlauf, list):
        print("  ❌ 'verlauf_aufgabe' sollte eine Liste sein.")
        return

    if len(verlauf) == 0:
        print("  ❌ Die Verlaufsliste ist leer.")
        print("     Wurde der Text in Abschnitte eingeteilt und der Score berechnet?")
        return

    if not all(isinstance(x, (int, float)) for x in verlauf):
        print("  ❌ Die Verlaufsliste sollte nur Zahlen enthalten.")
        return

    positive_abschnitte = sum(1 for x in verlauf if x > 0)
    negative_abschnitte = sum(1 for x in verlauf if x < 0)
    gesamt_score = sum(verlauf)

    print(f"  ✅ Stimmungsverlauf für '{name}' berechnet!")
    print(f"     Anzahl Abschnitte: {len(verlauf)}")
    print(f"     Positive Abschnitte: {positive_abschnitte}")
    print(f"     Negative Abschnitte: {negative_abschnitte}")
    print(f"     Gesamt-Score: {gesamt_score}")
    print()
    print("     ℹ️ Haben Sie auch eine Grafik erstellt? Vergleichen Sie den Verlauf")
    print("        mit Ihrem eigenen Eindruck des Märchens!")


def pruefe_09_aufgabe_2():
    """Prüft Aufgabe 2: Balkendiagramm für drei Märchen."""
    v = _hole_variablen()

    if "namen_aufgabe" not in v:
        print("  ❌ Variable 'namen_aufgabe' nicht gefunden.")
        print("     Speichern Sie die Märchennamen in einer Liste 'namen_aufgabe'.")
        return

    if "scores_aufgabe" not in v:
        print("  ❌ Variable 'scores_aufgabe' nicht gefunden.")
        print("     Speichern Sie die Scores in einer Liste 'scores_aufgabe'.")
        return

    namen = v["namen_aufgabe"]
    scores = v["scores_aufgabe"]

    if not isinstance(namen, list) or not isinstance(scores, list):
        print("  ❌ 'namen_aufgabe' und 'scores_aufgabe' sollten beide Listen sein.")
        return

    if len(namen) == 0 or len(scores) == 0:
        print("  ❌ Die Listen sind leer. Haben Sie Märchen ausgewählt und Scores berechnet?")
        return

    if len(namen) != len(scores):
        print(f"  ❌ Die Listen haben unterschiedliche Längen: {len(namen)} Namen, {len(scores)} Scores.")
        return

    if not all(isinstance(s, (int, float)) for s in scores):
        print("  ❌ 'scores_aufgabe' sollte nur Zahlen enthalten.")
        return

    print(f"  ✅ Balkendiagramm-Daten für {len(namen)} Märchen vorhanden!")
    print()
    for name, score in zip(namen, scores):
        balken = "🟢" if score > 0 else "🔴" if score < 0 else "⚪"
        print(f"     {balken} {name}: {score}")
    print()
    print("     ℹ️ Haben Sie auch ein Balkendiagramm erstellt?")


# ============================================================
# Kapitel 10: Abschlussprüfung Teil II
# ============================================================
# ⚠️ HINWEIS:
# Diese Prüffunktion ist als Selbstprüfung konzipiert.
# Gleiche Frage wie bei Kapitel 06: Selbstprüfung, Abgabe, oder beides?
# ============================================================

def pruefe_10_abschlusspruefung():
    """Prüft die Abschlussprüfung Teil II."""
    v = _hole_variablen()
    schritte_ok = 0

    # --- Aufgabe 1: Alle Scores berechnet? ---
    if "alle_namen" not in v or "alle_scores" not in v:
        print("  ❌ Aufgabe 1: 'alle_namen' und/oder 'alle_scores' nicht gefunden.")
        print("     Berechnen Sie die Scores und speichern Sie sie in diesen Listen.")
        return

    namen = v["alle_namen"]
    scores = v["alle_scores"]

    if not isinstance(namen, list) or not isinstance(scores, list):
        print("  ❌ Aufgabe 1: 'alle_namen' und 'alle_scores' sollten Listen sein.")
        return

    if len(namen) != len(scores):
        print(f"  ❌ Aufgabe 1: Unterschiedliche Anzahl: {len(namen)} Namen, {len(scores)} Scores.")
        return

    if len(namen) < 10:
        print(f"  ⚠️ Aufgabe 1: Es sollten 10 Märchen sein, Sie haben aber nur {len(namen)}.")
    else:
        print(f"  ✅ Aufgabe 1: Sentiment Scores für {len(namen)} Märchen berechnet.")
    schritte_ok += 1

    if not all(isinstance(s, (int, float)) for s in scores):
        print("  ❌ Aufgabe 1: 'alle_scores' enthält Werte, die keine Zahlen sind.")
        return

    # Ergebnisse anzeigen
    print()
    sortiert = sorted(zip(namen, scores), key=lambda x: x[1], reverse=True)
    print("     Ranking (positivstes → negativstes Märchen):")
    for i, (name, score) in enumerate(sortiert, 1):
        balken = "🟢" if score > 0 else "🔴" if score < 0 else "⚪"
        print(f"     {i:2}. {balken} {name}: {score}")
    print()

    # --- Aufgabe 3: Spannungskurve ---
    if "verlauf_pruefung" not in v:
        print("  ❌ Aufgabe 3: Variable 'verlauf_pruefung' nicht gefunden.")
        print("     Erstellen Sie eine Spannungskurve für das negativste Märchen.")
        return

    verlauf = v["verlauf_pruefung"]

    if not isinstance(verlauf, list) or len(verlauf) == 0:
        print("  ❌ Aufgabe 3: 'verlauf_pruefung' sollte eine nicht-leere Liste sein.")
        return

    if "maerchen_pruefung" not in v:
        print("  ❌ Aufgabe 3: Variable 'maerchen_pruefung' nicht gefunden.")
        return

    maerchen = v["maerchen_pruefung"]
    if not isinstance(maerchen, str) or maerchen == "...":
        print("  ❌ Aufgabe 3: Bitte tragen Sie den Namen des Märchens in 'maerchen_pruefung' ein.")
        return

    print(f"  ✅ Aufgabe 3: Spannungskurve für '{maerchen}' berechnet ({len(verlauf)} Abschnitte).")
    schritte_ok += 1

    # --- Zusammenfassung ---
    print()
    print("  " + "=" * 50)

    negativstes = sortiert[-1]
    positivstes = sortiert[0]
    print(f"  📊 Positivstes Märchen: {positivstes[0]} (Score: {positivstes[1]})")
    print(f"  📊 Negativstes Märchen: {negativstes[0]} (Score: {negativstes[1]})")
    print()
    print("  🎉 Abschlussprüfung Teil II abgeschlossen!")
    print("     Vergessen Sie nicht, Aufgabe 4 (Reflexion) zu beantworten.")