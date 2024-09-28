#For the future.
import os, csv
from PyQt6.QtWidgets import QInputDialog, QMessageBox
BASE_DIR = os.getcwd()

def model_selector(parent=None):
    folder_path = os.path.sep + "models"
    extension = ".gguf"
    files = [file for file in os.listdir(BASE_DIR + folder_path) if file.endswith(extension)]
    if not files:
        QMessageBox.warning(parent, "Model Selection", f"No {extension} models found in the folder.")
        return None

    selected_file, ok = QInputDialog.getItem(parent, "Model Selection", "Select a model:", files, 0, False)
    if ok and selected_file:
        return selected_file
    return None

def llama_args(parent=None, n_gpu_layers_default=-1, n_ctx_default=16386):
    var1, ok1 = QInputDialog.getInt(parent, "LLama Args", f"Change n_gpu_layers? (Default: {n_gpu_layers_default})", n_gpu_layers_default, -1, 100)
    if not ok1:
        return None, None
    
    var2, ok2 = QInputDialog.getInt(parent, "LLama Args", f"Change n_ctx? (Default: {n_ctx_default})", n_ctx_default, 1, 100000)
    if not ok2:
        return None, None
    
    return int(var1), int(var2)

def char_selector(parent=None):
    folder_path = "\history"
    extension = ".csv"
    shared_string = "history_"

    files = [file.replace(shared_string, "").replace(extension, "") for file in os.listdir(BASE_DIR + folder_path) if file.endswith(extension)]
    
    if not files:
        new_char, ok = QInputDialog.getText(parent, "New Character", "Provide a name for the new character:")
        if ok and new_char:
            return new_char
        return None

    selected_char, ok = QInputDialog.getItem(parent, "Character Selection", "Select a character or enter a new name:", files, 0, True)
    if ok and selected_char:
        if selected_char in files:
            return selected_char
        else:
            return selected_char  # This is a new character name
    return None

def prompter(role, content):
    message = '<|im_start|>'+ role +' \n' + content + '<|im_end|> \n'
    return message

def promp_generator(content):
    prompt = content +  '<|im_start|>assistant \n'
    return prompt

def history_update_print(role, conversation, conversation_dict, content, print_history=False, file_name=None):
    conversation += prompter(role, content)
    conversation_dict.append({"role": role, "content": content})
    if print_history:
        keys = conversation_dict[0].keys()
        history_path = os.path.join("history", f'history_{file_name}.csv')
        with open(history_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, keys)
            writer.writeheader()
            writer.writerows(conversation_dict)
    return conversation, conversation_dict