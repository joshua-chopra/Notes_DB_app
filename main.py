from website import create_app

app = create_app()

# if we run main.py we execute this line and run our app. only run web server if we run main.py, e.g., py main.py cmd
if __name__ == '__main__':
    # avoid re-running website over and over whenever we update.
    app.run(debug=True)