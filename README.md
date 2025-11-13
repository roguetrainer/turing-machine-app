# **🧠 The Computational Frontier: Turing Machine Simulators (Python & F\#)**

This repository contains two distinct implementations of a Turing Machine (TM) emulator, built to explore the foundations of computer science, complexity theory, and functional programming.

![TM](./Turing-machine.png)

## **🚀 Overview**

The Turing Machine, a foundational mathematical model conceived by Alan Turing, defines the limits of what is computable. This project simulates its behavior in two different programming paradigms:

1. **Python (.py):** An interactive, step-by-step simulator designed for use within a Jupyter environment using ipywidgets for visualization.  
2. **F\# (.fs):** A pure, console-based functional implementation that models the TM's immutable state transitions precisely.

## **✨ Features**

| Implementation | Files | Focus |
| :---- | :---- | :---- |
| **Python** | turing\_machine\_app.py, requirements.txt, setup.sh | **Interactive Visualization** of common TM algorithms (e.g., $L=\\{a^n b^n\\}$, Binary Incrementer). Great for demonstration and learning. |
| **F\#** | TuringMachine.fs | **Functional Purity** using Discriminated Unions and immutable records to elegantly model the TM's mathematical definition, including the **Busy Beaver** problem. |
| **Documentation** | turing\_machine\_overview.md | Theoretical document covering the TM's history, the Church-Turing Thesis, its link to Gödel's theorems, and Complexity Theory (P vs. NP). |

## **🐍 Getting Started (Python \- Interactive Jupyter App)**

This setup is required to run the interactive widget-based simulator (turing\_machine\_app.py).

### **Prerequisites**

You must have Python 3 and Jupyter installed.

### **Setup Instructions**

1. **Run the Setup Script:** The setup.sh script creates a virtual environment, installs necessary dependencies (ipywidgets), and enables the Jupyter extension.  
   bash setup.sh

2. **Activate the Environment:**  
   source .venv\_tm/bin/activate

3. **Launch Jupyter:**  
   jupyter notebook

4. **Run the Simulation:** Copy the contents of turing\_machine\_app.py into a new Jupyter Notebook cell and execute it to launch the interactive application.

## **⚙️ Getting Started (F\# \- Console Emulator)**

This setup is required to run the functional simulation (TuringMachine.fs).

### **Prerequisites**

You need the [.NET SDK](https://dotnet.microsoft.com/download) installed, which includes the F\# compiler (dotnet fsi).

### **Running the Simulator**

1. Navigate to the directory containing TuringMachine.fs.  
2. Execute the script using the F\# Interactive environment:  
   dotnet fsi TuringMachine.fs

The script will execute the defined examples for the Binary Incrementer and the 2-State Busy Beaver, printing the step-by-step tape configuration to the console.

## **📘 Documentation**

For a deep dive into the theory, please refer to the accompanying document:

* turing\_machine\_overview.md