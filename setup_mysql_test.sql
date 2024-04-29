#!/usr/bin/python3
""" a script that prepares a MySQL server for the project: """
# MySQL server configuration
MYSQL_ROOT_USER="root"
MYSQL_ROOT_PASSWORD="your_root_password"

# MySQL database and user details
DATABASE_NAME="hbnb_test_db"
DATABASE_USER="hbnb_test"
DATABASE_PASSWORD="hbnb_test_pwd"

# Checking if the database and user already exist
DB_EXISTS=$
(mysql -u $MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e "SELECT SCHEMA_NAME FROM
INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='$DATABASE_NAME'" --skip-column-names)
USER_EXISTS=$
(mysql -u $MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e
"SELECT User FROM mysql.user WHERE User='$DATABASE_USER'" --skip-column-names)

# Creating the database if it doesn't exist
if [ -z "$DB_EXISTS" ]; then
    mysql -u $MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE $DATABASE_NAME;"
    echo "Database '$DATABASE_NAME' created."
else
    echo "Database '$DATABASE_NAME' already exists."
fi

# Creating the user and set password if it doesn't exist
if [ -z "$USER_EXISTS" ]; then
    mysql -u $MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e
    "CREATE USER '$DATABASE_USER'@'localhost' IDENTIFIED BY '$DATABASE_PASSWORD';"
    echo "User '$DATABASE_USER' created."
else
    echo "User '$DATABASE_USER' already exists."
fi

# Granting privileges to the user
mysql -u $MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e
"GRANT ALL PRIVILEGES ON $DATABASE_NAME.* TO '$DATABASE_USER'@'localhost';"
mysql -u $MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e
"GRANT SELECT ON performance_schema.* TO '$DATABASE_USER'@'localhost';"
mysql -u $MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e "FLUSH PRIVILEGES;"

echo "Privileges granted to user '$DATABASE_USER'."

echo "MySQL server setup completed."