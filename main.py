from controllers.database import criar_banco, salvar_cliente, buscar_clientes, excluir_cliente
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QHBoxLayout, QListWidget, QStackedLayout, QLineEdit,
    QTextEdit, QComboBox, QMessageBox, QListWidgetItem, QTableWidget,
    QTableWidgetItem, QHeaderView, QFormLayout, QCheckBox
)
from PySide6.QtGui import QFont, QColor, QPalette
import sys

class MainWindow(QMainWindow):
    def salvar_cliente(self):
        nome = self.nome_cliente_input.text()
        celular = self.celular_input.text()
        email = self.email_input.text()
        oab = self.oab_input.text()

        if not nome or not celular:
            QMessageBox.warning(self, "Atenção", "Por favor, preencha pelo menos o nome e o celular do cliente.")
            return

        salvar_cliente(nome, celular, email, oab)
        QMessageBox.information(self, "Sucesso", "Cliente salvo com sucesso!")

        # Limpar campos
        self.nome_cliente_input.clear()
        self.celular_input.clear()
        self.email_input.clear()
        self.oab_input.clear()

        # Atualizar lista de clientes
        self.carregar_clientes()


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cálculos Judiciais")
        self.setGeometry(200, 100, 1000, 600)

        criar_banco()  # Garante que o banco será criado ao iniciar

        # Layout principal
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Menu lateral
        self.menu = QListWidget()
        self.menu.addItem("🏠 Dashboard")
        self.menu.addItem("👤 Clientes")
        self.menu.addItem("➕ Novo Cálculo")
        self.menu.addItem("📝 Cadastrar Cliente")
        self.menu.addItem("📑 Lista de Processos")
        self.menu.addItem("📤 Exportar")
        self.menu.setFixedWidth(200)
        self.menu.currentRowChanged.connect(self.display_page)

        # Área de conteúdo
        self.pages = QStackedLayout()

        # Página 1: Dashboard
        dashboard = QWidget()
        dash_layout = QVBoxLayout()
        dash_label = QLabel("Bem-vindo ao sistema de Cálculos Judiciais!")
        dash_label.setFont(QFont("Arial", 16))
        dash_layout.addWidget(dash_label)
        dashboard.setLayout(dash_layout)

        # Página 2: Clientes com filtros
        self.clientes_page = QWidget()
        self.clientes_layout = QVBoxLayout()

        filtro_layout = QHBoxLayout()
        self.filtro_nome = QLineEdit()
        self.filtro_nome.setPlaceholderText("Buscar por nome")
        buscar_btn = QPushButton("Buscar")
        buscar_btn.clicked.connect(self.carregar_clientes)

        filtro_layout.addWidget(self.filtro_nome)
        filtro_layout.addWidget(buscar_btn)

        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(5)
        self.tabela_clientes.setHorizontalHeaderLabels(["Nome", "Celular", "Email", "OAB", "Ações"])
        self.tabela_clientes.horizontalHeader().setStretchLastSection(True)
        self.tabela_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_clientes.setEditTriggers(QTableWidget.NoEditTriggers)

        self.clientes_layout.addLayout(filtro_layout)
        self.clientes_layout.addWidget(self.tabela_clientes)
        self.clientes_page.setLayout(self.clientes_layout)

        # Página 3: Novo Cálculo (atualizada com novo formulário)
        novo = QWidget()
        novo_layout = QVBoxLayout()
        titulo = QLabel("Cadastrar novo cálculo")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: #2e86de; margin-bottom: 10px;")

        form_layout = QFormLayout()

        self.processo_input = QLineEdit()
        self.prazo_input = QLineEdit()
        self.area_input = QComboBox()
        self.area_input.addItems(["Trabalhista", "Cível", "Federal", "Previdenciário"])
        self.valor_calc_input = QLineEdit()
        self.pago_input = QComboBox()
        self.pago_input.addItems(["Não", "Sim"])
        self.enviado_input = QComboBox()
        self.enviado_input.addItems(["Não", "Sim"])

        form_layout.addRow("Número do Processo:", self.processo_input)
        form_layout.addRow("Prazo (dias):", self.prazo_input)
        form_layout.addRow("Área do Processo:", self.area_input)
        form_layout.addRow("Valor do Cálculo (R$):", self.valor_calc_input)
        form_layout.addRow("Foi pago?", self.pago_input)
        form_layout.addRow("Foi enviado?", self.enviado_input)

        salvar_btn = QPushButton("💾 Salvar Cálculo")
        salvar_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 8px 16px; border-radius: 5px;")
        salvar_btn.clicked.connect(self.salvar_dados)

        novo_layout.addWidget(titulo)
        novo_layout.addLayout(form_layout)
        novo_layout.addWidget(salvar_btn)
        novo.setLayout(novo_layout)

        # Página 4: Cadastrar Cliente
        cadastrar_cliente = QWidget()
        cadastrar_layout = QVBoxLayout()
        titulo_cliente = QLabel("Cadastrar novo cliente")
        titulo_cliente.setFont(QFont("Arial", 14, QFont.Bold))
        titulo_cliente.setStyleSheet("color: #2e86de; margin-bottom: 10px;")

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.nome_cliente_input = QLineEdit()
        self.celular_input = QLineEdit()
        self.email_input = QLineEdit()
        self.oab_input = QLineEdit()

        form_layout.addRow("Nome completo:", self.nome_cliente_input)
        form_layout.addRow("Celular:", self.celular_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Carteira da OAB:", self.oab_input)

        salvar_cliente_btn = QPushButton("💾 Salvar Cliente")
        salvar_cliente_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px 16px; border-radius: 5px;")
        salvar_cliente_btn.clicked.connect(self.salvar_cliente)

        cadastrar_layout.addWidget(titulo_cliente)
        cadastrar_layout.addLayout(form_layout)
        cadastrar_layout.addWidget(salvar_cliente_btn)

        cadastrar_cliente.setLayout(cadastrar_layout)

        # Página 5: Lista de Processos
        self.lista_processos_page = QWidget()
        self.lista_processos_layout = QVBoxLayout()

        self.tabela_processos = QTableWidget()
        self.tabela_processos.setColumnCount(6)
        self.tabela_processos.setHorizontalHeaderLabels(["Nº Processo", "Prazo", "Área", "Valor (R$)", "Pago", "Enviado"])
        self.tabela_processos.horizontalHeader().setStretchLastSection(True)
        self.tabela_processos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.lista_processos_layout.addWidget(self.tabela_processos)
        self.lista_processos_page.setLayout(self.lista_processos_layout)

        # Página 6: Exportar
        exportar = QWidget()
        export_layout = QVBoxLayout()
        export_layout.addWidget(QLabel("Exportar dados em PDF ou Excel"))
        exportar.setLayout(export_layout)

        # Adiciona páginas ao layout
        self.pages.addWidget(dashboard)
        self.pages.addWidget(self.clientes_page)
        self.pages.addWidget(novo)
        self.pages.addWidget(cadastrar_cliente)
        self.pages.addWidget(self.lista_processos_page)
        self.pages.addWidget(exportar)

        main_layout.addWidget(self.menu)
        content_widget = QWidget()
        content_widget.setLayout(self.pages)
        main_layout.addWidget(content_widget)

        self.setCentralWidget(central_widget)
        self.carregar_clientes()

    def display_page(self, index):
        self.pages.setCurrentIndex(index)
        if index == 1:
            self.carregar_clientes()

    def salvar_dados(self):
        numero = self.processo_input.text()
        prazo = self.prazo_input.text()
        area = self.area_input.currentText()
        valor = self.valor_calc_input.text()
        pago = self.pago_input.currentText()
        enviado = self.enviado_input.currentText()

        row = self.tabela_processos.rowCount()
        self.tabela_processos.insertRow(row)
        self.tabela_processos.setItem(row, 0, QTableWidgetItem(numero))
        self.tabela_processos.setItem(row, 1, QTableWidgetItem(prazo))
        self.tabela_processos.setItem(row, 2, QTableWidgetItem(area))
        self.tabela_processos.setItem(row, 3, QTableWidgetItem(valor))
        self.tabela_processos.setItem(row, 4, QTableWidgetItem(pago))
        self.tabela_processos.setItem(row, 5, QTableWidgetItem(enviado))

        QMessageBox.information(self, "Info", "Cálculo salvo e adicionado à lista de processos!")

    def carregar_clientes(self):
        filtro_nome = self.filtro_nome.text().lower()
        todos_clientes = buscar_clientes()
        self.tabela_clientes.setRowCount(0)

        for cliente in todos_clientes:
            id_, nome, celular, email, oab = cliente
            if filtro_nome in nome.lower():
                row_position = self.tabela_clientes.rowCount()
                self.tabela_clientes.insertRow(row_position)
                self.tabela_clientes.setItem(row_position, 0, QTableWidgetItem(nome))
                self.tabela_clientes.setItem(row_position, 1, QTableWidgetItem(celular))
                self.tabela_clientes.setItem(row_position, 2, QTableWidgetItem(email))
                self.tabela_clientes.setItem(row_position, 3, QTableWidgetItem(oab))

                actions = QWidget()
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                btn_editar = QPushButton("Editar")
                btn_excluir = QPushButton("Excluir")
                btn_excluir.clicked.connect(lambda checked, id_=id_: self.excluir_cliente(id_))
                layout.addWidget(btn_editar)
                layout.addWidget(btn_excluir)
                actions.setLayout(layout)

                self.tabela_clientes.setCellWidget(row_position, 4, actions)

    def excluir_cliente(self, id_):
        confirmar = QMessageBox.question(self, "Confirmação", "Deseja realmente excluir este cliente?", QMessageBox.Yes | QMessageBox.No)
        if confirmar == QMessageBox.Yes:
            excluir_cliente(id_)
            QMessageBox.information(self, "Excluído", "Cliente removido com sucesso.")
            self.carregar_clientes()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
