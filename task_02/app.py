from flask import Flask, render_template
import login
app = Flask(__name__)

courses = login.execute()

print(courses)

@app.route('/')
def index():
    return render_template('index.html', courses=courses['results'])


if __name__ == '__main__':
    app.run(debug=True)
