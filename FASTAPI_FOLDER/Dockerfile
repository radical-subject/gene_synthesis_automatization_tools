
FROM continuumio/miniconda3
WORKDIR /FASTAPI_FOLDER

COPY env.yml .

RUN conda update -n base -c defaults conda

# install main bot dependencies
RUN conda env create -f env.yml

# # manually install node 15 for dev mode nodemon to work
# RUN apt-get update -y \
#   && apt-get install -y curl \
#   && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
#   && apt-get install -y nodejs \
#   && curl -L https://www.npmjs.com/install.sh | sh

# COPY package*.json ./
# RUN npm install

# copy all other files for bot
COPY . .

ENV PATH /opt/conda/envs/fastapi_env/bin:$PATH
RUN /bin/bash -c "source activate fastapi_env"

# Make RUN commands use the new environment: -- activate env doesnt work in miniconda!!!
# The SHELL instruction allows the default shell used for the shell form of commands to be overridden. The default shell on Linux is ["/bin/sh", "-c"], and on Windows is ["cmd", "/S", "/C"]. The SHELL instruction must be written in JSON form in a Dockerfile.
# RUN chown -R user /opt/conda/envs
# RUN chmod -R 777 /opt/conda/envs


# Make RUN commands use the new environment: -- activate env doesnt work in miniconda!!!
# The SHELL instruction allows the default shell used for the shell form of commands to be overridden. The default shell on Linux is ["/bin/sh", "-c"], and on Windows is ["cmd", "/S", "/C"]. The SHELL instruction must be written in JSON form in a Dockerfile.
# RUN chown -R user /opt/conda/envs
# RUN chmod -R 777 /opt/conda/envs
#RUN chown -R $USER:$USER /opt/conda/envs

SHELL ["conda", "run", "-n", "fastapi_env", "/bin/bash", "-c"] 
