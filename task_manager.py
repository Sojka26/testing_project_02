import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    """
    Připojení k databázi MySQL.

    Vrací:
        conn: Objekt připojení k databázi, pokud je připojení úspěšné.
        None: Pokud dojde k chybě při připojení.
    """
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin123',
            database='task_manager'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print("Chyba při připojení k databázi:", e)
        return None

def vytvoreni_tabulky():
    """
    Vytvoří tabulku `ukoly` v databázi, pokud neexistuje.
    """
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()

def pridat_ukol(nazev, popis):
    """
    Přidá nový úkol do databáze.

    Parametry:
        nazev (str): Název úkolu.
        popis (str): Popis úkolu.

    Vrací:
        True: Pokud byl úkol úspěšně přidán.
        None: Pokud došlo k chybě nebo jsou vstupy neplatné.
    """
    if not nazev or not popis:
        print("Název a popis nesmí být prázdné.")
        return None
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        conn.commit()
        cursor.close()
        conn.close()
        print(" Úkol přidán.")
        return True
    return None

def pridat_ukol_a_vrat_id(nazev, popis):
    """
    Přidá nový úkol do databáze a vrátí jeho ID.

    Parametry:
        nazev (str): Název úkolu.
        popis (str): Popis úkolu.

    Vrací:
        int: ID nově přidaného úkolu.
        None: Pokud došlo k chybě nebo jsou vstupy neplatné.
    """
    if not nazev or not popis:
        return None
    
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
    return None

def zobrazit_ukoly():
    """
    Zobrazí všechny aktivní úkoly (stav 'Nezahájeno' nebo 'Probíhá').
    """
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('Nezahájeno', 'Probíhá')")
        ukoly = cursor.fetchall()
        if not ukoly:
            print(" Seznam úkolů je prázdný.")
        else:
            print("\n Aktivní úkoly:")
            for u in ukoly:
                print(f"ID: {u[0]}, Název: {u[1]}, Popis: {u[2]}, Stav: {u[3]}")
        cursor.close()
        conn.close()

def aktualizovat_ukol(id_ukolu, novy_stav):
    """
    Aktualizuje stav úkolu podle jeho ID.

    Parametry:
        id_ukolu (int): ID úkolu, který má být aktualizován.
        novy_stav (str): Nový stav úkolu ('Probíhá' nebo 'Hotovo').

    Vrací:
        None
    """
    if novy_stav not in ['Probíhá', 'Hotovo']:
        print(" Neplatný stav.")
        return
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        if cursor.fetchone() is None:
            print(" Úkol s tímto ID neexistuje.")
        else:
            cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
            conn.commit()
            print(" Stav úkolu aktualizován.")
        cursor.close()
        conn.close()

def odstranit_ukol(id_ukolu):
    """
    Odstraní úkol z databáze podle jeho ID.

    Parametry:
        id_ukolu (int): ID úkolu, který má být odstraněn.

    Vrací:
        None
    """
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
        conn.commit()
        if cursor.rowcount == 0:
            print(" Úkol s tímto ID neexistuje.")
        else:
            print(" Úkol odstraněn.")
        cursor.close()
        conn.close()

def hlavni_menu():
    """
    Hlavní menu aplikace pro správu úkolů.
    Umožňuje uživateli přidávat, zobrazovat, aktualizovat a odstraňovat úkoly.
    """
    vytvoreni_tabulky()
    while True:
        print("\n --- SPRÁVCE ÚKOLŮ ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        volba = input("Zadejte číslo volby: ")

        if volba == '1':
            nazev = input("Zadejte název úkolu: ").strip()
            popis = input("Zadejte popis úkolu: ").strip()
            pridat_ukol(nazev, popis)

        elif volba == '2':
            zobrazit_ukoly()

        elif volba == '3':
            try:
                id_ukolu = int(input("Zadejte ID úkolu: "))
                print("1 = Probíhá, 2 = Hotovo")
                stav_volba = input("Zadejte nový stav (1/2): ")
                if stav_volba == '1':
                    aktualizovat_ukol(id_ukolu, 'Probíhá')
                elif stav_volba == '2':
                    aktualizovat_ukol(id_ukolu, 'Hotovo')
                else:
                    print("❌ Neplatná volba stavu.")
            except ValueError:
                print("❌ Neplatné ID.")

        elif volba == '4':
            try:
                id_ukolu = int(input("Zadejte ID úkolu k odstranění: "))
                odstranit_ukol(id_ukolu)
            except ValueError:
                print("❌ Neplatné ID.")

        elif volba == '5':
            print(" Ukončuji program.")
            break

        else:
            print(" Neplatná volba.")

# Automatické spuštění hlavního menu
if __name__ == "__main__":
    hlavni_menu()