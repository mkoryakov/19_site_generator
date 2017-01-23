import json
import os.path
from markdown import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_data_from_json(file_name):
    if not os.path.exists(file_name):
        return None
    with open(file_name) as f:
        return json.load(f)


def generate_index_page(topics, articles):
    for topic in topics[:1]:
        html_links = [article['title'] for article in articles
                      if topic['slug'] == article['topic']]
    return html_links


if __name__ == '__main__':
    config = load_data_from_json('config.json')
    topics = config['topics']
    articles = config['articles']
    html_links = generate_index_page(topics, articles)

    loader = FileSystemLoader('./templates')
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('index.html')

    # html_links = {'Main Page':'http://xgu.ru', 'Jinja':'http://xgu.ru/wiki/Jinja2'}
    data = {'title':'Site information','header_1':'Popular pages','links':html_links}

    with open("new.html", "w") as f:
        f.write(template.render(data))
        # f.write(markdown(open('articles/'+ articles[0]['source']).read(), extensions=['codehilite']))