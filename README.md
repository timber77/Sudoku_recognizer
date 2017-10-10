# sudoku_recognizer
some steps that have to be done once, in order for the programm to run:

0. Install python 3.6.2 (https://www.python.org/downloads/) Choose customize installation, add python to the path and make sure you also install pip.
1. Download the folder sudoku_recognizer
2. Download the 2 .whl files and the .exe file found under releases and save them in the same place as the requirements.txt

    for a 32bit windows: numpy-1.13.3+mkl-cp36-cp36m-win32.whl
                         opencv_python-3.3.0-cp36-cp36m-win32.whl

    for a 64bit windows: numpy-1.13.3+mkl-cp36-cp36m-win_amd64.whl
                         opencv_python-3.3.0+contrib-cp36-cp36m-win_amd64.whl

3. Execute the file "tesseract-ocr-setup-3.05.01.exe". Under additional language data check the Math/Equation detection module. Then you have to add the directory to the path-variable (Example-directory: "C:\Program Files (x86)\Tesseract-OCR")
4. Open the console.
5. Use the command cd to go to the directory where the previously donwloaded file requirements.txt is located.
6. Enter: "pip install -r requirements32.txt" or "pip install -r requirements64.txt" depending if you have a 32bit or a 64bit OS into the console. Make sure you have administrator rights.
7. Run the file recognition.py
