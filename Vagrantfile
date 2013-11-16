# -*- mode: ruby -*-
# vi: ft=ruby

Vagrant.configure("2") do |config|
  config.vm.box = "Fedora-19-x64"
  config.vm.box_url = "https://dl.dropboxusercontent.com/u/86066173/fedora-19.box"

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "plays/install-pull-mode.yml"
    ansible.inventory_path = "hosts-testing"
  end

  config.vm.define :test1 do |test1|
    test1.vm.network :private_network, ip: "10.10.10.100"
    test1.vm.provider "virtualbox" do |v|
      v.name = "ansible-test1"
    end
  end

end

