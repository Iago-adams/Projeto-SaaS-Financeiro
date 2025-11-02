from app import create_app, create_permissions

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        create_permissions()
        
    app.run(debug=True)
