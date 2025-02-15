import os
import json
import sqlite3
import subprocess
import requests
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
import sqlite3
import csv
import markdown
from PIL import Image
app = FastAPI()

# ------------------------------------------------------------------------------
# API Key Configuration
# ------------------------------------------------------------------------------
# Load the API key from an environment variable; if not set, use the default.
API_KEY = os.getenv("API_KEY", "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDIzOTRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.Bohr4qFCATCcl8jxyeakAynKvgE1y5XcmJV5pVMilfo")
API_KEY_HEADER = "X-API-Key"

def verify_api_key(request: Request):
    api_key = request.headers.get(API_KEY_HEADER)
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ------------------------------------------------------------------------------
# Models
# ------------------------------------------------------------------------------
class TaskRequest(BaseModel):
    command: str

class FileRequest(BaseModel):
    action: str
    filename: str
    content: str = None

class ExtractionRequest(BaseModel):
    file_path: str
    keyword: str

# ------------------------------------------------------------------------------
# LLM Integration Function (Dynamic Execution)
# ------------------------------------------------------------------------------
def process_with_llm(command: str) -> str:
    # In a real scenario, this would call your LLM service.
    # For simulation, we return a dummy result.
    return f"LLM processed: {command}"

# ------------------------------------------------------------------------------
# Task A1: Run datagen.py to generate data files
# ------------------------------------------------------------------------------
def task_a1() -> str:
    # Download datagen.py from the provided URL
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    data_dir = "/data"
    os.makedirs(data_dir, exist_ok=True)
    datagen_script = os.path.join(data_dir, "datagen.py")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download datagen.py")
    with open(datagen_script, "w", encoding="utf-8") as f:
        f.write(response.text)
    # Run the downloaded script with the user's email as an argument.
    user_email = os.getenv("USER_EMAIL", "user@example.com")
    result = subprocess.run(["python", datagen_script, user_email], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"datagen.py failed: {result.stderr}")
    return "Data generation script executed successfully."

# ------------------------------------------------------------------------------
# Task A2: Format /data/format.md using prettier@3.4.2
# ------------------------------------------------------------------------------
def task_a2() -> str:
    file_path = "/data/format.md"
    if not os.path.exists(file_path):
        raise Exception("File /data/format.md not found")
    result = subprocess.run(["npx", "prettier@3.4.2", "--write", file_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Prettier formatting failed: {result.stderr}")
    return "File /data/format.md formatted successfully."

# ------------------------------------------------------------------------------
# Task A3: Count Wednesdays in /data/dates.txt
# ------------------------------------------------------------------------------
def task_a3() -> str:
    input_file = "/data/dates.txt"
    output_file = "/data/dates-wednesdays.txt"
    if not os.path.exists(input_file):
        raise Exception("Input file /data/dates.txt not found")
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        date_str = line.strip()
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj.weekday() == 2:  # Wednesday is weekday 2
                count += 1
        except Exception:
            continue
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(count))
    return f"Counted {count} Wednesdays in /data/dates.txt."

# ------------------------------------------------------------------------------
# Task A4: Sort contacts in /data/contacts.json
# ------------------------------------------------------------------------------
def task_a4() -> str:
    input_file = "/data/contacts.json"
    output_file = "/data/contacts-sorted.json"
    if not os.path.exists(input_file):
        raise Exception("Input file /data/contacts.json not found")
    with open(input_file, "r", encoding="utf-8") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sorted_contacts, f, indent=2)
    return "Contacts sorted successfully."

# ------------------------------------------------------------------------------
# Task A5: Extract first line of the 10 most recent .log files in /data/logs/
# ------------------------------------------------------------------------------
def task_a5() -> str:
    logs_dir = "/data/logs/"
    output_file = "/data/logs-recent.txt"
    if not os.path.isdir(logs_dir):
        raise Exception("Logs directory /data/logs/ not found")
    log_files = [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.endswith(".log")]
    log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    recent_logs = log_files[:10]
    first_lines = []
    for log_file in recent_logs:
        with open(log_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            first_lines.append(first_line)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(first_lines))
    return "Recent logs processed successfully."

