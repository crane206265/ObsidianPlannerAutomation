# Obsidian Day Planner Automation

A Python utility for automatically generating structured planner notes in Obsidian, designed to work with the Day Planner plugin.

This project automates:

- 📝 **Daily note generation**
- 🔗 **Navigation linking**
- 📄 **Monthly indexing**
- 📊 **Planner analysis & visualization**

within an Obsidian vault.

---

## ✨ Features

### 📝 Generator
- 📅 Generate daily notes for a given date range  
- 🔗 Automatic navigation links (`Prev` / `Next`)  
- 🗂 Structured folder hierarchy:
  - Year → Month → Week  
- 📝 Weekday-based template system  
- 📄 Automatic monthly note generation  
- ⚙️ CLI-based execution  
- 🧪 Dry-run mode (preview without writing files)  
- 🔁 Overwrite / skip existing files  
- ▶️ One-click execution via `.bat` launcher  

### 📊 Analyzer
- Parse planner entries automatically  
- Extract time duration from schedule  
- Keyword-based task classification  
- Interactive category merging (manual grouping)  
- Category-wise time aggregation  
- Daily time trend visualization  
- xkcd-style graphs  
- Korean font support (bold adjustable)  
- CLI-based execution  

---

## 📁 Project Structure

```
project/
├── MarkdownGenerator.py
├── PlannerAnalyzer.py
├── run_MarkdownGenerator.bat
├── run_PlannerAnalyzer.bat
├── templates/
│   ├── Mon.md
│   ├── Tue.md
│   ├── Wed.md
│   ├── Thu.md
│   ├── Fri.md
│   ├── Sat.md
│   └── Sun.md
```

---

## 📁 Generated Folder Structure

```
<basePath>/
└── 2026/
    └── May. 2026/
        ├── May. 2026.md
        └── May. Week 1/
            ├── 2026-05-01.md
            ├── 2026-05-02.md
            ...
```

---

## 📄 Daily Note Format

```
Prev : [[2026-05-01]]
Next : [[2026-05-03]]
```

Template content is appended below this block.

---

## 📄 Monthly Note Format

```
### Notes

- [[2026-05-01]]
- [[2026-05-02]]
- [[2026-05-03]]
...
```

---

## 📊 Planner Format (Analyzer)

Analyzer parses only structured planner lines:

```
- [ ] 09:00 - 10:30 Study Rudin
- [x] 11:00 - 12:00 Python project
```

- `[ ]` / `[x]` → completion status  
- `HH:MM - HH:MM` → duration  
- `content` → classification target  

All other lines (notes, free text) are ignored.

---

## 🧠 Week Definition

- Week starts on **Monday**  
- The week containing the **1st day of the month is Week 1**

---

## 🧩 Template System

```
templates/
├── Mon.md
├── Tue.md
├── Wed.md
├── Thu.md
├── Fri.md
├── Sat.md
└── Sun.md
```

Each template is appended to the generated daily note.

---

# 🚀 Usage

## 📝 Generator

### Run via Python (CLI)

```
python MarkdownGenerator.py \
  --base-path "<your-vault-path>" \
  --start-date 2026-05-01 \
  --end-date 2026-06-30 \
  --generate-month-notes
```

---

## 📊 Analyzer

### Run via Python (CLI)

```
python PlannerAnalyzer.py \
  --base-path "<your-vault-path>" \
  --start-date 2026-04-01 \
  --end-date 2026-04-30 \
  --exclude-uncategorized \
  --font-weight heavy
```

---

## ⚙️ CLI Options (Analyzer)

| Option | Description |
|------|------------|
| `--base-path` | Obsidian vault planner path |
| `--start-date` | Start date (YYYY-MM-DD) |
| `--end-date` | End date (inclusive) |
| `--categories` | Suffix keywords (e.g. 공부 연습) |
| `--exclude-uncategorized` | Remove uncategorized data |
| `--no-xkcd` | Disable xkcd style |
| `--font-weight` | normal / bold / heavy |
| `--category-mode` | interactive / auto |
| `--show-missing` | Print missing files |

---

## 🧪 Examples

### Generate notes

```
python MarkdownGenerator.py --base-path "C:\Vault" --start-date 2026-05-01 --end-date 2026-06-30
```

### Analyze planner

```
python PlannerAnalyzer.py --base-path "C:\Vault" --start-date 2026-04-01 --end-date 2026-04-30 --exclude-uncategorized
```

---

## ▶️ Quick Run (Windows)

### Generator

```
run_MarkdownGenerator.bat
```

### Analyzer

```
run_PlannerAnalyzer.bat
```

---

## ⚠️ Windows Encoding Issue (IMPORTANT)

If your path contains Korean characters (e.g. `문서`),  
you may see broken paths like:

```
C:\Users\...\臾몄꽌\...
```

### ✅ Fix

Add this line at the top of your `.bat` file:

```bat
chcp 65001 > nul
```

### ✅ Example

```bat
@echo off
chcp 65001 > nul

cd /d "%~dp0"

python PlannerAnalyzer.py ^
  --base-path "C:\Users\dlgkr\OneDrive\문서\Obsidian\Planner" ^
  --start-date 2026-04-01 ^
  --end-date 2026-04-30 ^
  --exclude-uncategorized ^
  --font-weight heavy

pause
```

### ⚠️ Additional Note

If issues persist:

- Save `.bat` file as **UTF-8 with BOM**
- Or avoid non-ASCII paths

---

## 📊 Output

### Category Summary
- Total time per category (bar chart)

### Daily Trend
- Time per category over time (line chart)

---

## 🛠 Future Improvements

- [ ] Weekly note generation  
- [ ] Graph export (PNG → Obsidian embed)  
- [ ] Config file support (JSON / YAML)  
- [ ] Smart date options (`--today`, `--this-month`)  
- [ ] Automatic keyword extraction  

---

## 🤝 Contributing

Contributions, issues, and suggestions are welcome.

---

## 📜 License

MIT License