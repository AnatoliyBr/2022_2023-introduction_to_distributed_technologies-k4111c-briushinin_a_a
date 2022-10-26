import os


def create_dir(dir_name, dir_num):
    '''
    Создание директорий
    dir_name: str
    dir_num: int
    '''

    for i in range(1, dir_num + 1):
        if not os.path.isdir(dir_name + str(i)):
            os.mkdir(dir_name + str(i))

def create_file(file_name, file_type, dir_name, dir_num, text):
    '''
    Создание файлов
    file_name: str
    file_type: str
    dir_name: str
    dir_num: int
    '''

    for all_dir_path, all_dir_names, all_file_names in os.walk("."):
        for all_dir_name in all_dir_names:
            if dir_name in all_dir_name:
                if file_name not in all_file_names:
                    path = os.path.join(all_dir_name, all_dir_name + file_name + file_type)
                    with open(path, "w") as file:
                        file.write(text.replace('lab_num', all_dir_name.title()))

def main():

    dir_name = 'lab'
    dir_num = 4
    file_name = '_report'
    file_type = '.md'

    group = 'K4111c'
    author = 'Briushinin Anatolii Alekseevich'
    data = '21.10.2022'

    header_text = '''
        University: [ITMO University](https://itmo.ru/ru/)
        Faculty: [FICT](https://fict.itmo.ru)
        Course: [Introduction to distributed technologies](https://github.com/itmo-ict-faculty/introduction-to-distributed-technologies)
        Year: 2022/2023
        Group: {group}
        Author: {author}
        Lab: lab_num
        Date of create: {data}
        Date of finished: -
        '''.format(group = group, author = author, data = data)

    create_dir(dir_name, dir_num)
    create_file(file_name, file_type, dir_name, dir_num, header_text)

if __name__ == "__main__":
    main()