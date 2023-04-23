from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from api_gcs import etl_gcs

docker_container_block = DockerContainer.load("docker-block")

deployment_api_request = Deployment.build_from_flow(
    flow = etl_gcs, 
    name="api_request_flow", 
    infrastructure = docker_container_block
)

if __name__ == "__main__":
    deployment_api_request.apply()