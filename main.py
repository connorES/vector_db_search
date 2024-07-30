from multiprocessing import freeze_support
from app import Application

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    freeze_support()
    main()