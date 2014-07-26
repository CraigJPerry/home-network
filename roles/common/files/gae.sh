
if ! echo ${PATH} | /bin/grep -q /opt/google_appengine ; then
    PATH=/opt/google_appengine:${PATH}
fi

