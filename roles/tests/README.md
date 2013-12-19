## Testing Roles ##

All roles have proper tests because:

* Good tests prevent roles from scope-creeping
* Roles are reused, tests pay off many times over
* Roles are likely to be edited or extended

Add test cases if you're extending a role or adding new ones. Ensure
all tests pass before submitting pull requests.


### How-To ###

Tests are run in a virtual machine to allow cross-platform development
and prevent broken tests destroying your devbox.


#### Development Dependencies ####

Install these packages for your platform:

* Ansible (v1.3+)
* VirtualBox
* Vagrant (v1.1+)


#### Running Tests ####

Tests are always run as root to mirror how roles are run. To run all tests:

    [user@devbox ~]$ vagrant up
    [user@devbox ~]$ vagrant ssh
    [vagrant@vm ~]$ cd /vagrant
    [vagrant@vm /vagrant]$ sudo python2.7 -m unittest discover

To run a single test::

    [vagrant@vm /vagrant]$ sudo python2.7 -m unittest tests.test_install_ansible.InstallAnsible.test_setup_correctly

