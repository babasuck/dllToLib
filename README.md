# DllToLib
## Russian
Данная утилита служит для преобразования библиотек динамической компановки (dll) в файлы:
  * Библиотека иморта (.lib), которые служат для статической загрузки DLL в проект
  * Заголовочный файл (.inc), содержащий объявления функций для работы с MASM64
### Сборка и использование
Для корректной работы скрипта необходимо заранее установить и указать пути в переменую PATH для двух утилит:
* dumpbin.exe
* lib.exe

Они распространяются с Microsoft Visual Studio.
```
python -m venv venv - создание виртуального окружения
cd venv\Scripts && activate - активация виртуального окружения
python ../../main.py C:\Windows\System32 C:\masm64\lib C:\masm64\inc - пример использования
```
## English
This utility is used to convert dynamic linkage (dll) libraries into files:
  * Immort library (.lib), which are used to statically load DLL into the project
  * Header file (.inc), that contains functions declarations to work with MASM64
### Building and usage
For the script to work correctly, you must first install and specify the paths to the PATH variable for the two utilities:
* dumpbin.exe
* lib.exe

They are distributed with Microsoft Visual Studio.
```
python -m venv venv - create a virtual environment
cd venv\Scripts && activate - activate virtual environment
python ../../main.py C:\Windows\System32 C:\masmas64\lib C:\masm64\inc - example usage
```
