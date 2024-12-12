import json
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

#json file path
JSON_FILE = 'library.json'

#load books from json file
def load_books():
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return []

#save books to the JSON file
def save_books(books):
    with open(JSON_FILE, 'w') as file:
        json.dump(books, file, indent=4)