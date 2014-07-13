Bootstrap a host against this ansible repository:

    [you@host ~]$ ansible-playbook --connection=local --inventory-file=localhost, playbooks/bootstrap.yml

Or, if you have many remote hosts to bootstrap over SSH:

    [you@host ~]$ ansible-playbook --inventory-file=hosts [--limit=groupname] playbooks/bootstrap.yml

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
2. Edit `group_vars/all`
2.1 Set your forked repo url
2.2 Set you user accounts & default first time login password
3. Bootstrap your host(s) as above. Your hosts will begin polling your
   repo
4. Ammend the groups & actions in local.yml
5. Assign your hosts to relevant groups, they will now perform actions
   defined for their group in local.yml

