#!/usr/bin/python3
""" This is the ___init__ magic method for models directory"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()

