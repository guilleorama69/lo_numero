from app import create_app, mysocket

app = create_app()

if __name__ == '__main__':
    mysocket.run(app, port=5000, host='0.0.0.0')
