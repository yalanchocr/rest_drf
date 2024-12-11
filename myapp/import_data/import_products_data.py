import csv
import os
import zipfile
import shutil
import pandas as pd
from django.db import transaction
from django.core.files import File
from myapp.models import Product  # Replace with your actual model import


def handle_batch_import_excel(task_id, zip_file_path):
    try:
        extract_dir = os.path.join('/tmp', str(task_id))

        # Extract the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Identify Excel files
        excel_files = [f for f in os.listdir(extract_dir) if f.endswith('.xlsx')]

        # Check the number of Excel files
        if len(excel_files) != 1:
            raise ValueError(f"Expected exactly one Excel file, but found {len(excel_files)} Excel files")

        # Read the Excel file
        excel_file_path = os.path.join(extract_dir, excel_files[0])
        df = pd.read_excel(excel_file_path)

        # Check the required fields in the DataFrame
        if not all(field in df.columns for field in ['name', 'price', 'in_stock', 'photo_name']):
            raise ValueError("Excel file is missing required fields")

        # Start an atomic transaction
        with transaction.atomic():
            for index, row in df.iterrows():
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