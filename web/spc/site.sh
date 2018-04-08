sudo mv forum/src/coreScripts/myforum.conf /etc/apache2/conf-available
sudo mkdir -p /var/www/html/spc
sudo cp -r forum/src/UI/* /var/www/html/spc/
