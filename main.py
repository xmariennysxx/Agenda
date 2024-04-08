import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QScrollArea
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class ContactoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda de Contactos")

        self.contactos = {}

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        header_label = QLabel("Agenda de Contactos")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 20px; color: #333; margin-bottom: 20px;")
        layout.addWidget(header_label)

        form_layout = QVBoxLayout()
        layout.addLayout(form_layout)

        form_layout.addWidget(QLabel("Nombre:"))
        self.nombre_input = QLineEdit()
        self.nombre_input.setStyleSheet("padding: 5px; border: 1px solid #999; border-radius: 5px;")
        form_layout.addWidget(self.nombre_input)

        form_layout.addWidget(QLabel("Apellido:"))
        self.apellido_input = QLineEdit()
        self.apellido_input.setStyleSheet("padding: 5px; border: 1px solid #999; border-radius: 5px;")
        form_layout.addWidget(self.apellido_input)

        form_layout.addWidget(QLabel("Teléfono:"))
        self.telefono_input = QLineEdit()
        self.telefono_input.setStyleSheet("padding: 5px; border: 1px solid #999; border-radius: 5px;")
        form_layout.addWidget(self.telefono_input)

        form_layout.addWidget(QLabel("Segundo Teléfono:"))
        self.telefono2_input = QLineEdit()
        self.telefono2_input.setStyleSheet("padding: 5px; border: 1px solid #999; border-radius: 5px;")
        form_layout.addWidget(self.telefono2_input)

        form_layout.addWidget(QLabel("Correo electrónico:"))
        self.correo_input = QLineEdit()
        self.correo_input.setStyleSheet("padding: 5px; border: 1px solid #999; border-radius: 5px;")
        form_layout.addWidget(self.correo_input)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        guardar_button = QPushButton("Guardar Cambios")
        guardar_button.setStyleSheet("padding: 10px; background-color: #007bff; color: #fff; border: none; border-radius: 5px;")
        guardar_button.clicked.connect(self.guardar_contacto)
        button_layout.addWidget(guardar_button)

        limpiar_button = QPushButton("Limpiar Formulario")
        limpiar_button.setStyleSheet("padding: 10px; background-color: #dc3545; color: #fff; border: none; border-radius: 5px;")
        limpiar_button.clicked.connect(self.limpiar_formulario)
        button_layout.addWidget(limpiar_button)

        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.table = QTableWidget()
        self.table.setStyleSheet("border: 1px solid #ccc;")
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Nombre", "Apellido", "Teléfono 1", "Teléfono 2", "Correo", "Acciones"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        scroll_area.setWidget(self.table)

    def guardar_contacto(self):
        nombre = self.nombre_input.text()
        apellido = self.apellido_input.text()
        telefono = self.telefono_input.text()
        telefono2 = self.telefono2_input.text()
        correo = self.correo_input.text()

        self.contactos[nombre] = {"Apellido": apellido, "Teléfono": telefono, "Teléfono2": telefono2, "Correo electrónico": correo}

        self.actualizar_tabla_contactos()

        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.nombre_input.clear()
        self.apellido_input.clear()
        self.telefono_input.clear()
        self.telefono2_input.clear()
        self.correo_input.clear()

    def actualizar_tabla_contactos(self):
        self.table.setRowCount(0)

        for nombre, detalles in self.contactos.items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            nombre_item = QTableWidgetItem(nombre)
            nombre_item.setFont(QFont("Arial", 10))
            apellido_item = QTableWidgetItem(detalles["Apellido"])
            apellido_item.setFont(QFont("Arial", 10))
            telefono_item = QTableWidgetItem(detalles["Teléfono"])
            telefono_item.setFont(QFont("Arial", 10))
            telefono2_item = QTableWidgetItem(detalles["Teléfono2"])
            telefono2_item.setFont(QFont("Arial", 10))
            correo_item = QTableWidgetItem(detalles["Correo electrónico"])
            correo_item.setFont(QFont("Arial", 10))

            self.table.setItem(row_position, 0, nombre_item)
            self.table.setItem(row_position, 1, apellido_item)
            self.table.setItem(row_position, 2, telefono_item)
            self.table.setItem(row_position, 3, telefono2_item)
            self.table.setItem(row_position, 4, correo_item)

            # Botones de editar y borrar
            editar_button = QPushButton("Editar")
            editar_button.setFont(QFont("Arial", 10))
            editar_button.setFixedHeight(20)
            editar_button.clicked.connect(self.editar_contacto)
            borrar_button = QPushButton("Borrar")
            borrar_button.setFont(QFont("Arial", 10))
            borrar_button.setFixedHeight(20)
            borrar_button.clicked.connect(self.borrar_contacto)

            button_layout = QHBoxLayout()
            button_layout.addWidget(editar_button)
            button_layout.addWidget(borrar_button)

            button_container = QWidget()
            button_container.setLayout(button_layout)

            self.table.setCellWidget(row_position, 5, button_container)

    def editar_contacto(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            nombre = self.table.item(index.row(), 0).text()
            detalles = self.contactos[nombre]
            self.nombre_input.setText(nombre)
            self.apellido_input.setText(detalles["Apellido"])
            self.telefono_input.setText(detalles["Teléfono"])
            self.telefono2_input.setText(detalles["Teléfono2"])
            self.correo_input.setText(detalles["Correo electrónico"])

    def borrar_contacto(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            nombre = self.table.item(index.row(), 0).text()
            del self.contactos[nombre]
            self.actualizar_tabla_contactos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactoApp()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())