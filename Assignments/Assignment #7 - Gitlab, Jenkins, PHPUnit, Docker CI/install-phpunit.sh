#! /bin/bash

wget https://phar.phpunit.de/phpunit-6.5.phar
chmod +x phpunit-6.5.phar
sudo mv phpunit-6.5.phar /usr/local/bin/phpunit
phpunit --version

sudo apt-get install -y php-invoker

sudo apt-get install php-dom