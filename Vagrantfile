Vagrant.configure("2") do |config|
    config.vm.box = "trusty64uci"
    config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    config.vm.provision "shell", path: "setup/provision_local.sh"
    config.vm.hostname = "doris"
    config.vm.network "private_network", ip: "192.168.122.114"
end
