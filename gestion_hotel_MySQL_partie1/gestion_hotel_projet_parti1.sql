-- Supprimer la base de données si elle existe déjà pour repartir à zéro
DROP DATABASE IF EXISTS gestion_hotel_projet;
CREATE DATABASE gestion_hotel_projet;
USE gestion_hotel_projet;

-- Table Hotel
CREATE TABLE Hotel (
    Id_Hotel INT AUTO_INCREMENT PRIMARY KEY,
    Ville VARCHAR(255) NOT NULL,
    Pays VARCHAR(255) NOT NULL,
    Code_postal VARCHAR(10) -- Numérique dans MCD, mais code postal peut avoir des lettres ou commencer par 0
);

-- Table Type_Chambre
CREATE TABLE Type_Chambre (
    Id_Type INT AUTO_INCREMENT PRIMARY KEY,
    Type VARCHAR(100) NOT NULL,
    Tarif DECIMAL(10, 2) NOT NULL
);

-- Table Chambre
CREATE TABLE Chambre (
    Id_Chambre INT AUTO_INCREMENT PRIMARY KEY,
    Numero_chambre INT NOT NULL, -- Ajout d'un numéro de chambre, pas explicitement dans MCD mais logique
    Etage INT,
    Fumeurs BOOLEAN DEFAULT FALSE, -- Interprété comme booléen
    Id_Hotel INT,
    Id_Type INT,
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel) ON DELETE CASCADE,
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type) ON DELETE SET NULL,
    UNIQUE (Id_Hotel, Numero_chambre) -- Un numéro de chambre est unique au sein d'un hôtel
);

-- Table Client
CREATE TABLE Client (
    Id_Client INT AUTO_INCREMENT PRIMARY KEY,
    Adresse VARCHAR(255),
    Ville VARCHAR(255),
    Code_postal VARCHAR(10),
    Email VARCHAR(255) UNIQUE,
    Numero_telephone VARCHAR(20),
    Nom_complet VARCHAR(255) NOT NULL
);

-- Table Reservation
CREATE TABLE Reservation (
    Id_Reservation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivee DATE NOT NULL,
    Date_depart DATE NOT NULL,
    Id_Client INT,
    Id_Chambre INT,
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client) ON DELETE CASCADE,
    FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre) ON DELETE CASCADE,
    CONSTRAINT chk_dates CHECK (Date_depart > Date_arrivee)
);

-- Table Prestation
CREATE TABLE Prestation (
    Id_Prestation INT AUTO_INCREMENT PRIMARY KEY,
    Nom_prestation VARCHAR(255) NOT NULL, -- Renommé pour clarté, "Prestation" est le nom de la table
    Prix DECIMAL(10, 2) NOT NULL
);

-- Table Offre (Table de jointure pour Hotel et Prestation - relation N-N)
CREATE TABLE Offre (
    Id_Hotel INT,
    Id_Prestation INT,
    PRIMARY KEY (Id_Hotel, Id_Prestation),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel) ON DELETE CASCADE,
    FOREIGN KEY (Id_Prestation) REFERENCES Prestation(Id_Prestation) ON DELETE CASCADE
);

-- Table Evaluation
CREATE TABLE Evaluation (
    Id_Evaluation INT AUTO_INCREMENT PRIMARY KEY,
    Date_evaluation DATE NOT NULL, -- MCD a Date d'arrivée, mais Date_evaluation est plus logique
    La_note INT CHECK (La_note >= 1 AND La_note <= 5), -- Supposons une note sur 5
    Texte_descriptif TEXT,
    Id_Reservation INT UNIQUE, -- Une réservation a au plus une évaluation
    FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation) ON DELETE CASCADE
);


-- 2)

USE gestion_hotel_projet;

-- Hotel
INSERT INTO Hotel (Id_Hotel, Ville, Pays, Code_postal) VALUES
(1, 'Paris', 'France', '75001'),
(2, 'Lyon', 'France', '69002');

-- Type_Chambre
INSERT INTO Type_Chambre (Id_Type, Type, Tarif) VALUES
(1, 'Simple', 80.00),
(2, 'Double', 120.00);

-- Chambre (Id_Chambre, Numero_chambre, Etage, Fumeurs, Id_Type, Id_Hotel)
-- La donnée originale: (1, 201, 2, 0, 1, 1) -> Id_Chambre est auto-incrémenté
-- Numero_chambre, Etage, Fumeurs (0=false, 1=true), Id_Type, Id_Hotel
INSERT INTO Chambre (Numero_chambre, Etage, Fumeurs, Id_Type, Id_Hotel) VALUES
(201, 2, FALSE, 1, 1), -- ID auto: 1
(502, 5, TRUE,  1, 2), -- ID auto: 2
(305, 3, FALSE, 2, 1), -- ID auto: 3
(410, 4, FALSE, 2, 2), -- ID auto: 4
(104, 1, TRUE,  2, 2), -- ID auto: 5
(202, 2, FALSE, 1, 1), -- ID auto: 6
(307, 3, TRUE,  1, 2), -- ID auto: 7
(101, 1, FALSE, 1, 1); -- ID auto: 8

