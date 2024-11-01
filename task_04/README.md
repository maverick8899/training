# Setup EFK stack with TLS communication
This project focuses on deploying an EFK stack, with the *__bitnami edition__* in *bitnami.efk* and an *elastic edition* in *elastic.efk* folder used for expansion.
## Setup
### Generate the new set of keys 
This command will create the folder named *secrets* containing a set of keys for the EFK stack and more.
```
cd setup ; docker compose -f docker-compose.yml run --rm certs
``` 
### Replace the set of keys 
After generating the set of keys, if you want to replace the set of keys, use this script to update the keys in the _bitnami.efk_ folder:
```
cd setup/bin ; bash replace_keys.sh
```
## Get started
### Bitnami Edition
#### Running
In this edition in *bitnami.efk* folder, configurations for both single-node and cluster modes are completed for Compose and Swarm modes in docker. The _template_ folder contains the Compose and Swarm stack templates. Use the following command to simply run this stack:
```
cd bitnami.efk/template/compose; docker compose -f <compose file> up  
```
If you have set up a swarm cluster, you can run this command.
```
cd bitnami.efk/template/swarm; docker compose -f <swarm file> up  
```
#### Configuration
By default, this stack uses version 8.15.3 of *bitnami edition*. Here are some key configuration details:
-   **Kibana**: Starting with version 8.x, Kibana no longer supports _username:password_  authentication with Elasticsearch. To address this, I configured it to automatically retrieve the _service account token_ from Elasticsearch and apply it to _kibana.yml_. You can review this configuration in _kibana/bin/entrypoint.sh_.
    
-   **Elasticsearch**: Configuration files are located in _elasticsearch/config_. In detail, _elasticsearch.yml_ is used for single-node mode, while _elasticsearch[123].yml_ files support cluster mode. You can expand your cluster by basing on the configuration of _elasticsearch[123].yml_ to write new elasticsearch[x].yml and build new images.
    
-   **Fluentd**: Configuration for Fluentd to collect logs itself is implemented in _/fluentd/bin/init.sh_.



### Elastic Edition
In this edition in the *elastic.efk, it currently just includes elasticseach with single-node and kibana configs. This setup functions effectively and can be tested with:
```
cd elastic.efk ; docker compose up
```


## Reference
+ Github repo referenced:
 https://github.com/swimlane/elk-tls-docker
+ Bitnami 
	+ Dockerfile
		https://github.com/bitnami/containers
	+ Docker Hub
		https://hub.docker.com/r/bitnami/ 
+ Elastic 
	+ Dockerfile
	https://github.com/elastic
	+ Docker Hub
	https://hub.docker.com/u/elastic
+ Document:
https://www.elastic.co/guide/en/elasticsearch/reference/8.15/configuring-tls.html
https://www.elastic.co/guide/en/kibana/8.15/configuring-tls.html
