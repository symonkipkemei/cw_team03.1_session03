"""
02.1 - Copy and Modify Geometries from One Model to Another

"""

import copy
from main import get_client
from specklepy.transports.server import ServerTransport
from specklepy.api import operations
from specklepy.objects.base import Base
from specklepy.objects.other import Base
from specklepy.core.api.inputs.version_inputs import CreateVersionInput

PROJECT_ID = "128262a20c"
SOURCE_MODEL_ID = "a1014e4b32"
TARGET_MODEL_ID = "39d99ae41a"
OFFSET_Z = 16000 # Offset for the duplicated object in Z direction
# ? Why 16000 even if the model is in m

def offset_mesh_vertices(mesh, offset_z: float):
    """
    Move mesh vertices in the Z direction.
    Vertices are stored as flat list: [x1, y1, z1, x2, y2, z2, ...]
    """
    if hasattr(mesh, "vertices") and mesh.vertices:
        new_vertices = []
        for i in range(0, len(mesh.vertices), 3):
            new_vertices.append(mesh.vertices[i] )  # x 
            new_vertices.append(mesh.vertices[i + 1])  # y
            new_vertices.append(mesh.vertices[i + 2] + offset_z)  # z + offset
        mesh.vertices = new_vertices

def move_geometry(obj, offset_z: float):
    """
    Move geometry in the Z direction for mesh 
    ? Note: object is a mesh even if it is labelled as Brep
    """
    # Handle displayValue (common in Revit objects)
    display_value = getattr(obj, "displayValue", None) or getattr(obj, "@displayValue", None)
    if display_value:
        if isinstance(display_value, list):
            for mesh in display_value:
                offset_mesh_vertices(mesh, offset_z)
        else:
            offset_mesh_vertices(display_value, offset_z)

#TODO: simple copy (see docs)
def deep_copy_and_move(obj, offset_z: float):
    """
    Create a deep copy of a Speckle object and offset its geometry in Z direction.
    """
    # Serialize to dict and deserialize to create a copy
    from specklepy.serialization.base_object_serializer import BaseObjectSerializer
    
    # Create a new instance of Base
    new_obj = Base()
    
    # Copy all properties
    for key in obj.get_member_names():
        value = getattr(obj, key, None)
        if value is not None:
            try:
                setattr(new_obj, key, copy.deepcopy(value))
            except:
                setattr(new_obj, key, value)
    
    # Clear the id so a new one is generated
    new_obj.id = None
    
    # Generate a new applicationId for the copy
    import uuid
    new_obj.applicationId = str(uuid.uuid4())

    # Move geometry 
    move_geometry(new_obj, offset_z)
    
    return new_obj

def main():
    # Authenticate
    client = get_client()
    
    # Get the latest version
    versions = client.version.get_versions(SOURCE_MODEL_ID, PROJECT_ID, limit=1)
    if not versions.items:
        print("No versions found.")
        return
    
    latest_version = versions.items[0]
    print(f"✓ Fetching version: {latest_version.id}")
    
    # Receive the full data tree
    transport = ServerTransport(client=client, stream_id=PROJECT_ID)
    data = operations.receive(latest_version.referenced_object, transport)
    
    # Modify data / collection name
    data["name"] = "Speckle Model"
    print(data.name) 

    # Modify element / layer name
    elements = getattr(data, "elements", [])
    old_modules = elements[0]
    old_modules.name = "Old_Modules"
    print(old_modules.name)

    # Create new layer / element for the new module
    new_module = Base()
    new_module.name = "New_Module"
    print(new_module.name)

    # Duplicate the lower brep, move it up in Z and add to new layer
    breps = getattr(old_modules, "elements", [])
    new_module.elements = [deep_copy_and_move(breps[0], OFFSET_Z)]

    # Add new layer to data elements
    elements.append(new_module)

    # Create a new version in the target model with the received data
    object_id = operations.send(data, [transport])
    version = client.version.create(
        CreateVersionInput(
        object_id=object_id,
        model_id=TARGET_MODEL_ID,
        project_id=PROJECT_ID,
        message="Old and New Modules"
    ))

    print(f"✓ Created version: {version.id}")


if __name__ == "__main__":
    main()
