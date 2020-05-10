import survey

table = survey.Pregnancies()
table.ReadRecords()
print 'Number of pregnancies', len(table.records)


def live():
	live_births = 0

	for i in table.records:
		if i.outcome == 1:
			live_births += 1
	print("number of live births %i, percentage of live births: %f" % (live_births, float(live_births)/len(table.records)))

def Partition():
	live_births = [0,0]
	for i in table.records:
		if i.outcome == 1:
			if i.birthord == 1:
				live_births[0] += 1
			else:
				live_births[1] += 1
	print("First born live births %i, second born live births %i" % (live_births[0], live_births[1]))

live()
Partition()
