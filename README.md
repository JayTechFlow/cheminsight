# ChemInsight

ChemInsight is a web-based application developed as part of the FOSSEE Semester Long Internship screening task.  
The project focuses on analyzing CSV-based chemical equipment data and presenting meaningful insights through a clean and interactive web interface.

---

## 🔍 Problem Statement

Chemical plants often store equipment data in CSV files.  
Manually analyzing such data is time-consuming and error-prone.

This project provides:
- CSV upload functionality
- Automatic data analysis
- Summary statistics
- Visualization of equipment distribution
- History management for uploaded datasets

---

## ⚙️ Features

- Upload CSV files containing equipment data
- Automatically compute:
  - Total equipment count
  - Average flowrate
  - Average pressure
  - Average temperature
  - Equipment type distribution
- Visualize equipment distribution using bar charts
- Store and display last 5 uploaded datasets
- Clickable history to reload previous summaries without re-uploading
- Clean, responsive, and user-friendly interface

---

## 🛠️ Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- Pandas
- SQLite

### Frontend
- React (Vite)
- Axios
- Chart.js
- HTML & CSS

---

## 📂 Project Structure

