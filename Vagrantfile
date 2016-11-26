# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_check_update = false
  config.ssh.forward_agent = true

  config.vm.network "forwarded_port", guest: 22, host: 2226, id: 'ssh', auto_correct: true
  config.vm.network "private_network", ip: "192.168.23.95", auto_correct: true
  #config.vm.network "forwarded_port", guest: 9160, host: 9160, protocol: 'tcp', auto_correct: true

  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", "/var/www/application", :nfs => { group: "www-data", owner: "www-data" }, :mount_options => ['nolock,vers=3,udp,noatime']

  config.vm.provision "ansible" do |ansible|
    ansible.limit = "vagrant"
    ansible.inventory_path = "deploy/ansible/inventory/vagrant"
    ansible.playbook = "deploy/ansible/vagrant-playbook.yml"
    ansible.host_key_checking = false
    ansible.extra_vars = { ansible_ssh_user: 'vagrant',ansible_connection: 'ssh', ansible_ssh_args: '-o ForwardAgent=yes'}
  end
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.memory = 1000
    v.cpus = 2

    v.customize ["modifyvm", :id, "--usb", "on"]
    v.customize ["modifyvm", :id, "--usbehci", "on"]
    v.customize ["usbfilter", "add", "0",
        "--target", :id,
        "--name", "bluetooth dongle",
        "--manufacturer", "Apple Inc.",
        "--product", "Bluetooth USB Host Controller"]
  end
end
