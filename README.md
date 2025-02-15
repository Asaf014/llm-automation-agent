# llm-automation-agent
TDS Project-1
# LLM-Based Automation Agent

This project is an automation agent that leverages a Large Language Model (LLM) to process plain-English tasks and execute multi-step operations. It integrates both rule-based and dynamic LLM-based task execution to handle operations and business tasks, such as data processing, file operations, SQL queries, and more.

## Features

- **Phase A: Handle Operations Tasks**
  - **A1:** Install and run a data generation script.
  - **A2:** Format a Markdown file using Prettier.
  - **A3:** Count the number of Wednesdays in a dates list.
  - **A4:** Sort contacts in a JSON file.
  - **A5:** Process log files to extract specific information.
  - **A6:** Index Markdown files based on their H1 headers.
  - **A7:** Extract an email sender from an email file using LLM.
  - **A8:** Extract credit card numbers from images using LLM.
  - **A9:** Find the most similar pair of comments using embeddings.
  - **A10:** Calculate total sales from a SQLite database for a specific ticket type.

- **Phase B: Handle Business Tasks**
  - **B3:** Fetch data from an API and save it.
  - **B4:** Clone a Git repository and make a commit.
  - **B5:** Execute SQL queries on a database.
  - **B6:** Scrape data from a website.
  - **B7:** Compress or resize an image.
  - **B8:** Transcribe audio from an MP3 file.
  - **B9:** Convert Markdown files to HTML.
  - **B10:** Filter a CSV file and return JSON data.

- **Security & Reliability**
  - API key authentication for all endpoints.
  - Safe file operations that prevent unauthorized access.
  - Dynamic execution fallback using an LLM for unrecognized commands.

## Getting Started

### Prerequisites

- Python 3.11 or later
- Docker (optional, for containerization)
- Git

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/llm-automation-agent.git
   cd llm-automation-agent
