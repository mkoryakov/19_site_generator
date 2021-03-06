from json import load
from argparse import ArgumentParser
from os import mkdir
from os.path import exists, join, split, splitext
from shutil import copytree
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


def recurcive_copy_directory(src, dst):
    copytree(src, dst)


def get_tempate(template_name):
    loader = FileSystemLoader('templates')
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    return env.get_template(template_name)


def generate_html_page_from_template(template, context):
    return template.render(context)


def markdown_to_html(text):
    return markdown(text, extensions=['codehilite'], safe_mode='escape')


def generate_site(site_name, config):
    articles_dir = join(site_name, 'articles')
    if not exists(articles_dir):
        mkdir(articles_dir, mode=0o755)
    topics = config['topics']
    articles = config['articles']
    template_name = 'article.html'
    for article in articles:
        md_path = join('articles', article['source'])
        md_text = get_markdown_text(md_path)
        html_text = markdown_to_html(md_text)
        context = {'title': article['title'], 'text': html_text}
        template = get_tempate(template_name)
        html_page = generate_html_page_from_template(template, context)
        root, ext = splitext(article['source'])
        article['source'] = '%s%s' % (root, '.html')
        html_path = join(articles_dir, article['source'])
        save_text_to_file(html_path, html_page)
    template_name = 'index.html'
    context = {'topics': topics, 'articles': articles}
    template = get_tempate(template_name)
    html_page = generate_html_page_from_template(template, context)
    file_path = join(site_name, 'index.html')
    save_text_to_file(file_path, html_page)


def get_config_file_name():
    parser = ArgumentParser(prog='md_to_html',
                            description='Скрипт конвертирует файлы формата md в html')
    parser.add_argument('--config', help='файл постановки', type=str,
                        default='config.json')
    return parser.parse_args().config


if __name__ == '__main__':
    site_name = 'encyclopedia'
    if not exists(site_name):
        mkdir(site_name, mode=0o755)
    config_file_name = get_config_file_name()
    config = load_data_from_json(config_file_name)
    generate_site(site_name, config)
    if not exists(join(site_name, 'css')):
        recurcive_copy_directory('css', join(site_name, 'css'))
