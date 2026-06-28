import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Verkauf = r"verkauf.csv"


def Aufgabe1():
    print("###Daten Laden & erkunden###")
    try:
        Verkaufsbericht1 = pd.read_csv(Verkauf, nrows=5, encoding='utf-8-sig')
        print(Verkaufsbericht1)
        fehlend = Verkaufsbericht1[Verkaufsbericht1.isna().any(axis=1)]
        print("\nZeilen mit fehlenden Werten:")
        print(fehlend)
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {Verkauf}")
    except Exception as e:
        print(f"Fehler: {type(e).__name__}: {e}")


def Aufgabe2():
    print("###Neue Spalte berechnen###")
    try:
        df = pd.read_csv(Verkauf, encoding='utf-8-sig', on_bad_lines='skip', sep=None, engine='python')
        df.columns = df.columns.str.strip()
        df['Umsatz'] = df['Menge'] * df['Preis']
        print("Neue Spalte 'Umsatz' wurde erfolgreich hinzugefügt.")
        df.to_csv(Verkauf, index=False, encoding='utf-8-sig')
        print("Daten gespeichert.")
        print(df)
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {Verkauf}")
    except PermissionError:
        print(f"Keine Berechtigung: {Verkauf}")
    except Exception as e:
        print(f"Fehler: {type(e).__name__}: {e}")

def Aufgabe3():
    print("###Einfache Statistik###")
    try:
        df = pd.read_csv(Verkauf, encoding='utf-8-sig', on_bad_lines='skip', sep=None, engine='python')
        df.columns = df.columns.str.strip()
        df["Menge"] = pd.to_numeric(df["Menge"], errors='coerce')
        df["Preis"] = pd.to_numeric(df["Preis"], errors='coerce')
        df["Umsatz"] = df["Menge"] * df["Preis"]

        Gesamtumsatz = df["Umsatz"].sum()
        DurchschnittlicherUmsatz = round(df["Umsatz"].mean(), 2)
        EinzigartigeProdukte = df["Produkt"].nunique()

        print(f"Gesamtumsatz:               {Gesamtumsatz:,.2f} €")
        print(f"Durchschnittlicher Umsatz:  {DurchschnittlicherUmsatz:,.2f} €")
        print(f"Einzigartige Produkte:      {EinzigartigeProdukte}")
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {Verkauf}")
    except Exception as e:
        print(f"Fehler: {type(e).__name__}: {e}")


def Aufgabe4():
    print("###Gruppenanalyse###")

    try:
        df = pd.read_csv(Verkauf, encoding='utf-8-sig', on_bad_lines='skip', sep=None, engine='python')
        df.columns = df.columns.str.strip()
        df["Menge"] = pd.to_numeric(df["Menge"], errors='coerce')
        df["Preis"] = pd.to_numeric(df["Preis"], errors='coerce')
        df["Umsatz"] = df["Menge"] * df["Preis"]

        ProduktMitDemHoestenUmsatz = df.groupby("Produkt")["Umsatz"].sum().idxmax()
        KategorieMitDenMeistenVerkaeufen = df.groupby("Kategorie")["Menge"].sum().idxmax()
        UmsatzProKategorie = df.groupby("Kategorie")["Umsatz"].sum()
        UmsatzFormatiert = UmsatzProKategorie.map(lambda x: f"{x:,.2f} €")

        print(f"Produkt mit dem höchsten Gesamtumsatz:  {ProduktMitDemHoestenUmsatz}")
        print(f"Kategorie mit den meisten Verkäufen:    {KategorieMitDenMeistenVerkaeufen}")
        print(f"Umsatz pro Kategorie:                   {UmsatzFormatiert.to_string()}")
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {Verkauf}")
    except Exception as e:
        print(f"Fehler: {type(e).__name__}: {e}")


