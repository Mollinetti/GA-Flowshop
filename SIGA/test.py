joblist = []
with open('In/ta_20x5+instance') as fj:
    job_read = fj.read().splitlines()
for k in range(0, len(job_read)):
    line = job_read[k]
    joblist.append(line.split())
    joblist[k] = list(map(int, joblist[k]))

print(joblist)