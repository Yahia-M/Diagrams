from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Glue
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.compute import Server as Gitlab  # Use Server for GitLab
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.iac import Terraform
from diagrams.onprem.vcs import Github

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
        s3_bronze = S3("S3 Bronze (Raw Data)")
        s3_silver = S3("S3 Silver (Cleaned Data)")
        s3_gold = S3("S3 Gold (Curated Data)")
        glue = Glue("Glue (ETL)")
        schedule = Cloudwatch("Glue Schedule")

    # CI/CD Tools
    with Cluster("CI/CD Pipeline"):
        gitlab = Gitlab("GitLab")  # Using Server for GitLab
        jenkins = Jenkins("Jenkins")

    # PySpark
    pyspark = Spark("PySpark")

    # Deployment Options
    with Cluster("Deployment Options"):
        aws_cli = Terraform("AWS CLI (Local)")
        gitlab_ci = Github("GitLab CI/CD")
        jenkins_pipeline = Jenkins("Jenkins Pipeline")

    # Data Flow
    users >> Edge(color="brown") >> staging
    users >> Edge(color="brown") >> master_staging
    users >> Edge(color="brown") >> prod

    staging >> Edge(color="blue") >> s3_bronze
    master_staging >> Edge(color="blue") >> s3_silver
    prod >> Edge(color="blue") >> s3_gold

    s3_bronze >> Edge(color="green") >> glue
    s3_silver >> Edge(color="green") >> glue
    s3_gold >> Edge(color="green") >> glue

    glue >> Edge(color="green") >> pyspark
    schedule >> Edge(color="purple") >> glue

    # CI/CD Flow
    gitlab >> Edge(color="red") >> jenkins
    jenkins >> Edge(color="red") >> staging
    jenkins >> Edge(color="red") >> master_staging
    jenkins >> Edge(color="red") >> prod

    # Deployment Flow
    aws_cli >> Edge(color="orange") >> staging
    gitlab_ci >> Edge(color="orange") >> staging
    jenkins_pipeline >> Edge(color="orange") >> staging