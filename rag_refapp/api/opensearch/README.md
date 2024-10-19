## OpenSearch

### Configuration
We need to configure the following environment variable `OPENSEARCH_INITIAL_ADMIN_PASSWORD` in the `docker-compose.yml`
file. `opensearch-node1` and `opensearch-node2` both depend on this to be
configured to the same value.

### Running Locally
Invoke `docker compose up -d` in this
directory.

To verify that the nodes and the dashboard service are up and running, use `docker compose ps`

Lastly, use this `curl https://localhost:9200 -ku admin:@ThisIsMyPassword123` to verify we can authenticate
in. You should get this response:
```json
{
  "name" : "opensearch-node1",
  "cluster_name" : "opensearch-cluster",
  "cluster_uuid" : "a3WShhW3TX2-F67mZbJ5Ug",
  "version" : {
    "distribution" : "opensearch",
    "number" : "2.17.1",
    "build_type" : "tar",
    "build_hash" : "1893d20797e30110e5877170e44d42275ce5951e",
    "build_date" : "2024-09-26T21:59:32.078798875Z",
    "build_snapshot" : false,
    "lucene_version" : "9.11.1",
    "minimum_wire_compatibility_version" : "7.10.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

Alternatively, you can sign in at `http://localhost:5601` with username `admin` and
password `<value of OPENSEARCH_INITIAL_ADMIN_PASSWORD>`.

### Interacting with OpenSearch using REST

Invoke the health endpoint:
```bash
curl -X GET "https://localhost:9200/_cluster/health" -ku admin:<value of OPENSEARCH_INITIAL_ADMIN_PASSWORD>
```