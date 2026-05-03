# Utiliser une image de base avec Java 21
FROM eclipse-temurin:21-jdk

# Installation de Python et pip
RUN apt install ca-certificates && apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    maven \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application
COPY . .

# Installation de Spring Boot CLI
RUN curl -O https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot-cli/3.2.2/spring-boot-cli-3.2.2-bin.tar.gz \
    && tar xzf spring-boot-cli-3.2.2-bin.tar.gz -C /opt \
    && ln -s /opt/spring-3.2.2/bin/spring /usr/local/bin/spring \
    && rm spring-boot-cli-3.2.2-bin.tar.gz

# Exposer le port de Flask (à ajuster selon votre configuration)
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["python3", "app.py"]