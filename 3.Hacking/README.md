Fork this repo and customise the config to suit yourself. The primary
configuration areas are:

1. Setup your own kickstart file under ``1.Bootstrap``
2. Update the hosts list under ``2.Config/hosts`` for your network
3. Change the Ansible configuration under ``2.Config``


## Testing Playbooks ##

All playbooks have associated tests. The ``Vagrantfile`` in this
directory defines a machine suitable for running the tests. To run the
tests:

1. Install vagrant + virtualbox
2. Clone this repo
3. Run ``vagrant up`` from this directory
3.1. This will install a bare virtual machine
3.2. Install ansible in pull mode on the virtual machine, cloning the
     ``testing`` branch from this repo in the process
3.3. Launch the full test suite (once)
3.4. Write out test results in this directory
4. You can rerun individual tests adhoc or you can ``vagrant destroy``
   the ``vagrant up`` again to repeat the tests from the top with any
   fresh changes on the ``testing`` branch

