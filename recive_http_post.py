import io
import json
import logging
from fdk import response
import oci
import time


def handler(ctx, data: io.BytesIO = None):
    if None == ctx.RequestURL():
        return "Function loaded properly but not invoked via an HTTP request."
    signer = oci.auth.signers.get_resource_principals_signer()
    logging.getLogger().info("URI: " + ctx.RequestURL())
    config = {
        # update with your tenancy's OCID
        "tenancy": "ocid1.bucket.oc1.il-jerusalem-1.aaaaaaaaosgbu7vyfhxi4bgvgswf2cf37j3b4ybaskbhv5vzw4evhlfot7va",
        # replace with the region you are using
        "region": "il-jerusalem-1"
    }
    if (ctx._method == "GET"):
        try:
            object_storage = oci.object_storage.ObjectStorageClient(config, signer=signer)
            namespace = object_storage.get_namespace().data
            # update with your bucket name
            bucket_name = "cloud_seminar_homework"
            file_object_name = ctx.RequestURL()
            if file_object_name.endswith("/"):
                logging.getLogger().info("Adding index.html to reques URL " + file_object_name)
                file_object_name += "index.html"

            # strip off the first character of the URI (i.e. the /)
            file_object_name = file_object_name[1:]

            obj = object_storage.get_object(namespace, bucket_name, file_object_name)
            return response.Response(
                ctx, response_data=obj.data.content,
                headers={"Content-Type": obj.headers['Content-type']}
            )
        except (Exception) as e:
            return response.Response(
                ctx, response_data="500 Server error- GET",
                headers={"Content-Type": "text/plain"}
            )
    else:
        try:
            # Load the OCI config file
            config = oci.config.from_file("/home/jonathan_i/.oci/config")
            # Create an Object Storage client
            object_storage_client = oci.object_storage.ObjectStorageClient(config)
            # Set the namespace and bucket name
            namespace = config["namespace"]
            bucket_name = "cloud_seminar_homework"
            # Set the object name and content
            object_name = 'request_body_' + str(int(time.time())) + '.json'
            object_content = str(data.getvalue())
            # Use the put_object function to upload the object
            object_storage_client.put_object(namespace, bucket_name, object_name, object_content)
            # return a success response
            return {'status': 'success', 'object_name': object_name}
        except (Exception) as e:
            return response.Response(
                ctx, response_data="500 Server error- POST, {0}".format(e),
                headers={"Content-Type": "text/plain"}
            )

    return response.Response(
        ctx, response_data="{0},{1}".format(ctx._method, str(data.getvalue()) ),
        headers={"Content-Type": "text/plain"}
    )

