# terminal-llm
A simple LLM interface with both terminal and GUI options to lower the entry barrier to this technology.

## How to use?

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the GUI version:
   ```
   python gui_main.py
   ```

3. For the terminal version, use:
   ```
   python llm_local.py
   ```

## New GUI Features
The application now features a graphical user interface built with PyQt6. You can interact with the LLM chat, create files and ideas, load and delete ideas, and list available ideas all through a user-friendly interface.

### GUI Features:
- Chat interface with the LLM
- Create new files
- Create, load, and delete ideas
- List available ideas
- Select different LLM models

### How to use the GUI:
1. Launch the application by running `gui_main.py`
2. Select a model from the dropdown menu and click "Select Model"
3. Use the chat interface to communicate with the LLM
4. Use the function buttons to create files, manage ideas, and perform other actions

## Terminal Version
The terminal version is still available and provides the same functionality as before. Use `llm_local.py` to run the terminal version.

## Configuration
The `llm_config.json` file contains settings for the LLM. You can modify these settings to adjust the behavior of the model.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the terms of the LICENSE file in the root directory of this project.