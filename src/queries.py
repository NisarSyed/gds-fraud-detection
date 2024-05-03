def view_labels(driver):
    query = "CALL db.labels() YIELD label\
            CALL apoc.cypher.run('MATCH (:'+label+') RETURN count(*) as count', {})\
            YIELD value\
            RETURN label as Label, value.count AS Count"
    return run_query(driver, query)
            
def view_relationships(driver):
    query = "CALL db.relationshipTypes() YIELD relationshipType\
            CALL apoc.cypher.run('MATCH ()-[:'+relationshipType+']->() RETURN count(*) as count', {})\
            YIELD value\
            RETURN relationshipType as Relationship, value.count AS Count"
    return run_query(driver, query)

def view_shared_identifiers(driver):
    query = "MATCH (c1:Client) - [s:SHARED_IDENTIFIERS] -> (c2:Client) WHERE s.count >= 2 RETURN c1 AS Client1, c2 AS Client2;"
    return run_query(driver, query)

def run_query(driver, query):
    with driver.session() as session:
        try:
            result = session.run(query)
        except Exception as e:
            return None
        
        return result.data()