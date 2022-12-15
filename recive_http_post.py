import json
from oci.object_storage import ObjectStorageClient

def save_to_bucket(bucket_name, object_name, data):
  # Create a new ObjectStorageClient instance
  object_storage_client = ObjectStorageClient()

  # Generate the full object name, including the bucket and object names
  object_name = f"{bucket_name}/{object_name}"

  # Write the data to the object storage bucket as JSON
  object_storage_client.put_object(
    namespace_name="my_namespace",
    bucket_name=bucket_name,
    object_name=object_name,
    body=json.dumps(data)
  )

# Receive the JSON-encoded data from the POST request
data = request.get_json()

# Call the save_to_bucket function to write the data to the object storage bucket
save_to_bucket("my_bucket", "my_file.json", data)
