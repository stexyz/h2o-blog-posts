# Making Use of Machine Learning

So you've built a machine learning model which delivers a high level of accuracy and does not overfit. 
What value does it have now? Well at the moment, nothing, zero, diddly squat. Over a series of blogs that I plan to write then the motto of all them will be: "There is no economic value in a model that is not used in production." 

So how can data scientist cover the "last mile" to the end zone named production? How do we quickly make the most of the model that has been built? For many organisations this is the toughest nut to crack and there are many valid paths that can be taken to deployment. I will be exploring many of these over my subsequent posts, drawing on experience and solutions that I have gleaned from working with many customers at my current employee, H2O.ai. However, first things first. What questions should we be asking to determine the path we should take? They are built on a foundation centred around xxx pillars. These are

1. Data source and format
2. Model and data lifecycle
3. How To Measure Success
4. Bringing the Model to Production
5. External Limitations Restrictions

**TODO**: mention 'lessions learned'
**TODO**: moto2: treat your machine learning models like other software components. (testing/monitoring/deployment)

## Data Source and Format

Will the same data with the same structure be available in production when predictions will be computed? 

For the model training, is the data source reachable from the machines where it will be ingested by the ML framework? One of the most common *show stoppers* in enterprise environment is the lack of network access to your data and among systems involved. It may take long weeks and substantial effort to gain such access so plan and test ahead of time.

Make sure that the storage system is compatible with the connectors available in the ML platform and the data format well supported. It may look trivial to change the representation and location of your data sets when experimenting with sample small data sets but all changes with volume. Lastly, make sure that the data set size fits - many claim to be *big data ready*, few really are. No matter the power of the machine learning solution be sure you know that you're not including data that is clearly irrelevant.

How to measure data set size? Both physical size (GBs) and the number of rows and colums pose computational challenge to the machine learning task. Be aware that both columns and rows may be sampled to decrease the required run time.

**TODO**: one size fits all? do you need a scaling solution that require more admin?
**TODO**: network accessibility of data and problems with locality (oversees transfers)
**TODO**: data sink - where do the predictions go?

## Model and Data Lifecycle

### Model Decay
How fast do your models decay? How severaly will the decreased accuracy impact your business case? How costly is it to retrain the model and redeploy the new one into production? What overhead does it have? Are you able to replace the old model with a new one without bringing down the whole operation and if not, what is the cost of such maintenance window?
How often are you able to collect data from your systems for retraining of the models? How large is the gap in the historical data between 'now' and the last data point that was collected? 
These imposed costs of having a fresh model in productions have to be evaluated with business stake holders.

### Versioning
Like with other assets, there is a good reason to keep old models archived and versioned. Authorities may require you to document the underlying logic of business at any moment in the past, internal audit may be required by executives or a flaw in a current model may enforce a rollback to the last known correct version of the model.
There is litte value in storing just the plain model, meta data describing the parameters and structure of the model need to be stored too. For experimenting with new ideas using methods like A/B testing versioning of the models with their KPIs is invaluable.

## How to Measure Success

No matter what you do you, by the end of the day you should be able to tell a success from a failure. Beauty may be found in all things, let us, however, look at more objective metrics.

### Model Testing and Other Metrics
There is just one model quality and it is how well it performs in production. Sadly, we have to design and select the right model before we see it shine or fail in deployment. Therefore we try to measure the performance in the testing phase as good as possible.

**TODO**: following is totally wrong: any of the following may be crutial - scorer metric, stability of the model (sensitivity), latency, throughput etc.. -> rephrase!!

Clearly, the prime metric is the accuracy measured by our scorer of choice. From experience we need to come up with a requirement of such score that will determine whether we've managed to build a model that is likely to be good enough to bring value when replacing the current model in production. If we have no model in production, we just try our best.
In some cases, however, a mix of KPIs need to be met. 
For online business or low latency trading we need good predictions being computed within a given time period otherwise they become obsolete.
Edge devices like swarms of actuators require the models to be small in size and scores 'cheap' to compute due to limited memory and possibly batery life.

