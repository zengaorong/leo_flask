#coding=utf-8
from . import novel


@novel.route('/', methods=['GET', 'POST'])
def index():
    return "hello world"