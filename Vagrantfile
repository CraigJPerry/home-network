# -*- mode: ruby -*-
# vi: ft=ruby
#
# A virtual machine to run playbook tests from within. Playbooks modify
# the system in ways that can result in a broken machine during
# development / testing cycles. It's good to be able to blow away the
# machine and get a fresh start with one command!
#

Vagrant.configure("2") do |config|
  config.vm.box = "Fedora-19-x64"
  config.vm.box_url = "https://dl.dropboxusercontent.com/u/86066173/fedora-19.box"

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "plays/install-pull-mode.yml"
    ansible.inventory_path = "hosts-testing"
  end

  config.vm.define :ansible-test-runner do |ansible-test-runner|
    ansible-test-runner.vm.network :private_network, ip: "10.10.10.100"
    ansible-test-runner.vm.provider "virtualbox" do |v|
      v.name = "ansible-ansible-test-runner"
    end
  end

end

