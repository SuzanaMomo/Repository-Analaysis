from git import Repo
import datetime

working_dir = 'C:\\Users\\suzan\\Documents\\git analysis\\nova'
months = 6
days = 30

repo = Repo(working_dir)
git_repo = repo.git
current_date = datetime.date.today()
since = current_date - datetime.timedelta(months * days)
print('--since={}'.format(since))

commit_dirs = git_repo.log('--since={}'.format(since), '--pretty=tformat:', '--name-only').split('\n')

# for directory in commit_dirs:
# 	print(directory)

commits = git_repo.log('--since={}'.format(since)).split('\n')

sha_list = []

for line in commits:
	split_line = line.split(' ') 
	if split_line[0] == 'commit':
		sha_list.append(split_line[1])