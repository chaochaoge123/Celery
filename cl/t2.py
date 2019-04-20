from tasks import run_cmd

r=run_cmd.delay('df-h')
print(r.get())