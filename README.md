# JMH Performance Analysis and Replication Study

This repository contains the scripts and results for Task 2 of the take-home assignment related to Java Microbenchmark Harness (JMH) performance variability analysis and replication study. The data used for this analysis is from the study **"Towards Effective Assessment of Steady State Performance in Java Software: Are We There Yet?"** by Luca Traini et al. The data can be accessed through the following link:

**Data Source**: [Zenodo: JMH Performance Data](https://zenodo.org/records/5961018)

## Project Overview

This project focuses on three main tasks:
1. **Data Exploration**: Calculation of basic descriptive statistics and visualization of key performance metrics using the JMH dataset.
2. **Replication of Findings**: Replication of a critical finding from the original study, using change point detection to analyze performance variability during the warmup phase.
3. **Novel Analysis**: A new analysis examining the variability of performance across different JDK versions.

### Files and Directories
- **`scripts/`**: Contains the Python scripts used for the analysis.
    - `jdk_performance_analysis.py`: Performs JDK performance variability analysis.
    - `data_exploration_analysis.py`: Explores the dataset by calculating and visualizing descriptive statistics.
    - `pelt_replication_study.py`: Replicates the original study's findings using the PELT algorithm for changepoint detection.
- **`results/`**: Contains plots and figures generated from the analysis.


## How to Run the Scripts

1. Clone the repository.
2. Ensure you have Python installed along with the necessary libraries such as `pandas`, `matplotlib`, `numpy`, and `ruptures`.
3. Execute each script from the command line or in a Jupyter Notebook.

```bash
python jdk_performance_analysis.py
```

This will generate output files and plots in the `results/` directories.

## Results and Analysis
- **Task 1**: Descriptive statistics of the dataset showed significant variability in benchmark performance.
- **Task 2**: Using the PELT algorithm, the replication study identified multiple changepoints, confirming the variability during JVM warmup.
- **Task 3**: Our novel analysis revealed that different JDK versions exhibit distinct performance characteristics, with JDK 1.8.0 241 showing more variability than JDK 11.0.6.
