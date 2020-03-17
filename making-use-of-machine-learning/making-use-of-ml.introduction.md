# Maximing the impact of Machine Learning

So you have built a machine learning (ML) model which delivers a high level of accuracy and does not overfit. What value does it have now? Well, at the moment, nothing, zero, diddly squat. There is no economic value in a machine learning model that never sees the light of day and is not used in production making business decisions.

So how can data scientists cover the "last mile" to that elusive end zone that is named production? How do we quickly make the most of the model that has been built? For many organisations this is the toughest nut to crack and there are many valid paths that can be taken to deployment. What questions should we be asking to determine the path we should take? They are built on a foundation centred around 4 pillars. These are:

1. Data Sources and their format
2. How To Measure Success
3. Bringing the Model to Production
4. External Limitations and Restrictions

## Data Sources and their format

Some of the key questions and pointers that need to be asked are:

- Will the same data with the same structure be available in production when the predictions are calculated? 

- Is the data source and prediction destination reachable from the machines where it will be ingested by the ML framework? One of the most common *show stoppers* in an enterprise environment is the lack of network access, low bandwidth and a long roundtrip (don't repeatedly transfer big data sets over the ocean) of your data and among systems involved. Solving these problems may take long weeks and substantial effort so plan and test and involve IT ahead of time.

- Is the storage system compatible with the connectors available in the ML platform and the data format is well supported. It may look trivial to change the representation and location of your data sets when experimenting with sample small data but all changes when you start increasing the volume of your data. 

 - Will the *ML framework fits the data set size*. Avoid the lure of using heavy-duty frameworks for simple problems but also beware that many claim to be *big data ready*, few really are.  No matter the power of the machine learning solution, you need to make sure that you're not including a possibly large burden of data that is not necessary as part of the scoring process.  Measuring data set size is important. Both the physical size (GBs) and the number of rows and columns pose computational challenge to the machine learning task. Columns and rows downsampling may be required to decrease the required run time, proper exploratory data analysis and preliminary modelling may let you reduce the data set too.

## How to Measure Success

No matter what you do you, at the end of the day you should be able to tell a success from a failure. Beauty may be found in all things, however let us consider some more objective metrics.

### Translate to Business
Are you able to express the expectations of the non-technical consumer of your ML models to be built in a formalised way using standard ML metrics?

### Model Testing and Other Metrics
Based on the discussion with business, nature of the data set and other inputs we design our validation strategy choosing right scorers and data set splits, investigate the stability, sensitivity, fairness and interpretability of the model, and other metrics. Since we are no parlour data scientists, most likely a number of other KPIs need to be met too.

For online business or low latency trading we need good predictions being computed within a given time period otherwise they become obsolete.
Edge devices like swarms of actuators require the models to be small in size and scores 'cheap' to compute due to limited memory and possibly battery life.

### Model Decay
How fast do your models decay? How severely will the decreased accuracy impact your business case? How costly is it to retrain the model and redeploy the new one into production? What overhead does it have? Are you able to replace the old model with a new one without bringing down the whole operation and if not, what is the cost of such maintenance window?
How often are you able to collect data from your systems for retraining of the models? How large is the gap in the historical data between 'now' and the last data point that was collected? 
These imposed costs of having a fresh model in productions have to be evaluated with business stake holders.

### Staging of Models
Sadly, we have to design and select the right model before we see it shine or fail in deployment. Therefore we try to measure the quality of the model in the testing phase as good as possible. To this end we need to establish and further maintain base line criteria that will determine whether we've managed to build a model that is likely to be good enough to bring value when replacing the current model in production. If we have no model in production, we just need to rely on lab results.

When a new version of a software component is being developed, it is often the case that the release candidate gets promoted through the series of staging areas. Such progression usually includes need to pass through automated unit tests, integration tests, some form of manual testing, performance testing and eventually acceptance user testing. There is no reason not to treat machine learning models differently. Following the notion of economy of scale one may easily benefit from existing process by adding machine learning models as another component of the software engineering process in place. 

To further mitigate the risk of a new model roll-out have you considered A/B testing it?

### Model Monitoring
To ensure that our model keeps performing reasonably well in production we need to monitor the same qualities as we have in lab. 

It is worth talking to the IT team to find out what is the monitoring tool of choice and try to collect the metrics in a standard way. It is heavily dependant on the flavour of integration of the scoring logic inside the production system. For the scoring logic implemented using a REST server from H2O we can utilise the JMX endpoint exposed by the REST server that H2O provides. For the code-level integration we can utilise corresponding modules in our code base that are already used for such matter. In simple words, do not try to reinvent the wheel, in best case you won't make any dev-ops person happy by adding an extra dashboard to look at.

Does the data change substantially compared to our training data set? Do other KPIs fall outside an expected value range what do we do? We can keep a back-up older model in place to fall back to and/or have some simpler back up system ready (like your old pre-machine learning rule based model). It is always a good practice to use the standard dev-ops alerts that are very likely to be implemented for the application using the machine learning model.

On top of the metrics we also may want to generate metadata documenting what input has been seen, which values were unknown to the models (unseen categorical values, invalid input or even run time errors). We need to decide if this information needs to be processed real-time to trigger some immediate actions or offline batch recording is enough for later post-mortem analysis. Do you have some proven logging sink or journals in place? Use these over adding new destinations of your records.

**TODO**: think of other things that can go wrong

### Resource Utilisation
We've talked about application metrics but the principles of prudent management of the assets command us also to monitor the usage of resources. The consumption of resources is a dynamic figure and for serious business case excessive hardware sizing should be avoided as well as growing consumption should trigger operations team to increase the resource pool prior to facing sudden drop in performance due to lack of resources.

## Bringing the Model to Production

### Multi-tennant Environment
Many enterprises serve multiple tenants at once. It is important to distinguish between the cases where different tenants can benefit from using a common machine learning model trained on a joined data set and the case where such approach may lead to suboptimal results mainly in accuracy. Legal impact of such trade-off often conditions the possibility of such optimisation.

### High Availability
As with any other software components a certain number of "9s" of availability may be (possibly contractually) required from you scoring login deployment. Have you considered notions of advanced load balancing with auto-scaling, "exactly once" execution, warm start of deployed models?

### Versioning
Like with other assets, there is a good reason to keep old models archived and versioned. Authorities may require you to document the underlying logic of business at any moment in the past, internal audit may be required by executives or a flaw in a current model may enforce a rollback to the last known correct version of the model.
There is little value in storing just the plain model, meta data describing the parameters and structure of the model together with production metrics discussed earlier need to be stored too. For experimenting with new ideas using methods like A/B testing versioning of the models with their KPIs is invaluable.

### Integration of Scoring Logic
It is impossible to foresee all the different flavours of scoring logic integration. Underestimating the proper planing of integration has led to the situation where productisation of great machine learning models has taken significantly longer than the actual model development.

H2O has had this in mind for a long time understanding that a trained model itself has to be as agile in ways it can be deployed as possible providing the user of its platform with large number of ways the deployment can be carried out. One vital characteristic common to all of the deployment flavours is the self-containdness of the scoring logic not needing any H2O server-like infrastructure.

As we will focus on each one of them in further posts, let's merely list them here in no particular order:

* **Bash-like file->file** stand-alone scoring invokable on an operating system process level operable by UNIX(-like) system admin tools like Cron
* **Micro Service** spanning across several different implementations of a self-hosted (RESTful) service with JSON/binary content both on-premise and cloud
* **AWS Lambda** scalable one-click deployment (possibly API-automated) to AWS Lambda
* **Code Embedded Scoring** using runtime libraries callable from JVM languages, Python, C++ and C# offering code-level integration with model being decoupled from runtime libraries
* **Spark Pipelines** deployment utilising H2O models as native Spark pipelines operating on Spark data structures

## External Limitations and Restrictions
In simple words - what was possible in the R&D lab may be a very serious problem in the target environment.

### Privileged Access
A very unpleasant discovery may be a need of privileged access to run scoring logic or set up the dependencies of the scoring run time. This may be an unsolvable problem or may take very long to resolve.

### Hermetic Environment
Access to sensitive data may require a hermetically closed environment without access to the internet or other sources of dependencies. Lazily resolved dependencies or just model deployment process requiring an online dependency resolution may not be available and missed deadlines may occur during fixing this issue.

### Legal Limitation
NNs and other methods may not be available due to regulatory reasons. Make sure that even law department is part of the inception discussions to mitigate such risks.
