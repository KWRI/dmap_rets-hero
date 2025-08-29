# Hello, this file is RETS Hero!

Python is needed to run this successfully, I used python 3.13.3. Docker is optional, is still being worked out fully, so use with caution. Some general things to remember:

* Make sure python 3.13.3 is installed on your system
* Make sure you are working out of the correct directory for everything.

# RETS Client Script: Windows Installation & Run Guide

## Prerequisites

1. **Install Python 3.x**

   - Download and install Python from [python.org](vscode-file://vscode-app/c:/Users/yanir.regev2/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).
   - During installation, check **"Add Python to PATH"**.
2. **Install Git (optional, if you want to clone from a repository)**

   - Download and install Git from [git-scm.com](vscode-file://vscode-app/c:/Users/yanir.regev2/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).
3. **Install pip (if not included with Python)**

   - **Open Command Prompt and run:**
     ```powershell
     python -m ensurepip --upgrade
     ```
4. **Install Tkinter (usually included with Python)**

   - Tkinter is bundled with standard Python installers for Windows. No extra steps are needed.
5. **Install VcXsrv (only if running from Docker and need GUI forwarding)**

   - Download and install [VcXsrv](vscode-file://vscode-app/c:/Users/yanir.regev2/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).

---

## Steps to Install and Run

### 1. **Download or Clone the Script**

- **Clone with Git:**
  ```powershell
  git clone [https://github.com/your-repo/rets-client.git](https://github.com/your-repo/rets-client.git)

  cd rets-client
  ```
- **Or** simply download the script files and place them in a folder, e.g., `C:\rets_client`.

### 2. **(Optional) Create a Virtual Environment**

```powershell
python -m venv venv_name
venv\Scripts\activate
```

### 3. **Install Required Python Packages**

```powershell
pip install rets
```

### 4. **Run the Script**

```powershell
python refindly_rets_v2.py
```

- The Tkinter GUI should appear.
- Fill in the fields or use the provided defaults.

---

## (Optional) Running with Docker

1. **Install Docker Desktop**

   - Download and install from [docker.com](vscode-file://vscode-app/c:/Users/yanir.regev2/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).
2. **Install VcXsrv and Start It**

   - Run XLaunch, select "Multiple windows", display number `0`, and **Disable access control**.
3. **Set DISPLAY Environment Variable**

   - In Command Prompt or PowerShell:

     ```powershell
     set DISPLAY=host.docker.internal:0
     ```
4. **Build the Docker Image**

   ```powershell
   docker build -t rets\_client .
   ```
5. **Run the Docker Container**

   ```powershell
   docker run -it --rm -e DISPLAY=host.docker.internal:0 rets\_client
   ```

---

## Troubleshooting

- If you get a `ModuleNotFoundError`, ensure you installed all required packages.
- If the GUI does not appear when using Docker, ensure VcXsrv is running and `DISPLAY` is set correctly.
- For any authentication or RETS errors, double-check your credentials and server URL.

