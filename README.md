# ARTS

## Introduction
ARTS is a lightweight approach that make LLM rely on prompt engineering to automatically repair GUI test scripts based on GUI visual and structural information. This project is implemented in Python language and is intended to be run in PyCharm Community Edition.

## I.Requirement
1. [Appium 2.0.1](https://github.com/appium/appium)
2. [Android SDK](https://developer.android.com/studio)
3. Android phone or Emulator (Android 7.0 or higher)

## III. Connect Android Phones or Emulator to the Computer
1. Execute `adb conenct` on the terminal after ensuring that the phone is connected to the computer.
2. If it is an emulator, Execute `adb connect <your own device IP address>` on the terminal.

## III. Run the Service of Appium
Execute `Appium` on the terminal

## IV. Run ARTS
1. Clone this project.
2. Locate **scriptRepair\GPT.py**, which provides few-shot learning and chain-of-thought learning to help the LLM understand the test script repair work, send them to the LLM to learn when the first repair is performed, and then the subsequent repair can directly input the test action to be repaired.
3. Fill in your own Apikey of chatGpt.
4. Locate **scriptRepair\main.py**, which serves as the main file for inputting related information and generating the final repair result.
5. Run the `main.py`, and then run the `GPT.py`.
6. Re-execute the test script by copying the generated repair to the crashed test action.
7. If the generated repair result is incorrect, delete the node corresponding to the last generated repair result in the target_vresion_xml_encoding.html file and run GPT.py again to generate a new repair result.
