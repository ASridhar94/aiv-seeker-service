FROM centos:latest

# Install Python
RUN yum -y update && \
    yum -y groupinstall "Development Tools" && \
    yum -y install wget curl gcc openssl-devel bzip2-devel postgresql libffi-devel sqlite-devel git && \
    yum -y install bc libnsl

WORKDIR /opt

RUN wget "https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz" && \
 tar xzf Python-3.8.5.tgz

WORKDIR Python-3.8.5
RUN ./configure --enable-optimizations --enable-loadable-sqlite-extensions && \
    make install

# Setup Conda
WORKDIR /
RUN curl -O https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
RUN bash Anaconda3-2020.07-Linux-x86_64.sh -b

# Install conda env for AIV seeker
RUN git  clone https://github.com/ASridhar94/AIV_seeker.git

RUN /root/anaconda3/bin/conda env create --name aiv_seeker --file /AIV_seeker/AIV_seeker_env.yml

# Copy our project
COPY . /aiv_seeker_service

WORKDIR /aiv_seeker_service

# Install the pip requirements
RUN pip3.8 install -r requirements.txt

# Expose the Django server port.
EXPOSE 8000