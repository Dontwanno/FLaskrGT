import os
from flask import Flask, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/query-example')
    def query_example():
        # if key doesn't exist, returns None
        language = request.args.get('language')

        # if key doesn't exist, returns a 400, bad request error
        framework = request.args['framework']

        # if key doesn't exist, returns None
        website = request.args.get('website')

        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>
                  <h1>The website value is: {}'''.format(language, framework, website)

    @app.route('/form-example')
    @app.route('/form-example', methods=['GET', 'POST'])
    def form_example():
        # handle the POST request
        if request.method == 'POST':
            language = request.form.get('language')
            framework = request.form.get('framework')
            return '''
                      <h1>The language value is: {}</h1>
                      <h1>The framework value is: {}</h1>'''.format(language, framework)

        # otherwise handle the GET request
        return '''
               <form method="POST">
                   <div><label>Language: <input type="text" name="language"></label></div>
                   <div><label>Framework: <input type="text" name="framework"></label></div>
                   <input type="submit" value="Submit">
               </form>'''

    @app.route('/json-example', methods=['POST'])
    def json_example():
        request_data = request.get_json()

        language = None
        framework = None
        python_version = None
        example = None
        boolean_test = None

        if request_data:
            if 'language' in request_data:
                language = request_data['language']

            if 'framework' in request_data:
                framework = request_data['framework']

            if 'version_info' in request_data:
                if 'python' in request_data['version_info']:
                    python_version = request_data['version_info']['python']

            if 'examples' in request_data:
                if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
                    example = request_data['examples'][0]

            if 'boolean_test' in request_data:
                boolean_test = request_data['boolean_test']

        return '''
               The language value is: {}
               The framework value is: {}
               The Python version is: {}
               The item at index 0 in the example list is: {}
               The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

    return app
