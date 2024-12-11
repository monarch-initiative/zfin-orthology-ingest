# This wraps preprocess.sql so that we don't gain a depenency on the duckdb cli utility,
# with a downside that we don't get the terminal output

import duckdb

con = duckdb.connect(database=':memory:')

with open('scripts/preprocess.sql', 'r') as sql_file:
    sql_script = sql_file.read()

# Execute the SQL script
con.execute(sql_script)
