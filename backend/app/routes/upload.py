from fastapi import APIRouter, UploadFile
import shutil
import os

from ..services.ingestion import load_csv
from ..services.profiling import generate_metadata
from ..services.embeddings import get_embedding
from ..services.search import add_to_index
from ..db_utils import save_dataset

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load data
    df = load_csv(file_path)

    # Generate metadata + summary (LLM)
    metadata, summary = generate_metadata(df, file.filename)

    # Save in database
    save_dataset(file.filename, summary)

    # DATASET EMBEDDING
    dataset_text = f"""
        Dataset Name: {metadata['name']}

        This dataset contains customer information including age, income, and spending behavior.

        It can be used for:
        - Customer segmentation
        - Marketing analysis
        - Customer behavior analysis
        - Identifying high value customers
        """
    dataset_embedding = get_embedding(summary)
    add_to_index(dataset_embedding, metadata, level="dataset")

    # COLUMN EMBEDDINGS (IMPORTANT)
    for col in metadata["column_details"]:
        col_text = f"""
            Column Name: {col['name']}

            This column represents {col['name']} in a customer dataset.

            Possible meaning:
            - Used for customer analysis
            - Helps in segmentation and behavior understanding

            Data type: {col['dtype']}
            Missing values: {col['missing']}
            """
        col_embedding = get_embedding(col_text)

        add_to_index(col_embedding, col, level="column")

    return {
        "message": "File processed successfully",
        "dataset_name": file.filename,
        "columns_indexed": len(metadata["column_details"])
    }