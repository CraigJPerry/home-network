Bootstrap a host against this ansible repository:

    [you@host ~]$ ansible-playbook --connection=local --inventory-file=localhost, playbooks/bootstrap.yml

Or, if you have many remote hosts to bootstrap over SSH:

    [you@host ~]$ ansible-playbook --inventory-file=hosts playbooks/bootstrap.yml

This will automatically:

* Use sudo if you are not root. If you are root, sudo will not be used
* Ensure ansible and git are installed
* Create an ansible user account
* Provision the ansible user account with required sudo access
* Establish a crontab to download and play local.yml every hour

### Notes ###

All my roles come with a tests.yml, there is no widely adopted
convention for tests as yet. This works for me, so far.

