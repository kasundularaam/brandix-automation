# 🌟 BRANDIX-AUTOMATION 🌟

## 📄 Project Overview

BRANDIX-AUTOMATION is a project designed to automate the data collection process for production machines. The system monitors changes in a specified Excel file (`machines.xlsx`) and updates another Excel file (`productions.xlsx`) accordingly. This ensures that the production data is always up-to-date and accurately reflects the current state of the machines.

## 🎯 Purpose

The primary purpose of this project is to streamline and automate the data collection process, reducing manual effort and minimizing the chances of human error. By using this automated system, production data can be collected and updated in real-time, ensuring high accuracy and efficiency.

## 🚀 Features

- **Real-time Monitoring:** The system continuously monitors changes to the `machines.xlsx` file.
- **Automated Data Update:** Automatically updates the `productions.xlsx` file with new data from `machines.xlsx`.
- **Web Interface:** Provides a web interface to view the latest production data and the last updated time.
- **Easy Configuration:** File paths and key columns can be easily configured.

## 📁 Project Structure

```
BRANDIX-AUTOMATION/
│
├── app.py                     # Main Flask application
├── templates/
│   └── index.html             # HTML template for the web interface
├── venv/                      # Virtual environment directory
├── requirements.txt           # Required Python packages
└── README.md                  # Project documentation
```

## ⚙️ Installation

1. Clone the repository:

```sh
git clone https://github.com/kasundularaam/brandix-automation.git
cd brandix-automation
```

2. Create a virtual environment:

```sh
python -m venv venv
```

3. Activate the virtual environment:

```sh
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install the required packages:

```sh
pip install -r requirements.txt
```

## 🛠️ Usage

1. Start the Flask server:

```sh
python app.py
```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. To start monitoring the `machines.xlsx` file for changes, send a GET request to `http://127.0.0.1:5000/start_monitor`.

## 📝 Configuration

- **File Paths:** Update the paths for the reading and writing Excel files by modifying the `READING_FILE_PATH` and `WRITING_FILE_PATH` variables in `app.py`.
- **Key Column:** Update the key column for identifying unique rows by modifying the `READING_KEY` variable in `app.py`.

## 📦 Requirements

The `requirements.txt` file lists all the Python packages required to run the project:

```
Flask==2.1.1
pandas==1.4.2
openpyxl==3.0.9
watchdog==2.1.9
```

## 👤 Author

- [Kasun Dulara (Berry)](https://github.com/kasundularaam)

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
