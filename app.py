import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

DB_NAME = "gestion_hotel.db"

# --- Fonctions d'interaction avec la base de données ---
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Pour accéder aux colonnes par nom
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# 1. Consulter la liste des réservations
def get_reservations():
    conn = get_db_connection()
    query = """
    SELECT 
        R.Id_Reservation, 
        C.Nom_complet AS Client, 
        H.Ville AS Hotel,
        CH.Numero_chambre,
        R.Date_arrivee, 
        R.Date_depart
    FROM Reservation R
    JOIN Client C ON R.Id_Client = C.Id_Client
    JOIN Chambre CH ON R.Id_Chambre = CH.Id_Chambre
    JOIN Hotel H ON CH.Id_Hotel = H.Id_Hotel
    ORDER BY R.Date_arrivee DESC;
    """
    reservations = pd.read_sql_query(query, conn)
    conn.close()
    return reservations

# 2. Consulter la liste des clients
def get_clients():
    conn = get_db_connection()
    clients = pd.read_sql_query("SELECT Id_Client, Nom_complet, Email, Ville, Numero_telephone FROM Client ORDER BY Nom_complet", conn)
    conn.close()
    return clients

# 3. Consulter la liste des chambres disponibles pendant une période donnée
def get_available_rooms(start_date_str, end_date_str):
    conn = get_db_connection()
    query = """
    SELECT 
        CH.Id_Chambre,
        CH.Numero_chambre,
        H.Ville AS Hotel,
        TC.Type AS Type_Chambre,
        TC.Tarif,
        CH.Etage,
        CASE CH.Fumeurs WHEN 1 THEN 'Oui' ELSE 'Non' END AS Fumeurs
    FROM Chambre CH
    JOIN Hotel H ON CH.Id_Hotel = H.Id_Hotel
    JOIN Type_Chambre TC ON CH.Id_Type = TC.Id_Type
    WHERE CH.Id_Chambre NOT IN (
        SELECT R.Id_Chambre
        FROM Reservation R
        WHERE R.Date_arrivee < ?  -- end_date_str
          AND R.Date_depart > ?   -- start_date_str
    )
    ORDER BY H.Ville, CH.Numero_chambre;
    """
    # Convertir les dates en format YYYY-MM-DD pour la requête
    params = (end_date_str, start_date_str)
    available_rooms = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return available_rooms

# 4. Ajouter un client
def add_client(nom_complet, email, adresse, ville, code_postal, telephone):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO Client (Nom_complet, Email, Adresse, Ville, Code_postal, Numero_telephone)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (nom_complet, email, adresse, ville, code_postal, telephone))
        conn.commit()
        return True, "Client ajouté avec succès !"
    except sqlite3.IntegrityError: # Gère l'erreur si l'email est déjà utilisé (UNIQUE constraint)
        return False, "Erreur : L'email existe déjà."
    except sqlite3.Error as e:
        return False, f"Erreur SQLite : {e}"
    finally:
        conn.close()

