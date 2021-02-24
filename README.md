# Assignment-3-465820

#  CSE427S- Cloud Computing and Big Data Applications

**Lab 3**

For this lab, we will practive more with Docker and get familiar with Kubernet.
We will take our created docker image from Lab 2 and host it in a MiniKube cluster.


#  Step 1: Download MiniKube #
Follow this link [here](https://minikube.sigs.k8s.io/docs/start/) to download MiniKube.

After finish installation of MiniKube, we can start our cluster with this command: 
`minikube start --vm=true`

We want to enable VM mode for later use of Ingress.


# Step 2: Setup Configuration #

Our files for this lab will be stored in _charts_ directory.

Structure for this lab would need these requirements:
- Healthchecks
- Credentials to read from S3
- Replication
- A service to expose it

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/)


# Step 3: Create Secret File.

A _secret.yaml_ file will store and manage sensitive information.
For this lab, we will store our **AWS_SECRET_KEY** and **AWS_ACCESS_KEY** inside our _secret.yaml_

Keep in mind that these values are required to encoded in base64.
I use this command to encode my value:
`echo -n "<AWS_KEY>" | base64`

We can later use these information from these environment variables.

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/secret.png)

# Step 4: Create ConfigMaps File and Service File

A _configmap.yaml_ will store non-confidential data in key-value pairs, so that Pods can consume as environment variables.

For the purpose of this Lab, we will store two things inside our ConFigMaps.
Firstly, it is our S3 Bucket.
Secondly, it is the target port in our service.

A _service.yaml_ will store our port information.


![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/configmap.png)

# Step 5: Create Ingress File <EXTRA CREDIT>

Enable Ingress with this command:
`minikube addons enable ingress`

Then verify that the NGINX Ingress controller is running with this command:
`kubectl get pods -n kube-system`

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/ingress.png)

Now, we need to modify our ingress file _ingress.yaml_

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/ingressfile.png)

Under **host** of Ingress, we type the domain name we want for the app, _iris-world.info_ in our case. The **port** is the internal port which is **80** in our case. 
***Later we will completely this step.***


# Step 6: Create Deployment File

We can use the documentation of Kubernet as a format for our deployment file [here](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/deployment.png)
We want to have 3 replicas (3 running pods) for this deployment.
Next, under container we included the image of our application.

Pay attention that I have two different versions of python, hence I included : **command: ["/usr/bin/python3", "/code/app.py"]** right after my docker container and remove the similar command in my dockerfile of my image. 

In order for our pods to use environment variables from Configmaps and Secret, we use _envFrom:_ , this will let us use **ALL** environment variables from these files.

Next is liveness and readiness probe for our pods.

Liveness Probe is used to detect the states of our pods (broken or healthy). If the liveness probe fails, it will signal the kubelet kills the container and restarts it.

Readiness probe on the other hand tells if the container is ready to receive incoming network traffic or not. More information [here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)


![](https://github.com/CSE-427/assignment-2-anhhavo-465820/blob/master/images/lsdebug.png)

# Step 7: Modify Our Code

We need to adjust our code, since the application is now running in MiniKube cluster, we need to provide credentials to read/write from/to S3-Bucket. These information can now be collected from environment variables. We can directly call the environment variables by using `environ.get('<ENV_VAR>')`

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/code.png)

Remember to change the port to the environment variable.

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/codeport.png)
Now, build and push this new image with a new tag.
Next, go to our _deployment.yaml_ and include this image.

# Step 8: Start Our Service 

Now we have everything we need: deployment, service, secret, configmap. Let's finish the lab. 
Under the _charts_ directory, let's apply these yaml files:
`kubectl apply -f deployment.yaml`

`kubectl apply -f secret.yaml`

`kubectl apply -f configmap.yaml`


When first deployment, you can see that our readiness probes are working. The pods are running but not ready.

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/notready.png)


Then they become ready.

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/ready.png)

Here is the description of our pod:
In this description, you can see the Image we pulled from, Liveness/Readiness probe,
Environment Variables from. 

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/description.png)

Before starting our service, let's complete our Ingress file.
Type `kubectl get ingress`

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/getingress.png)

You can see the internal port of our service (one we included in _ingress.yaml_), and then we need to map our address to the host that we declared in our ingress file, _iris-world.info_ in our case. In this picture, I already completely the step, that is why the HOSTS show risi-world.info

Type _sudo vim /etc/hosts_ and do the mapping.
![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/host.png)


Finally, we can run our service.
You can do this by either port-forwarding 
![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/portforward.png)

Or type _minikube service <your_app_service>_
![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/minikubeservice.png)

Then go to ***iris-world.info*** to see our beautiful charts.

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/http.png)

If we want to manage our cluster, type `minikube dashboard`, and it will load up a dashboard of minikube cluster:

![](https://github.com/CSE-427/assignment-3-anhvo/blob/main/images/cluster.png)