### Staging of Models
When a new version of a software component is being developed, it is often the case that the release candidate gets promoted through the series of staging areas. Such progression usually includes need to pass through automated unit tests, integration tests, some form of manual testing, performance testing and eventually acceptance user testing. There is no reason not to treat machine learning models differently. Following the notion of economy of scale one may easily benefit from existing process by adding machine learning models as another component.

### Model Performance
We've got a model that performs well in our lab. We need to be able to ensure that it will remain performing well in production too, therefore we need to monitor the same metrics live. It is worth talking to the IT team to find out what is the monitoring tool of choice and try to collect the metrics in a standard way. It is heavily dependant on the flavour of integration of the scoring logic inside the production system. If the scoring is implemented using a REST server from H2O, one may utilise the JMX endpoint exposed by the REST server that H2O provides. We will look at this option in more detail later in this series.

If the KPIs do not fall within expected value range what do we do? We can keep a back-up older model in place to fall back to and/or have some simpler back up system ready (like your old pre-machine learning rule based model). It is always a good practice to use the standard dev-ops alerts that are very likely to be implemented for the application using the machine learning model.

On top of the metrics we also may want to generate metadata documenting what input has been seen, which values were unknown to the models (unseen categorical values, invalid input or even run time errors). We need to decide if this information needs to be processed real-time to trigger some imediate actions or offline batch recording is enough for later post-mortem analysis. This may results in substantial architetural desisions.

**TODO**: add model drift, think of other things that can go wrong

### Resource Utilisation
We've talked about application metrics but the principles of prudent management of the assets command us also to monitor the usage of resources. The consumption of resources is dynamic figure and for serious business case excessive hardware sizing should be avoided as well as growing consumption should trigger operations team to increase the resource pool prior to facing sudden drop in performance due to lack of resources.

### Model Fairness
### Model Interpretability

## Bringing the Model to Production

### Multi-tenant Environment
Many enterprises serve multiple tenants at once. It is important to distinguish between the cases where different tenants can benefit from using a common machine learning model trained on a joined data set and the case where such approach may lead to suboptimal results mainly in accuracy. Legal impact of such trade-off often conditions the possibility of such optimisation.

### Integration of Scoring Logic
It is impossible to forsee all the different flavours of scoring logic integration. Underestimating the proper planing of integration has lead to the situation where productisation of great machine learning models has taken significantly longer than the actual model development.
H2O has had this in mind for long time understanding that a trained model itself has to be as agile in ways it can be deployed as possible providing the user of its platform with large number of ways the deployment can be carried out.

As we will focus on each one of them in further posts, let's merely list them here. 

One vital characteristic common to all of the deployment flavours is the self-containdness of the scoring logic not needing any H2O server-like infrastructure.

#### Bash-like file->file
A stand-alone scoring invokable on an operating system process level. Easy to operate by UNIX(-like) system admin tools like Cron.

#### Micro Service
Several different implementations of a self-hosted (RESTful) service with JSON/binary content. Both on-premise and cloud.

#### AWS Lambda
Scalable one-click deployment (possibly API-automated) to AWS Lambda.

#### Code Embedded Scoring
Runtime libraries callable from JVM languages, Python, C++ and C# offering code-level integration with model being decoupled from runtime libraries.

#### Spark
Library allowing utilisation of H2O models as native Spark pipelines operating on Spark data structures. **TODO: validate wording with Kuba Hava.**

## External Limitations Restrictions
In simple words - what was possible in the R&D lab may be a very serious problem in the target environment.

### Priviledged Access
A very unpleasant discovery may be a need of priviledged access to run scoring logic or set up the dependencies of the scoring run time. This may be an unsolvable problem or may take very long to resolve.

### Hermetic Environment
Access to sensitive data may require a hermetically closed environment without access to the internet or other sources of dependencies. Lazily resolved dependencies or just model deployment process requiring an online dependency resolution may not be available and missed deadlines may occur during fixing this issue.

### IT limitations 
* access across different network partitions - data->training, data->scoring->sink, UI access to modelling environment

### Legal Limitation
NNs and other methods may not be available due to regulatory reasons. Make sure that even law department is part of the inception discussions to mitigate such risks.