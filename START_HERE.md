# 🚀 START HERE - Super Simple Guide

## 📁 Step 1: Create These 2 Files

You need to **manually create** these files in your project folder:

### **File 1: `run.sh` (for Linux/Mac)** or **`run.bat` (for Windows)**

Copy the content I provided above into these files.

### **File 2: `test.sh` (for Linux/Mac)** or **`test.bat` (for Windows)**

Copy the content I provided above into these files.

---

## 🎯 Step 2: Choose Your Operating System

### **🐧 LINUX / MAC USERS - Follow This:**

#### **A. Make scripts executable:**
```bash
chmod +x run.sh test.sh setup.sh
```

#### **B. Run setup (ONE TIME ONLY):**
```bash
./setup.sh
```
**OR if that doesn't work:**
```bash
bash setup.sh
```

#### **C. Start the application:**
```bash
./run.sh
```
**OR:**
```bash
bash run.sh
```

#### **D. Open browser:**
Go to: `http://localhost:5000`

#### **E. Test it (in NEW terminal):**
```bash
./test.sh --demo
```

---

### **🪟 WINDOWS USERS - Follow This:**

#### **A. Open Command Prompt or PowerShell**
- Press `Win + R`
- Type `cmd` or `powershell`
- Press Enter

#### **B. Navigate to your project folder:**
```cmd
cd C:\path\to\cyber-threat-detector
```

#### **C. Create virtual environment (ONE TIME ONLY):**
```cmd
python -m venv venv
```

#### **D. Activate virtual environment:**
```cmd
venv\Scripts\activate
```
You should see `(venv)` in your prompt.

#### **E. Install dependencies (ONE TIME ONLY):**
```cmd
pip install -r requirements.txt
```
Wait 2-5 minutes for installation.

#### **F. Create templates folder:**
```cmd
mkdir templates
```
Make sure `dashboard.html` is inside this folder!

#### **G. Start the application:**
```cmd
python app.py
```

**OR use the batch file:**
```cmd
run.bat
```

#### **H. Open browser:**
Go to: `http://localhost:5000`

#### **I. Test it (open NEW Command Prompt):**
```cmd
cd C:\path\to\cyber-threat-detector
venv\Scripts\activate
python test_detector.py --demo
```

**OR:**
```cmd
test.bat --demo
```

---

## 🆘 IF SCRIPTS DON'T EXIST - MANUAL METHOD

### **Don't have run.sh or test.sh? Do this instead:**

#### **EVERY TIME you want to run the app:**

**Linux/Mac:**
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run app
python app.py
```

**Windows:**
```cmd
REM 1. Activate virtual environment
venv\Scripts\activate

REM 2. Run app
python app.py
```

#### **To run tests:**

**Linux/Mac:**
```bash
# 1. Make sure app is running in another terminal
# 2. Open NEW terminal
source venv/bin/activate
python test_detector.py --demo
```

**Windows:**
```cmd
REM 1. Make sure app is running in another window
REM 2. Open NEW Command Prompt
venv\Scripts\activate
python test_detector.py --demo
```

---

## ✅ QUICK CHECKLIST

Before starting, make sure you have:

- [ ] Python 3.8+ installed (`python --version` or `python3 --version`)
- [ ] All project files in one folder
- [ ] `templates/dashboard.html` file exists
- [ ] Terminal/Command Prompt open in project folder

---

## 🎬 COMPLETE FIRST-TIME SETUP (Windows Example)

```cmd
REM 1. Navigate to project
cd C:\Users\YourName\cyber-threat-detector

REM 2. Create virtual environment
python -m venv venv

REM 3. Activate it
venv\Scripts\activate

REM 4. Upgrade pip
pip install --upgrade pip

REM 5. Install dependencies
pip install -r requirements.txt

REM 6. Create folders
mkdir templates
mkdir logs

REM 7. Verify dashboard.html is in templates folder
dir templates\dashboard.html

REM 8. Run the app
python app.py
```

---

## 🎬 COMPLETE FIRST-TIME SETUP (Linux/Mac Example)

```bash
# 1. Navigate to project
cd ~/cyber-threat-detector

# 2. Make scripts executable
chmod +x setup.sh run.sh test.sh

# 3. Run automated setup
./setup.sh

# 4. Start the app
./run.sh
```

---

## 📱 WHAT YOU SHOULD SEE

### **In Terminal:**
```
🚨 Starting Cyber Threat Detector...
✓ Activating virtual environment...
✓ Starting application...

 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### **In Browser (http://localhost:5000):**
- 🎨 Dark themed dashboard
- 📊 Four statistic cards showing 0s
- 📈 Empty chart
- 🚨 "No threats detected yet" message

---

## 🧪 TESTING THE APP

Once the app is running:

1. **Keep the first terminal running** (don't close it!)
2. **Open a SECOND terminal/command prompt**
3. **Navigate to project folder**
4. **Activate venv**
5. **Run:** `python test_detector.py --demo`

You'll see threats appear on the dashboard in real-time!

---

## 🐛 COMMON PROBLEMS

### **"python not found"**
- Try `python3` instead of `python`
- Or install Python from python.org

### **"No module named flask"**
- Make sure venv is activated (you should see `(venv)` in prompt)
- Run: `pip install -r requirements.txt`

### **"Port 5000 already in use"**
- Something else is using port 5000
- Kill that process or use a different port
- **Linux/Mac:** `lsof -i :5000`
- **Windows:** `netstat -ano | findstr :5000`

### **"templates/dashboard.html not found"**
- Create `templates` folder
- Move `dashboard.html` inside it
- Verify: `ls templates/` or `dir templates\`

### **Dashboard shows blank page**
- Check terminal for errors
- Press F12 in browser, check Console tab
- Make sure app is running without errors

---

## 🎯 QUICK COMMANDS REFERENCE

### **Start App:**
- **Auto:** `./run.sh` (Linux/Mac) or `run.bat` (Windows)
- **Manual:** `source venv/bin/activate && python app.py`

### **Run Tests:**
- **Auto:** `./test.sh --demo`
- **Manual:** `python test_detector.py --demo`

### **Stop App:**
- Press `Ctrl + C` in the terminal

### **View Logs:**
- `tail -f logs/threat_detector.log` (Linux/Mac)
- `type logs\threat_detector.log` (Windows)

---

## 💡 PRO TIPS

1. **Always activate venv first** before running any Python commands
2. **Keep the app terminal open** while using it
3. **Use a second terminal** for testing
4. **Check browser console** (F12) if something doesn't work
5. **Read error messages carefully** - they usually tell you what's wrong

---

## ✨ YOU'RE READY!

If you can see the dashboard at `http://localhost:5000`, **you're all set!** 🎉

Now explore the features and have fun detecting threats!

---

**Still stuck? Tell me:**
1. What operating system are you using?
2. What error message do you see?
3. What step are you on?