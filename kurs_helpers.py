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
# Kapitel 03: Listen (TODO)
# ============================================================


# ============================================================
# Kapitel 04: Texte einlesen und bereinigen (TODO)
# ============================================================

# Hier kommen später:
# - lade_maerchen(dateiname) — lädt und bereinigt ein Märchen
# - pruefe_04_aufgabe_X() — Prüffunktionen für Kapitel 04


# ============================================================
# Kapitel 05: Text bereinigen, Schleifen, Bedingungen (TODO)
# ============================================================


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