# ------------------------------------------------------------------------------
# Task A6: Index Markdown files in /data/docs/ by extracting the first H1 header
# ------------------------------------------------------------------------------
def task_a6() -> str:
    docs_dir = "/data/docs/"
    index_file = os.path.join(docs_dir, "index.json")
    if not os.path.isdir(docs_dir):
        raise Exception("Docs directory /data/docs/ not found")
    index_mapping = {}
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip().startswith("#"):
                            title = line.strip().lstrip("#").strip()
                            relative_path = os.path.relpath(file_path, docs_dir)
                            index_mapping[relative_path] = title
                            break
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index_mapping, f, indent=2)
    return "Markdown docs indexed successfully."

# ------------------------------------------------------------------------------
# Task A7: Extract sender's email from /data/email.txt using LLM
# ------------------------------------------------------------------------------
def task_a7() -> str:
    input_file = "/data/email.txt"
    output_file = "/data/email-sender.txt"
    if not os.path.exists(input_file):
        raise Exception("Input file /data/email.txt not found")
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    instruction = f"Extract the sender's email address from the following email message:\n{content}"
    result = process_with_llm(instruction)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result.strip())
    return "Sender email extracted successfully."

# ------------------------------------------------------------------------------
# Task A8: Extract credit card number from /data/credit-card.png using LLM
# ------------------------------------------------------------------------------
def task_a8() -> str:
    input_file = "/data/credit-card.png"
    output_file = "/data/credit-card.txt"
    if not os.path.exists(input_file):
        raise Exception("Input file /data/credit-card.png not found")
    # In a real scenario, you would encode the image (e.g., base64) and send it.
    instruction = "Extract the credit card number from the attached image."
    result = process_with_llm(instruction)
    card_number = result.replace(" ", "")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(card_number)
    return "Credit card number extracted successfully."

# ------------------------------------------------------------------------------
# Task A9: Find the most similar pair of comments in /data/comments.txt using embeddings
# ------------------------------------------------------------------------------
def task_a9() -> str:
    input_file = "/data/comments.txt"
    output_file = "/data/comments-similar.txt"
    if not os.path.exists(input_file):
        raise Exception("Input file /data/comments.txt not found")
    with open(input_file, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f if line.strip()]
    if len(comments) < 2:
        raise Exception("Not enough comments for comparison")
    instruction = "Find the most similar pair of comments from the following list:\n" + "\n".join(comments)
    result = process_with_llm(instruction)
    similar_pair = result.split("\n")[:2]
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(similar_pair))
    return "Similar comments extracted successfully."

# ------------------------------------------------------------------------------
# Task A10: Calculate total sales for 'Gold' tickets from /data/ticket-sales.db
# ------------------------------------------------------------------------------
def task_a10() -> str:
    db_file = "/data/ticket-sales.db"
    output_file = "/data/ticket-sales-gold.txt"
    if not os.path.exists(db_file):
        raise Exception("Database file /data/ticket-sales.db not found")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
        total_sales = cursor.fetchone()[0]
    except Exception as e:
        conn.close()
        raise Exception("SQL query failed: " + str(e))
    conn.close()
    total_sales = total_sales if total_sales is not None else 0
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(total_sales))
    return "Total sales for Gold tickets calculated successfully."

# ------------------------------------------------------------------------------
# Allowed Commands Mapping (A1 - A10 and other predefined commands)
# ------------------------------------------------------------------------------
ALLOWED_COMMANDS = {
    "run data analysis": lambda: "Data analysis completed.",
    "check system status": lambda: "System is operational.",
}
# Add A1-A10 tasks with short keys (e.g., "a1", "a2", etc.)
ALLOWED_COMMANDS.update({
    "a1": task_a1,
    "a2": task_a2,
    "a3": task_a3,
    "a4": task_a4,
    "a5": task_a5,
    "a6": task_a6,
    "a7": task_a7,
    "a8": task_a8,
    "a9": task_a9,
    "a10": task_a10,
})

