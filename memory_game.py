import random
import os
import json
import unittest

# SISTEM DE SCOR 

FISIER_SCORURI = "scoruri_nume.txt"

def salveaza_scor(nume, scor_nou):
    if scor_nou <= 0:
        return
    nume = nume.replace(",", "").strip()
    if not nume:
        nume = "Anonim"
    scoruri = citeste_scoruri()
    scoruri.append((nume, scor_nou))
    scoruri.sort(key=lambda x: x[1], reverse=True)
    scoruri = scoruri[:5]
    try:
        with open(FISIER_SCORURI, "w", encoding="utf-8") as f:
            for intrare in scoruri:
                f.write(f"{intrare[0]},{intrare[1]}\n")
    except Exception as e:
        print(f"Eroare salvare scor: {e}")

def citeste_scoruri():
    if not os.path.exists(FISIER_SCORURI):
        return []
    lista_scoruri = []
    try:
        with open(FISIER_SCORURI, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 2 and parts[1].isdigit():
                    lista_scoruri.append((parts[0], int(parts[1])))
    except:
        return []
    return lista_scoruri


# LOGICA DE BAZĂ: TABLĂ, AMESTECARE ȘI REGULI DE POTRIVIRE

class CardModel:
    def __init__(self, id_unic, valoare):
        self.id_unic = id_unic
        self.valoare = valoare
        self.este_vizibil = False
        self.este_potrivit = False


class MemoryGameBackend:
    def __init__(self, total_simboluri=8):
        self.total_simboluri = total_simboluri
        self.cards = []
        self.prima_carte_selectata = None
        self.a_doua_carte_selectata = None
        self.mutari = 0
        self.perechi_gasite = 0
        self.initializeaza_tabla()

    def initializeaza_tabla(self):
        valori = list(range(1, self.total_simboluri + 1)) * 2
        random.shuffle(valori)
        
        self.cards = []
        for idx, val in enumerate(valori):
            self.cards.append(CardModel(id_unic=idx, valoare=val))
        
        self.prima_carte_selectata = None
        self.a_doua_carte_selectata = None
        self.mutari = 0
        self.perechi_gasite = 0

    def selecteaza_carte(self, id_unic):
        carte = next((c for c in self.cards if c.id_unic == id_unic), None)
        if not carte or carte.este_vizibil or carte.este_potrivit:
            return "INVALID"
        
        carte.este_vizibil = True
        if self.prima_carte_selectata is None:
            self.prima_carte_selectata = carte
            return "PRIMA_CARTE"
        elif self.a_doua_carte_selectata is None:
            self.a_doua_carte_selectata = carte
            self.mutari += 1
            return "VERIFICA_PERECHE"
        return "INVALID"

    def verifica_potrivire(self):
        if not self.prima_carte_selectata or not self.a_doua_carte_selectata:
            return None

        if self.prima_carte_selectata.valoare == self.a_doua_carte_selectata.valoare:
            self.prima_carte_selectata.este_potrivit = True
            self.a_doua_carte_selectata.este_potrivit = True
            self.perechi_gasite += 1
            match_gasit = True
        else:
            self.prima_carte_selectata.este_vizibil = False
            self.a_doua_carte_selectata.este_vizibil = False
            match_gasit = False

        self.prima_carte_selectata = None
        self.a_doua_carte_selectata = None
        return match_gasit

    def este_jocul_terminat(self):
        return self.perechi_gasite == self.total_simboluri


# TESTE AUTOMATE

class TestMemoryGameBackend(unittest.TestCase):
    def setUp(self):
        self.game = MemoryGameBackend(total_simboluri=4)

    def test_initializare_si_amestecare(self):
        self.assertEqual(len(self.game.cards), 8)
        self.assertFalse(self.game.este_jocul_terminat())

    def test_selectie_si_potrivire(self):
        c1 = self.game.cards[0]
        c2 = next(c for c in self.game.cards if c.valoare == c1.valoare and c.id_unic != c1.id_unic)
        
        self.game.selecteaza_carte(c1.id_unic)
        self.game.selecteaza_carte(c2.id_unic)
        match = self.game.verifica_potrivire()
        
        self.assertTrue(match)
        self.assertTrue(c1.este_potrivit)
        self.assertTrue(c2.este_potrivit)


if __name__ == "__main__":
    unittest.main()
