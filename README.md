# Сирин / Sirin

Sirin registra las peticiones de los equipos del centro cuando arrancan y después permite obtener una lista de IPs para utilizar con el parámetro `--limit` de `ansible-playbook`, ejecutando el `playbook` sobre los ordenadores que están encendidos.

La idea es que un ordenador notifica a Sirin que está encendido en cada arranque, pero Sirin únicamente registra la petición del ordenador si ha transcurrido el tiempo definido por el parámetro de configuración `EXCLUSION_TIME` desde la última solicitud registrada y procesada por `Ansible` (o si es la primera vez que recibe una solicitud de este equipo).

El comando `python manage.py listpendingrequests` permite obtener una lista de las peticiones registradas por Sirin que aún no han sido atendidas por `Ansible`.

~~~
(env) usuario@laika:~/desarrollo/sirin/sirin$ python manage.py listpendingrequests
ID       ADDRESS                          DATETIME                        
8        192.168.1.144                    2020-12-26 18:21:16             
9        192.168.1.1                      2020-12-01 10:42:26             
10       192.168.1.2                      2020-12-02 00:00:00             
(env) usuario@laika:~/desarrollo/sirin/sirin$
~~~

El comando `python manage.py gethosts` retorna una lista con la dirección de cada equipo por procesar en el `playbook` utilizando el parámetro `--limit=` de `ansible-playbook`.

~~~
python manage.py gethosts
192.168.1.144,192.168.1.1,192.168.1.2,
~~~

Cuando se ejecuta el comando `python manage.py gethosts` las solicitudes correspondientes a las direcciones devueltas pasarán a considerarse procesadas. Y no se marcarán como no procesadas hasta que no se vuelva a recibir una petición de ese equipo pasado `EXCLUSION_TIME`.

# Puesta en marcha

Sirin es una aplicación Django así que se utilizará Python. El ORM de Django únicamente guarda las solicitudes de los equipos (dirección, datetime) así que probablemente SQLite sea suficiente para manejar muchos equipos.

Para utilizar una aplicación Django en producción conviene [seguir las recomendaciones oficiales.](https://docs.djangoproject.com/en/3.1/howto/deployment/)

## Instalación

a) Instalamos `python3-venv`

~~~
apt update
apt install python3-venv
~~~

b) Creamos un directorio y un `venv`

~~~
mkdir sirin
cd sirin
python3 -m venv venv
~~~

c) Activamos el `venv`

~~~
source venv/bin/activate
~~~

d) Descargamos Sirin

~~~
git clone https://github.com/vcarceler/sirin.git
~~~

e) Instala los requisitos, procesa las migraciones y crea un usuario administrador

~~~
cd sirin
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
~~~

f) Ejecuta el servidor

~~~
python manage.py runserver *:8000
~~~

## Built With

* [Django](https://www.djangoproject.com/) - Web framework
* [Python](https://www.python.org/) - Programming language


## Authors

* Victor Carceler

## License

This project is licensed under the GNU General Public License v3.0 - see the [COPYING](COPYING) file for details.