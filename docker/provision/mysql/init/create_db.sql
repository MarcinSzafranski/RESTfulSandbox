CREATE DATABASE IF NOT EXISTS `sqlalchemy`;
CREATE DATABASE IF NOT EXISTS `celery`;
DROP USER 'root';
FLUSH PRIVILEGES;
CREATE USER 'root' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root';