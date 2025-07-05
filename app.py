import webview

from src.ui.chat_ui import demo as gradio_app  # UPDATED IMPORT PATH

gradio_app.launch(prevent_thread_lock=True)

webview.create_window("Simplify your life", gradio_app.local_url)  # Change the title if needed
webview.start()