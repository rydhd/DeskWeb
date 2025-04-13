from website import create_app  # Import the function to initialize the Flask app


app = create_app()  # Create and configure the Flask app instance
    
if __name__ == '__main__':  # Ensures the script runs only when executed directly
    app.run(debug=True)  # Starts the Flask web server in debug mode, allowing live updates and error tracking

