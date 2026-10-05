BOOK RECOMMENDATION SYSTEM
===========================

Overview
--------

This repository contains the data, recommendation code, language-model
prompting code, and evaluation tools used to develop and assess a book
recommendation system.

The project is organized into separate directories for source data,
processed data, recommendation generation, LLM-based workflows, and
evaluation. This separation makes it easier to reproduce experiments,
compare recommendation approaches, and extend the system with new methods.


Repository Structure
--------------------

Eval/
    Contains the code used to evaluate generated book recommendations.
    Evaluation functionality is organized into three subdirectories,
    including a dedicated directory for evaluating LLM-based
    recommendations.

LLM Code/
    Contains the code used to create and run prompts for large language
    model (LLM)-based recommendation workflows.

Rec/
    Contains the code responsible for generating book recommendations.
    This directory contains the core recommendation implementations used
    by the project.

processed_data/
    Contains JSONL files with processed book and user information. These
    files are prepared for use by the recommendation and evaluation code.

starting_data/
    Contains the original CSV files obtained from the BookCrossing dataset.
    These files provide the starting point for data processing and
    experimentation.
