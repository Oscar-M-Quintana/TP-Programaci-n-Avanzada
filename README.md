# TP-Programación Avanzada

Trabajo practico para la materia Programación Avanzada de la Universidad Nacional de Almirante Brown

Selenium.
[text](https://selenium-python.readthedocs.io/)

Instalación y carga de páginas
para utilizar Selenium debemos, en primer lugar, instalar el propio paquete. La
instalación se hace de la misma forma que cualquier paquete Python; el método
estándar es tecleando en el terminal:
python -m pip install selenium
La segunda parte de la instalación es específica de Selenium. Para ello, debemos
instalar el cliente del navegador que se desee utilizar.
En nuestro caso vamos a utilizar el explorador Google Chrome:

- Google Chrome: el cliente para Selenium, llamado chromedriver, se puede
  obtener en:
  https://googlechromelabs.github.io/chrome-for-testing/
  (Pagina aportada por la documentación oficial de Selenium)

Hay más drivers, que podemos encontrar en la página de Selenium: Opera, Safari, Android, Edge y muchos otros.

En cualquier caso, tras descargar el fichero correspondiente debemos
descomprimirlo, obteniendo el ejecutable. Aún nos queda una cosa por hacer:
Debemos lograr que el fichero ejecutable sea visible desde nuestra aplicación Python.
