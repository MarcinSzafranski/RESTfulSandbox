import requests
from time import sleep
from definitions import DOCKER_FLASK_URL


class ApiRequestTask:
    task_id: str
    name: str
    url: str
    server_url: str

    def __init__(self, name, url, **kwargs):
        print(f"Setting request task name as: {name},\n url address: {url}")
        self.name = name
        self.url = url
        self.set_server_url(**kwargs)
        self.get_url_contents()

    def set_server_url(self, **kwargs):
        if kwargs.get("url_address"):
            self.server_url = kwargs.get("url_address")
        else:
            self.server_url = DOCKER_FLASK_URL
        if not self.server_url.endswith("/"):
            self.server_url = self.server_url + "/"

    def get_url_contents(self):
        response = requests.post(f'{self.server_url}url/{self.name}/{self.url}')
        self.task_id = response.text.strip().strip('"')
        print(f"Requesting URL contents. Task ID:{self.task_id}")

    def get_task_status(self):
        response = requests.get(f'{self.server_url}status/{self.task_id}')
        print(f"Task '{self.name}' state is: \n{response.text.strip()}")

    def download_content(self, data_type):
        if data_type in ["images", 'text']:
            return f'Download link: {self.server_url}download/{self.name}/{data_type}'
        else:
            print(f"Unknown data type {data_type}")


if __name__ == "__main__":
    task1 = ApiRequestTask(name="Star_Wars", url="https://en.wikipedia.org/wiki/Star_Wars")
    task2 = ApiRequestTask(name="paintings", url="https://www.saatchiart.com/paintings")
    task1.get_task_status()
    task2.get_task_status()
    sleep(10)
    task2.get_task_status()
    task1.get_task_status()
    sleep(1)
    print(task1.download_content("images"))
    sleep(1)
    print(task2.download_content("images"))
    sleep(1)
    print(task1.download_content("text"))
    sleep(1)
    print(task2.download_content("text"))
