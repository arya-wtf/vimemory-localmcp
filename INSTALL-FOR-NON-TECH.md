# Installing Memory Share in Claude Desktop — the easy way

This guide is for **non-technical people**. No coding needed. Just follow each step
exactly. It takes about 10 minutes the first time.

By the end, you'll be able to type *"save this to my memory"* in Claude Desktop,
and later get it back from any AI model.

**Before you start, you need two things from your admin (the person who set up the
server):**

1. The **gateway address** — looks like `https://memory.elux.space`
2. Your **personal API key** — a long code starting with `msk_`

Keep these two handy. You'll paste them in near the end.

---

## Step 1 — Install Python (the engine that runs the connector)

Python is free software the connector needs to run.

**On Mac:**
1. Open the **Terminal** app (press `Cmd + Space`, type "Terminal", hit Enter).
2. Type this and press Enter:
   ```
   python3 --version
   ```
3. If you see a number like `Python 3.11.x`, you already have it — skip to Step 2.
4. If not, go to **python.org/downloads**, download the Mac installer, run it, click through.

**On Windows:**
1. Go to **python.org/downloads**, download the Windows installer.
2. Run it. **IMPORTANT:** on the first screen, tick the box **"Add Python to PATH"**, then click Install.

---

## Step 2 — Get the connector files

Your admin will give you the project folder (`memoryshare`). Two ways:

- **If you got a zip file:** unzip it somewhere easy to find, like your Documents folder.
- **If your admin uses GitHub:** they'll send a link; click the green **Code → Download ZIP** button, then unzip.

Inside, find the folder named **`local-mcp`**. That's the only part you need.
Note where it lives, for example:
- Mac: `/Users/yourname/Documents/memoryshare/local-mcp`
- Windows: `C:\Users\yourname\Documents\memoryshare\local-mcp`

---

## Step 3 — Install the connector's helpers

1. Open **Terminal** (Mac) or **Command Prompt** (Windows — press `Win`, type "cmd", Enter).
2. Type `cd ` (with a space after), then **drag the `local-mcp` folder** into the
   window — it pastes the path for you. Press Enter.
3. Now type this and press Enter:
   ```
   pip install -r requirements.txt
   ```
   Wait for it to finish (it prints a lot — that's normal).

---

## Step 4 — Find your Python location

You'll need this in the next step.

- **Mac:** in Terminal, type `which python3` and press Enter. Copy the line it prints
  (e.g. `/usr/bin/python3`).
- **Windows:** type `where python` and press Enter. Copy the first line
  (e.g. `C:\Users\yourname\AppData\Local\Programs\Python\Python311\python.exe`).

---

## Step 5 — Tell Claude Desktop about the connector

1. Open **Claude Desktop**.
2. Open its settings file. Easiest way:
   - **Mac:** in Finder, press `Cmd + Shift + G`, paste
     `~/Library/Application Support/Claude/` and press Enter.
   - **Windows:** in File Explorer's address bar, paste
     `%APPDATA%\Claude\` and press Enter.
3. Find the file **`claude_desktop_config.json`**.
   - If it's not there, create a new text file with exactly that name.
4. Open it with a plain text editor (TextEdit on Mac, Notepad on Windows).
5. Paste this in, then replace the **four** highlighted bits:

   ```json
   {
     "mcpServers": {
       "memory-share": {
         "command": "PASTE_YOUR_PYTHON_PATH_HERE",
         "args": ["PASTE_PATH_TO_local-mcp/server.py_HERE"],
         "env": {
           "MEMORY_GATEWAY_URL": "PASTE_GATEWAY_ADDRESS_HERE",
           "MEMORY_API_KEY": "PASTE_YOUR_msk_KEY_HERE"
         }
       }
     }
   }
   ```

   - `command` → the Python path from Step 4.
   - `args` → the full path to `server.py` inside `local-mcp`
     (e.g. `/Users/yourname/Documents/memoryshare/local-mcp/server.py`).
   - `MEMORY_GATEWAY_URL` → the gateway address your admin gave you.
   - `MEMORY_API_KEY` → your personal `msk_` key.

   > **Windows paths:** use double backslashes, like
   > `"C:\\Users\\yourname\\Documents\\memoryshare\\local-mcp\\server.py"`.

6. Save the file.

> Already have other things in this file? Just add the `"memory-share": { … }`
> block inside the existing `"mcpServers"` section, separated by a comma.

---

## Step 6 — Restart Claude Desktop

**Fully quit** Claude Desktop (don't just close the window — quit it completely),
then open it again. After it loads, look for the tools icon (🔌). You should see
**memory-share** listed. Done! 🎉

---

## How to use it

Just talk normally in Claude Desktop:

- *"Save this to my memory: we decided Project-X is 500k/month, Pro tier."*
- *"What did we decide about Project-X pricing?"*
- *"List my recent memories."*

To use the same memory in another model (OpenWebUI / ChatGPT), see the separate
OpenWebUI guide your admin has.

---

## If it doesn't show up

- **No "memory-share" in the list:** the config file probably has a typo. Common causes:
  a missing comma, a single `\` instead of `\\` on Windows, or a wrong path. Re-check Step 5.
- **It shows but errors when you use it:** your gateway address or API key is wrong.
  Double-check both with your admin.
- **Still stuck:** send your admin a screenshot — the fix is usually one character.
