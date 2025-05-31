import sqlite3

def create_connection(db_file="gestion_hotel.db"):
    """ Crée une connexion à la base de données SQLite """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = ON;") # Activer les clés étrangères
        print(f"SQLite version: {sqlite3.sqlite_version}")
        print(f"Connexion à {db_file} réussie.")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """ Crée les tables dans la base de données SQLite """
    sql_create_hotel_table = """
    CREATE TABLE IF NOT EXISTS Hotel (
        Id_Hotel INTEGER PRIMARY KEY AUTOINCREMENT,
        Ville TEXT NOT NULL,
        Pays TEXT NOT NULL,
        Code_postal TEXT
    );
    """

    sql_create_type_chambre_table = """
    CREATE TABLE IF NOT EXISTS Type_Chambre (
        Id_Type INTEGER PRIMARY KEY AUTOINCREMENT,
        Type TEXT NOT NULL,
        Tarif REAL NOT NULL
    );
    """

    sql_create_chambre_table = """
    CREATE TABLE IF NOT EXISTS Chambre (
        Id_Chambre INTEGER PRIMARY KEY AUTOINCREMENT,
        Numero_chambre INTEGER NOT NULL,
        Etage INTEGER,
        Fumeurs INTEGER DEFAULT 0, -- 0 for False, 1 for True
        Id_Hotel INTEGER,
        Id_Type INTEGER,
        FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel) ON DELETE CASCADE,
        FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type) ON DELETE SET NULL,
        UNIQUE (Id_Hotel, Numero_chambre)
    );
    """

    sql_create_client_table = """
    CREATE TABLE IF NOT EXISTS Client (
        Id_Client INTEGER PRIMARY KEY AUTOINCREMENT,
        Adresse TEXT,
        Ville TEXT,
        Code_postal TEXT,
        Email TEXT UNIQUE,
        Numero_telephone TEXT,
        Nom_complet TEXT NOT NULL
    );
    """

    sql_create_reservation_table = """
    CREATE TABLE IF NOT EXISTS Reservation (
        Id_Reservation INTEGER PRIMARY KEY AUTOINCREMENT,
        Date_arrivee TEXT NOT NULL, -- Store as 'YYYY-MM-DD'
        Date_depart TEXT NOT NULL, -- Store as 'YYYY-MM-DD'
        Id_Client INTEGER,
        Id_Chambre INTEGER,
        FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client) ON DELETE CASCADE,
        FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre) ON DELETE CASCADE,
        CONSTRAINT chk_dates CHECK (Date_depart > Date_arrivee)
    );
    """

    sql_create_prestation_table = """
    CREATE TABLE IF NOT EXISTS Prestation (
        Id_Prestation INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_prestation TEXT NOT NULL,
        Prix REAL NOT NULL
    );
    """

    sql_create_offre_table = """
    CREATE TABLE IF NOT EXISTS Offre (
        Id_Hotel INTEGER,
        Id_Prestation INTEGER,
        PRIMARY KEY (Id_Hotel, Id_Prestation),
        FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel) ON DELETE CASCADE,
        FOREIGN KEY (Id_Prestation) REFERENCES Prestation(Id_Prestation) ON DELETE CASCADE
    );
    """

    sql_create_evaluation_table = """
    CREATE TABLE IF NOT EXISTS Evaluation (
        Id_Evaluation INTEGER PRIMARY KEY AUTOINCREMENT,
        Date_evaluation TEXT NOT NULL, -- Store as 'YYYY-MM-DD'
        La_note INTEGER CHECK (La_note >= 1 AND La_note <= 5),
        Texte_descriptif TEXT,
        Id_Reservation INTEGER UNIQUE,
        FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation) ON DELETE CASCADE
    );
    """

    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_hotel_table)
        cursor.execute(sql_create_type_chambre_table)
        cursor.execute(sql_create_chambre_table)
        cursor.execute(sql_create_client_table)
        cursor.execute(sql_create_reservation_table)
        cursor.execute(sql_create_prestation_table)
        cursor.execute(sql_create_offre_table)
        cursor.execute(sql_create_evaluation_table)
        conn.commit()
        print("Tables créées avec succès (ou existent déjà).")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création des tables: {e}")

