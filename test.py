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