-- Client (Id_Client, Adresse, Ville, Code_postal, Email, Numero_telephone, Nom_complet)
INSERT INTO Client (Id_Client, Adresse, Ville, Code_postal, Email, Numero_telephone, Nom_complet) VALUES
(1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
(2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
(3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
(4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
(5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud');

-- Prestation (Id_Prestation, Nom_prestation, Prix)
INSERT INTO Prestation (Id_Prestation, Nom_prestation, Prix) VALUES
(1, 'Petit-déjeuner', 15.00),
(2, 'Navette aéroport', 30.00),
(3, 'Wi-Fi gratuit', 0.00),
(4, 'Spa et bien-être', 50.00),
(5, 'Parking sécurisé', 20.00);

-- Offre (Id_Hotel, Id_Prestation) - Données inventées car non fournies
INSERT INTO Offre (Id_Hotel, Id_Prestation) VALUES
(1, 1), -- Hotel Paris offre Petit-déjeuner
(1, 3), -- Hotel Paris offre Wi-Fi gratuit
(1, 5), -- Hotel Paris offre Parking sécurisé
(2, 1), -- Hotel Lyon offre Petit-déjeuner
(2, 2), -- Hotel Lyon offre Navette aéroport
(2, 3), -- Hotel Lyon offre Wi-Fi gratuit
(2, 4); -- Hotel Lyon offre Spa

-- Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client)
-- L'Id_Chambre sera ajouté manuellement pour l'exemple, car non spécifié directement dans les données de réservation fournies.
-- Disons que les réservations sont pour des chambres spécifiques.
-- Client 1 (Jean Dupont)
INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client, Id_Chambre) VALUES
(1, '2025-06-15', '2025-06-18', 1, 1); -- Jean Dupont, Chambre 201 à Paris (Id_Chambre=1)
-- Client 2 (Marie Leroy)
INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client, Id_Chambre) VALUES
(2, '2025-07-01', '2025-07-05', 2, 2), -- Marie Leroy, Chambre 502 à Lyon (Id_Chambre=2)
(7, '2025-11-12', '2025-11-14', 2, 7), -- Marie Leroy, Chambre 307 à Lyon (Id_Chambre=7)
(10, '2026-02-01', '2026-02-05', 2, 4); -- Marie Leroy, Chambre 410 à Lyon (Id_Chambre=4)
-- Client 3 (Paul Moreau)
INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client, Id_Chambre) VALUES
(3, '2025-08-10', '2025-08-14', 3, 3); -- Paul Moreau, Chambre 305 à Paris (Id_Chambre=3)
-- Client 4 (Lucie Martin)
INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client, Id_Chambre) VALUES
(4, '2025-09-05', '2025-09-07', 4, 6), -- Lucie Martin, Chambre 202 à Paris (Id_Chambre=6)
(9, '2026-01-15', '2026-01-18', 4, 8); -- Lucie Martin, Chambre 101 à Paris (Id_Chambre=8)
-- Client 5 (Emma Giraud)
INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client, Id_Chambre) VALUES
(5, '2025-09-20', '2025-09-25', 5, 5); -- Emma Giraud, Chambre 104 à Lyon (Id_Chambre=5)


-- Evaluation (Id_Evaluation, Date_evaluation, La_note, Texte_descriptif, Id_Reservation)
INSERT INTO Evaluation (Id_Evaluation, Date_evaluation, La_note, Texte_descriptif, Id_Reservation) VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5);


-- 3)

-- a)
SELECT R.Id_Reservation, C.Nom_complet AS Nom_Client, H.Ville AS Ville_Hotel, R.Date_arrivee, R.Date_depart
FROM Reservation R
JOIN Client C ON R.Id_Client = C.Id_Client
JOIN Chambre CH ON R.Id_Chambre = CH.Id_Chambre
JOIN Hotel H ON CH.Id_Hotel = H.Id_Hotel;

-- b)
SELECT Nom_complet, Adresse, Email
FROM Client
WHERE Ville = 'Paris';

-- c)
SELECT C.Nom_complet, COUNT(R.Id_Reservation) AS Nombre_Reservations
FROM Client C
LEFT JOIN Reservation R ON C.Id_Client = R.Id_Client
GROUP BY C.Id_Client, C.Nom_complet
ORDER BY Nombre_Reservations DESC;

-- d)
SELECT TC.Type, COUNT(CH.Id_Chambre) AS Nombre_Chambres
FROM Type_Chambre TC
LEFT JOIN Chambre CH ON TC.Id_Type = CH.Id_Type
GROUP BY TC.Id_Type, TC.Type
ORDER BY Nombre_Chambres DESC;

-- e) 

-- Définir les variables pour le test (en MySQL Workbench ou votre client SQL)
SET @user_start_date = '2025-07-01';
SET @user_end_date = '2025-07-10';

SELECT CH.*, H.Ville AS Hotel_Ville, TC.Type AS Type_Chambre
FROM Chambre CH
JOIN Hotel H ON CH.Id_Hotel = H.Id_Hotel
JOIN Type_Chambre TC ON CH.Id_Type = TC.Id_Type
WHERE CH.Id_Chambre NOT IN (
    SELECT R.Id_Chambre
    FROM Reservation R
    WHERE R.Date_arrivee < @user_end_date  -- La réservation commence avant la fin de la période souhaitée
      AND R.Date_depart > @user_start_date -- La réservation se termine après le début de la période souhaitée
);
