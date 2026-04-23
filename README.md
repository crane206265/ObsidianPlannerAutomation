# Obsidian Day Planner Automation

A Python utility for automating daily planner note generation in Obsidian, designed to integrate with the Day Planner plugin.

This project focuses on **structured daily note generation**, **navigation linking**, and **planner-ready formatting**.

---

## ✨ Features

- 📅 Generate daily markdown notes for a given date range  
- 🔗 Automatic `Prev` / `Next` navigation links  
- 🗂 Hierarchical folder structure:
  - Year → Month → Week  
- 🧩 Designed for Obsidian Day Planner plugin usage  
- 📝 **Template support (planned)**
  - Different templates per weekday (Mon–Sun)  
- ⚙️ Customizable generation options (planned)
  - Skip existing files / overwrite mode  

---

## 📁 Folder Structure

Generated notes follow this structure:

```
<basePath>/
└── 2026/
    └── May. 2026/
        └── May. Week 1/
            ├── 2026-05-01.md
            ├── 2026-05-02.md
            ...
```

---

## 📄 Generated Note Format

Each file includes navigation links:

```
Prev : [[2026-05-01]]
Next : [[2026-05-03]]
```

Planned (template-based content):

```
# Daily Plan

## Schedule
-

## Tasks
-

## Notes
-
```

---

## 🧠 Week Definition

This project uses a **custom week-of-month definition**:

- Week starts on **Monday**  
- The week containing the **1st day of the month is Week 1**

---

## 🚀 Usage

### 1. Clone repository

```
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

---

### 2. Configure parameters

Edit inside `main.py`:

```python
base_path = r"C:\Your\Obsidian\Vault\Path"
start_date = "2026-05-01"
end_date = "2026-06-30"
```

---

### 3. Run script

```
python main.py
```

---

## ⚙️ Configuration

| Parameter     | Description                          |
|--------------|--------------------------------------|
| base_path    | Path to Obsidian vault               |
| start_date   | Start date (YYYY-MM-DD)              |
| end_date     | End date (inclusive)                 |

---

## 🧩 Template System (Planned)

Future versions will support **weekday-based templates**:

```
templates/
├── Mon.md
├── Tue.md
├── Wed.md
...
```

Each generated note will automatically load the appropriate template based on the date.

---

## 🛠 Planned Features

- [ ] Weekday-based template system  
- [ ] CLI support (`argparse`)  
- [ ] JSON/YAML config file  
- [ ] Overwrite / skip existing files option  
- [ ] Custom output formats  
- [ ] Obsidian URI integration  
- [ ] Logging / dry-run mode  

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

---

## 📜 License

MIT License
