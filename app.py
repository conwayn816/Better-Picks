from flask import Flask, render_template, redirect, url_for
from mongoengine import connect
import constants

connect(
    db="betterPicks",
    host=constants.MONGO_URI,
)

app = Flask(__name__)

# Views data
views_data = {
    'view1': {
        'title': 'View 1',
        'box_items': ["View 1 Item 1", "View 1 Item 2", "View 1 Item 3", "View 1 Item 4"]
    },
    'view2': {
        'title': 'View 2',
        'box_items': ["View 2 Item 1", "View 2 Item 2", "View 2 Item 3", "View 2 Item 4"]
    },
    'view3': {
        'title': 'View 3',
        'box_items': ["View 3 Item 1", "View 3 Item 2", "View 3 Item 3", "View 3 Item 4"]
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # By default, set the active view to 'view1'
    active_view = 'view1'
    return render_template('index.html', **views_data[active_view], active_view=active_view)

@app.route('/<view_name>', methods=['GET', 'POST'])
def switch_view(view_name):
    # Check if the requested view exists, if not, redirect to the default view
    if view_name not in views_data:
        return redirect(url_for('index'))
    return render_template('index.html', **views_data[view_name], active_view=view_name)

if __name__ == '__main__':
    app.run(debug=True)