# 5. Ajouter une réservation
def add_reservation(id_client, id_chambre, date_arrivee_str, date_depart_str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Vérification supplémentaire de disponibilité (bonne pratique)
        cursor.execute("""
            SELECT COUNT(*) FROM Reservation
            WHERE Id_Chambre = ? AND Date_arrivee < ? AND Date_depart > ?
        """, (id_chambre, date_depart_str, date_arrivee_str))
        if cursor.fetchone()[0] > 0:
            return False, "Erreur : La chambre n'est plus disponible pour ces dates."

        cursor.execute("""
        INSERT INTO Reservation (Id_Client, Id_Chambre, Date_arrivee, Date_depart)
        VALUES (?, ?, ?, ?)
        """, (id_client, id_chambre, date_arrivee_str, date_depart_str))
        conn.commit()
        return True, "Réservation ajoutée avec succès !"
    except sqlite3.Error as e:
        return False, f"Erreur SQLite : {e}"
    finally:
        conn.close()

# --- Fonctions utilitaires pour les dropdowns ---
def get_all_clients_for_dropdown():
    conn = get_db_connection()
    clients = conn.execute("SELECT Id_Client, Nom_complet FROM Client ORDER BY Nom_complet").fetchall()
    conn.close()
    return {client['Nom_complet']: client['Id_Client'] for client in clients} # Nom: ID

def get_all_chambres_for_dropdown(start_date_str, end_date_str):
    # Utilise la fonction existante et formate pour le dropdown
    df_rooms = get_available_rooms(start_date_str, end_date_str)
    if df_rooms.empty:
        return {}
    # Créer une chaîne descriptive pour chaque chambre
    return {f"Ch.{row['Numero_chambre']} ({row['Type_Chambre']}) à {row['Hotel']}": row['Id_Chambre'] 
            for index, row in df_rooms.iterrows()}


# --- Interface Streamlit ---
st.set_page_config(layout="wide", page_title="Gestion Hôtel")
st.title("🏨 Système de Gestion Hôtelière")

menu = ["Consulter les réservations", "Consulter les clients", "Consulter les chambres disponibles", "Ajouter un client", "Ajouter une réservation"]
choice = st.sidebar.selectbox("Menu", menu)

st.sidebar.markdown("---")
st.sidebar.info("Projet Bases de Données INFS4 - Pr. J.ZAHIR")

if choice == "Consulter les réservations":
    st.subheader("Liste des Réservations")
    reservations_df = get_reservations()
    if reservations_df.empty:
        st.info("Aucune réservation trouvée.")
    else:
        st.dataframe(reservations_df, use_container_width=True)

elif choice == "Consulter les clients":
    st.subheader("Liste des Clients")
    clients_df = get_clients()
    if clients_df.empty:
        st.info("Aucun client trouvé.")
    else:
        st.dataframe(clients_df, use_container_width=True)

elif choice == "Consulter les chambres disponibles":
    st.subheader("Rechercher des Chambres Disponibles")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Date d'arrivée", value=date.today(), min_value=date.today())
    with col2:
        end_date = st.date_input("Date de départ", value=pd.to_datetime(date.today()) + pd.Timedelta(days=1), min_value=date.today() + pd.Timedelta(days=1))

    if start_date >= end_date:
        st.error("La date de départ doit être après la date d'arrivée.")
    else:
        if st.button("Rechercher les chambres disponibles"):
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            available_rooms_df = get_available_rooms(start_date_str, end_date_str)
            if available_rooms_df.empty:
                st.info("Aucune chambre disponible pour les dates sélectionnées.")
            else:
                st.dataframe(available_rooms_df, use_container_width=True)

elif choice == "Ajouter un client":
    st.subheader("Ajouter un Nouveau Client")
    with st.form("client_form"):
        nom_complet = st.text_input("Nom complet*", help="Le nom et prénom du client.")
        email = st.text_input("Email*", help="L'adresse email du client (doit être unique).")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.text_input("Code postal")
        telephone = st.text_input("Numéro de téléphone")
        
        submitted = st.form_submit_button("Ajouter Client")
        if submitted:
            if not nom_complet or not email:
                st.warning("Veuillez remplir les champs obligatoires (Nom complet, Email).")
            else:
                success, message = add_client(nom_complet, email, adresse, ville, code_postal, telephone)
                if success:
                    st.success(message)
                else:
                    st.error(message)

elif choice == "Ajouter une réservation":
    st.subheader("Ajouter une Nouvelle Réservation")
    
    clients_dict = get_all_clients_for_dropdown()
    if not clients_dict:
        st.warning("Aucun client dans la base. Veuillez d'abord ajouter un client.")
    else:
        with st.form("reservation_form"):
            # Sélection du client
            client_nom_selectionne = st.selectbox("Choisir un client*", list(clients_dict.keys()), help="Sélectionnez le client qui fait la réservation.")
            
            # Sélection des dates
            col1_res, col2_res = st.columns(2)
            with col1_res:
                res_start_date = st.date_input("Date d'arrivée pour la réservation*", value=date.today(), min_value=date.today(), key="res_start")
            with col2_res:
                res_end_date = st.date_input("Date de départ pour la réservation*", value=pd.to_datetime(date.today()) + pd.Timedelta(days=1), min_value=date.today() + pd.Timedelta(days=1), key="res_end")

            if res_start_date >= res_end_date:
                st.error("La date de départ doit être après la date d'arrivée.")
                chambres_dispo_dict = {} # Pas de chambres si dates invalides
            else:
                res_start_date_str = res_start_date.strftime('%Y-%m-%d')
                res_end_date_str = res_end_date.strftime('%Y-%m-%d')
                chambres_dispo_dict = get_all_chambres_for_dropdown(res_start_date_str, res_end_date_str)

            if not chambres_dispo_dict:
                 st.info("Aucune chambre disponible pour les dates sélectionnées. Modifiez les dates.")
                 selected_chambre_id = None # Pour éviter une erreur si le dictionnaire est vide
                 chambre_desc_selectionnee = st.selectbox("Choisir une chambre*", ["Aucune chambre disponible"], disabled=True, help="Les chambres disponibles s'afficheront ici.")

            else:
                chambre_desc_selectionnee = st.selectbox("Choisir une chambre*", list(chambres_dispo_dict.keys()), help="Sélectionnez une chambre parmi celles disponibles.")
                selected_chambre_id = chambres_dispo_dict.get(chambre_desc_selectionnee)


            submitted_res = st.form_submit_button("Ajouter Réservation")

            if submitted_res:
                if not client_nom_selectionne or not selected_chambre_id or res_start_date >= res_end_date:
                    st.warning("Veuillez remplir tous les champs correctement et vous assurer que les dates sont valides et qu'une chambre est sélectionnée.")
                else:
                    selected_client_id = clients_dict[client_nom_selectionne]
                    
                    success, message = add_reservation(selected_client_id, selected_chambre_id, res_start_date_str, res_end_date_str)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)