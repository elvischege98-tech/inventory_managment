# Inventory Management System

A Python Flask REST API for managing inventory items.

The application also integrates with the Open Food Facts API to retrieve product information using a barcode.

## Features

- View all inventory items
- Find an inventory item by ID
- Add inventory items
- Update inventory items using PUT
- Partially update inventory items using PATCH
- Delete inventory items
- Search Open Food Facts by barcode
- Command-line interface
- Automated unit tests
- Mocked external API tests

## Technologies

- Python
- Flask
- Requests
- Pytest
- unittest.mock
- Open Food Facts API

## Installation

Create a virtual environment:

```bash
python -m venv venv