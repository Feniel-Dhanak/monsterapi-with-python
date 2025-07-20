import os
import sys
import webbrowser

file_path = sys.argv[1]

if os.path.exists(file_path):
    webbrowser.open(file_path)
    print("\nFile accessed")
else:
    print("File not found!")