from db.mongodb import db
from typing import List
from datetime import datetime # use it for inserted data
# import datetime
from bson import ObjectId


def insert_one_invoice_document(
    invoice_data: dict,
    base64_images: List[str],
    collection="invoice"
):
    # update base64_image, create into invoice_data
    invoice_data['base64_images'] = base64_images
    invoice_data['inserted_date'] = datetime.utcnow() # UTC timestamp
    # create the collection
    collection = db[collection]
    # insert the data
    result = collection.insert_one(invoice_data)

    return str(result.inserted_id)

# fetch all invoice documents from mongodb
def fetch_all_invoices(collection='invoice'):

    col = db[collection]

    documents = list(col.find().sort('inserted_date',-1)) # -1 is decending 

    # convert object_id to string 
    for doc in documents:
        doc['id'] = str(doc['_id'])

    return documents

# fetch invoice by id
def fetch_invoice_by_id(invoice_id: str, collection="invoice"):
    col = db[collection]

    document = col.find_one({'_id': ObjectId(invoice_id)})
    
    document['_id'] = str(document['_id'])

    return document
