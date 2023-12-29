from snpapp import create_app, db
from snpapp.models import SNPAnnotation

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)