import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLineEdit, QLabel, QComboBox, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt
from modules.functions import create_file, create_idea, load_idea, delete_idea, list_ideas
from modules.helpers import model_selector, llama_args, char_selector
from llama_cpp import Llama
import json

class LLMChatGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Chat Interface")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_ui()
        self.load_config()
        self.initialize_llm()

    def setup_ui(self):
        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.layout.addWidget(self.chat_area)

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        self.layout.addLayout(input_layout)

        # Function buttons
        function_layout = QHBoxLayout()
        self.create_file_button = QPushButton("Create File")
        self.create_file_button.clicked.connect(self.create_file_dialog)
        self.create_idea_button = QPushButton("Create Idea")
        self.create_idea_button.clicked.connect(self.create_idea_dialog)
        self.load_idea_button = QPushButton("Load Idea")
        self.load_idea_button.clicked.connect(self.load_idea_dialog)
        self.delete_idea_button = QPushButton("Delete Idea")
        self.delete_idea_button.clicked.connect(self.delete_idea_dialog)
        self.list_ideas_button = QPushButton("List Ideas")
        self.list_ideas_button.clicked.connect(self.list_ideas)
        function_layout.addWidget(self.create_file_button)
        function_layout.addWidget(self.create_idea_button)
        function_layout.addWidget(self.load_idea_button)
        function_layout.addWidget(self.delete_idea_button)
        function_layout.addWidget(self.list_ideas_button)
        self.layout.addLayout(function_layout)

        # Model selection
        model_layout = QHBoxLayout()
        self.model_selector = QComboBox()
        self.model_selector.addItems(["Model 1", "Model 2", "Model 3"])  # Replace with actual model names
        self.select_model_button = QPushButton("Select Model")
        self.select_model_button.clicked.connect(self.select_model)
        model_layout.addWidget(QLabel("Model:"))
        model_layout.addWidget(self.model_selector)
        model_layout.addWidget(self.select_model_button)
        self.layout.addLayout(model_layout)

    def load_config(self):
        with open('llm_config.json', 'r') as file:
            self.llm_config = json.load(file)

    def initialize_llm(self):
        model_name = model_selector(self)
        if model_name:
            n_gpu, n_context = llama_args(self)
            if n_gpu is not None and n_context is not None:
                self.llm = Llama(model_path="./models/" + model_name, chat_format="llama-2", n_gpu_layers=n_gpu, n_ctx=n_context)
                self.llm_name = char_selector(self)
                self.chat_area.append(f"Initialized LLM: {self.llm_name}")

    def send_message(self):
        user_message = self.input_field.text()
        self.chat_area.append(f"User: {user_message}")
        self.input_field.clear()

        # Process the message and get LLM response
        output = self.llm(prompt=user_message,
                          max_tokens=self.llm_config["max_tokens"],
                          stop=self.llm_config["stop"],
                          temperature=self.llm_config["temperature"],
                          top_p=self.llm_config["top_p"],
                          top_k=self.llm_config["top_k"],
                          min_p=self.llm_config["min_p"],
                          repeat_penalty=self.llm_config["repeat_penalty"])
        assistant_message = output["choices"][0]["text"]
        self.chat_area.append(f"{self.llm_name}: {assistant_message}")

    def create_file_dialog(self):
        file_name, ok = QInputDialog.getText(self, "Create File", "Enter file name:")
        if ok and file_name:
            result = create_file(file_name)
            QMessageBox.information(self, "File Creation", result)

    def create_idea_dialog(self):
        idea_name, ok1 = QInputDialog.getText(self, "Create Idea", "Enter idea name:")
        if ok1 and idea_name:
            content, ok2 = QInputDialog.getMultiLineText(self, "Create Idea", "Enter idea content:")
            if ok2:
                result = create_idea(idea_name, content)
                QMessageBox.information(self, "Idea Creation", result)

    def load_idea_dialog(self):
        idea_name, ok = QInputDialog.getText(self, "Load Idea", "Enter idea name:")
        if ok and idea_name:
            content = load_idea(idea_name)
            if content != "Idea not found":
                self.chat_area.append(f"Loaded Idea '{idea_name}':\n{content}")
            else:
                QMessageBox.warning(self, "Load Idea", "Idea not found")

    def delete_idea_dialog(self):
        idea_name, ok = QInputDialog.getText(self, "Delete Idea", "Enter idea name:")
        if ok and idea_name:
            result = delete_idea(idea_name)
            QMessageBox.information(self, "Delete Idea", result)

    def list_ideas(self):
        ideas = list_ideas()
        if isinstance(ideas, list):
            self.chat_area.append("Available Ideas:\n" + "\n".join(ideas))
        else:
            self.chat_area.append(ideas)

    def select_model(self):
        selected_model = self.model_selector.currentText()
        # Implement model switching logic here
        QMessageBox.information(self, "Model Selection", f"Selected model: {selected_model}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LLMChatGUI()
    window.show()
    sys.exit(app.exec())
