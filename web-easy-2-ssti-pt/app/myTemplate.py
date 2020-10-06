
def my_template(data: str):
    template = ''
    with open('templates/index_page.html', 'r') as file:
        template += file.read()
        file.close()
    return (template % data)



