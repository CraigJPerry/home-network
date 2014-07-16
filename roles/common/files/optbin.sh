
if ! echo ${PATH} | /bin/grep -q /opt/bin ; then
    PATH=/opt/bin:${PATH}
fi

