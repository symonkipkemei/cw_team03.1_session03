"""
01.1 - Create a Model in a Speckle Project

"""

from main import get_client
from specklepy.core.api.inputs.model_inputs import CreateModelInput

WORKSPACE_ID = "a1cd06bae2"
PROJECT_ID = "128262a20c"

def main():
    # Authenticate
    client = get_client()
    # Create a new model inside the project
    model = client.model.create(CreateModelInput(
        name="homework/session03/team_03.1",
        description="Learning specklepy - Model",
        project_id=PROJECT_ID
    ))
    print(f"✓ Created model in project: {PROJECT_ID}")
    print(f"  Model name: {model.name}")
    print(f"  Model description: {model.description}")

if __name__ == "__main__":
    main()