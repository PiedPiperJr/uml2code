import { Injectable } from '@angular/core';

export interface Category {
  name: string;
  values: {
    id?: string;
    name: string;
    description: string;
  }[];
}

@Injectable({
  providedIn: 'root'
})
export class SpringCategoriesService {
  private categories : Category[] = [{
    name: "Developer Tools",
    values: [
      {
        id: "native",
        name: "GraalVM Native Support",
        description: "Support for compiling Spring applications to native executables using the GraalVM native-image compiler."
      },
      {
        id: "dgs-codegen",
        name: "GraphQL DGS Code Generation",
        description: "Generate data types and type-safe APIs for querying GraphQL APIS by parsing schema files."
      },
      {
        id: "devtools",
        name: "Spring Boot DevTools",
        description: "Provides fast application restarts, LiveReload, and configurations for enhanced development experience."
      },
      {id: "lombok", name: "Lombok", description: "Java annotation library which helps to reduce boiler^late code."},
      {
        id: "configuration-processor",
        name: "Spring Configuration Processor",
        description: "Generate metadata for developers to offer contextual help and \"code completion\" when working with custom configuration keys (ex.application.properties/.yml files)."
      },
      {
        id: "docker-compose",
        name: "Docker Compose Support",
        description: "Provides docker compose support for enhanced development experience."
      },
      {id: "modulith", name: "Spring Modulith", description: "Support for building modular monolithic applications."}
    ]
  },

    {
      name: "Web",
      values: [
        {
          id: "web",
          name: "Spring Web",
          description: "Build web, including RESTful, applications using Spring MVC. Uses A"
        },
        {
          id: "web",
          name: "Spring Reactive Web",
          description: "Build reactive web applications with Spring WebFlux and Netty."
        },
        {
          id: "graphql",
          name: "Spring for GraphQL",
          description: "Build GraphQL applications with Spring for GraphQL and GraphQL Java."
        },
        {
          id: "data-rest",
          name: "Rest Repositories",
          description: "Exposing Spring Data repositories over REST via Spring Data REST."
        },
        {
          id: "session",
          name: "Spring Session",
          description: "Provides an API and implementations for managing user session information."
        },
        {
          id: "data-rest-explorer",
          name: "Rest Repositories HAL Explorer",
          description: "Browsing Spring Data REST repositories in your browser."
        },
        {
          id: "hateoas",
          name: "Spring HATEOAS",
          description: "Eases the creation of RESTful APIs that follow the HATEOAS principle when working."
        },
        {
          id: "web-services",
          name: "Spring Web Service",
          description: "Facilitates contract-first SOAP development. Allows for the creation of flexible web services using one of the many ways to manipulate XML payloads."
        },
        {
          id: "jersey",
          name: "Jersey",
          description: "Framework for developing RESTful Web Services in Java that provides support for JAX-RS APIs."
        },
        {
          id: "vaadin",
          name: "Vaadin",
          description: "The full-stack web app platform for Spring. Build views fully in Java with Flow, or in React using Hilla."
        },
        {
          id: "netflix-dgs",
          name: "Netflix DGS",
          description: "Build GraphQL application with Netflix DGS and Spring for GraphQL."
        },
        {
          id: "htmx",
          name: "htmx",
          description: "Build modern user interfaces with the simplicity and power of hypertext."
        }
      ]
    },

    {
      name: "Template Engine",
      values: [
        {
          id: "thymeleaf",
          name: "Thymeleaf",
          description: "A moder server-side Java template engine for both web and standalone environments. Allows HTML to be correctly displayed in browsers and as static prototypes."
        },
        {
          id: "freemarker",
          name: "Apache Freemarker",
          description: "Java library to generate text output (HTML web pages, e-mails, configuration files, source code, etc.) based on templates and changing data."
        },
        {
          id: "mustache",
          name: "Mustache",
          description: "Logic-less templates for both web and standalone environments. There are no if statements, else clauses, or for loops. Instead there are only tags."
        },
        {id: "groovy-templates", name: "Groovy Templates", description: "Groovy templating engine."},
        {name: "JTE", description: "Secure and lightweight template engine for Java and Kotlin."},
      ]
    },

    {
      name: "Security",
      values: [
        {
          id: "oauth2-client",
          name: "OAuth2 Client",
          description: "Spring Boot integration for Spring Security's Oauth2/OpenID Connect client features."
        },
        {
          id: "oauth2-authorization-server",
          name: "OAuth2 Authorization Server",
          description: "Spring Boot integration for Spring Authorization Sever."
        },
        {
          id: "oauth2-resource-server",
          name: "OAuth2 Resource Server",
          description: "Spring Boot integration for Spring Security's OAuth2 resource server features."
        },
        {
          id: "data-ldap",
          name: "Spring LDAP",
          description: "Makes it easier to build Spring based applications that use the Lightweight Directory Access Protocol."
        },
      ]
    },

    {
      name: "SQL",
      values: [
        {
          id: "jdbc",
          name: "JDBC API",
          description: "Database Connectivity API that defines how a client my connect and query a database."
        },
        {
          id: "data-jpa",
          name: "Spring Data JPA",
          description: "Persist data in SQL stores with Java Persistence API using Spring Data and Hibernate."
        },
        {
          id: "data-jdbc",
          name: "Spring Data JDBC",
          description: "Persist data in SQL stores with plain JDBC using Spring Data."
        },
        {
          id: "data-r2dbc",
          name: "Spring Data R2DBC",
          description: "Provides Reactive Relational Database Connectivity to persist data in SQL stores using Spring Data in reactive applications."
        },
        {
          id: "liquibase",
          name: "Liquibase Migration",
          description: "Liquibase database migration and source control library."
        },
        {
          id: "flyway",
          name: "Flyway Migration",
          description: "Version control for your database so you can migrate from any version (incl. an empty database) to the laster version of the schema."
        },
        {
          id: "jooq",
          name: "JOOQ Access Layer",
          description: "Generate Java code from your database and build type sage SQL queries through a fluent API."
        },
        {id: "db2", name: "IBM DB2 Driver", description: "A JDBC driver that provides access to IBM DB2"},
        {
          name: "Apache Derby Database",
          description: "An open source relational database implemented entirely in Java."
        },
        {
          id: "h2",
          name: "H2 Database",
          description: "Provides a fast in-memory database that supports JDBC API and R2DBC access, with a small (2mb) footprint. Support embedded and server modes as well as a browser based console application."
        },
        {id: "hsql", name: "HyperSQL Database", description: "Lightweight 100% Java SQL Database Engine."},
        {name: "MariaDB Driver", description: "MariaDB JDBC and R2DBC driver."},
        {
          id: "sqlserver",
          name: "MS SQL Server Driver",
          description: "A JDBC and R2DBC driver that provides access to Microsoft SQL server and Azure SQL Database from any Java application."
        },
        {id: "mysql", name: "MySQL Drive", description: "MySQL JDBC driver."},
        {id: "oracle", name: "Oracle Driver", description: "A JDBC driver that provides access to Oracle."},
        {
          id: "postgresql",
          name: "PostgreSQL Driver",
          description: "A JDBC and R2DBC driver that allows Java programs to connect to a PostgreSQL database using standard, database independent Java code."
        }
      ]
    },

    {
      name: "NoSQL",
      values: [
        {
          id: "data-redis",
          name: "Spring Data Redis (Access+Driver)",
          description: "Advanced and thread-sage Java Redis client for synchronous, asynchronous, and reactive usage. Supports Cluster, Sentinel, Pipelining, Auto-Reconnect, Codecs and much more."
        },
        {
          id: "data-redis-reactive",
          name: "Spring Data Reactive Redis",
          description: "Access Redis key-value data stores in a reactive fashion with Spring Data Redis."
        },
        {
          id: "data-mongodb",
          name: "Spring Data MongoDB",
          description: "Store data in flexible, JSON-like documents, meaning fields can vary from document to document and data structure can be changed over time."
        },
        {
          id: "data-mongodb-reactive",
          name: "Spring Data Reactive MongoDB",
          description: "Provides asynchronous stream processing with non-blocking back pressure for MongoDB."
        },
        {
          id: "data-elasticsearch",
          name: "Spring Data Elasticsearch (Access+Driver)",
          description: "A distributed, RESTful search and analytics engin with Spring Data Elasticsearch."
        },
        {
          id: "data-cassandra",
          name: "Spring Data for Apache Cassandra",
          description: "A free and open-source, distributed, NoSQL database management system that offers high-scalability and high-performance."
        },
        {
          id: "data-cassandra-reactive",
          name: "Spring Data Reactive for Apache Cassandra",
          description: "Access Cassandra NoSQL Database in a reactive fashion."
        },
        {
          id: "data-couchbase",
          name: "Spring Data Couchbase",
          description: "NoSQL document-oriented database that offers in memory-first architecture, geo-distributed deployments, and workload isolation."
        },
        {
          id: "data-couchbase-reactive",
          name: "Spring Data Reactive Couchbase",
          description: "Access Couchbase NoSQL database in a reactive fashion with Spring Data Couchbase."
        },
        {
          id: "data-neo4j",
          name: "Spring Data Neo4j",
          description: "An open source NoSQL database that stores data structures as graphs consisting of nodes, connected by relationships."
        }
      ]
    },

    {
      name: "Messaging",
      values: [
        {
          id: "integration",
          name: "Spring Integration",
          description: "Adds support for Enterprise Integration Patterns. Enables lightweight messaging and supports integration with external systems via declarative adapters."
        },
        {
          id: "amqp",
          name: "Spring for RabbitMQ",
          description: "Gives your applications a common platform to send and receive messages, and your messages a safe place to live until received."
        },
        {
          id: "amqp-streams",
          name: "Spring for RabbitMQ Streams",
          description: "Building stream processing applications with RabbitMQ."
        },
        {
          id: "kafka",
          name: "Spring for Apache Kafka",
          description: "Publish, subscribe, store, and process streams of records."
        },
        {
          id: "kafka-streams",
          name: "Spring for Apache Kafka Streams",
          description: "Building streams processing application with Apache Kafka Streams."
        },
        {
          id: "activemq",
          name: "Spring for Apache ActiveMQ 5",
          description: "Spring JMS support with Apache ActiveMQ 'Classic'."
        },
        {
          id: "artemis",
          name: "Spring for Apache ActiveMQ Artemis",
          description: "Spring JMS support with Apache ActiveMQ Artemis."
        },
        {
          id: "pulsar",
          name: "Spring for Apache Pulsar",
          description: "Build messaging applications with Apache Pulsar."
        },
        {
          id: "pulsar-reactive",
          name: "Spring for Apache Pulsar (Reactive)",
          description: "Build reactive messaging application with Apache Pulsar."
        },
        {
          id: "websocket",
          name: "WebSocket",
          description: "Build Servlet-based WebSocket applications with SockJS and STOMP."
        },
        {id: "rsocket", name: "RSocket", description: "RSocket.is applications with Spring Messaging and Netty."},
        {
          id: "camel",
          name: "Apache Camel",
          description: "Apache Camel is an open source integration framework that empowers you to quickly and easily integrate various systems consuming or producing data."
        },
      ]
    },

    {
      name: "IO",
      values: [
        {
          id: "batch",
          name: "Spring Batch",
          description: "Batch applications with transactions, retry/skip and chunk base processing."
        },
        {id: "validation", name: "Validation", description: "Bean Validation with Hibernate validator."},
        {
          id: "mail",
          name: "Java Mail Sender",
          description: "Send email using Java Mail and Spring Framework's JavaMailSender."
        },
        {id: "quartz", name: "Quarts Scheduler", description: "Schedule jobs using Quartz"},
        {
          id: "cache",
          name: "Spring Cache Abstraction",
          description: "Provides cache-relate operations, such ash the ability to update the content of the cache, but does not provide the actual data store."
        },
        {id: "spring-shell", name: "Spring Shell", description: "Build command line applications with spring."}
      ]
    },

    {
      name: "OPS",
      values: [
        {
          name: "Spring Boot Actuator",
          description: "Support built in (or custom) endpoints that let you monitor and manage your application-such as application health metrics, session, etc."
        },
        {name: "CycloneDX SBOM support", description: "Creates a Sofware Bill of Material in CycloneDX format."},
        {
          id: "codecentric-spring-boot-admin-client",
          name: "codecentric's Spring Boot Admin (Client)",
          description: 'Required for your application to register with a Codecentrics Spring Boot Admin server instance.'
        },
        {
          id: "codecentric-spring-boot-admin-server",
          name: "codecentric's Spring Boot Admin (Server)",
          description: 'A community project to manage and monitor your Spring Boot applications. Provides a UI on top of the Spring Boot Actuator endpoints.'
        },
      ]
    },

    {
      name: "Observability",
      values: [
        {
          id: "datadog",
          name: "Datadog",
          description: "Publish Micrometer metrics to Datadog, a dimensional time-series SasS with built-in dashboarding and alerting."
        },
        {
          id: "dynatrace",
          name: "Dynatrace",
          description: "Publish metrics to Dynatrace, a platform featuring observability, AIOPs, application security and analytics."
        },
        {
          id: "influx",
          name: "Influx",
          description: "Publish Micrometer metrics to InfluxDB, a dimensional time-series server that support real-time stream processing of data."
        },
        {
          id: "graphite",
          name: "Graphite",
          description: "Publish Micrometer metrics Graphite, a hierarchical metrics system backed by a fixed-size database."
        },
        {
          id: "new-relic",
          name: "New Relic",
          description: "Publish Micrometer to New Relic, a SaaS offering with a full UI and a query language called NRQL."
        },
        {
          id: "otlp-metrics",
          name: "OTLP for metrics",
          description: "Publish Micrometer metrics to an OpenTelemetry Protocol (OTLP) capable backend."
        },
        {
          id: "prometheus",
          name: "Prometheus",
          description: "Expose Micrometer metrics in Prometheus format, an in-memory dimensional time series database with a simple built-in UI, a custom query language, and math operations."
        },
        {id: "distributed-tracing", name: "Distributed Tracing", description: "Enable span and trace IDs in logs."},
        {
          id: "wavefront",
          name: "Wavefront",
          description: "Publish metrics and optionally distributed traces to Tanzu Observability by Wavefront, a SassS-based metrics monitoring and analytics platform that lets you visualize, query, and alert over data from across your entire stack."
        },
        {name: "Zipkin", description: "Enable and expose span an trace IDs to Zipkin."}
      ]
    },

    {
      name: "Testing",
      values: [
        {
          id: "restdocs",
          name: "Spring REST Docs",
          description: "Document RESTful services by combining hand-written with Asciidoctor and auto-generated snippets produced with Spring MVC Test."
        },
        {
          id: "testcontainers",
          name: "Testconstainers",
          description: "Provide lightweight, throwaway instances of common databases, Selenium web browsers, or anything els that can run in Docker container."
        },
        {
          id: "cloud-contract-verifier",
          name: "Contract Verifier",
          description: "Moves TDD to the level of software architecture enabling Consumer Driven Contract (CDC) development."
        },
        {
          id: "cloud-contract-stub-runner",
          name: "Contract Stub Runner",
          description: "Stub Runner for HTTP/Messaging based communication. Allows creating WireMock stubs from RestDocs test."
        },
        {
          id: "unboundid-ldap",
          name: "Embedded LDAP Server",
          description: "Provides a platform neutral way for running a LDAP server in unit tests."
        }
      ]
    },

    {
      name: "Spring Cloud",
      values: [
        {
          id: "cloud-starter",
          name: "Cloud Bootstrap",
          description: "Non-specific Spring Cloud features, unrelated to external libraries or integrations (e.g. Boostrap context and @RefreshScope)."
        },
        {
          id: "cloud-function",
          name: "Function",
          description: "Promotes the implementation of business logic via functions and supports a uniform programming model across serverless providers, as well as the ability to run standalone (locally or in a PassS)."
        },
        {
          id: "cloud-task",
          name: "Task",
          description: "Allows a user to develop and run short lived microservices using Spring Cloud. Run them locally, in the cloud, and on Spring Cloud Data Flow."
        },
      ]
    },

    {
      name: "Spring Cloud Config",
      values: [
        {
          id: "cloud-config-client",
          name: "Config Client",
          description: "Client that connects to a Spring Cloud Config Server to fetch the application's configuration."
        },
        {
          id: "cloud-config-server",
          name: "Config Server",
          description: "Central management for confiugration via Git, SVN, or HashiCorp Vautl."
        },
        {
          id: "cloud-starter-vault-config",
          name: "Vault Configuration",
          description: "Provides client-side support for externalize configuration in a distributed system. Using HashiCorp's vault you have a central place to manage external secret properties for applications across all environments."
        },
        {
          id: "cloud-starter-zookeeper-config",
          name: "Apache Zookeeper Configuration",
          description: "Enable and configure common patterns inside your application and build large distributed systems with Apache Zookeeper based components. The provides patterns include Service Discovery and Configuration."
        },
        {
          id: "cloud-starter-consul-config",
          name: "Consul Configuration",
          description: "Enable and confiugra the common patterns inside your application and build large distributed systems with Hashicrop's Consul. The patterns provided include Service Discovery, Distributed Configuration and Control Bus."
        }
      ]
    },

    {
      name: "Spring Cloud Discovery",
      values: [
        {
          id: "cloud-eureka",
          name: "Eureka Discovery Client",
          description: "A REST based service for location services for the purpose of load balancing and failover of middle-tier servers."
        },
        {id: "cloud-eureka-server", name: "Eureka Server", description: "spring-cloud-netflix Eureka Server."},
        {
          id: "cloud-starter-zookeeper-discovery",
          name: "Apache Zookeeper Discovery",
          description: "Service discovery with Apache Zookeeper."
        },
        {
          id: "cloud-starter-consul-discovery",
          name: "Consul Discovery",
          description: "Service discovery with Hashicorp Consul"
        }
      ]
    },

    {
      name: "Spring Cloud Routing",
      values: [
        {
          id: "cloud-gateway",
          name: "Gateway",
          description: "Provides a simple, yet effective way to route to APIs in Servlet-based applications. Provides cross-cutting concerns to those APISs such as security, monitoring/metrics, and resiliency."
        },
        {
          id: "cloud-gateway-reactive",
          name: "Reactive Gateway",
          description: "Provides a simple, yet effective way to route to APIs in reactive applications. Provides cross-cutting concerns to those APISs such as security, monitoring/metrics, ans resiliency."
        },
        {
          id: "cloud-feign",
          name: "OpenFeign",
          description: "Declarative REST Client. OpenFeign creates a dynamic implementation of an interface ecorated with JAXRS or Spring MVC annotations."
        },
        {
          id: "cloud-loadbalancer",
          name: "Cloud LoadBalancer",
          description: "Client-sid load-balancing with Spring Cloud LoadBalancer."
        }
      ]
    },

    {
      name: "Spring Cloud Circuit Breaker",
      values: [
        {
          id: "cloud-resilience4j",
          name: "Resilience4J",
          description: "Spring Cloud Circuit breaker with Resilience5J as the underlying implementations."
        },
      ]
    },

    {
      name: "Spring Cloud Messaging",
      values: [
        {
          id: "cloud-bus",
          name: "Cloud Bus",
          description: "Links nodes of a distributed system with a lightweight message broker which can used to broadcast state changes or other management instructions (required a binder, e.g Apache Kafka or RabbitMQ)."
        },
        {
          id: "cloud-stream",
          name: "Cloud Stream",
          description: "Framework for building highly scalable event-driven microservices connected with shared messaging systems (required a binder, e.g Apache Kafka, Apache Pulsar, RabbitMQ, or Solace PubSub+)."
        },
      ]
    },

    {
      name: "VMware Tanzu Application Service",
      values: [
        {
          id: "scs-config-client",
          name: "Config Client (TAS)",
          description: "Config client on VMware Tanzu Application Service."
        },
        {
          id: "scs-service-registry",
          name: "Service Registry (TAS)",
          description: "Eureka service discovery client on VMware Tanzu Application Service."
        }
      ]
    },

    {
      name: "Microsoft Azure",
      values: [
        {
          id: "azure-active-directory",
          name: "Azure Active Directory",
          description: "Spring Security integration with Azure Active Directory for authentication."
        },
        {
          id: "azure-cosmo-db",
          name: "Azure Cosmos DB",
          description: "Fully managed NoSQL database service modern app development, including Spring Data Support."
        },
        {
          id: "azure-keyvault",
          name: "Azure Key Vault",
          description: "All key vault features are supported, e.g. manage application secrets and certificates."
        },
        {
          id: "azure-storage",
          name: "Azure Storage",
          description: "All Strorage features are supported, e.g. blob, fileshae and queue."
        }
      ]
    },

    {
      name: "AI",
      values: [
        {
          id: "spring-ai-anthropic",
          name: "Anthropic Claude",
          description: "Spring AI support for Anthropic Claude AI models."
        },
        {
          id: "spring-ai-azure-openai",
          name: "Azure OpenAI",
          description: "Spring AI support for Azure's OpenAi offering, powered by ChatGPT. It extends beyond traditional OpenAI capabilities, delivering AI-driven text generation with enhanced functionality."
        },
        {
          id: "spring-ai-bedrock",
          name: "Amazon Bedrock",
          description: "Spring Ai support for Amazon Bedrock. It is a manage service that provides foundation models from various AI providers, available through a unified API."
        },
        {
          id: "spring-ai-bedrock-converse",
          name: "Amazon Bedrock Converse",
          description: "Spring AI support for Amazon bedrock Converse. Il provides a unified interfaces for conversational AI models with enhanced capabilities including function/tool calling, multimodal inputs, and streaming responses."
        },
        {
          id: "spring-ai-vectordb-cassandra",
          name: "Apache Cassandra Vector Database",
          description: "Spring AI vector database support for Apache Cassandra."
        },
        {
          id: "spring-ai-vectordb-chroma",
          name: "Chroma Vector Database",
          description: "Spring AI support for Chroma. It is an open-source embedding database and gives you the tools to store document embedding, content, and metadata. It also allows to search through those embeddings, including metadata filtering."
        },
        {
          id: "spring-ai-vectordb-elasticsearch",
          name: "Elasticsearch Vector Database",
          description: "Spring AI vector database support for Elasticsearch."
        },
        {
          id: "spring-ai-vectordb-milvus",
          name: "Milvus Vector Database",
          description: "Spring AI vector database support for Milvus. It is an open-source vector database that has garnered significant attention in the fields of data science an machine learning. ON of ist standout features lies in its robust support for vector indexing and querying."
        },
        {
          id: "spring-ai-mistral",
          name: "Mistral AI",
          description: "Spring AI support fo Mistral AI, the open and portable generative AI for devs and businesses."
        },
        {
          id: "spring-ai-vectordb-mongodb-atlas",
          name: "MongoDB Atlas Vector Database",
          description: "Spring Ai vector database for MongoDB Atlas. It is a fully manage cloud database service that provides an eas way to deploy, operate an scale a MongoDB database in the cloud"
        },
        {
          id: "spring-ai-vectordb-neo4j",
          name: "Neo4j Vector Database",
          description: "Spring AI vector database for Neo4j's Vector Search. It allows users to query vector embeddings from large datasets."
        },
        {
          id: "spring-ai-ollama",
          name: "Ollama",
          description: "Spring AI support for Ollama. It allows you to run Large Language Models (LLMs) locally and generate text from them."
        },
        {
          id: "spring-ai-openapi",
          name: "OpenAI",
          description: "Spring AI support for ChatGPT, the AI language and DALL-E, the image generation model from OpenAI."
        },
        {
          id: "spring-ai-vectordb-oracle",
          name: "Oracle Vector Database",
          description: "Spring AI vector database support for Oracle. Enables storing, indexing and searching vector embeddings in Oracle Database 23ai."
        },
        {
          id: "spring-ai-vectordb-pgvector",
          name: "PGvector Vector Database",
          description: "Spring Ai vector database support for PGvector. It is an open-source extension for PostgreSQL that enables storing and searching over machine learning-generated embedding."
        },
        {
          id: "spring-ai-vectordb-pinecone",
          name: "Pinecone Vector Database",
          description: "Spring Ai vector database support for Pinecone. It is a popular cloud-base vector database and allows you to store and search vectors efficiently."
        },
        {
          id: "spring-ai-postgresml",
          name: "PostgresML",
          description: "Spring AI support for the PostgresML text embeddings models."
        },
        {
          id: "spring-ai-vectordb-redis",
          name: "Redis Search and Query Vector Database",
          description: "Spring Ai vector database support for Reis Search and Query. It extends the core features of Redis OSS and allows you to use Redis as a vector database."
        },
        {
          id: "spring-ai-stabilityai",
          name: "Stability AI",
          description: "Spring Ai support for Stability Ai's text to image generation model."
        },
        {
          id: "spring-ai-transformers",
          name: "Transformers (ONNX) Embeddings",
          description: "Spring AI support fro pre-trained transformer models, serialized into Open Neural Network Exchange (ONNX) format."
        },
        {
          id: "spring-ai-vertexai-gemini",
          name: "Vertex AI Gemini",
          description: "Spring AI support for Google Vertex Gemini chat. Doesn't support embeddings."
        },
        {
          id: "spring-ai-vertexai-embeddings",
          name: "Vertex AI Embeddings",
          description: "Spring AI support for Google Vertex text and multimodal embedding models."
        },
        {
          id: "spring-ai-vectordb-qdrant",
          name: "Qdrant Vector Database",
          description: "Spring Ai vector database support for Typesense"
        },
        {
          id: "spring-ai-vectordb-weaviate",
          name: "Weaviate Vector Database",
          description: "Spring AI vector database support for Weaviate, an open-source vector database. It allows you to store data objects and vector embeddings from your favorite ML-models and scale seamlessly into billions of data objects."
        },
        {
          id: "spring-ai-markdown-document-reader",
          name: "Markdown Document Reader",
          description: "Spring AI Markdown document reader. It allows to load Markdown documents, converting them into a list of Spring AI Document objects."
        },
        {
          id: "spring-ai-tika-document-reader",
          name: "Tika Document Reader",
          description: "Spring Ai Tika document readder. It uses Apache Tika to extract text from a variety of document formats, such as PDF, DOC/DOX, /PPT/PPTX, and HTML. The documents ar converted into a list of Spring AI Document objects."
        },
        {
          id: "spring-ai-pdf-document-reader",
          name: "PDF Document Reader",
          description: "Spring AI PDF document reader. It uses Apache PdfBox to extract text form PDF documents and converting them into a list of Spring AI Document objects."
        }
      ]
    }];

  constructor() { }

  getCategories() : Category[] {
    return this.categories;
  }
}
