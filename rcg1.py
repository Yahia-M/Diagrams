from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Glue
from diagrams.onprem.compute import Server as Schedule  # Generic node for scheduling
from diagrams.onprem.compute import Server as Gitlab  # Use Server for GitLab
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server

# Create the diagram
with Diagram("Medallion Architecture - Contrôle de Gestion", show=False, direction="LR"):

    # Users
    users = Users("End Users (Contrôle de Gestion)")

    # Environments
    with Cluster("Environments"):
        staging = Server("Staging")
        master_staging = Server("Master-Staging")
        prod = Server("Prod")

    # AWS Services
    with Cluster("AWS Services"):
        s3 = S3("S3 (Data Lake)")
        glue = Glue("Glue (ETL)")
        schedule = Schedule("Glue Schedule")  # Using generic Server node

    # CI/CD Tools
    with Cluster("CI/CD Pipeline"):
        gitlab = Gitlab("GitLab")  # Using Server for GitLab
        jenkins = Jenkins("Jenkins")

    # PySpark
    pyspark = Spark("PySpark")

    # Data Flow
    users >> Edge(color="brown") >> staging
    users >> Edge(color="brown") >> master_staging
    users >> Edge(color="brown") >> prod

    staging >> Edge(color="blue") >> s3
    master_staging >> Edge(color="blue") >> s3
    prod >> Edge(color="blue") >> s3

    s3 >> Edge(color="green") >> glue
    glue >> Edge(color="green") >> pyspark
    schedule >> Edge(color="purple") >> glue

    gitlab >> Edge(color="red") >> jenkins
    jenkins >> Edge(color="red") >> staging
    jenkins >> Edge(color="red") >> master_staging
    jenkins >> Edge(color="red") >> prod