def Aufgabe5():
    print("###Zeitanalyse###")

    try:
        df = pd.read_csv(Verkauf, encoding='utf-8-sig', on_bad_lines='skip', sep=None, engine='python', dayfirst=True)
        df.columns = df.columns.str.strip()

        df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")
        df["Monat"] = df["Datum"].dt.month

        print(df["Monat"])

        UmsatzProMonat = df.groupby("Monat")["Umsatz"].sum()
        UmsatzProMonatFormatiert = UmsatzProMonat.map(lambda x: f"{x:,.2f} €")
        WannWurdeAmMeistenVerkauftMonat = df.groupby("Monat")["Umsatz"].sum().idxmax()
        WannWurdeAmMeistenVerkauftMonatFormatiert = WannWurdeAmMeistenVerkauftMonat.map(lambda x: f"{x:,.2f} €")

        print(f"Umsatz Pro Monat: {UmsatzProMonatFormatiert}")
        print(f"Monat mit dem Höhsten Umsatz: {WannWurdeAmMeistenVerkauftMonatFormatiert}")


    except Exception as e:
        print(f"Fehler: {type(e).__name__}: {e}")


def Aufgabe6():
    print("###Visualisierungen###")
    try:
        df = pd.read_csv(Verkauf, encoding='utf-8-sig', on_bad_lines='skip', sep=None, engine='python')
        df.columns = df.columns.str.strip()

        ### Datum
        df["Datum"] = pd.to_datetime(df["Datum"], dayfirst=True, errors="coerce")
        df["Monat"] = df["Datum"].dt.month

        UmsatzProProdukt = df.groupby("Produkt")["Umsatz"].sum().sort_values()
        UmsatzProMonat   = df.groupby("Monat")["Umsatz"].sum().sort_index()
        UmsatzProKategorie = df.groupby("Kategorie")["Umsatz"].sum().sort_values()

        figure, axes = plt.subplots(1, 3, figsize=(12, 5))

        axes[0].bar(UmsatzProProdukt.index, UmsatzProProdukt.values)
        axes[0].set_title("Umsatz pro Produkt")
        axes[0].set_ylabel("Umsatz (€)")
        axes[0].tick_params(axis='x', rotation=45)

        axes[1].plot(UmsatzProMonat.index ,UmsatzProMonat.values, marker="o")
        axes[1].set_title("Monatlicher Umsatz im Verlauf")
        axes[1].set_ylabel("Umsatz (€)")
        axes[1].set_xlabel("Monat")
        axes[1].set_xticks(UmsatzProMonat.index)

        axes[2].pie(UmsatzProKategorie.values,
                    labels=UmsatzProKategorie.index,
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=90
                    )
        axes[2].set_title("Umsatz pro Kategorie (% - Anteilig)")

        figure.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Datei nicht gefunden: {Verkauf}")
    except Exception as e:
        print(f"Fehler: {type(e).__name__}: {e}")




# -------------------------------------------
# Hauptmenu
# -------------------------------------------

aufgaben = {
    1: Aufgabe1,
    2: Aufgabe2,
    3: Aufgabe3,
    4: Aufgabe4,
    5: Aufgabe5,
    6: Aufgabe6,
}


def Hauptmenu():
    print("\n###Hauptmenu###")
    print("1. Aufgabe 1: Daten einlesen und fehlende Werte anzeigen")
    print("2. Aufgabe 2: Neue Spalte 'Umsatz' hinzufügen und speichern")
    print("3. Aufgabe 3: Einfache Statistik berechnen")
    print("4. Aufgabe 4: Gruppenanalyse")
    print("5. Aufgabe 5: Zeitanalyse")
    print("6. Aufgabe 6: Visualisierungen")
    try:
        auswahl = int(input("Bitte wählen Sie eine Aufgabe (1-6): "))
        if auswahl in aufgaben:
            aufgaben[auswahl]()
        else:
            print("Ungültige Auswahl. Bitte wählen Sie eine Zahl zwischen 1 und 6.")
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")


if __name__ == "__main__":
    while True:
        Hauptmenu()


