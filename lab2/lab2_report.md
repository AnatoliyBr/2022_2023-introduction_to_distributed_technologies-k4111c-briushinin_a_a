
        University: [ITMO University](https://itmo.ru/ru/)
        Faculty: [FICT](https://fict.itmo.ru)
        Course: [Introduction to distributed technologies](https://github.com/itmo-ict-faculty/introduction-to-distributed-technologies)
        Year: 2022/2023
        Group: K4111c
        Author: Briushinin Anatolii Alekseevich
        Lab: Lab2
        Date of create: 21.10.2022
        Date of finished: -
        
apiVersion: v1  
kind: Pod  
metadata:  
name: itdt-contained-frontend
labels:
run: itdt-contained-frontend
spec:
containers:
-name: itdt-contained-frontend
image: docker.io/ifilyaninitmo/itdt-contained-frontend:master