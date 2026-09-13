# Data Analytics Assignments

Welcome to the Data Analytics Assignments repository! This repository contains a collection of Hadoop MapReduce projects and HDFS guides, ranging from cluster setup to data processing algorithms.

## Prerequisites
To run the code in this repository, you will need:
- **Java** (Java 8 or 11 recommended)
- **Hadoop** (Configured in Pseudo-Distributed or Distributed mode)

## Assignments & Projects

This repository is organized into numbered folders inside the `Code/` directory. Each project has its own dedicated `README.md` with step-by-step instructions on how to compile, set up, and run the job.

### [Project 1: Hadoop Installation and HDFS Tasks](./Code/1/README.md)
A comprehensive, end-to-end guide on installing Hadoop from scratch on macOS via Homebrew. It covers configuring XML files for a Pseudo-Distributed cluster and provides a cheat sheet for fundamental HDFS commands (creating directories, uploading, downloading, and deleting files).

### [Project 2: MapReduce Word Count](./Code/2/README.md)
Demonstrates the classic MapReduce "Word Count" algorithm. The guide shows how to run the highly optimized Hadoop built-in WordCount example, as well as how to compile and run the custom Java implementation provided in the folder.

### [Project 3: Matrix Multiplication](./Code/3/README.md)
A MapReduce application that performs Matrix Multiplication. This project includes a sparse matrix input format and demonstrates how to pass matrix dimensions to the Mapper and Reducer through the Hadoop Configuration object.

### [Project 4: Movie Tags Extraction](./Code/4/README.md)
A data extraction job using the popular MovieLens dataset. This MapReduce program processes the `tags.csv` file, filters out the headers, and groups all user-generated tags by `movieId` into a clean, separated list. 

---

## How to Use This Repository
1. **Clone the repository:**
   ```bash
   git clone https://github.com/tatha-bot/Data-Analytics-Assignments.git
   cd Data-Analytics-Assignments
   ```
2. **Navigate to a specific project:**
   ```bash
   cd Code/<Project_Number>
   ```
3. **Follow the instructions:**
   Open the `README.md` inside that specific project folder and follow the step-by-step execution guide!
