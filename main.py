import os # Importieren des os-Moduls um das aktuelle Verzeichnis zu ermitteln

# Konstanten für die Bethe-Weizsäcker-Formel
AV = 15.67
AS = 17.23
AC = 0.714
AA = 93.15

AP = 11.2 # A für Delta
delta = 0 # Wird später auf Wert in MeV gesetzt

u = 1.660538921 / 10**(27) # Atomare Masseneinheit in kg
e = 1.602176565 / 10**(19) # Elementarladung in C


def bethe_weizsacker(Z, A):
    term1 = AV * A
    term2 = AS * A**(2/3)
    term3 = AC * Z*(Z-1) / A**(1/3)
    term4 = AA * (A - 2*Z)**2 / (4*A)

    N = A - Z
    term5 = delta if N % 2 == 0 and Z % 2 == 0 else -delta if N % 2 != 0 and Z % 2 != 0 else 0

    B = term1 - term2 - term3 - term4 - term5
    return B, term1, term2, term3, term4, term5

def mass_defect(B):
    c = 299792458  # Lichtgeschwindigkeit in m/s
    delta_m = ((B * e * 10*(6)) / c*2) / u
    return delta_m

def nuclear_mass(Z, A, delta_m):
    m_p = 1.007276467  # Masse eines Protons in u
    m_n = 1.008664916  # Masse eines Neutrons in u
    M = Z*m_p + (A-Z)*m_n - delta_m
    return M


def read_isotopes():
    isotopes = []
    with open("data/isotope.csv") as f:
        first_line = f.readline()
        reader = f.readlines()
        for row in reader:
            try:
                row = row.split("\n")[0]
            except:
                pass
            isotopes.append(row.split(";"))
    return isotopes

def find_isotope(Z, A, isotopes):
    for isotope in isotopes:
        if isotope[1] == Z and isotope[3] == A:
            return isotope
    return None

def read_elements():
    elements = []
    with open("data/elements.csv") as f:
        first_line = f.readline()
        reader = f.readlines()
        for row in reader:
            try:
                row = row.split("\n")[0]
            except:
                pass
            elements.append(row.split(","))
    return elements

def find_element(symbol, elements):
    symbol = symbol.lower()
    print(symbol)
    for element in elements:
        print(element)
        print(element[2].lower())
        if element[2].lower() == symbol:
            return element
    return None


def save_file(A: int, Z: int, delta, delta_m, B, term1, term2, term3, term4, term5, M, isotope, element):
    """
    Speichert die Ergebnisse in einer Datei

    :param A: Massenzahl
    :param Z: Protonenzahl
    :param delta: Delta-Wert
    :param delta_m: Massendefekt
    :param B: Bindungsenergie
    :param term1: Term1 der Bethe-Weizsäcker-Formel
    :param term2: Term2 der Bethe-Weizsäcker-Formel
    :param term3: Term3 der Bethe-Weizsäcker-Formel
    :param term4: Term4 der Bethe-Weizsäcker-Formel
    :param term5: Term5 der Bethe-Weizsäcker-Formel
    :param M: Atomkernmasse
    :param isotope: Gefundenes Isotop
    :param element: Gefundenes Element
    """
    with open(f"{isotope[0]}.txt", "w") as f:
        f.write("-------------------------------------------------------------\n")
        f.write("Programm zur Berechnung der Bindungsenergie und Atomkernmasse\n")
        f.write("-------------------------------------------------------------\n")
        f.write(f"Elementname: {element[1]}\n")
        f.write(f"Nuclide: {isotope[1]}\n")
        f.write(f"Protonenzahl (Z): {isotope[2]}\n")
        f.write(f"Neutronenzahl: {isotope[3]}\n")
        f.write(f"Massenzahl (A): {isotope[4]}\n")
        f.write("-------------------------------------------------------------\n")
        f.write(f"Bindungsenergie: {B} MeV\n")
        f.write(f"Term1: {term1} MeV, Term2: -{term2} MeV, Term3: -{term3} MeV, Term4: -{term4} MeV, Term5: {term5} MeV\n")
        f.write(f"Massendefekt: {delta_m} u\n")
        f.write(f"Atomkernmasse: {M} u\n")
        f.write("-------------------------------------------------------------\n")
        f.write("Ergebnisse wurden gespeichert")

    print("Ergebnisse wurden gespeichert")


isotopes = read_isotopes() # Einlesen der Isotope aus data/isotopes.csv

elements = read_elements() # Einlesen der Elemente aus data/elements.csv

running = True
while running:
    os.system("cls" if os.name == "nt" else "clear") # Löschen des Konsoleninhalts

    # Kleine Hilfestellung
    print("-------------------------------------------------------------")
    print("Programm zur Berechnung der Bindungsenergie und Atomkernmasse")
    print("-------------------------------------------------------------")
    print("Drücken Sie Enter ohne Eingabe um das Programm zu beenden\n")


    # Eingabe von A und Z
    try:
        A = int(input("Geben Sie die Massenzahl (A) ein: "))
        Z = int(input("Geben Sie die Protonenzahl (Z) ein: "))

    except ValueError: # Wenn keine Zahl eingegeben wird -> Kleine Hilfestellung :)
        print("Programm wird beendet")
        break


    # Suche nach Isotop in data/isotopes.csv
    isotope = find_isotope(str(Z),str(A), isotopes)
    if isotope == None:
        print("Isotop nicht gefunden. Programm wird beendet.")
        break

    element = find_element(isotope[0].split("-")[0], elements)

    if isotope:
        print("\nGefundenes Isotop:")
        print("-------------------------------------------------------------")
        print(f"Elementname: {element[1]}")
        print(f"Nuclide: {isotope[1]}")
        print(f"Protonenzahl (Z): {isotope[2]}")
        print(f"Neutronenzahl: {isotope[3]}")
        print(f"Massenzahl (A): {isotope[4]}")
        print("-------------------------------------------------------------\n")


    delta = AP*A**(-1/2) # Berechnung von delta

    B, term1, term2, term3, term4, term5 = bethe_weizsacker(Z, A)
    print(f"Bindungsenergie: {B} MeV")
    print(f"Term1: {term1} MeV, Term2: -{term2} MeV, Term3: -{term3} MeV, Term4: -{term4} MeV, Term5: {term5} MeV")

    delta_m = mass_defect(B)
    print(f"Massendefekt: {delta_m} u")

    M = nuclear_mass(Z, A, delta_m)
    print(f"Atomkernmasse: {M} u")
    print("-------------------------------------------------------------\n")

    running = input("Weitere Berechnung? (j/n)  - (s zum speichern der Ergebnisse in z.B. He-5.txt im aktuellen Ordner)")

    if running.lower() == "s":
        # Wenn "s" eingegeben wird, werden die Ergebnisse in einer Datei gespeichert
        save_file(A, Z, delta, delta_m, B, term1, term2, term3, term4, term5, M, isotope, element)

    elif running.lower() == "j":
        # Wenn "j" eingegeben wird, wird die Schleife erneut durchlaufen
        running = True # Eigentlich unnötig, da running bereits True ist

    else:
        # Wenn etwas anderes als "j" eingegeben wird, wird die Schleife beendet
        running = False

