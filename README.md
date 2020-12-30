# Сирин / Sirin

Sirin permite ejecutar `playbooks` de `Ansible` cuando los ordenadores lo solicitan. Imponiendo una ventana definida por `EXCLUSION_TIME` durante la que no se volverá considerar el equipo aunque haga nuevas peticiones.

Está pensado para que cada ordenador haga una petición a Sirin (normalmente en el momento del arranque). Sirin identifica a los equipos por la `IP` desde la que realizan la petición. Si para este equipo no existía una petición previa en la BBDD entonces se guardará la petición.

Una petición consta de:

 * ID: Valor entero autoincremental.
 * LABEL: Etiqueta indicada en el momento de hacer la petición o 'default'. Sirve para agrupar las peticiones de un conjunto de equipos que comparten `playbook`.
 * ADDRESS: Dirección IP del ordenador que ha realizado la petición.
 * DATETIME: Fecha y hora en la que se ha recibido.
 * STATE: procesada o pendiente.

Si ya existía una petición para esta dirección `IP` en la BBDD entonces puede ocurrir:

a) Que todavía no haya trancurrido el plazo `EXCLUSION_TIME` desde que se registró la peticón en la BBDD hasta este momento. En tal caso se ignora la petición actual y no se modifica la BBDD.

b) Que desde la petición registrada en la BBDD hasta el momento actual se haya superado el plazo `EXCLUSION_TIME`. Entonces se actualiza la petición de la BBDD con el DATETIME actual y STATE pendiente.

Así únicamente se escribe en la BBDD cuando se recibe una petición para un ordenador que no tenía una IP registrada o cuando ha transcurrido `EXCLUSION_TIME` desde la petición registrada.

La peticiones pendientes de procesar corresponden a ordenadores que deben ser incluidos en la ejecución del `playbook` de `Ansible` mediante el parámetro `--limit` de `ansible-playbook`.

Cuando Sirin retorna la lista de direcciones de peticiones las marca como procesadas para no retornarlas de nuevo hasta que vuelvan a estar pendientes después de que hayan sido actualizadas tras recibir una nueva petición (transcurrido `EXCLUSION_TIME`).

# Puesta en marcha

Sirin es una aplicación Django así que se utilizará Python. El ORM de Django únicamente guarda las solicitudes de los equipos así que probablemente SQLite sea suficiente para manejar muchos equipos.

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

e) Finalmente conviene instalar los requisitos, procesar las migraciones y crear un usuario administrador

~~~
cd sirin
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
~~~

f) Ejecuta el servidor

~~~
python manage.py runserver 0:8000
~~~

# Uso de Sirin

Sirin está pensado para estar instalado en la misma máquina en la que se utiliza Ansible y posiblemente [ARA](https://github.com/ansible-community/ara).

Los equipos controlados deberán hacer una petición a Sirin en cada arranque y una tarea periodica (crontab o timer) consultará la lista de equipos con peticiones pendientes para utilizar con el parámetro `--limit` de `ansible-playbook`.

## Petición de un host a Sirin

Cualquier petición HTTP a `<ip>:<puerto>/launcher` hará que Sirin reciba la IP del equipo solicitante y si procede registre la petición en su base de datos.

La interfaz es intencionadamente simple. Sirin extrae la IP de la petición del equipo cliente, no debe haber NAT ni ningún proxy entre el cliente y Sirin.

Ejemplo: Un cliente puede registrarse en la instancia de Sirin que escucha en la IP 10.118.10.171 y en el puerto 8000 con:

~~~
wget http://10.118.10.171:8000/launcher
~~~

La repuesta de Sirin incluye la IP del cliente, en este caso:

~~~
Request from: 10.118.10.1
~~~

Si para la IP del cliente no había una solicitud previa, o la había pero procesada hace más de EXCLUSION_TIME entonces se registrará la petición del cliente en la BBDD.

Todas las peticiones que se reciban sin especificar etiqueta tendrán asignada la etiqueta `default`.

Si se quiere se puede especificar una etiqueta concreta en el momento de realizar la petición:

~~~
wget http://10.118.10.171:8000/launcher?label=<etiqueta>
~~~

Las etiquetas pueden servir para identificar a los equipos que comparten `playbook`.

## Consulta de las peticiones sin procesar

El comando `python manage.py listpendingrequests` permite mostrar las peticiones pendientes de procesar.

Una posible salida puede ser:

~~~
python manage.py listpendingrequests
ID       LABEL                            ADDRESS                          DATETIME                        
9        label2                           192.168.1.1                      2020-12-01 10:42:26             
10       label2                           192.168.1.2                      2020-12-02 00:00:00             
11       label1                           10.118.10.23                     2020-12-27 20:43:46             
23       label1                           192.168.1.144                    2020-12-30 09:31:23 
~~~

## Consulta del número de peticiones pendientes

Es posible comprobar el número de peticiones pendientes de ser procesadas para una etiqueta con el comando: `python manage.py getnumberofrequests <etiqueta>`

Por ejemplo, al comprobar el número de peticiones pendientes para la etiqueta `label1`:

~~~
python manage.py getnumberofrequests label1
2
~~~

Este comando puede servir para comprobar si hay equipos pendientes para lanzar el `playbook`.

## Obtención de los hosts por procesar

Cuando se quiera ejecutar `ansible-playbook` se podrá invocar el comando `python manage.py gethosts` para obtener la lista de las IPs pendientes de procesar.

La lista se retorna en el formato que espera el parámetro `--limit` de `ansible-playbook` que permite limitar el alcance del `playbook` a la lista de equipos especificados.

En este caso, para la etiqueta `label1` tenemos:

~~~
python manage.py gethosts label1
10.118.10.23,192.168.1.144,
~~~

Este comando marcará las solicitudes como procesadas y no volverán a aparecer en la lista de peticiones pendientes hasta que no sean incluídas de nuevo pasado el periodo de exclusión.

## Vista web de las peticiones pendientes

La URL `http://<IP>:<PORT>/launcher/listpendingrequests` resulta equivalente al comando `python manage.py listpendingrequests`.

En estos momentos y considerando que ya se han marcado como procesadas las peticiones con etiqueta `label1` el resultado en el navegador será:

~~~
ID 	LABEL 	ADDRESS 	DATETIME
9 	label2 	192.168.1.1 	1 de Diciembre de 2020 a las 10:42
10 	label2 	192.168.1.2 	2 de Diciembre de 2020 a las 00:00
~~~

## Built With

* [Django](https://www.djangoproject.com/) - Web framework
* [Python](https://www.python.org/) - Programming language


## Authors

* Victor Carceler

## License

This project is licensed under the GNU General Public License v3.0 - see the [COPYING](COPYING) file for details.