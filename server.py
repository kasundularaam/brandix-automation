from flask import Flask, jsonify, render_template
import pandas as pd
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time

app = Flask(__name__)

# Configurable variables
READING_FILE_PATH = 'machines.xlsx'
WRITING_FILE_PATH = 'productions.xlsx'
READING_KEY = 'serialNo'
COLUMNS = ['serialNo', 'operator', 'power', 'productsPerHr', 'location']

last_updated = None


def update_productions():
    global last_updated
    try:
        # Add a small delay to ensure the file system has released the lock
        time.sleep(1)

        # Load READING_FILE_PATH with engine specified
        machines_df = pd.read_excel(READING_FILE_PATH, engine='openpyxl')
        # Strip leading/trailing whitespace from column names
        machines_df.columns = machines_df.columns.str.strip()
        print("Machines DataFrame columns:", machines_df.columns.tolist())

        # Check if WRITING_FILE_PATH exists
        if not os.path.exists(WRITING_FILE_PATH):
            # Create WRITING_FILE_PATH with required columns
            productions_df = pd.DataFrame(columns=COLUMNS)
            productions_df.to_excel(
                WRITING_FILE_PATH, index=False, engine='openpyxl')
        else:
            productions_df = pd.read_excel(
                WRITING_FILE_PATH, engine='openpyxl')
            # Strip leading/trailing whitespace from column names
            productions_df.columns = productions_df.columns.str.strip()
        print("Productions DataFrame columns:",
              productions_df.columns.tolist())

        # Ensure READING_KEY column exists in both DataFrames
        if READING_KEY not in machines_df.columns or READING_KEY not in productions_df.columns:
            raise KeyError(
                f"'{READING_KEY}' column not found in one of the Excel files")

        # Find new rows in READING_FILE_PATH not in WRITING_FILE_PATH
        new_rows = machines_df[~machines_df[READING_KEY].isin(
            productions_df[READING_KEY])]

        if not new_rows.empty:
            # Add the new rows to productions_df with empty columns for operator, power, productsPerHr
            new_rows = new_rows.assign(
                operator='', power='', productsPerHr='')
            productions_df = pd.concat(
                [productions_df, new_rows], ignore_index=True)

            # Save the updated WRITING_FILE_PATH
            productions_df.to_excel(
                WRITING_FILE_PATH, index=False, engine='openpyxl')
            last_updated = time.strftime("%Y-%m-%d %H:%M:%S")
            print("Productions updated successfully with new rows")
        else:
            print("No new rows to update")

    except Exception as e:
        print(f"Error updating {WRITING_FILE_PATH}: {e}")


class Watcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(READING_FILE_PATH):
            print(f"{event.src_path} has been modified")
            update_productions()


def start_watching():
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    observer.join()


@app.route('/start_monitor', methods=['GET'])
def start_monitor():
    threading.Thread(target=start_watching).start()
    return jsonify(message=f"Started monitoring {READING_FILE_PATH} for changes")


@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Load the data from WRITING_FILE_PATH
        productions_df = pd.read_excel(WRITING_FILE_PATH, engine='openpyxl')
        productions_df.columns = productions_df.columns.str.strip()

        # Replace NaN values with empty strings or appropriate values
        productions_df = productions_df.fillna('')

        # Convert DataFrame to dictionary
        data = productions_df.to_dict(orient='records')

        # Include last updated time in the response
        return jsonify(data=data, last_updated=last_updated)
    except Exception as e:
        print(f"Error reading {WRITING_FILE_PATH}: {e}")
        return jsonify(data=[], last_updated="Unknown")


@app.route('/')
def index():
    try:
        productions_df = pd.read_excel(WRITING_FILE_PATH, engine='openpyxl')
        productions_df.columns = productions_df.columns.str.strip()
        data = productions_df.to_dict(orient='records')
    except Exception as e:
        data = []
        print(f"Error reading {WRITING_FILE_PATH}: {e}")

    return render_template('index.html', data=data, last_updated=last_updated)


if __name__ == '__main__':
    app.run(debug=True)
