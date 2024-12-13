import csv
import os
import zipfile
import shutil
import pandas as pd
from django.db import transaction
from django.core.files import File
from myapp.models import Product  # Replace with your actual model import
from django.conf import settings
from typing import List, Dict

REQUIRED_FIELDS = ['name', 'price', 'in_stock', 'photo_name']


def handle_batch_import_excel(task_id: str, zip_file_path: str) -> Dict:
    log: List[str] = []
    success_count = 0
    error_count = 0
    problem_rows: List[int] = []
    extract_dir = os.path.join('/tmp', settings.APP_NAME, str(task_id))

    try:
        # Extract the zip file
        extract_dir = extract_zip_file(zip_file_path, extract_dir)

        # Identify and validate Excel file
        excel_file_path = find_excel_file(extract_dir)

        # Read and validate the Excel file
        df = read_and_validate_excel(excel_file_path)

        # Start an atomic transaction

        for index, row in df.iterrows():
            with transaction.atomic():
                num_row = index + 2  # Adjust for header
                try:
                    process_row(row, extract_dir)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    problem_rows.append(num_row)
                    log.append(f"Row {num_row}: Error - {e}")

        return build_response(success_count, error_count, problem_rows, log)

    except Exception as e:
        log.append(f"Error during batch import: {e}")
        return build_response(success_count, error_count, problem_rows, log, str(e))

    finally:
        clean_up(zip_file_path, extract_dir)


def extract_zip_file(zip_file_path: str, extract_dir: str) -> str:
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    return extract_dir


def find_excel_file(extract_dir: str) -> str:
    excel_files = [f for f in os.listdir(extract_dir) if f.endswith('.xlsx')]
    if len(excel_files) != 1:
        raise ValueError(f"Expected exactly one Excel file, but found {len(excel_files)}")
    return os.path.join(extract_dir, excel_files[0])


def read_and_validate_excel(excel_file_path: str) -> pd.DataFrame:
    df = pd.read_excel(excel_file_path)
    if not all(field in df.columns for field in REQUIRED_FIELDS):
        raise ValueError(f"Excel file is missing required fields: {REQUIRED_FIELDS}")
    return df.where(pd.notna(df), None)


def process_row(row: pd.Series, extract_dir: str) -> None:
    name = row['name']
    price = row['price'] if not pd.isna(row['price']) else None
    in_stock = str(row['in_stock']).lower() == 'true' if row['in_stock'] else None
    photo_name = row['photo_name']

    # Validate fields
    if not name or not price or photo_name is None:
        raise ValueError(f"Invalid data in row: {row.to_dict()}")

    # Validate and save the product
    product = Product(name=name, price=price, in_stock=in_stock)
    photo_path = os.path.join(extract_dir, 'images', photo_name)
    if not os.path.exists(photo_path):
        raise ValueError(f"Photo file '{photo_name}' not found")
    with open(photo_path, 'rb') as photo_file:
        product.photo.save(photo_name, File(photo_file), save=True)


def build_response(success_count: int, error_count: int, problem_rows: List[int], log: List[str], msg_err: str = "") -> Dict:
    return {
        "status": "success" if error_count == 0 else "failed",
        "success_count": success_count,
        "error_count": error_count,
        "problem_rows": problem_rows,
        "msg_err": msg_err,
        "log": log,
    }


def clean_up(zip_file_path: str, extract_dir: str) -> None:
    try:
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
    except Exception as e:
        print(f"Error during cleanup: {e}")

