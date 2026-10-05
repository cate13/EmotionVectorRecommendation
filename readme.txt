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


Project Workflow
----------------

The project generally follows this workflow:

    1. Original BookCrossing CSV files are stored in starting_data/.
    2. The source data is processed into JSONL files in processed_data/.
    3. Recommendation methods in Rec/ generate book recommendations.
    4. LLM-based workflows in LLM Code/ create and execute prompts when
       language-model recommendations are being evaluated.
    5. The generated recommendations are evaluated using the tools in Eval/.


Data Sources
------------

The original source data is based on the BookCrossing dataset. The files in
starting_data/ represent the original CSV data, while the files in
processed_data/ contain the corresponding processed book and user information
used by the project.

When adding or replacing data, preserve the distinction between original
source files and processed files. This helps maintain reproducibility and
makes it possible to regenerate processed data when necessary.


Reproducibility Notes
---------------------

For reproducible experiments:

    * Keep original input files in starting_data/.
    * Store processed JSONL files in processed_data/.
    * Keep recommendation-generation code in Rec/.
    * Keep LLM prompt-generation and execution code in LLM Code/.
    * Use the appropriate evaluation code in Eval/ for each recommendation
      approach.
    * Record the data version, recommendation method, prompt configuration,
      and evaluation configuration used for each experiment.


Extending the Repository
------------------------

New recommendation methods should be added to Rec/ and evaluated using the
appropriate tools in Eval/. New LLM-based approaches should be implemented in
LLM Code/ and should have their outputs evaluated using the LLM-related
evaluation code in Eval/.

Any new input or intermediate data files should be placed in the directory
that matches their role: original source data in starting_data/ and processed
JSONL data in processed_data/.


License and Attribution
-----------------------

This project uses data originating from the BookCrossing dataset. Please
consult the dataset's original documentation and licensing or usage terms
before redistributing the data or derived files.