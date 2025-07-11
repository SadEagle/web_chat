# Setup postgre environment script
# TODO: wrap into shell
create role chatter option createdb login password 'secret';
set role chatter;
create database prod_chat owner chatter;
create database dev_chat owner chatter;
create database test_chat owner chatter;
