#!/bin/bash

# source parse_yaml.sh
# eval $(parse_yaml launch-configuration.yaml)
# echo "admin_mount = ${admin_mount}" 
# if [ ! -d ${admin_mount} ] ; then 
#   echo "path $(eval echo \$${f}) doesn't exist! Aborting!"
#   exit 1
# fi
# users_mounts_docker=""
# for f in $users_mounts_ ; do
#   eval echo \$f "=" \$${f}
#   if [ ! -d $(eval echo \$${f}) ] ; then 
#     echo "path $(eval echo \$${f}) doesn't exist! Aborting!"
#     exit 1
#   fi
#   users_mounts_docker="${users_mounts_docker} -v $(eval echo \$${f}):/mnt/user-mounts/$f"
# done
# # echo "users_mounts_docker: ${users_mounts_docker}"

# groups_mounts_docker=""
# for f in $groups_mounts_ ; do
#   eval echo \$f "=" \$${f}
#   if [ ! -d $(eval echo \$${f}) ] ; then 
#     echo "path $(eval echo \$${f}) doesn't exist! Aborting!"
#     exit 1
#   fi
#   groups_mounts_docker="${groups_mounts_docker} -v $(eval echo \$${f}):/mnt/group-mounts/$f"
# done
# # echo "groups_mounts_docker: ${groups_mounts_docker}"

# docker run --name some-nginx -d -p 8080:80 -p 5000:5000 hello-world-nginx
app_root="/var/www/myapp"

docker run --name cuno-py-manager \
  -d \
  -p 5000:5000 \
  -v $PWD/myapp/config.py:$app_root/config.py:ro \
  -v $PWD/myapp/flask_app.py:$app_root/flask_app.py:ro \
  -v $PWD/myapp/utils:$app_root/utils:ro \
  -v $PWD/myapp/static:$app_root/static:ro \
  -v $PWD/myapp/templates:$app_root/templates:ro \
  -v $PWD/launch-configuration.yaml:$app_root/launch-configuration.yaml:ro \
  -v $PWD/setup.py:/var/www/setup.py:ro \
  -v $PWD/tests:/tests \
  cuno-python-web-app

# -v $admin_mount:/mnt/admin-mount/ \
#   $users_mounts_docker \
#   $groups_mounts_docker \
  

docker exec -d cuno-py-manager systemctl start myapp

# docker exec some-nginx systemctl status myapp
# docker restart some-nginx
