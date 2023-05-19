# Proyecto Final Lenguajes Formales y Compiladores

## Integrantes
- [**Juan Felipe Restrepo**](https://github.com/JuanFelipeRestrepoBuitrago)
- [**Kevin Quiroz**](https://github.com/KevinQzG)
- [**Evelyn Alejandra Zapata**](https://github.com/EvelynZapata20)

## Descripción
El proyecto consiste en la implementación de dos analizadores sintácticos en Python, con el objetivo de determinar la validez de una cadena de texto y asegurarse de que pertenezca a la gramática indicada.

1. **Analizador Top-Down**: Este analizador utiliza un enfoque orientado a objetivos. Comienza desde el símbolo de inicio de la sintaxis y busca una derivación sintáctica adecuada. Calcula los conjuntos "first" y "follow" de la gramática dada y construye la tabla de análisis sintáctico predictivo.

2. **Analizador Bottom-Up**: Este analizador parte de los símbolos terminales de entrada y aplica reglas de reducción hasta llegar al símbolo inicial de la gramática. Calcula los conjuntos "closure" y las funciones "GoTo" y "Action" de la gramática dada y construye la tabla de análisis LR.

## Lenguaje de Programación
 **Python** 


![Python Logo](https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg)

## Mínima versión de Python para su ejecución
**3.7**

## Ejecución
El archivo que debes ejecutar para ver el resultado final es `main.py`, el cual se encuentra en la raíz del proyecto. Si deseas ver el resultado del analizador top-down o del analizador bottom-up, debes especificar en ese mismo archivo cuál analizador deseas ejecutar. Cada analizador se implementa en una función separada.

