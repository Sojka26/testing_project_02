# testing_project_02
# Projekt: Vylepšený Task Manager

## Popis
Tento projekt je vylepšený správce úkolů, který umožňuje:
- Přidávat, zobrazovat, aktualizovat a mazat úkoly (CRUD)
- Úkoly se ukládají do MySQL databáze
- Testování funkcionality pomocí `pytest`
- Použití MySQL Workbench pro správu databáze

## Databáze
Databáze se jmenuje `task_manager` a obsahuje tabulku `ukoly` se sloupci:
- `id` (INT, primární klíč)
- `nazev` (VARCHAR, povinný)
- `popis` (TEXT, povinný)
- `stav` (ENUM: 'Nezahájeno', 'Probíhá', 'Hotovo')
- `datum_vytvoreni` (DATETIME, automaticky generovaný)

SQL skript: `task_manager.sql`

## Spuštění aplikace
```bash
python task_manager.py
```

## Spuštění testů
```bash
pytest test_task_manager.py
```

## Požadavky
- Python 3.8+
- Balíček `mysql-connector-python`
- MySQL server (např. XAMPP, WAMP, samostatná instalace)

Instalace požadovaného balíčku:
```bash
pip install mysql-connector-python pytest
```

## Autor
Tvůj tým / jméno

## Poznámka
Před prvním použitím spusť SQL skript `task_manager.sql`, např. v MySQL Workbench.
