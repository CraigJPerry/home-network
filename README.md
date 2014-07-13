Bootstrap a host against this ansible repository:

    [you@host ~]$ ansible-playbook --connection=local --inventory-file=localhost, playbooks/bootstrap.yml

Or, if you have many remote hosts to bootstrap over SSH:

    [you@host ~]$ ansible-playbook --inventory-file=hosts playbooks/bootstrap.yml

This will automatically:

* Use sudo if you are not root
* Ensure ansible and git are installed
* Create an ansible user account
* Provision the ansible user account with required sudo access
* Establish a crontab to download and play local.yml every hour

### Notes ###

All my roles come with a tests.yml, there is no widely adopted
convention for tests as yet. This works for me, so far.

## Making It Your Own ##

1. Fork this project
2. Edit `group_vars/all`, see comments for how to set a default password
   (you will be forced to choose a new one on login)
3. Update the `pull_command` variable to point to your forked repo (see
   `roles/install_ansible_pull/defaults/main.yml`)
4. At this point, you can bootstrap hosts by running the bootstrap
   playbook. You hosts will begin polling your repo and they'll maintain
   their ansible-pull configuration but nothing else. I.e. all they'll
   do is keep checking your repo.
5. Assign your hostnames to as many groups as makes sense
6. Set your groups to do things in local.yml

