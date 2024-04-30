from JobFinder import create_app
# Everything in __init__ is ran when a package is loaded!

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
