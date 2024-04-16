<h1 align=center>Final Project</h1>
<h3 align=center>First step</h3>
<b>Download project:</b>
<p>git clone https://github.com/HabibiDev/Final-Project.git</p>
<b>Create and activation virtualenv:</b>
<p>python3 -m venv env</p>
<p>. env/bin/active</p>
<b>Install requirements:</b>
<p>cd Final-Project</p>
<p>pip install -r requirements.txt</p>
<h3 align=center>Second Step</h3>
<b>Install postgres and create database</b>
<p>sudo apt-get update</p>
<p>sudo apt install postgresql postgresql-contrib</p>
<p>sudo -u postgres psql</p>
<p>CREATE USER slando_admin WITH PASSWORD '123';</p>
<p>ALTER USER slando_admin CREATEDB;</p>
<p>ALTER ROLE slando_admin SET CLIENT_ENCODING TO 'utf8';</p>
<p>ALTER ROLE slando_admin SET TIMEZONE TO 'UTC';</p>
<p>CREATE DATABASE slando_db OWNER slando_admin;</p>
<h3 align=center>Third step</h3>
<b>Create migrate, loaddata and run webapp</b>
<p>cd slando</p>
<p>python manage.py migrate</p>
<p>python manage.py loaddata fixtures/users</p>
<p>python manage.py loaddata fixtures/post_models</p>
<p>python manage.py runserver</p>
<b>Open another terminal and run celery</b>
<p>Open two terminal for worker and beat in your project directory</p>
<p>Activate virtualenv<p>
<p>cd Final-Project/slando/</p> 
<p>in first terminal run: celery -A slando worker -l info</p>
<p>in second terminal run: celery -A slando beat -l info</p>
<h3 align=center>Last step</h3>
<p>Open browser and run http://127.0.0.1:8000/</p>
<h3 align=center>Users</h3>
<p><b>Username:</b> 'admin' <b>Password:</b> 'admin'</p>
<p><b>Username:</b> 'User_1' <b>Password:</b> '1111111'</p>
<p><b>Username:</b> 'User_2' <b>Password:</b> '22222222'</p>
<p><b>Username:</b> 'User_3' <b>Password:</b> '33333333'</p>
<h3 align=center>Urls</h3>
<p>http://127.0.0.1:8000/accounts/login</p>
<p>http://127.0.0.1:8000/register</p>
<p>http://127.0.0.1:8000/swagger</p>
