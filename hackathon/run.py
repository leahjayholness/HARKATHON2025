from app import create_app  # Import the application factory

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the app
    app.run(debug=True)  # Set debug=True for development; disable for production
