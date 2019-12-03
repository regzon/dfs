from time import sleep
from client import Client

if __name__ == '__main__':
    client = Client('http://104.248.137.248:80')
    response = client.init()
    response = client.create_dir('/kek/')
    response = client.create_file('/kek/main.txt')
    response = client.write_file('/kek/main.txt', 'before.txt')
    sleep(4)
    client.read_file('/kek/main.txt')
    response = client.create_dir('/kek/cheburek')
    # response = client.delete_file('/kek/main.txt')
    client.copy_file('/kek/main.txt', '/kek/cheburek/example.txt')
    client.move_file('/kek/main.txt', '/last.txt')
    response = client.read_dir('/kek/')
    # response = client.delete_dir('/kek/')
    response = client.read_dir('/kek/')
    print(response)
