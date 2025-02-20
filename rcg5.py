from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Glue
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.vcs import Gitlab
# from diagrams.onprem.compute import Server as Gitlab  # Use Server for GitLab
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.iac import Terraform
from diagrams.onprem.vcs import Github

# Create the diagram
with Diagram("AWS Cloud - Contrôle de Gestion", show=False, direction="LR", filename="medallion_architecture_AWS Cloud"):

    # Users
    users = Users("End Users (Contrôle de Gestion)")

    # Environments
    with Cluster("Environments"):
        with Cluster("Staging"):
            staging_bronze = S3("S3 Bronze (Raw)")
            staging_silver = S3("S3 Silver (Cleaned)")
            staging_gold = S3("S3 Gold (Curated)")
            staging_glue = Glue("Glue (ETL)")
            staging_schedule = Cloudwatch("Glue Schedule")

        with Cluster("Master-Staging"):
            master_staging_bronze = S3("S3 Bronze (Raw)")
            master_staging_silver = S3("S3 Silver (Cleaned)")
            master_staging_gold = S3("S3 Gold (Curated)")
            master_staging_glue = Glue("Glue (ETL)")
            master_staging_schedule = Cloudwatch("Glue Schedule")

        with Cluster("Prod"):
            prod_bronze = S3("S3 Bronze (Raw)")
            prod_silver = S3("S3 Silver (Cleaned)")
            prod_gold = S3("S3 Gold (Curated)")
            prod_glue = Glue("Glue (ETL)")
            prod_schedule = Cloudwatch("Glue Schedule")

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
    users >> Edge(color="brown") >> staging_bronze
    users >> Edge(color="brown") >> master_staging_bronze
    users >> Edge(color="brown") >> prod_bronze

    staging_bronze >> Edge(color="blue") >> staging_glue
    staging_glue >> Edge(color="blue") >> staging_silver
    staging_silver >> Edge(color="blue") >> staging_gold

    master_staging_bronze >> Edge(color="blue") >> master_staging_glue
    master_staging_glue >> Edge(color="blue") >> master_staging_silver
    master_staging_silver >> Edge(color="blue") >> master_staging_gold

    prod_bronze >> Edge(color="blue") >> prod_glue
    prod_glue >> Edge(color="blue") >> prod_silver
    prod_silver >> Edge(color="blue") >> prod_gold

    # Glue and PySpark
    staging_glue >> Edge(color="green") >> pyspark
    master_staging_glue >> Edge(color="green") >> pyspark
    prod_glue >> Edge(color="green") >> pyspark

    # Glue Schedule
    staging_schedule >> Edge(color="purple") >> staging_glue
    master_staging_schedule >> Edge(color="purple") >> master_staging_glue
    prod_schedule >> Edge(color="purple") >> prod_glue

    # CI/CD Flow
    gitlab >> Edge(color="red") >> jenkins  # GitLab triggers Jenkins
    jenkins >> Edge(color="red") >> staging_bronze  # Jenkins deploys to Staging
    jenkins >> Edge(color="red") >> master_staging_bronze  # Jenkins deploys to Master-Staging
    jenkins >> Edge(color="red") >> prod_bronze  # Jenkins deploys to Prod

    # Deployment Flow
    aws_cli >> Edge(color="orange") >> staging_bronze  # Local deployment to Staging
    gitlab_ci >> Edge(color="orange") >> jenkins  # GitLab CI/CD triggers Jenkins
    jenkins_pipeline >> Edge(color="orange") >> jenkins  # Jenkins Pipeline triggers Jenkins