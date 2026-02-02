# Session-03-SpecklePy
Basics of SpecklePy

## Getting Started

### 1. Clone this repository

Clone this repo to your PC (make a local copy):

```bash
git clone https://github.com/YOUR_USERNAME/session03-Specklepy.git
```

Or in VSCode (in the Welcome tab), use the option **"Clone Git Repository..."** and provide the URL.

### 2. Install uv (if not already installed)

Open VSCode's terminal and install uv:

```bash
pip install uv
```

### 3. Set up the virtual environment

Navigate to the project folder and sync dependencies:

```bash
cd tower-teachers
uv sync
```

This will:
- Create a virtual environment in `.venv/`
- Install all required packages (`specklepy`, `python-dotenv`)

### 4. Activate the virtual environment

In VSCode, with ">Python: Select Interpreter", select the Python interpreter located at `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (macOS/Linux).

### 5. Verify installation

Run the test script to confirm everything is working:

```bash
python main.py
```

You should see a success message confirming the Speckle client connection.

---

## Authentication

> **IMPORTANT:** To avoid sharing passwords or tokens, the `.gitignore` file already excludes `.env` files and the `.venv/` folder.

### Set up your Speckle token

1. Go to [app.speckle.systems](https://app.speckle.systems). Click your avatar -> **Settings** -> **Developer** -> **Access Tokens**

2. Click **"New Token"**, give it a name and select the required scopes, then copy the token.

3. Copy the `.env.example` file to `.env` in the `tower-teachers` folder:

```bash
cp .env.example .env
```

4. Edit `.env` and replace `your_token_here` with your actual token:

```dotenv
SPECKLE_TOKEN=your_token_here
SPECKLE_SERVER=https://app.speckle.systems
```

5. Run `main.py` to test the authentication.
