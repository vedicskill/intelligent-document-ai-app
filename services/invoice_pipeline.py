# services
from services.file_handler import (
    is_pdf,
    is_req_file_type,
    convert_pdf_to_base64_images,
    encode_image_base64
)
from services.vision_service import extract_text_from_image
from services.extraction_service import extraction_model
from models.invoice_model import Invoice
from services.storage_service import insert_one_invoice_document
from prompts.invoice_prompts import invoice_extract_prompt

import os
from pathlib import Path
from pydantic import ValidationError
from fastapi import UploadFile, HTTPException


def process_invoice_document(file_path: str) -> dict:
    
    # 1. Convert to base64 images
    if is_pdf(file_path):
        base64_images = convert_pdf_to_base64_images(file_path)
    else:
        base64_images = encode_image_base64(file_path)

    print("INFO: Sucessfully converted document into base64 image format")
    # 2. Text Extraction (Image → Text)
    invoice_text = extract_text_from_image(base64_images)
    print("INFO: Sucessfully extract text from Image")
    # 3. Structures extraction (Text → JSON)
    llm = extraction_model()
    chain = invoice_extract_prompt | llm
    response = chain.invoke(
        {
            "invoice_text": invoice_text

        }
    )
    print("INFO: Extract entities from text")
    # 4. Validate using Pydantic
    try:
        validation_invoice = Invoice.model_validate_json(response.content)
        # validation_invoice is an pydantic object
    except ValidationError as e:
        print("Pydantic Validation error \n", e)
        raise HTTPException(
            status_code=422,
            details = "Invoice validation failed: Extract data is invalid"
        )
    print("INFO: Sucessfully validated pydantic data model")
    # Insert into MongoDB
    inserted_id  = insert_one_invoice_document(
        invoice_data=validation_invoice.model_dump(),
        base64_images=base64_images
    )
    print("INFO: Sucessfully saved document in mongodb")
    # Response data
    response_data = {
        "invoice": validation_invoice.model_dump(),
        "images": base64_images,
        "mongo_id": inserted_id
    }

    return response_data




def process_invoice(upload_file: UploadFile) -> dict:

    file_path = None
    try:
            
        # 1. Validate the data type of upload file
        # pdf, image (png, jpg and jpeg)
        filename = upload_file.filename

        if not is_req_file_type(filename):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Only PDF, PNG, JPG, JPEG allowed"
            )
        
        print(f"File validated sucessfully: {filename}")

        # 2. Save this file in temporary folder in static
        temp_dir = Path('static/temp')
        temp_dir.mkdir(exist_ok=True)

        file_path = temp_dir.joinpath(filename)
        # save the file
        with open(file_path, "wb") as buffer:
            buffer.write(upload_file.file.read())

        print(f"File saved temporarily at {file_path}")

        # 3. Process invoice
        file_path_str = file_path.as_posix()
        response_data = process_invoice_document(file_path_str)

        # print("Response =", response_data)

        return response_data
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing the document"
        )
    
    finally:
        if file_path:
            try:
                # clean the temporary file
                if file_path and file_path.exists():
                    os.remove(file_path)
                    print("Temporary file is removed")
            except Exception as clean_error:
                print(f"Warning: cleanup failed", clean_error)