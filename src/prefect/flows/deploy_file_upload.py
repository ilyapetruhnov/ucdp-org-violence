from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from file_upload import upload_csv_data

docker_container_block = DockerContainer.load("docker-block")

deployment_file_upload = Deployment.build_from_flow(
    flow = upload_csv_data, 
    name="file_upload_flow", 
    infrastructure = docker_container_block
)

if __name__ == "__main__":
    deployment_file_upload.apply()