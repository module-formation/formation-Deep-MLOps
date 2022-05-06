Advanced Docker Security
Photo by Ian Taylor on Unsplash

In today’s world, developing apps entails much more than just writing code. The use of several languages, frameworks, and architectures, as well as discontinuous interfaces between tools for each stage of the development lifecycle, results in immense complexity. Docker streamlines and accelerates your process while allowing developers the opportunity to create by utilising their preferred tools, application stacks, and deployment environments for each project, according to their needs.

Introduction

Docker has made it easy for the operations team to directly deploy applications and websites without having to worry about dependencies, configuration settings, or the versions of packages installed on the server. Because of its simplicity in terms of just fetching the image from the registry and executing it with a command (docker run), we frequently fail to recognise that it requires the same level of security as any other entity.

We’ve already done a couple of articles on docker security best practices which can be found here and here.

In this blog post, we shall cover some more advanced concepts about Docker Security which will definitely prove to be helpful if you are working with multiple containers, want to prevent privilege escalation, etc.

Nologin Shell
nologin shell

Your Docker container can house multiple user accounts. Root account is the highest privilege that a user can gain in the container and once he has the root permission, he can actually execute root commands or can do a lot more in the container. To ensure that a malicious user doesn’t upgrade to the root account, even if he has access to the root account’s password you can change the shell to nologin. You could alternatively also make use of restricted shells for the user. To disable root login (inside the container), all you have to do is modify your Dockerfile and add the following line.

RUN chsh –s /usr/bin/nologin root

nologin shells are used to deny login access to an account. This line will ensure that even if a a malicious user gets hold of the root user’s account, he’ll not be able to login as it is denied in the nologin file hence no user, even the root can’t login to his account.

Disable Privilege Escalation using SUID

Before we talk about the mitigation technique, we should understand what SUID is. SUID, which stands for Set owner User ID up on execution is a special type of file permissions given to a file. If a root user gives this permission to an executable, it could be used to escalate privileges to root. All the root user has to do to set a SUID bit is type in

chmod +x <binary_name>

These are exploited in the wild to escalate privileges in docker containers. To prevent this you can use a special tag — security-opt=”no-new-privileges” while spinning up the docker container.

This tag ensures that processes and child processes (spawned by the parent process) do not gain any additional privileges using the SUID or SGID bit for that matter.

For example,

docker run –it <image_id> --security-opt=”no-new-privileges" /bin/bash

Note: Here image_id is the Id of the image of your docker container. To find the image id of your container just type in docker image ls
docker image ls

Create a Read-Only File System

Read only file system ensures that the users aren’t able to create any files in the system. This will prevent them from downloading and installing malicious files in the docker container which can further be used for other malicious purposes such as malware, keylogger or a back connect shell. So, it is essential that you protect docker from unauthorized access by creating a read only file system.

To create a read only file system we can use this command

docker run --read-only –it <image_id> /bin/bash

It is understandable that a container with no writing permissions could be of some inconvenience for the users. So, what you can do is set up a temporary file system. In this example, I’ve selected my /opt directory for the temporary file system. So, the user will be able to download the files only in the specified directory and they can’t be moved to home or any other directories. It can be achieved by running this command.

docker run --read-only --tmps /opt -it <image_id> /bin/bash

Preventing Inter Container Communication
Source

It’s normal for you to install multiple containers once you’ve set up Docker in a production environment because they are responsible for distinct activities. For example, you might be utilizing MongoDB in one container while hosting an application in another. However, did you know that it is possible to communicate across containers? The following scenario: A docker container running a vulnerable instance of an application that was exposed via a port is exposed to the outside world. A malevolent user seated on the other docker container has the potential to jeopardize the entire application’s security.

Therefore, unless required, you can prevent inter-container communication.

You can start off by looking at the default networks that come built in with docker.

docker network ls

list of networks

Here, we’ll be inspecting a network type. For this example, we’ll look at the bridge network type.

docker network inspect bridge

Inspecting Bridge

If you scroll down, you’ll see that it has com.docker.network.bridge.enable-icc set to true.

Because multiple devices and containers can be joined to a bridge connection in order for them to communicate, bridge connections are used to interconnect the containers and make them more accessible.

Creating a new network and setting it to false is all that we need to do in order to block inter-container communication. Then, when we’re establishing a new container, we can include it in the newly established network that we’ve set up. As a result, the container will be separated and will only be capable of holding one container.

Let’s begin by creating a new network

docker network create  --driver bridge –o “com.docker.network.bridge.enable-icc”:”false” testnet1

Creating a new network

Here we’ve created a network of the type bridge and set the inter-container communication as false. The name of the network that we have created is set as testnet1

With all this done, what we can do is run a docker container with the network set as testnet1.
Listing the networks

docker run –it –network testnet1 <image_id> /bin/bash

Note: Here image_id is the Id of the image of your docker container. To find the image id of your container just type in docker image ls
Listing Docker Images

Conclusion

In this blog article, we discussed some of the most critical features of Docker’s safety. Despite the fact that a user has access to the root password, we learned how to block root logins. In the next lessons, we learned how to avoid privilege escalation through the usage of SUID or SGID files. We learned about constructing read-only file systems at the end of the course, as well as how to block inter-container communication by creating a different network. These steps are vital to secure your docker installation. As we learn more about docker security, we’ll be adding more articles to this series.

Advanced Docker Security Part II
Source
Introduction

