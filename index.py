from flask import Flask, redirect, url_for, render_template
from flask_htmlmin import HTMLMIN
from jinja2.exceptions import TemplateNotFound


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 604800
app.config['MINIFY_PAGE'] = True

HTMLMIN(app)

@app.errorhandler(403)
def page_access_forbidden(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/<filename>')
def root(filename):
    if filename.startswith("/"):
        filename = filename[1:]

    return redirect(url_for('static', filename='root/' + filename))

@app.route('/about')
def about():
    return render_template('about/about.html')

@app.route('/projects/')
def projects():
    return render_template('projects/gallery/gallery.html')

@app.route('/projects/<project>')
def show_project(project):
    return try_to_render_template('projects/%s/index.html' % project)

@app.route('/projects/<project>/<page>')
def show_project_page(project, page):
    return try_to_render_template('projects/%s/pages/%s.html' % (project, page))

@app.route('/research/')
def research():
    return redirect(url_for('research_project', project='virtual-dialogue'))

@app.route('/research/<project>')
def research_project(project):
    return try_to_render_template('research/%s/index.html' % project)

@app.route('/contact')
def contact():
    return render_template('contact/contact.html')


def try_to_render_template(url):
    try:
        return render_template(url)
    except TemplateNotFound as error:
        return page_not_found(error)
    except Exception as other_exception:
        raise other_exception


if __name__ == '__main__':
    app.run(debug=True)
