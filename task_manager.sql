
-- Vytvoření databáze
CREATE DATABASE IF NOT EXISTS task_manager
CHARACTER SET utf8mb4
COLLATE utf8mb4_czech_ci;

-- Použití databáze
USE task_manager;

-- Vytvoření tabulky ukoly
CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT NOT NULL,
    stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
    datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
);
