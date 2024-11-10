# Fintrack-API

![Build Status](https://github.com/FranciscoPGuimaraes/Fintrack-API/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/language-Python-yellow)

## Overview

**Fintrack-API** is a financial management application designed to help users track their finances effectively. This application is developed as part of the Software Engineering project for **C214**, a course at the National Institute of Telecommunications (**INATEL**). The main goal of this project is to provide a functional API that enables users to manage their financial data, offering operations such as creating, updating, and deleting records.

## Index

1. [Folder Structure](#folder-structure)

2. [Setting up the Environment](#setting-up-the-environment)

    - [Option 1: Manual Setup](#option-1-manual-setup)

    - [Option 2: Using the provided script](#option-2-using-the-provided-script)

3. [Running the Application](#running-the-application)

4. [Running Tests](#running-tests)

5. [Viewing Test Reports](#viewing-test-reports)
    - [HTML Report](#html-report)
    - [Log File](#log-file)

6. [Contributors](#contributors)

---

## Folder Structure

The project is structured as follows:

```mermaid
graph TD;
    subgraph Fintrack-API

        C1[requirements.txt]
        C2[report.html]
        C3[logfile.log]

        subgraph scripts
            D1[create_and_activate_venv.sh]
        end
        
        subgraph docs
            B1[code_explanation.md]
        end

        subgraph src
            A1[main.py]

            subgraph tests
                subgraph alert
                    T1a[test_alert_add.py]
                    T1b[test_alert_delete.py]
                    T1c[test_alert_update.py]
                    T1d[test_alert_visualization.py]
                end
                subgraph expenditure
                    T2a[test_expenditure_add.py]
                    T2b[test_expenditure_delete.py]
                    T2c[test_expenditure_update.py]
                    T2d[test_expenditure_visualization.py]
                end
                subgraph reminder
                    T3a[test_reminder_add.py]
                    T3b[test_reminder_delete.py]
                    T3c[test_reminder_update.py]
                    T3d[test_reminder_visualization.py]
                end
                subgraph revenue
                    T4a[test_revenue_add.py]
                    T4b[test_revenue_delete.py]
                    T4c[test_revenue_update.py]
                    T4d[test_revenue_visualization.py]
                end
                subgraph user
                    T5a[test_user_add.py]
                    T5b[test_user_delete.py]
                    T5c[test_user_update.py]
                    T5d[test_user_visualization.py]
                end
                subgraph utils_tests
                    T6a[test_utils.py]
                end
            end

            subgraph fintrack_api

                U2[api.py]
                U3[dependencies.py]

                subgraph models
                    M1[TokenModels.py]
                    M2[userModels.py]
                end
                
                subgraph routes
                    R1[add_router.py]
                    R2[delete_router.py]
                    R3[update_router.py]
                    R4[user_router.py]
                    R5[visualization_router.py]
                end
                
                subgraph services
                    subgraph CRUD
                        S1[create.py]
                        S2[read.py]
                        S3[update.py]
                        S4[delete.py]
                    end
                    subgraph db
                        S5[sql_connection]
                    end
                end

                subgraph utils
                    U1[fintrack_api_utils.py]
                end
            end
        end
    end
```

---

## Setting up the Environment

To run the **Fintrack-API** project, you will need to create and activate a virtual environment and install the required dependencies. You can set up the environment in two ways:

### Option 1: Manual Setup

1. Create the virtual environment:
    ```bash
    python -m venv C214venv
    ```

2. Activate the virtual environment:
    - For Windows:
        ```bash
        .\C214venv\Scripts\activate
        ```

    - For macOS/Linux:
        ```bash
        source C214venv/bin/activate
         ```

3. Install the dependencies::
    ```bash
    pip install -r requirements.txt
    ```

### Option 2: Using the provided script

You can also create and activate the virtual environment using the provided script:

1. Run the script:
    ```bash
    ./scripts/create_and_activate_venv.sh
    ```

2. Install the dependencies::
    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Application locally

Once the environment is set up, you can start the application by running the following command:

```bash
python src/main.py
```

This will start the Fintrack-API and allow you to make requests for managing financial records.

---

## Running Tests

The Fintrack API includes a suite of automated tests to ensure the reliability and accuracy of its functionalities. To execute these tests, use the following command in your terminal:

```bash
pytest --html=report.html --self-contained-html --cov=./ --cov-report=html --log-cli-level=INFO --log-file=logfile.log --log-file-level=DEBUG
```

This command performs the following actions:

- **Generates an HTML Report**: Creates a detailed HTML report (`report.html`) of the test results, summarizing the status and outcome of each test case.
- **Tracks Code Coverage**: Analyzes the code coverage, providing insights into the portions of the codebase that are exercised by the tests. The coverage report can be viewed in an HTML format in the `htmlcov` directory.
- **Logs Test Execution**: Outputs detailed logs of the test execution, saving them to a file (`logfile.log`) with log levels up to DEBUG for comprehensive traceability and debugging.

---

## Viewing Test Reports

### HTML Report
To view the comprehensive test report, open the generated [report.html](/report.html) file. On Windows, you can use the following command to launch it directly in your default browser:

```bash
start report.html
```

### Log File

For a more detailed log of the test execution, including informational messages and debug-level output, refer to [logfile.log](/logfile.log). This file contains step-by-step logs that can be helpful for debugging and analysis.

---

## Contributors

### [Álvaro Ribeiro](https://github.com/AlvaroLucioRibeiro)

Undergraduate student in the eighth (8th) semester of Software Engineering at the National Institute of Telecommunications (Inatel). Industrial Apprentice in Installation and Repair of Computer Networks at Senai Orlando Chiarini. I have participated in a Scientific Initiation at the Cybersecurity and Internet of Things Laboratory (CS&ILAB) with the project: 'Secure Software Development - Phases 01 and 02.' Currently, I am an intern at the Inatel Competence Center (ICC) in the R&D Software area.

### [Francisco Guimarães](https://github.com/FranciscoPGuimaraes)
Currently, I am completing my degree in Software Engineering at INATEL and working as a Data Science Intern at Embraer.

### [Laura Pivoto](https://github.com/LauraPivoto)

Currently graduating in Software Engineering, researcher in Secure Software development at CS&I Lab. and object-oriented programming monitor at the Instituto Nacional de Telecomunicações. I have experience in IoT, mobile and web development in Android Studio, Thunkable, Flutter, Visual Studio Code and intermediate knowledge in C++, Java and Python.

### [Matheus Fonseca](https://github.com/matheusAFONSECA)

Undergraduate student in the eighth (8th) semester of Computer Engineering at the National Institute of Telecommunications (Inatel). I participated in a Scientific Initiation at the Cybersecurity and Internet of Things Laboratory (CS&ILAB), where, in the Park Here project, I developed skills in computer vision applied to parking systems, focusing on license plate recognition and vehicle identification. Additionally, I served as a teaching assistant for Physics 1, 2, and 3, helping with practical classes, report writing, and answering theoretical questions. Currently, I am an intern at the Inatel Competence Center (ICC) in the PDI SW department.


--- 
