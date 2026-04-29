"""
Script d'envoi du lineage à Marquez
Ce script décrit le parcours complet des données dans le projet TechShop :
  Site web (logs) → NiFi (GetFile → MergeContent → PutFile) → Output → Dashboard

Il utilise le protocole OpenLineage pour envoyer ces informations à Marquez.
"""

import requests
import json
from datetime import datetime, timezone
import uuid


# ============================================================
# CONFIGURATION
# ============================================================
# URL de l'API Marquez (port 5002 sur ton PC = port 5000 dans Docker)
MARQUEZ_API = "http://localhost:5002"

# Namespace = un espace de travail qui regroupe tous tes jobs et datasets
NAMESPACE = "techshop-analytics"

# URL de l'API OpenLineage de Marquez
LINEAGE_URL = f"{MARQUEZ_API}/api/v1/lineage"


# ============================================================
# FONCTION UTILITAIRE
# ============================================================
def send_openlineage_event(event: dict):
    """
    Envoie un événement OpenLineage à Marquez.
    Un événement = "tel job a fait telle action avec telles données"
    """
    print(f"  Envoi: {event['job']['name']} ({event['eventType']})...", end=" ")
    response = requests.post(LINEAGE_URL, json=event)
    if response.status_code in [200, 201]:
        print("✅ OK")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")
    return response


def create_run_id():
    """Génère un identifiant unique pour chaque exécution (run) d'un job"""
    return str(uuid.uuid4())


# ============================================================
# ÉVÉNEMENTS DE LINEAGE
# Chaque événement décrit : quel job, quelles données en entrée,
# quelles données en sortie, et si le job a réussi ou non.
# ============================================================

def create_event(job_name, run_id, event_type, inputs, outputs, description=""):
    """
    Crée un événement OpenLineage.
    
    Paramètres :
    - job_name : nom du job (ex: "nifi_getfile")
    - run_id : identifiant unique de l'exécution
    - event_type : "START" (début), "COMPLETE" (terminé), ou "FAIL" (échoué)
    - inputs : liste des datasets en entrée
    - outputs : liste des datasets en sortie
    - description : description du job
    """
    event = {
        "eventTime": datetime.now(timezone.utc).isoformat(),
        "producer": "https://github.com/techshop/analytics-pipeline",
        "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/definitions/RunEvent",
        "eventType": event_type,
        "run": {
            "runId": run_id,
            "facets": {}
        },
        "job": {
            "namespace": NAMESPACE,
            "name": job_name,
            "facets": {
                "documentation": {
                    "_producer": "https://github.com/techshop/analytics-pipeline",
                    "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/DocumentationJobFacet.json",
                    "description": description
                }
            }
        },
        "inputs": inputs,
        "outputs": outputs
    }
    return event


