
# Tasks Called Tasks

Welcome to the **Tasks Called Tasks** repository!

----------

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Abdul-Ikram/Tasks-Called-Tasks.git
cd Tasks-Called-Tasks
```

### 2. Set Up the Environment

#### Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # For macOS/Linux
.venv\Scripts\activate     # For Windows
```

#### Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py makemigrations && python manage.py migrate
```

### 4. Run the Server

```bash
python manage.py runserver
```

----------

## Postman Collection

To test the APIs, use the provided Postman collection.

1.  **Download the Postman Collection:**  
    The Postman collection file is located [here](https://github.com/Abdul-Ikram/Tasks-Called-Tasks/blob/main/PostDock/tasks_called_tasks.postman_collection.json).
    
2.  **Import the Collection:**
    -   Open Postman.
    -   Click on `File > Import`.
    -   Select the `Boilerplates.postman_collection.json` file.

3.  **Environment Variables (Optional):**  
    Configure Postman variables to handle dynamic URLs and tokens.
    
    ```bash
    Key: boilerAccessToken
    Value: <Your access token>
    ```
    
----------

## Contributing

1.  Fork the repository.
2.  Create a new branch for your feature:
    
    ```bash
    git checkout -b feature/new-api
    ```
    
3.  Commit your changes:
    
    ```bash
    git commit -m "Add new API for <feature>"
    ```
    
4.  Push to your branch:
    
    ```bash
    git push origin feature/new-api
    ```
    
5.  Submit a pull request.

----------
