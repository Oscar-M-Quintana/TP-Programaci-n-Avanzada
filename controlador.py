from vista import Vista


class Controlador:
    def __init__(self):
        self.vista = Vista()

    def run(self):
        self.vista.mainloop()


if __name__ == "__main__":
    app = Controlador()
    app.run()
