from website import create_app

if __name__ == "__main__":
    app = create_app()
    
    # everytime you make a change to python code, 
    # it will automatically run code
    app.run(debug=True) # default port 5000
    # app.run(debug=True, port=3000)  <- this is how to change port


    