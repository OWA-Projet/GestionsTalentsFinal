import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ctypes import windll

# Empêche l'ordinateur de se mettre en veille
windll.kernel32.SetThreadExecutionState(0x80000002)


def scrape_profile():  # Plus besoin de paramètre "metier" car tout est interactif
    # Initialisation et configuration du WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # URL cible
    url = "https://entreprise.francetravail.fr/recherche-profil/rechercheprofil"
    driver.get(url)

    # Attente explicite pour s'assurer que la page est chargée correctement
    wait = WebDriverWait(driver, 10)

    # Liste pour stocker les résultats
    resultats = []

    try:
        # Attendre que l'utilisateur entre le métier dans le champ de recherche
        wait.until(
            EC.presence_of_element_located((By.ID, "token-input-champsMultitagQuoi")))  # Assure le chargement complet
        print("🔔 Veuillez entrer le MÉTIER dans le champ de recherche de l'interface web.")
        print("Puis, cliquez sur le bouton 'Rechercher CV'.")

        # Pause pour permettre à l'utilisateur de remplir manuellement le formulaire
        input("⏳ Quand vous avez terminé, appuyez sur Entrée pour continuer le scraping...")
  # Cliquer sur le bouton "Voir le profil" si disponible
        try:
            profile_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.lienclic-profil")))
            profile_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Aucun bouton 'Voir profil' trouvé pour le métier : {e}")


        # Pause courte pour permettre au site de mettre à jour les résultats
        time.sleep(3)

        # Commencer à extraire les résultats après recherche
        i = 1

        while i <= 2000:  # Limite arbitraire pour éviter une boucle infinie
            try:
                # Vérifier si une donnée est chargée
                soup = BeautifulSoup(driver.page_source, "html.parser")
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "profil-bd")))

                # Extraction des profils
                profils = soup.find_all("div", class_="profil-bd")

                # Arrêtez si aucun profil n'est trouvé
                if not profils:
                    print(f"⚠️ Aucun profil trouvé sur la page {i}. Fin de la pagination.")
                    break

                for profil in profils:
                    # Récupérer les détails du profil
                    competences_container = profil.find("div", id="zoneAfficherCompetences")

                    # Vérifiez si le conteneur des compétences est disponible
                    if competences_container:
                        competences = [tag.get_text(strip=True) for tag in
                                       competences_container.select("li.tag.competence span.tag-name")]
                        savoir_etre = [tag.get_text(strip=True) for tag in
                                       competences_container.select("li.tag.qualite span.tag-name")]
                        langues = [tag.get_text(strip=True) for tag in
                                   competences_container.select("li.tag.langue span.tag-name")]
                        permis = [tag.get_text(strip=True) for tag in
                                  competences_container.select("li.tag.permis span.tag-name")]
                    else:
                        competences, savoir_etre, langues, permis = [], [], [], []

                    # Extraction des formations
                    formations = [li.get_text(strip=True, separator=" ") for li in
                                  profil.select("ul.list-unstyled.list-event > li.block-form.event.formation")]

                    # Extraction des expériences
                    experiences = [li.get_text(strip=True, separator=" ") for li in
                                   profil.select("ul.list-unstyled.list-event > li.block-form.event.experience")]

                    # Ajout des données au tableau
                    resultats.append({
                        "formations": formations,
                        "experiences": experiences,
                        "competences": competences,
                        "Qualités": savoir_etre,
                        "langues": langues,
                        "permis": permis,
                    })

                # Passer à la page suivante, s’il existe un bouton "Suivant"
                try:
                    next_button = driver.find_element(By.XPATH, '//button[contains(@class, "btn-nav next")]')

                    # Vérifiez si le bouton est désactivé
                    if "disabled" in next_button.get_attribute("class"):
                        print("⚠️ Bouton 'Suivant' désactivé – Fin de la pagination.")
                        break

                    next_button.click()
                    time.sleep(2)  # Pause pour le chargement
                except Exception as e:
                    print(f"⚠️ Impossible de naviguer à la page suivante. Erreur : {e}")
                    break

            except Exception as e:
                print(f"❌ Erreur lors de l'extraction des données à la page {i}. Erreur : {e}")
                break

            i += 1

    except Exception as e:
        print(f"❌ Erreur générale : {e}")

    # Sauvegarde des résultats dans un fichier CSV
    if resultats:
        df = pd.DataFrame(resultats)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file_name = f"Ingénieur logiciel.csv"
        df.to_csv(csv_file_name, index=False, encoding="utf-8")
        print(f"✅ Données sauvegardées avec succès dans le fichier '{csv_file_name}'.")
    else:
        print("❌ Aucun résultat n'a pu être extrait.")

    # Fermer le navigateur
    driver.quit()


# Exécuter la fonction (pas de métier en paramètre, car c'est entièrement manuel maintenant)
scrape_profile()

metiers = [
    "---------------------------------",
    "Testeur informatique ",
    "Formateur informatique ",
    "Stage en informatique ",
    "Développeur Informatique ",
    "sécurité informatique ",
    "Ingénieur cloud computing ",
    "Administrateur de base de données ",
    "Data scientist ",
    "Ingénieur télécoms et réseaux ",
    "Ingénieur en systèmes embarqués ",
    "Développeur mobiles ",
    "Big data ",
    "Scrum Master Agile ",
    "Product owner ",
    "Architecte web ",
    "Data analyst ",
    "Ingénieur logiciel ",
    "",
]