from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# fa43da3d-e2e6-04f9-4551-33143c0353b5

# auth
# HRKU-5eaee473-9e4a-4f08-a3d8-0afec07cfb05