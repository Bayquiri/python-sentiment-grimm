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
# Kapitel 06: Abschlussprüfung Teil I (TODO)
# ============================================================


# ============================================================
# Kapitel 07: Emotionale Wörter / Sentimentanalyse (TODO)
# ============================================================

# Hier kommen später:
# - STOPPWOERTER = [...]
# - POSITIVE_WOERTER = [...]
# - NEGATIVE_WOERTER = [...]


# ============================================================
# Kapitel 08: Abschlussprüfung Teil II (TODO)
# ============================================================


# ============================================================
# Kapitel 09: Visualisierung (TODO)
# ============================================================