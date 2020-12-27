# Sirin

Sirin registra las peticiones de los equipos del centro cuando arrancan, y después permite obtener una lista de IPs para utilizar con el parámetro `--limit` de `ansible-playbook` ejecutando el `playbook` sobre los ordenadores que están encendidos.

La idea es que un ordenador notifica a Sirin que está encendido en cada arranque, pero Sirin únicamente registra la petición del ordenador si ha transcurrido el tiempo definido por el parámetro de configuración `EXCLUSION_TIME` desde la última solicitud registrada y no procesada por `Ansible`.

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

Cuando se ejecuta el comando `python manage.py gethosts` las solicitudes registradas en Sirin pasarán a considerarse procesadas. Y no se marcarán como no procesadas hasta que no se vuelva a recibir una petición de ese equipo pasado `EXCLUSION_TIME`.