def create_dataset(namespace, name, fields=None):
    """
    Crée la description d'un dataset (source ou destination de données).
    
    Paramètres :
    - namespace : espace de travail
    - name : nom du dataset
    - fields : liste des colonnes/champs du dataset
    """
    dataset = {
        "namespace": namespace,
        "name": name,
        "facets": {}
    }
    
    if fields:
        dataset["facets"]["schema"] = {
            "_producer": "https://github.com/techshop/analytics-pipeline",
            "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/SchemaDatasetFacet.json",
            "fields": [{"name": f, "type": "VARCHAR"} for f in fields]
        }
    
    return dataset


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================
def main():
    print("=" * 60)
    print("📊 Envoi du lineage TechShop à Marquez")
    print("=" * 60)
    
    # ----------------------------------------------------------
    # Vérifier que Marquez est accessible
    # ----------------------------------------------------------
    print("\n🔍 Vérification de la connexion à Marquez...")
    try:
        r = requests.get(f"{MARQUEZ_API}/api/v1/namespaces")
        print(f"  ✅ Marquez accessible (status {r.status_code})")
    except Exception as e:
        print(f"  ❌ Impossible de contacter Marquez: {e}")
        print("  Vérifie que les conteneurs Docker tournent (docker ps)")
        return
    
    # ----------------------------------------------------------
    # Définir les champs des datasets
    # ----------------------------------------------------------
    # Ce sont les colonnes présentes dans tes données
    log_fields = [
        "event_type", "timestamp", "page", "session_id",
        "user_agent", "screen_width", "screen_height",
        "product_id", "product_name", "product_price"
    ]
    
    merged_fields = log_fields  # Les mêmes champs, juste fusionnés
    
    dashboard_fields = [
        "total_events", "unique_sessions", "unique_pages",
        "events_by_type", "top_products", "hourly_distribution"
    ]
    
    # ----------------------------------------------------------
    # ÉTAPE 1 : Job "nifi_getfile"
    # NiFi lit les fichiers de logs du site web
    # Entrée : logs du site web
    # Sortie : fichiers logs individuels (en mémoire dans NiFi)
    # ----------------------------------------------------------
    print("\n📁 Étape 1/4 : NiFi GetFile (lecture des logs)...")
    run_id_1 = create_run_id()
    
    # Événement START (le job commence)
    event_start = create_event(
        job_name="nifi_getfile",
        run_id=run_id_1,
        event_type="START",
        inputs=[create_dataset(NAMESPACE, "website_logs", log_fields)],
        outputs=[],
        description="NiFi GetFile: Lit les fichiers JSON de logs depuis etape1-website/logs/"
    )
    send_openlineage_event(event_start)
    
    # Événement COMPLETE (le job a terminé avec succès)
    event_complete = create_event(
        job_name="nifi_getfile",
        run_id=run_id_1,
        event_type="COMPLETE",
        inputs=[create_dataset(NAMESPACE, "website_logs", log_fields)],
        outputs=[create_dataset(NAMESPACE, "nifi_raw_flowfiles", log_fields)],
        description="NiFi GetFile: Lit les fichiers JSON de logs depuis etape1-website/logs/"
    )
    send_openlineage_event(event_complete)
    
    # ----------------------------------------------------------
    # ÉTAPE 2 : Job "nifi_mergecontent"
    # NiFi fusionne les fichiers individuels en gros fichiers
    # Entrée : fichiers logs individuels
    # Sortie : fichiers fusionnés
    # ----------------------------------------------------------
    print("\n🔄 Étape 2/4 : NiFi MergeContent (fusion des fichiers)...")
    run_id_2 = create_run_id()
    
    event_start = create_event(
        job_name="nifi_mergecontent",
        run_id=run_id_2,
        event_type="START",
        inputs=[create_dataset(NAMESPACE, "nifi_raw_flowfiles", log_fields)],
        outputs=[],
        description="NiFi MergeContent: Fusionne les fichiers JSON par lots de 50 ou toutes les 60 secondes"
    )
    send_openlineage_event(event_start)
    
    event_complete = create_event(
        job_name="nifi_mergecontent",
        run_id=run_id_2,
        event_type="COMPLETE",
        inputs=[create_dataset(NAMESPACE, "nifi_raw_flowfiles", log_fields)],
        outputs=[create_dataset(NAMESPACE, "nifi_merged_files", merged_fields)],
        description="NiFi MergeContent: Fusionne les fichiers JSON par lots de 50 ou toutes les 60 secondes"
    )
    send_openlineage_event(event_complete)
    
    # ----------------------------------------------------------
    # ÉTAPE 3 : Job "nifi_putfile"
    # NiFi écrit les fichiers fusionnés dans le dossier output
    # Entrée : fichiers fusionnés
    # Sortie : fichiers dans etape4-nifi/output/
    # ----------------------------------------------------------
    print("\n💾 Étape 3/4 : NiFi PutFile (écriture dans output/)...")
    run_id_3 = create_run_id()
    
    event_start = create_event(
        job_name="nifi_putfile",
        run_id=run_id_3,
        event_type="START",
        inputs=[create_dataset(NAMESPACE, "nifi_merged_files", merged_fields)],
        outputs=[],
        description="NiFi PutFile: Écrit les fichiers fusionnés dans etape4-nifi/output/"
    )
    send_openlineage_event(event_start)
    
    event_complete = create_event(
        job_name="nifi_putfile",
        run_id=run_id_3,
        event_type="COMPLETE",
        inputs=[create_dataset(NAMESPACE, "nifi_merged_files", merged_fields)],
        outputs=[create_dataset(NAMESPACE, "nifi_output_files", merged_fields)],
        description="NiFi PutFile: Écrit les fichiers fusionnés dans etape4-nifi/output/"
    )
    send_openlineage_event(event_complete)
    
    # ----------------------------------------------------------
    # ÉTAPE 4 : Job "dashboard_analytics"
    # Le dashboard Streamlit lit les fichiers output de NiFi
    # Entrée : fichiers output
    # Sortie : métriques affichées dans le dashboard
    # ----------------------------------------------------------
    print("\n📊 Étape 4/4 : Dashboard Analytics (lecture et affichage)...")
    run_id_4 = create_run_id()
    
    event_start = create_event(
        job_name="dashboard_analytics",
        run_id=run_id_4,
        event_type="START",
        inputs=[create_dataset(NAMESPACE, "nifi_output_files", merged_fields)],
        outputs=[],
        description="Dashboard Streamlit: Lit les fichiers NiFi et affiche les métriques et graphiques"
    )
    send_openlineage_event(event_start)
    
    event_complete = create_event(
        job_name="dashboard_analytics",
        run_id=run_id_4,
        event_type="COMPLETE",
        inputs=[create_dataset(NAMESPACE, "nifi_output_files", merged_fields)],
        outputs=[create_dataset(NAMESPACE, "dashboard_metrics", dashboard_fields)],
        description="Dashboard Streamlit: Lit les fichiers NiFi et affiche les métriques et graphiques"
    )
    send_openlineage_event(event_complete)
    
    # ----------------------------------------------------------
    # RÉSUMÉ
    # ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("✅ Lineage envoyé avec succès !")
    print("=" * 60)
    print("\n📊 Résumé du lineage enregistré :")
    print("  website_logs → [nifi_getfile] → nifi_raw_flowfiles")
    print("  nifi_raw_flowfiles → [nifi_mergecontent] → nifi_merged_files")
    print("  nifi_merged_files → [nifi_putfile] → nifi_output_files")
    print("  nifi_output_files → [dashboard_analytics] → dashboard_metrics")
    print(f"\n🌐 Visualise le lineage sur : http://localhost:3000")
    print(f"   Sélectionne le namespace '{NAMESPACE}' dans le menu déroulant en haut à droite")


if __name__ == "__main__":
    main()
