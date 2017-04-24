iMobility Async Service Scaffold
================================

This project has everything for you to kick off a new microservice based on `aiohttp`.

Initialization
--------------
After creating a new GitHub repository (do not initialize with a README), execute the following commands,
modifying the first line to fit the name of your repository:

```bash
export SERVICE_NAME=new-service

git clone git@github.com:i-mobility/async-scaffold.git $SERVICE_NAME
cd $SERVICE_NAME
git remote set-url origin git@github.com:i-mobility/$SERVICE_NAME.git

sed -e "s/SERVICE_NAME/"$SERVICE_NAME"/g" README.template.md > README.md
rm README.template.md
git commit -am "scaffold initalization for $SERVICE_NAME"

git push -u origin master
git checkout -b develop
git push -u origin develop

git flow init -d
./setupgithooks.sh
```
