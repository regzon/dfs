from client import Client

if __name__ == '__main__':
    client = Client('http://localhost:8080')
    response = client.init()
    response = client.create_dir('/kek/')
    response = client.create_file('/kek/main.txt')
    response = client.create_dir('/kek/cheburek')
    response = client.read_dir('/kek/')
    print(response)
