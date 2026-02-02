"""
03.1 - Add Properties to Objects in a Speckle Model

"""

import random
from main import get_client
from specklepy.transports.server import ServerTransport
from specklepy.api import operations
from specklepy.objects.base import Base

PROJECT_ID = "128262a20c"
MODEL_ID = "39d99ae41a"

# Sort breps by z position (assuming brep.basePoint.z exists)
def get_z(brep):
    try:
        return getattr(getattr(brep, "basePoint", None), "z", 0)
    except Exception:
        return 0

def main():
    # Authenticate
    client = get_client()

    # Get the latest version
    versions = client.version.get_versions(MODEL_ID, PROJECT_ID, limit=1)
    if not versions.items:
        print("No versions found.")
        return
    latest_version = versions.items[0]
    print(f"✓ Fetching version: {latest_version.id}")

    # Receive the data
    transport = ServerTransport(client=client, stream_id=PROJECT_ID)
    data = operations.receive(latest_version.referenced_object, transport)

    # Ensure 'properties' exists
    if getattr(data, "properties", None) is None:
        data["properties"] = {}

    # Now you can safely assign
    data["properties"]["Tower"] = "Team_03.1"

    # Or add properties to child elements
    elements = getattr(data, "elements", [])
    module_numbers = {"Old_Modules": ["01", "03"], "New_Module": ["02"]}

    for element in elements:
        module_name = getattr(element, "name", None)
        numbers = module_numbers.get(module_name, [])
        print(numbers)
        breps = getattr(element, "elements", [])
        for i, brep in enumerate(breps):
            if isinstance(brep, Base):
                if getattr(brep, "properties", None) is None:
                    brep["properties"] = {}
                # Assign the custom number if available, else fallback to index+1
                brep["properties"]["Module"] = numbers[i] if i < len(numbers) else "01"
                #pick random values
                randomnames = ["Elena Corio", "Symon Kipkemei"]
                selected_name = random.choice(randomnames)
                brep["properties"]["Designer"] = selected_name
                print(brep["properties"])
    print(f"✓ Added properties to elements")

    # Send the modified data back to Speckle
    object_id = operations.send(data, [transport])
    print(f"✓ Sent object: {object_id}")

    # Create a new version with the modified data
    from specklepy.core.api.inputs.version_inputs import CreateVersionInput

    version = client.version.create(CreateVersionInput(
        projectId=PROJECT_ID,
        modelId=MODEL_ID,
        objectId=object_id,
        message="Added custom properties via specklepy"
    ))

    print(f"✓ Created version: {version.id}")


if __name__ == "__main__":
    main()
