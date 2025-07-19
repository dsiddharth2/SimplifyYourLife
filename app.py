from src.ui.chat_ui import demo as gradio_app  # UPDATED IMPORT PATH

if __name__ == "__main__":
    try:
        gradio_app.launch(
            prevent_thread_lock=False,  # Changed to False to block main thread
            inbrowser=True
        )
    except KeyboardInterrupt:
        print("Application stopped by user")
    except Exception as e:
        print(f"Error launching application: {e}")
        input("Press Enter to exit...")  # Keep window open to see error