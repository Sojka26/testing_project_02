import pytest
from task_manager import (
    pripojeni_db,
    vytvoreni_tabulky,
    pridat_ukol,
    pridat_ukol_a_vrat_id,
    aktualizovat_ukol,
    odstranit_ukol
)

@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Příprava databázové tabulky před spuštěním testů.
    Zajišťuje, že tabulka `ukoly` existuje v databázi.
    """
    vytvoreni_tabulky()

def test_pridat_ukol():
    """
    Test přidání úkolu do databáze.
    Ověřuje, že úkol byl úspěšně přidán, a poté jej odstraní.
    """
    pridat_ukol("Test Úkol", "Testovací popis")
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Test Úkol'")
    result = cursor.fetchone()
    assert result is not None
    cursor.execute("DELETE FROM ukoly WHERE nazev = 'Test Úkol'")
    conn.commit()
    cursor.close()
    conn.close()

def test_pridat_ukol_prazdny():
    """
    Test přidání úkolu s prázdnými poli.
    Ověřuje, že funkce vrátí `None` pro neplatný vstup.
    """
    result = pridat_ukol("", "")
    assert result is None

def test_aktualizovat_ukol():
    """
    Test aktualizace stavu existujícího úkolu.
    Ověřuje, že stav je aktualizován na 'Hotovo', a poté úkol odstraní.
    """
    id_ukolu = pridat_ukol_a_vrat_id("Aktualizuj mě", "Popis")
    assert id_ukolu is not None
    aktualizovat_ukol(id_ukolu, "Hotovo")
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (id_ukolu,))
    result = cursor.fetchone()
    assert result is not None and result[0] == "Hotovo"
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
    conn.commit()
    cursor.close()
    conn.close()

def test_aktualizovat_neexistujici():
    """
    Test aktualizace neexistujícího úkolu.
    Ověřuje, že funkce správně zpracuje neplatné ID úkolu.
    """
    aktualizovat_ukol(-1, "Hotovo")

def test_odstranit_ukol():
    """
    Test odstranění existujícího úkolu.
    Ověřuje, že úkol je úspěšně odstraněn z databáze.
    """
    id_ukolu = pridat_ukol_a_vrat_id("Smazat mě", "Popis")
    assert id_ukolu is not None
    odstranit_ukol(id_ukolu)
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
    result = cursor.fetchone()
    print("DEBUG:", result)
    assert result is None
    cursor.close()
    conn.close()

def test_odstranit_neexistujici():
    """
    Test odstranění neexistujícího úkolu.
    Ověřuje, že funkce správně zpracuje neplatné ID úkolu.
    """
    odstranit_ukol(-1)