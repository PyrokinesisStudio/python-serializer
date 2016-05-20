import packer


# Define the table (do this once per table on all hosts)
table = packer.TableDef('player')
table.define('uint16', 'number')  # Type, name, and default value (omit to require a value)
table.define('float', 'x', 0.0)   # See pack.py for all supported types
table.define('float', 'y', 0.0)
table.define('float', 'z', 0.0)
table.define('json', 'name', 'unnamed')

# Prepare a table (do this when you need to send data)
table = packer.Table('player')
table.set('number', 15)
table.set('name', 'Bob Johnson')

# Convert the table to bytes (this goes in the packet)
buff = packer.to_bytes(table)

# Convert the bytes back to a table (pulled from the packet)
table = packer.to_table(buff)

# Grab the table's name or ID so you know what it's for
print ("Table Name:", table.tableName())
print ("Table ID:", table.tableID())

# Observe the data
print (table.get('number'))
print (table.get('x'))
print (table.get('y'))
print (table.get('z'))
print (table.get('name'))


# Let's do another to test buffer aggregation, handy for optimizing packet size
table2 = packer.TableDef('AnotherTable')
table2.define('uint16', 'number')
table2.define('json', 'text', 'default')

table2 = packer.Table('AnotherTable')
table2.set('number', 20)
table2.set('text', 'asdf1234')

buff2 = packer.to_bytes(table2)

# Now join the buffers
joined_buffer = packer.join_buffers([buff, buff2])

# Unjoin
bufflist = packer.unjoin_buffers(joined_buffer)

# And we have usable tables again
print ('\nUnpacked tables:')
for b in bufflist:
    t = packer.to_table(b)

    if t.tableID() == 0:
        print (t.tableName(), t.get('name'))
    else:
        print (t.tableName(), t.get('text'))