This is part II of the Advanced Docker Series where we’ll be covering some advanced concepts to secure your docker container and ensure that even if your container is compromised, the attacker will not be able to achieve much. In case you’ve missed the first part of the series you can check it out here.
Limiting Resources

The security of Docker and the factors that influence it may be broken down into two core and crucial categories: Namespaces and cgroups are the terms used to describe them.

Namespaces, according to the Docker website, “provide isolation for running processes (containers), limiting their access to system resources without the running process being aware of the constraints.” Namespaces were not introduced by Docker. It was already present as part of the Linux kernel at the time of writing.

The second most crucial thing to know is about cgroups. It is a Linux Kernel feature that lets you restrict access to processes and containers to specific system resources such as CPU, RAM, IOPS, and the network connection.
Restricting PIDs

PIDs are the number of processes or threads the container has created. The PIDS column contains the total number of processes and kernel threads that were created by the container in the previous step. The Linux kernel refers to this as “threads.” Alternatively, “lightweight process” or “kernel job” are used to describe the same thing. The presence of a large number in the PIDS column combined with a modest number of processes (as reported by ps or top) may indicate that something within the container is generating a significant number of threads. If an attacker gets access to your container, he can cripple it by eating up all the resources of the server and bringing it to a halt. It is therefore recommended to reduce the number of processes that can be spawned on the system.

Let’s first start by learning how to check the maximum number of PIDs that a container can spawn.

To check the current PIDs, you can find that by typing in docker stats
docker stats

Let’s run a docker container in detached mode.

In detached mode, the container starts up and runs in the background. That means, you start up the container and could use the console after startup for other commands.

The opposite of detached mode is foreground mode. That is the default mode, when the -d option is not used. In this mode, the console you are using to execute docker run will be attached to standard input, output and error. That means your console is attached to the container’s process.

You can run docker in detached mode by adding an additional flag d along with –it.
docker run -itd <image_id>

As we can see, it provides us with an ID, fa7175306b6ae53d2be39d1e53d47e12d98fbb2cfac9f8d3abf82752f60cca0e

This is nothing but a directory for our just spawned container. The contents of this directory would contain important information.

find /sys/fs/cgroup -name fa7175306b6ae53d2be39d1e53d47e12d98fbb2cfac9f8d3abf82752f60cca0e

List of directories matched

If you look at the name convention of the first directory, you’ll notice pids in it. This directory would contain information regarding the PIDs of our just spawned container. Our directory of concern is /sys/fs/cgroup/pids/docker/fa7….ca0e

Looking at the contents, you’ll see a bunch of files stored in the directory.
switching to the pids directory of our container

The pids.max file contains the maximum number of processes that can be spawned in our docker container. If you look at the contents of the pids.max file, you’ll find that it contains the word max. This means any number of processes can be spawned in our container.
pids.max is set to max

Depending upon the use case, you can set an upper bound on the number of PIDs that can be spawned.

docker run –pids-limit 100 825d55fb6340

Note: Here 825d55fb6340 is the image ID. To view your image IDs, just type in docker image ls
pids-limit set to 100

In the example above, I’ve set a maximum limit on the number of processes that can be spawned, which is effectively 100. Deepening upon your use case, you can set it to a lot lower or higher.

Let’s confirm it by visiting the /sys/fs/cgroup/pids/docker/08a1b005840b54bda92116ad810ea228ae32d558a6fc81491b5f6ba042244f7e/pids.max file.
pids-limit set to 100

As you can verify, the maximum number of pids has been set to 100.
Docker Socket
Source

Let’s understand what socket is first

A socket is typically referred to in terms of an IP Address and a port. To interact with a website, or an interface, all you’ll need is a socket which means an IP Address and a port associated with the IP Address on which the service is running.

You can then send request(s) to the socket and expect a response. This is commonly referred to as a TCP Socket. There is another socket called the UNIX socket. These sockets are commonly used for Inter Process Communication (IPC) within the same computer/system.

The Docker Socket is a UNIX socket. When you type in a docker command like docker pull, run, etc., behind the scenes the docker client is interacting with the docker daemon via the UNIX socket to execute your commands.

The docker.sock file is located in the /var/run directory and the owner of the file is the root. It is essential that you don’t tamper with the permissions of this file because this can lead the attacker to gain access to the underlying host system.

Also, it is not advisable to mount this file onto a newly spun docker container, as it can be abused by malicious users to gain access to the underlying host system. But why would the /var/run/docker.sock file be mounted by anyone on the container?

If you have a couple of docker containers and you want to access/control all of them from a different docker container, then you’ll need to mount this file to the docker container from which you wish to control/access the rest of the docker containers.

The process to mount is by adding the –v tag, followed by what you wish to mount and where you wish to mount.

Example, -v /opt/important:/tmp

In this example, I’ve mounted the /opt/important directory from the host system to the /tmp directory in the docker container.

Therefore, if you encounter a DockerFile with a line similar to the one provided below, you can be sure of the fact that any malicious user, with access to the docker container will be able to mount the host file system and read all the sensitive files.

docker run –it –name ubuntu –v /var/run/docker.sock:/var/run/docker.sock /bin/bash

Conclusion

This was a blog post that was more focused on the practical side of things. We gained an understanding of the concept of Process IDs and how we might restrict access to them. Later on, we discovered that mounting a docker.sock file can lead to security vulnerabilities in the Docker container. Security is extremely important in the Docker environment. In addition to being complicated, technological security is also difficult to achieve. As a result, we must make certain that everything is properly corrected and protected prior to the deployment.