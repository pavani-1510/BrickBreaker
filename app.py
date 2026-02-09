from flask import Flask, render_template_string

app = Flask(__name__)

# Read the HTML file content
with open('brick_breaker.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

@app.route('/')
def index():
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
