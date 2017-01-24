from json import load
from os import mkdir
from os.path import exists, join, split, splitext
from markdown import markdown
from jinja2 import Environment, FileSystemLoader


def load_data_from_json(file_path):
    if not exists(file_path):
        return None
    with open(file_path) as f:
        return load(f)


def get_markdown_text(file_path):
    if not exists(file_path):
        return None
    with open(file_path) as f:
        return f.read()


def save_text_to_file(file_path, text):
    dir_name, file_name = split(file_path)
    if not exists(dir_name):
        mkdir(dir_name, mode=0o755)
    with open(file_path, 'w') as f:
        f.write(text)


def generate_page_from_template(template_name, data):
    loader = FileSystemLoader('templates')
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_name)
    return template.render(data)


def markdown_to_html(text):
    return markdown(text, extensions=['codehilite'])


def generate_site(site_name, config):
    articles_dir = '%s/%s' % (site_name, 'articles')
    if not exists(articles_dir):
        mkdir(articles_dir, mode=0o755)
    topics = config['topics']
    articles = config['articles']
    template = 'article.html'
    for article in articles:
        md_path = join('articles', article['source'])
        md_text = get_markdown_text(md_path)
        html_text = markdown_to_html(md_text)
        data = {'title': article['title'], 'text': html_text}
        page = generate_page_from_template(template, data)
        root, ext = splitext(article['source'])
        article['source'] = '%s%s' % (root, '.html')
        html_path = join(articles_dir, article['source'])
        save_text_to_file(html_path, page)
    template = 'index.html'
    data = {'topics': topics, 'articles': articles}
    page = generate_page_from_template(template, data)
    file_path = join(site_name, 'index.html')
    save_text_to_file(file_path, page)


if __name__ == '__main__':
    site_name = 'encyclopedia'
    if not exists(site_name):
        mkdir(site_name, mode=0o755)
    config = load_data_from_json('config.json')
    generate_site(site_name, config)
