from client import Client

if __name__ == '__main__':
    client = Client('http://localhost:8080')
    response = client.delete_dir('./your/name')
    print(response)
