# Text to SQL with Teradata MCP

A command-line demo that answers questions about synthetic data stored in Teradata Vantage. It uses an OpenAI-compatible LLM endpoint to generate SQL, runs that SQL through the Teradata MCP server, then asks the model to summarize the returned rows.

## Prerequisites

- Python and a working project virtual environment
- Access to a ClearScape Analytics environment with Vantage credentials
- Permission to create and load tables in the target database
- A read-only Vantage account for MCP queries
- Teradata MCP server
- An OpenAI-compatible LLM endpoint, such as local Ollama

## 1. Configure the project

Copy `.env.example` to `.env` in the project root:

```powershell
Copy-Item .env.example .env
```

Fill in the values using credentials and connection details provided for your ClearScape Analytics environment. 

Example settings:

```dotenv
# Used by the data loader
TD_HOST=host
TD_USER=username
TD_PASSWORD=my_variable

# Used by the Teradata MCP server
DATABASE_URI=teradata://TD_USER:TD_PASSWORD@TD_HOST:1025/TD_USER
MCP_TRANSPORT=streamable-http
MCP_PORT=8001
PROFILE=base
DEFAULT_ROW_LIMIT=100
MAX_ROW_LIMIT=1000

# Used by the Python app to connect to TD MCP
MCP_URL=http://localhost:8001/mcp

# Used by the Python app to connect to an OpenAI-compatible LLM
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=qwen3:4b
```

## 2. Load the synthetic data

Activate the project virtual environment, then run:

```powershell
python -m app.load_data
```

The loader reads the workbook configured in `app/load_data.py` and creates or replaces the listed tables in Vantage. 
## 3. Install Teradata MCP

Install `uv`, then the Teradata MCP server:

```powershell
pip install uv
uv tool install teradata-mcp-server
```

## 4. load mcp variables into process environment and start the server 
Open a separate PowerShell terminal in the project root, where `.env` is located. The Teradata MCP server reads a `.env` file from its current working directory. Start it with HTTP transport:

```powershell
Get-Content .env | Where-Object { $_ -match '^[A-Za-z_][A-Za-z0-9_]*=' } | ForEach-Object {
    $name, $value = $_ -split '=', 2
    [Environment]::SetEnvironmentVariable($name, $value, 'Process')
}
```
## 4. Start the Teradata MCP server

Open a separate PowerShell terminal in the project root, where `.env` is located. The Teradata MCP server reads a `.env` file from its current working directory. Start it with HTTP transport:

```powershell
teradata-mcp-server --mcp_transport streamable-http --mcp_port 8001
```

Leave this terminal running. Confirm the startup output indicates `streamable-http`, not `stdio`. If the server reports that `DATABASE_URI` is missing, check that `.env` is in the current directory and contains a complete URI with the real host and database values. Do not use variable references such as `${TD_HOST}` inside `DATABASE_URI`.

The server configuration and transport options are documented in the [Teradata MCP configuration guide](https://github.com/Teradata/teradata-mcp-server/blob/main/docs/server_guide/CONFIGURATION.md).

## 5. Configure and start the LLM

This example uses Ollama
```powershell
ollama run qwen3:4b
```

Check that Ollama is responding:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

The model shown by Ollama must match `LLM_MODEL` in `.env`. If you use a different OpenAI-compatible service, set `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL` to that provider’s values.

## 6. Test the app

Keep the MCP server running and ensure Ollama is available. 
Then run the question-answering app:

```powershell
python -m app.ask
```

Enter a question answerable from the loaded data. The app should generate SQL, send it through MCP to Vantage, and print an answer based on the returned rows.


Question example: What is the iscore for customer id =1046?