def insert_initial_data(conn):
    """ Insère les données initiales fournies dans l'annexe """
    cursor = conn.cursor()

    try:
        # Vérifier si les données existent pour éviter les doublons (simpliste)
        cursor.execute("SELECT COUNT(*) FROM Hotel")
        if cursor.fetchone()[0] > 0:
            print("Les données initiales semblent déjà exister. L'insertion est ignorée.")
            return

        # Hotel
        hotels = [
            (1, 'Paris', 'France', '75001'),
            (2, 'Lyon', 'France', '69002')
        ]
        cursor.executemany("INSERT INTO Hotel (Id_Hotel, Ville, Pays, Code_postal) VALUES (?,?,?,?)", hotels)

        # Type_Chambre
        types_chambre = [
            (1, 'Simple', 80.00),
            (2, 'Double', 120.00)
        ]
        cursor.executemany("INSERT INTO Type_Chambre (Id_Type, Type, Tarif) VALUES (?,?,?)", types_chambre)

        # Chambre (Numero_chambre, Etage, Fumeurs (0/1), Id_Type, Id_Hotel)
        # Id_Chambre est AUTOINCREMENT
        chambres = [
            (201, 2, 0, 1, 1), (502, 5, 1, 1, 2), (305, 3, 0, 2, 1),
            (410, 4, 0, 2, 2), (104, 1, 1, 2, 2), (202, 2, 0, 1, 1),
            (307, 3, 1, 1, 2), (101, 1, 0, 1, 1)
        ]
        cursor.executemany("INSERT INTO Chambre (Numero_chambre, Etage, Fumeurs, Id_Type, Id_Hotel) VALUES (?,?,?,?,?)", chambres)

        # Client
        clients = [
            (1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
            (2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
            (3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
            (4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
            (5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
        ]
        cursor.executemany("INSERT INTO Client (Id_Client, Adresse, Ville, Code_postal, Email, Numero_telephone, Nom_complet) VALUES (?,?,?,?,?,?,?)", clients)

        # Prestation
        prestations = [
            (1, 'Petit-déjeuner', 15.00), (2, 'Navette aéroport', 30.00),
            (3, 'Wi-Fi gratuit', 0.00), (4, 'Spa et bien-être', 50.00),
            (5, 'Parking sécurisé', 20.00)
        ]
        cursor.executemany("INSERT INTO Prestation (Id_Prestation, Nom_prestation, Prix) VALUES (?,?,?)", prestations)
        
        # Offre (Id_Hotel, Id_Prestation) - Données inventées
        offres = [
            (1, 1), (1, 3), (1, 5), (2, 1), (2, 2), (2, 3), (2, 4)
        ]
        cursor.executemany("INSERT INTO Offre (Id_Hotel, Id_Prestation) VALUES (?,?)", offres)

        # Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client, Id_Chambre)
        # Id_Chambre doit correspondre aux Id_Chambre auto-incrémentés (1 à 8 dans notre cas)
        reservations = [
            (1, '2025-06-15', '2025-06-18', 1, 1), # Jean Dupont, Chambre ID 1 (201 Paris)
            (2, '2025-07-01', '2025-07-05', 2, 2), # Marie Leroy, Chambre ID 2 (502 Lyon)
            (7, '2025-11-12', '2025-11-14', 2, 7), # Marie Leroy, Chambre ID 7 (307 Lyon)
            (10,'2026-02-01', '2026-02-05', 2, 4), # Marie Leroy, Chambre ID 4 (410 Lyon)
            (3, '2025-08-10', '2025-08-14', 3, 3), # Paul Moreau, Chambre ID 3 (305 Paris)
            (4, '2025-09-05', '2025-09-07', 4, 6), # Lucie Martin, Chambre ID 6 (202 Paris)
            (9, '2026-01-15', '2026-01-18', 4, 8), # Lucie Martin, Chambre ID 8 (101 Paris)
            (5, '2025-09-20', '2025-09-25', 5, 5)  # Emma Giraud, Chambre ID 5 (104 Lyon)
        ]
        # Important: SQLite auto-incrémente Id_Reservation si on ne le spécifie pas.
        # Pour correspondre aux IDs de l'annexe, on les insère explicitement.
        cursor.executemany("INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client, Id_Chambre) VALUES (?,?,?,?,?)", reservations)

        # Evaluation
        evaluations = [
            (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
            (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
            (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
            (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
            (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
        ]
        cursor.executemany("INSERT INTO Evaluation (Id_Evaluation, Date_evaluation, La_note, Texte_descriptif, Id_Reservation) VALUES (?,?,?,?,?)", evaluations)

        conn.commit()
        print("Données initiales insérées avec succès.")
    except sqlite3.IntegrityError as e:
        print(f"Erreur d'intégrité lors de l'insertion des données (peut-être déjà insérées ou problème de clé étrangère): {e}")
    except sqlite3.Error as e:
        print(f"Erreur SQLite lors de l'insertion des données: {e}")


if __name__ == '__main__':
    db_file = "gestion_hotel.db"
    conn = create_connection(db_file)
    if conn:
        create_tables(conn)
        insert_initial_data(conn) # Insérer les données seulement si nécessaire
        conn.close()
        print("Base de données SQLite initialisée.")
