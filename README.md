# Proyecto Final Lenguajes Formales y Compiladores
Integrantes: 
- Juan Felipe Restrepo Buitrago
- Kevin Quiroz
- Evelyn Alejandra Zapata

Descripción: 
El proyecto consiste en la implementación de dos analizadores sintácticos, con el objetivo de determinar la validez de una cadena de texto, asegurándose de que pertenezca a la gramática indicada.
Uno de los analizadores el es top-down, que trabaja en un método orientado a objetivos, lo que significa que busca a partir del símbolo de inicio de la sintaxis y busca una derivación sintáctica adecuada; para ello calcula los conjuntos first y follow de la gramática dada, y con ello construye la tabla de análisis sintáctico predictivo.
El otro analizador es el bottom-up, que parte de los símbolos terminales de entrada y aplica reglas de reducción hasta llegar al símbolo inicial de la gramática; para lo cual calcula los conjuntos closure y las funciones GoTo y Action de la gramática dada, y construye la tabla de análisis LR.

Lenguaje de Programación: Python

Mínima versión de Python para su ejecución: 3.7

El archivo que debe ejecutar para ver el resultado final es "main.py" que está justo al entrar al proyecto. Si desea ver el resultado del top-down parser o del bottom-up parser, debe especificar en este mismo archivo cuál parser desea ejecutar, los cuales se dividen en 1 función cada uno.