# def handle_batch_import_excel(task_id, zip_file_path):
#     log = []
#     success_count = 0
#     error_count = 0
#     problem_rows = []
#
#     try:
#         extract_dir = os.path.join('/tmp', settings.APP_NAME, str(task_id))
#
#         # Extract the zip file
#         with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#             zip_ref.extractall(extract_dir)
#
#         # Identify Excel files
#         excel_files = [f for f in os.listdir(extract_dir) if f.endswith('.xlsx')]
#
#         # Check the number of Excel files
#         if len(excel_files) != 1:
#             raise ValueError(f"Expected exactly one Excel file, but found {len(excel_files)} Excel files")
#
#         # Read the Excel file
#         excel_file_path = os.path.join(extract_dir, excel_files[0])
#         df = pd.read_excel(excel_file_path)
#
#         # Check the required fields in the DataFrame
#         if not all(field in df.columns for field in ['name', 'price', 'in_stock', 'photo_name']):
#             raise ValueError("Excel file is missing required fields")
#
#         df = df.where(pd.notna(df), None)
#
#         for index, row in df.iterrows():
#             # Start an atomic transaction
#             with transaction.atomic():
#                 num_row= index + 2 #header and start from 1 instead of 0
#                 try:
#                     name = row['name']
#                     price = row['price'] if not pd.isna(row['price']) else None
#                     in_stock = row['in_stock'] == 'True'
#                     photo_name = row['photo_name']
#
#                     # Validate and save the product
#                     if not name or not price or photo_name is None:
#                         raise ValueError(f"Invalid data in row: {row}")
#
#                     product = Product(name=name, price=price, in_stock=in_stock)
#                     photo_path = os.path.join(extract_dir, 'images', photo_name)
#                     if not os.path.exists(photo_path):
#                         raise ValueError(f"Photo file '{photo_name}' not found")
#
#                     with open(photo_path, 'rb') as photo_file:
#                         product.photo.save(photo_name, File(photo_file), save=True)
#                     success_count += 1
#
#                 except Exception as e:
#                     error_count += 1
#                     problem_rows.append(num_row)
#                     log.append(f"Row {num_row}: Error - {e}")
#
#         return {
#             "status": "success" if error_count == 0 else "failed",
#             "success_count": success_count,
#             "error_count": error_count,
#             "problem_rows": problem_rows,
#             "msg_err": "",
#             "log": log
#         }
#
#     except Exception as e:
#         # Log the error
#         print(f"Error during batch import: {e}")
#         return {
#             "status": "failed",
#             "success_count": success_count,
#             "error_count": error_count,
#             "problem_rows": problem_rows,
#             "msg_err": e,
#             "log": log
#         }
#
#     finally:
#         # Clean up the zip file and the extracted directory
#         if os.path.exists(zip_file_path):
#             os.remove(zip_file_path)
#         if os.path.exists(extract_dir):
#             shutil.rmtree(extract_dir)

def handle_batch_import(task_id, zip_file_path):
    try:
        extract_dir = os.path.join('/tmp', str(task_id))

        # Extract the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Identify CSV files
        csv_files = [f for f in os.listdir(extract_dir) if f.endswith('.csv')]

        # Check the number of CSV files
        if len(csv_files) != 1:
            raise ValueError(f"Expected exactly one CSV file, but found {len(csv_files)} CSV files")

        # Read the CSV file
        csv_file_path = os.path.join(extract_dir, csv_files[0])


        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if not all(field in reader.fieldnames for field in ['name', 'price', 'in_stock', 'photo_name']):
                raise ValueError("CSV file is missing required fields")

            # Start an atomic transaction
            with transaction.atomic():
                for row in reader:
                    name = row['name']
                    price = row['price']
                    in_stock = row['in_stock'] == 'True'
                    photo_name = row['photo_name']

                    # Validate and save the product
                    if not name or not price or photo_name is None:
                        raise ValueError(f"Invalid data in row: {row}")

                    product = Product(name=name, price=price, in_stock=in_stock)
                    photo_path = os.path.join(extract_dir, 'images', photo_name)
                    if not os.path.exists(photo_path):
                        raise ValueError(f"Photo file '{photo_name}' not found")

                    with open(photo_path, 'rb') as photo_file:
                        product.photo.save(photo_name, File(photo_file), save=True)

        return "Import successful"

    except Exception as e:
        # Log the error
        print(f"Error during batch import: {e}")
        return f"Error: {e}"

    finally:
        # Clean up the zip file and the extracted directory
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)


def handle_batch_import_simple(task_id, zip_file_path):
    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        extract_dir = os.path.join('/tmp', str(task_id))
        zip_ref.extractall(extract_dir)

    # Read the CSV file
    csv_file_path = os.path.join(extract_dir, 'data.csv')
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            price = row['price']
            in_stock = row['in_stock'] == 'True'
            photo_name = row['photo_name']

            # Save the product
            product = Product(name=name, price=price, in_stock=in_stock)
            photo_path = os.path.join(extract_dir, 'photos', photo_name)
            with open(photo_path, 'rb') as photo_file:
                product.photo.save(photo_name, File(photo_file), save=True)

    # Clean up
    os.remove(zip_file_path)
    os.rmdir(extract_dir)