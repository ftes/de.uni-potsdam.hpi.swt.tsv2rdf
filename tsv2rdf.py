import os

output = open("output/out.turtle", "w")
output.write("base <http://public-mediawiki.ftes.de/hpi/swt_ws13/aufgabenblatt/2/aufgabe/4/b/> .\n")
output.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
output.write("@prefix attr: <http://public-mediawiki.ftes.de/hpi/swt_ws13/aufgabenblatt/2/aufgabe/4/b/attributes/> .\n\n")

tables = {
	"Actor": ["id", "name", "surname", "birthdate"],
	"Broadcast": ["id", "name"],
	"TelevisionShow": ["id", "name", "yearFrom", "yearTo"]
	}

relationships = {
	"broadcastedBy": {"from": "TelevisionShow", "to": "Broadcast", "type": "N:1"},
	"starring": {"from": "TelevisionShow", "to": "Actor", "type": "N:M"}
}

# get relationship data
relationshipData = {}
for name, data in relationships.iteritems():
	if not(data["from"] in relationshipData):
		relationshipData[data["from"]] = {}
	f = open("data/" + name + ".tsv")
	if (data["type"] == "N:1"):
		for line in f.read().splitlines():
			columns = line.split("\t")
			if not(columns[0] in relationshipData[data["from"]]):
				relationshipData[data["from"]][columns[0]] = []
			relationshipData[data["from"]][columns[0]].append("attr:{0} <{1}/{2}>".format(name, data["to"], columns[1]))
	elif (data["type"] == "N:M"):
		fromTo = {}
		for line in f.read().splitlines():
			columns = line.split("\t")
			if not(columns[0] in fromTo):
				fromTo[columns[0]] = []
			fromTo[columns[0]].append(columns[1])
		for fromName, tos in fromTo.iteritems():
			object = "attr:{0} ( ".format(name)
			for to in tos:
				object += "<{0}/{1}> ".format(data["to"], to)
			object += ")"
			if not(fromName in relationshipData[data["from"]]):
				relationshipData[data["from"]][fromName] = []
			relationshipData[data["from"]][fromName].append(object)
		

for name, columnNames in tables.iteritems():
	f = open("data/" + name + ".tsv")
	for line in f.read().splitlines():
		columns = line.split("\t")
		recordId = columns[columnNames.index("id")]
		output.write("<{0}/{1}>".format(name, recordId))
		for columnName, columnData in zip(columnNames, columns):
			output.write(" attr:{0} \"{1}\" ;\n".format(columnName, columnData))

		if name in relationshipData and recordId in relationshipData[name]:
			for relationship in relationshipData[name][recordId]:
				output.write(" {0} ;\n".format(relationship))

		output.seek(-2, os.SEEK_END)
		output.truncate()
		output.write(".\n\n")
	f.close()

	# replace ;\n with .\n

output.close()

print "output written to output/out.turtle"
