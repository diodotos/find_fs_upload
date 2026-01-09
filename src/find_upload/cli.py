import argparse
from google.cloud.firestore import Client

def parse_args():
    # one required positional argument: record id
    parser = argparse.ArgumentParser()
    parser.add_argument("record_id", type=str, help="The ID of the record to find upload information for")
    return parser.parse_args()

def main():
    args = parse_args()
    record_id = args.record_id

    db = Client()

    uploader_id = db.collection("records").document(record_id).get().to_dict().get("uploaded_by", None)
    if not uploader_id:
        print("No uploader found for record")
        return

    try:
        uploader_info = db.collection("users").document(uploader_id).get().to_dict()
    except Exception as e:
        print(f"Error getting uploader info: {e}")
        return

    print(f"""\
Uploaded by:

Name: {uploader_info.get("name", "Unknown")}
Email: {uploader_info.get("email", "Unknown")}
Company: {uploader_info.get("associated_company", "Unknown")}
"""
)