version: '3.8'
services:
  gateway:
    image: nginx:latest
    container_name: gateway
    ports:
      - "80:80"
    volumes:
      - ./gateway/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - auth_service
      - srar
      - sfd
      - master_svc

  auth_service:
    build: ./services/auth_service
    container_name: auth_service
    # ...other config...

  srar:
    build: ./services/SRAR
    container_name: srar
    # ...other config...

  sfd:
    build: ./services/SFD
    container_name: sfd
    # ...other config...

  master_svc:
    build: ./services/MASTER_SVC
    container_name: master_svc
    # ...other config...
