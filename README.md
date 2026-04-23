# Obsidian Day Planner Automation

A Python utility for automatically generating structured planner notes in Obsidian, designed to work with the Day Planner plugin.

This project focuses on **automating daily note generation**, **navigation linking**, and **structured organization** within an Obsidian vault.

---

## ✨ Features

- 📅 Generate daily notes for a given date range  
- 🔗 Automatic navigation links (`Prev` / `Next`)  
- 🗂 Structured folder hierarchy:
  - Year → Month → Week  
- 📝 Weekday-based template system  
- 📄 Automatic monthly note generation  
- ⚙️ CLI-based execution  
- 🧪 Dry-run mode (preview without writing files)  
- 🔁 Overwrite / skip existing files  

---

## 📁 Project Structure

```
project/
├── MarkdownGenerator.py
├── templates/
│   ├── Mon.md
│   ├── Tue.md
│   ├── Wed.md
│   ├── Thu.md
│   ├── Fri.md
│   ├── Sat.md
│   └── Sun.md
```

This repository is intended to grow into a modular toolkit for Obsidian automation.

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

Each daily note includes navigation links:

```
Prev : [[2026-05-01]]
Next : [[2026-05-03]]
```

Template content is appended below this block.

---

## 📄 Monthly Note Format

Monthly notes are generated as a simple index:

```
### Notes

- [[2026-05-01]]
- [[2026-05-02]]
- [[2026-05-03]]
...
```

---

## 🧠 Week Definition

- Week starts on **Monday**  
- The week containing the **1st day of the month is Week 1**

---

## 🧩 Template System

Templates are selected based on weekday:

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

## 🚀 Usage

Run the generator script:

```
python MarkdownGenerator.py \
  --base-path "<your-vault-path>" \
  --start-date 2026-05-01 \
  --end-date 2026-06-30
```

---

## ⚙️ CLI Options

| Option | Description |
|------|------------|
| `--base-path` | Obsidian vault root path |
| `--start-date` | Start date (YYYY-MM-DD) |
| `--end-date` | End date (inclusive) |
| `--overwrite` | Overwrite existing files |
| `--dry-run` | Preview without writing files |
| `--generate-month-notes` | Generate monthly notes |

---

## 🧪 Examples

### Generate notes

```
python MarkdownGenerator.py --base-path "C:\Vault" --start-date 2026-05-01 --end-date 2026-06-30
```

### Dry run (no files created)

```
python MarkdownGenerator.py --base-path "C:\Vault" --start-date 2026-05-01 --end-date 2026-06-30 --dry-run
```

### Overwrite existing files

```
python MarkdownGenerator.py --base-path "C:\Vault" --start-date 2026-05-01 --end-date 2026-06-30 --overwrite
```

### Generate monthly notes

```
python MarkdownGenerator.py --base-path "C:\Vault" --start-date 2026-05-01 --end-date 2026-06-30 --generate-month-notes
```

---

## 🛠 Future Improvements

- [ ] Weekly note generation  
- [ ] Config file support (JSON / YAML)  
- [ ] Template placeholders (e.g. `{date}`)  
- [ ] Logging system  
- [ ] Obsidian URI integration  

---

## 🤝 Contributing

Contributions, issues, and suggestions are welcome.

---

## 📜 License

MIT License