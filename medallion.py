from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank
from diagrams.generic.storage import Storage
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Internet
from diagrams.onprem.workflow import Airflow

# Create the Medallion Architecture diagram
with Diagram("Medallion Architecture - Contrôle de Gestion", show=False, direction="LR"):
    # External Data Sources
    with Cluster("External Data Sources"):
        external_sources = [
            Internet("ERP System"),
            Internet("CRM System"),
            Internet("Financial Systems")
        ]

    # Data Ingestion Layer
    with Cluster("Data Ingestion"):
        ingestion = Spark("Spark Ingestion")
        external_sources >> ingestion

    # Bronze Layer (Raw Data)
    with Cluster("Bronze Layer - Raw Data"):
        bronze_storage = Storage("Bronze Storage")
        ingestion >> bronze_storage

    # Silver Layer (Cleaned and Enriched Data)
    with Cluster("Silver Layer - Cleaned Data"):
        silver_processing = Spark("Spark Processing")
        silver_storage = Storage("Silver Storage")
        bronze_storage >> silver_processing >> silver_storage

    # Gold Layer (Business-ready Data)
    with Cluster("Gold Layer - Business Data"):
        gold_processing = Spark("Spark Aggregation")
        gold_storage = Storage("Gold Storage")
        silver_storage >> gold_processing >> gold_storage

    # Data Consumption Layer
    with Cluster("Data Consumption"):
        reporting_tool = Server("Reporting Tool")
        analytics_tool = Server("Analytics Tool")
        gold_storage >> reporting_tool
        gold_storage >> analytics_tool

    # Orchestration
    with Cluster("Orchestration"):
        airflow = Airflow("Airflow Orchestration")
        airflow >> ingestion
        airflow >> silver_processing
        airflow >> gold_processing

# Render the diagram
print("Diagram generated successfully!")