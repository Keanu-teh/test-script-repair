# ARTS

## Introduction
ARTS is a lightweight approach that make LLM rely on prompt engineering to automatically repair GUI test scripts based on GUI visual and structural information. This project is implemented in Python language and is intended to be run in PyCharm Community Edition.

## Usage
1. Clone this project.
2. Locate **scriptRepair\GPT.py**, which provides few-shot learning and chain-of-thought learning to help the LLM understand the test script repair work, send them to the LLM to learn when the first repair is performed, and then the subsequent repair can directly input the test action to be repaired.
3. Change the Apikey of chatGpt to yours.
4. Locate **scriptRepair\main.py**, which serves as the main file for inputting related information and generating the final repair result.
5. Run the `main.py`, and then run the `GPT.py`.
6. Re-execute the test script by copying the generated repair to the crashed test action.

