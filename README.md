# RESTfulSandbox
This project is a flask-celery web scraper, easy to deploy on docker.
To see how it works, please set DOCKER_FLASK_URL at definitions.py change the docker IP address for the one you can reach from your environment.
Next, you can check use_example.py for simply use command 'python use_example.py'. 
It will run API queries example with a 10 second brake for the execution.

# API classes examples:
1. GetUrlContents downloads URL contents (images and text). Images are stored in the archive with the name given in the API query.
Names are unique. It responds with task id.
http://HOST_IP:5000/url/<name>/<path:url>       : http://HOST_IP:5000/url/painting/https://www.saatchiart.com/paintings
2. GetTaskStatus gets task status of task with specified id.
http://HOST_IP:5000/status/<task_id>            : http://HOST_IP:5000/status/0b81ce65-0316-40db-8bf0-c641427203d3
3. DownloadFile allows to download the images and text scraped by GetUrlContents.
http://HOST_IP:5000/download/<name>/<file_type> : http://HOST_IP:5000/download/painting/images
                                                : http://HOST_IP:5000/download/painting/text
