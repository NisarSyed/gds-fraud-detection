def view_stats(driver):
    query = "CALL apoc.meta.stats();"
    return run_query(driver, query)

def view_labels(driver):
    query = """
    CALL apoc.meta.stats()
    YIELD labels
    UNWIND keys(labels) AS nodeLabel
    RETURN nodeLabel, labels[nodeLabel] AS nodeCount
    """
    return run_query(driver, query)
            
def view_relationships(driver):
    query = """
    CALL apoc.meta.stats()
    YIELD relTypesCount
    UNWIND keys(relTypesCount) AS relationshipType
    RETURN relationshipType, relTypesCount[relationshipType] AS relationshipCount
    """
    return run_query(driver, query)

def view_transactions(driver):
    query = """
    MATCH (t:Transaction)
    WITH count(t) AS globalCnt
    UNWIND ['CashIn', 'CashOut', 'Payment', 'Debit', 'Transfer'] AS TransactionType
        CALL apoc.cypher.run('MATCH (t:' + TransactionType + ')
            RETURN count(t) AS txCnt', {})
        YIELD value
    RETURN TransactionType, value.txCnt AS NumberOfTransactions,
        round(toFloat(value.txCnt)/toFloat(globalCnt), 2) AS `%Transactions`
    ORDER BY `%Transactions` DESC;
    """
    return run_query(driver, query)

def view_shared_identifiers(driver):
    query = "MATCH (c1:Client) - [s:SHARED_IDENTIFIERS] -> (c2:Client) WHERE s.count >= 2 RETURN DISTINCT c1.name AS Client1"
    return run_query(driver, query)

def view_fp_fraudsters(driver):
    query = """
    MATCH (f:FirstPartyFraudster) 
    RETURN DISTINCT f.name AS FirstPartyFraudsters, f.firstPartyFraudScore as FraudScore
    ORDER BY FraudScore DESC;
    """
    return run_query(driver, query)

def view_similar_clients(driver):
    query = """
    MATCH (c1:Client) - [s:SIMILAR_TO] -> (c2:Client)
    WHERE c1 <> c2
    RETURN DISTINCT c1.name AS Client1, c2.name AS Client2, s.jaccardScore AS Similarity
    ORDER BY Similarity DESC;
    """
    return run_query(driver, query)

def view_fp_transactions(driver):
    query = """
    MATCH p=(:Client:FirstPartyFraudster)-[]-(:Transaction)-[]-(c:Client)
    WHERE NOT c:FirstPartyFraudster
    RETURN DISTINCT c.name;
    """
    return run_query(driver, query)

def run_query(driver, query):
    with driver.session() as session:
        try:
            result = session.run(query)
        except Exception as e:
            return None
        
        return result.data()