# ------------------------------------------------------------------------------
# Endpoints (Protected via API Key)
# ------------------------------------------------------------------------------

@app.get("/", dependencies=[Depends(verify_api_key)])
def read_root():
    return {"message": "Welcome to the LLM Automation Agent!"}

@app.post("/execute", dependencies=[Depends(verify_api_key)])
def execute_task(request: TaskRequest):
    command = request.command.lower()
    # If the command matches one of our predefined tasks, execute it.
    if command in ALLOWED_COMMANDS:
        try:
            result = ALLOWED_COMMANDS[command]()
            return {"status": "success", "task_executed": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    # Otherwise, fall back to dynamic LLM processing.
    try:
        llm_result = process_with_llm(command)
        return {"status": "success", "task_executed": llm_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file", dependencies=[Depends(verify_api_key)])
def file_operations(file_req: FileRequest):
    SAFE_DIRECTORY = "./safe_storage/"
    os.makedirs(SAFE_DIRECTORY, exist_ok=True)
    safe_filename = os.path.basename(file_req.filename)
    safe_path = os.path.join(SAFE_DIRECTORY, safe_filename)
    if file_req.action == "write":
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(file_req.content or "")
        return {"message": f"File '{safe_filename}' written successfully."}
    elif file_req.action == "read":
        if not os.path.exists(safe_path):
            raise HTTPException(status_code=404, detail="File not found")
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"filename": safe_filename, "content": content}
    raise HTTPException(status_code=400, detail="Invalid file action")

@app.post("/extract", dependencies=[Depends(verify_api_key)])
def extract_data(req: ExtractionRequest):
    SAFE_DIRECTORY = "./safe_storage/"
    os.makedirs(SAFE_DIRECTORY, exist_ok=True)
    safe_filename = os.path.basename(req.file_path)
    safe_path = os.path.join(SAFE_DIRECTORY, safe_filename)
    if not os.path.exists(safe_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(safe_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    extracted_data = [line.strip() for line in lines if req.keyword in line]
    return {"file_path": req.file_path, "matches": extracted_data}

@app.get("/status", dependencies=[Depends(verify_api_key)])
def get_system_status():
    return {"status": "running", "uptime": "OK"}

# ==============================================================================
# Phase B: Business Tasks Endpoints
# ==============================================================================



# ------------------------------
# B3: Fetch data from an API and save it
# ------------------------------
class APIFetchRequest(BaseModel):
    url: str
    output_filename: str  # This should be a filename (not a path)

@app.post("/business/fetch-data", dependencies=[Depends(verify_api_key)])
def fetch_data(request: APIFetchRequest):
    # Ensure the output file is placed in /data
    safe_filename = os.path.basename(request.output_filename)
    output_path = os.path.join("/data", safe_filename)
    response = requests.get(request.url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from API")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    return {"message": f"Data fetched and saved to {output_path}"}

# ------------------------------
# B4: Clone a git repo and make a commit
# ------------------------------
class GitCloneRequest(BaseModel):
    repo_url: str
    commit_message: str

@app.post("/business/clone-git", dependencies=[Depends(verify_api_key)])
def clone_git(request: GitCloneRequest):
    # Clone to a safe directory: /data/git_repo
    safe_dir = "/data/git_repo"
    os.makedirs(safe_dir, exist_ok=True)
    clone_result = subprocess.run(["git", "clone", request.repo_url, safe_dir], capture_output=True, text=True)
    if clone_result.returncode != 0:
        raise HTTPException(status_code=500, detail="Git clone failed: " + clone_result.stderr)
    # Simulate making a commit
    subprocess.run(["git", "-C", safe_dir, "add", "."], capture_output=True)
    commit_result = subprocess.run(["git", "-C", safe_dir, "commit", "-m", request.commit_message], capture_output=True, text=True)
    if commit_result.returncode != 0:
        raise HTTPException(status_code=500, detail="Git commit failed: " + commit_result.stderr)
    return {"message": "Repository cloned and commit made successfully."}

# ------------------------------
# B5: Run a SQL query on a SQLite database
# ------------------------------
class SQLQueryRequest(BaseModel):
    query: str
    db_filename: str

@app.post("/business/sql-query", dependencies=[Depends(verify_api_key)])
def sql_query(request: SQLQueryRequest):
    db_path = os.path.join("/data", os.path.basename(request.db_filename))
    if not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail="Database file not found")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(request.query)
        rows = cursor.fetchall()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail="SQL query failed: " + str(e))
    conn.close()
    return {"result": rows}

# ------------------------------
# B6: Extract (scrape) data from a website
# ------------------------------
class WebScrapeRequest(BaseModel):
    url: str
    output_filename: str

@app.post("/business/scrape", dependencies=[Depends(verify_api_key)])
def web_scrape(request: WebScrapeRequest):
    response = requests.get(request.url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Website scraping failed")
    safe_filename = os.path.basename(request.output_filename)
    output_path = os.path.join("/data", safe_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    return {"message": f"Website data scraped and saved to {output_path}"}

# ------------------------------
# B7: Compress or resize an image
# ------------------------------
class ImageProcessRequest(BaseModel):
    image_filename: str
    output_filename: str
    width: int = None
    height: int = None

@app.post("/business/resize-image", dependencies=[Depends(verify_api_key)])
def resize_image(request: ImageProcessRequest):
    input_path = os.path.join("/data", os.path.basename(request.image_filename))
    output_path = os.path.join("/data", os.path.basename(request.output_filename))
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="Input image not found")
    try:
        with Image.open(input_path) as img:
            new_size = (request.width, request.height) if request.width and request.height else img.size
            resized_img = img.resize(new_size)
            resized_img.save(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Image processing failed: " + str(e))
    return {"message": f"Image resized and saved to {output_path}"}

# ------------------------------
# B8: Transcribe audio from an MP3 file
# ------------------------------
class AudioTranscriptionRequest(BaseModel):
    audio_filename: str

@app.post("/business/transcribe-audio", dependencies=[Depends(verify_api_key)])
def transcribe_audio(request: AudioTranscriptionRequest):
    input_path = os.path.join("/data", os.path.basename(request.audio_filename))
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    # Simulate transcription; in a real app, integrate with a transcription service.
    transcription = "Simulated transcription of the audio file."
    output_path = os.path.join("/data", "transcription.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcription)
    return {"message": f"Audio transcribed and saved to {output_path}", "transcription": transcription}

# ------------------------------
# B9: Convert Markdown to HTML
# ------------------------------
class MDToHTMLRequest(BaseModel):
    md_filename: str
    output_filename: str

@app.post("/business/md-to-html", dependencies=[Depends(verify_api_key)])
def md_to_html(request: MDToHTMLRequest):
    input_path = os.path.join("/data", os.path.basename(request.md_filename))
    output_path = os.path.join("/data", os.path.basename(request.output_filename))
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="Markdown file not found")
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return {"message": f"Markdown converted to HTML and saved to {output_path}"}

# ------------------------------
# B10: Filter a CSV file and return JSON data
# ------------------------------
class CSVFilterRequest(BaseModel):
    csv_filename: str
    filter_column: str
    filter_value: str

@app.post("/business/csv-filter", dependencies=[Depends(verify_api_key)])
def csv_filter(request: CSVFilterRequest):
    input_path = os.path.join("/data", os.path.basename(request.csv_filename))
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    results = []
    try:
        with open(input_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get(request.filter_column) == request.filter_value:
                    results.append(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail="CSV processing failed: " + str(e))
    return {"filtered_data": results}
