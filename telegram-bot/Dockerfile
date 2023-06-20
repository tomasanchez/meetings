# Establecer la imagen base
FROM node:alpine

# Establecer el directorio de trabajo en el contenedor
WORKDIR /bot

# Copiar los archivos del proyecto al directorio de trabajo
COPY ./package.json ./

# Instalar las dependencias
RUN npm i

# Copiar el resto de los archivos del proyecto
COPY . .

# Compilar el código TypeScript
RUN npm run build

# Exponer el puerto que utilizará la aplicación de Telegraf (por defecto, el puerto 3000)
EXPOSE 3000

# Ejecutar la aplicación de Telegraf
CMD ["node", "dist/index.js"]